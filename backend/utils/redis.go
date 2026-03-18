package utils

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/redis/go-redis/v9"
)

// RedisClient Redis 客户端封装
type RedisClient struct {
	client *redis.Client
}

// DeviceShadow 设备影子结构
type DeviceShadow struct {
	DeviceID      string     `json:"device_id"`
	IsOnline      bool       `json:"is_online"`
	BatteryLevel  int        `json:"battery_level"`
	CurrentMode   string     `json:"current_mode"`
	LastIP        string     `json:"last_ip"`
	LastHeartbeat *time.Time `json:"last_heartbeat"`
	DesiredConfig string     `json:"desired_config"`
}

// NewRedisClient 创建 Redis 客户端
func NewRedisClient(addr, password string, db int) (*RedisClient, error) {
	client := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: password,
		DB:       db,
	})

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := client.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("Redis 连接失败: %w", err)
	}

	return &RedisClient{client: client}, nil
}

// SetDeviceShadow 设置设备影子
func (r *RedisClient) SetDeviceShadow(deviceID string, shadow DeviceShadow, ttl time.Duration) error {
	ctx := context.Background()
	key := fmt.Sprintf("shadow:%s", deviceID)

	data, err := json.Marshal(shadow)
	if err != nil {
		return err
	}

	if ttl > 0 {
		return r.client.Set(ctx, key, data, ttl).Err()
	}
	return r.client.Set(ctx, key, data, 0).Err()
}

// GetDeviceShadow 获取设备影子
func (r *RedisClient) GetDeviceShadow(deviceID string) (*DeviceShadow, error) {
	ctx := context.Background()
	key := fmt.Sprintf("shadow:%s", deviceID)

	data, err := r.client.Get(ctx, key).Bytes()
	if err != nil {
		return nil, err
	}

	var shadow DeviceShadow
	if err := json.Unmarshal(data, &shadow); err != nil {
		return nil, err
	}

	return &shadow, nil
}

// GetAllShadowKeys 获取所有设备影子 Key
func (r *RedisClient) GetAllShadowKeys() ([]string, error) {
	ctx := context.Background()
	keys, err := r.client.Keys(ctx, "shadow:*").Result()
	if err != nil {
		return nil, err
	}
	return keys, nil
}

// DelDeviceShadow 删除设备影子
func (r *RedisClient) DelDeviceShadow(deviceID string) error {
	ctx := context.Background()
	key := fmt.Sprintf("shadow:%s", deviceID)
	return r.client.Del(ctx, key).Err()
}

// Close 关闭连接
func (r *RedisClient) Close() error {
	return r.client.Close()
}
