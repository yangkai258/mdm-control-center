package mqtt

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	"mdm/backend/utils"

	"github.com/eclipse/paho.mqtt.golang"
)

// MQTTConfig MQTT 配置
type MQTTConfig struct {
	Broker   string
	ClientID string
	Username string
	Password string
}

// Handler MQTT 消息处理
type Handler struct {
	Redis *utils.RedisClient
}

// StatusPayload 心跳上报 JSON 结构
type StatusPayload struct {
	DeviceID         string `json:"device_id"`
	Timestamp        string `json:"timestamp"`
	ConnectionStatus string `json:"connection_status"` // online, offline, poor_network
	BatteryLevel     int    `json:"battery_level"`     // 0-100
	ChargingStatus   bool   `json:"charging_status"`
	CurrentMode      string `json:"current_mode"` // sleeping, roaming, listening, talking, idle
	RSSI            *int   `json:"rssi,omitempty"`
}

// PropertyPayload 属性上报 JSON 结构
type PropertyPayload struct {
	DeviceID        string `json:"device_id"`
	FirmwareVersion string `json:"firmware_version"`
	HardwareModel   string `json:"hardware_model"`
	LastIPAddress   string `json:"last_ip_address,omitempty"`
}

// NewHandler 创建 MQTT 处理器
func NewHandler(redisClient *utils.RedisClient) *Handler {
	return &Handler{
		Redis: redisClient,
	}
}

// SetupSubscriber 设置订阅回调
func (h *Handler) SetupSubscriber(client mqtt.Client) {
	// 订阅设备心跳上报主题
	topic := "/mdm/device/+/up/status"
	token := client.Subscribe(topic, 0, h.StatusMessageHandler)
	if token.Wait() && token.Error() != nil {
		log.Printf("[MQTT] 订阅 %s 失败: %v", topic, token.Error())
	} else {
		log.Printf("[MQTT] 成功订阅: %s", topic)
	}

	// 订阅设备属性上报主题
	topicProp := "/mdm/device/+/up/property"
	tokenProp := client.Subscribe(topicProp, 0, h.PropertyMessageHandler)
	if tokenProp.Wait() && tokenProp.Error() != nil {
		log.Printf("[MQTT] 订阅 %s 失败: %v", topicProp, tokenProp.Error())
	} else {
		log.Printf("[MQTT] 成功订阅: %s", topicProp)
	}
}

// StatusMessageHandler 心跳消息处理
func (h *Handler) StatusMessageHandler(client mqtt.Client, msg mqtt.Message) {
	log.Printf("[MQTT] 收到心跳消息: %s", msg.Topic())

	var payload StatusPayload
	if err := json.Unmarshal(msg.Payload(), &payload); err != nil {
		log.Printf("[MQTT] 解析心跳JSON失败: %v", err)
		return
	}

	// 解析时间戳
	timestamp, err := time.Parse(time.RFC3339, payload.Timestamp)
	if err != nil {
		timestamp = time.Now()
	}

	// 在线状态判断
	isOnline := payload.ConnectionStatus == "online"
	if payload.ConnectionStatus == "poor_network" {
		// 弱网也算在线
		isOnline = true
	}

	// 更新 Redis 设备影子 (TTL 90秒)
	shadow := utils.DeviceShadow{
		DeviceID:      payload.DeviceID,
		IsOnline:      isOnline,
		BatteryLevel:  payload.BatteryLevel,
		CurrentMode:   payload.CurrentMode,
		LastHeartbeat: &timestamp,
	}

	if err := h.Redis.SetDeviceShadow(payload.DeviceID, shadow, 90*time.Second); err != nil {
		log.Printf("[MQTT] 更新设备影子失败: %v", err)
		return
	}

	log.Printf("[MQTT] 设备 %s 心跳更新: online=%v, battery=%d%%, mode=%s",
		payload.DeviceID, isOnline, payload.BatteryLevel, payload.CurrentMode)
}

// PropertyMessageHandler 属性消息处理
func (h *Handler) PropertyMessageHandler(client mqtt.Client, msg mqtt.Message) {
	log.Printf("[MQTT] 收到属性消息: %s", msg.Topic())

	var payload PropertyPayload
	if err := json.Unmarshal(msg.Payload(), &payload); err != nil {
		log.Printf("[MQTT] 解析属性JSON失败: %v", err)
		return
	}

	// 可以在这里处理属性更新，比如更新设备固件版本等信息
	log.Printf("[MQTT] 设备 %s 属性更新: firmware=%s, model=%s",
		payload.DeviceID, payload.FirmwareVersion, payload.HardwareModel)
}

// StartHeartbeatChecker 启动心跳检查器（检测离线设备）
func (h *Handler) StartHeartbeatChecker() {
	ticker := time.NewTicker(30 * time.Second)
	go func() {
		for range ticker.C {
			h.checkOfflineDevices()
		}
	}()
}

// checkOfflineDevices 检查离线设备
func (h *Handler) checkOfflineDevices() {
	// 从 Redis 获取所有设备影子
	keys, err := h.Redis.GetAllShadowKeys()
	if err != nil {
		return
	}

	now := time.Now()
	for _, key := range keys {
		shadow, err := h.Redis.GetDeviceShadow(key)
		if err != nil || shadow == nil {
			continue
		}

		// 检查心跳超时 (90秒)
		if shadow.LastHeartbeat != nil {
			elapsed := now.Sub(*shadow.LastHeartbeat)
			if elapsed > 90*time.Second && shadow.IsOnline {
				// 标记为离线
				shadow.IsOnline = false
				h.Redis.SetDeviceShadow(shadow.DeviceID, *shadow, 0)
				log.Printf("[MQTT] 设备 %s 心跳超时，标记为离线", shadow.DeviceID)
			}
		}
	}
}

// PublishCommand 下发指令到设备
func (h *Handler) PublishCommand(client mqtt.Client, deviceID string, cmd interface{}) error {
	topic := fmt.Sprintf("/mdm/device/%s/down/cmd", deviceID)
	payload, err := json.Marshal(cmd)
	if err != nil {
		return err
	}

	token := client.Publish(topic, 0, false, payload)
	if token.Wait() && token.Error() != nil {
		return token.Error()
	}

	log.Printf("[MQTT] 向设备 %s 下发指令: %s", deviceID, string(payload))
	return nil
}
