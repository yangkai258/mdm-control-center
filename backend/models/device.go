package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// Device 设备资产主表
type Device struct {
	ID              uint           `gorm:"primaryKey" json:"id"`
	DeviceID        string         `gorm:"type:varchar(36);uniqueIndex;not null" json:"device_id"`
	MacAddress      string         `gorm:"type:varchar(17);uniqueIndex;not null" json:"mac_address"`
	SnCode          string         `gorm:"type:varchar(32);uniqueIndex;not null" json:"sn_code"`
	HardwareModel   string         `gorm:"type:varchar(32);not null" json:"hardware_model"`
	FirmwareVersion string         `gorm:"type:varchar(32);not null" json:"firmware_version"`
	BindUserID      *string        `gorm:"type:varchar(36);index" json:"bind_user_id"`
	LifecycleStatus int            `gorm:"type:smallint;default:1" json:"lifecycle_status"` // 1:待激活 2:服役中 3:维修 4:报废
	CreatedAt       time.Time      `json:"created_at"`
	UpdatedAt       time.Time      `json:"updated_at"`
	DeletedAt       gorm.DeletedAt `gorm:"index" json:"-"`
}

// BeforeCreate 创建前自动生成 UUID
func (d *Device) BeforeCreate(tx *gorm.DB) error {
	if d.DeviceID == "" {
		d.DeviceID = uuid.New().String()
	}
	return nil
}

// DeviceShadow 设备影子表
type DeviceShadow struct {
	DeviceID       string                 `gorm:"primaryKey;type:varchar(36)" json:"device_id"`
	IsOnline       bool                   `gorm:"default:false" json:"is_online"`
	BatteryLevel   int                    `gorm:"type:smallint" json:"battery_level"`
	CurrentMode    string                 `gorm:"type:varchar(20);default:'idle'" json:"current_mode"`
	LastIP         string                 `gorm:"type:varchar(45)" json:"last_ip"`
	LastHeartbeat  *time.Time             `gorm:"index" json:"last_heartbeat"`
	DesiredConfig  map[string]interface{} `gorm:"type:jsonb" json:"desired_config"`
}

// OTAPackage OTA固件包
type OTAPackage struct {
	ID             uint      `gorm:"primaryKey" json:"id"`
	VersionCode    string    `gorm:"type:varchar(32);uniqueIndex;not null" json:"version_code"`
	HardwareModel  string    `gorm:"type:varchar(32);not null" json:"hardware_model"`
	BinURL        string    `gorm:"type:varchar(255);not null" json:"bin_url"`
	Md5Hash       string    `gorm:"type:varchar(32);not null" json:"md5_hash"`
	IsMandatory    bool      `gorm:"default:false" json:"is_mandatory"`
	ReleaseStatus  int       `gorm:"type:smallint;default:0" json:"release_status"` // 0:测试 1:灰度 2:全量
	CreatedAt      time.Time `json:"created_at"`
}

// PetProfile 宠物配置
type PetProfile struct {
	DeviceID         string                 `gorm:"primaryKey;type:varchar(36)" json:"device_id"`
	PetName          string                 `gorm:"type:varchar(64);default:'Mimi'" json:"pet_name"`
	Personality      string                 `gorm:"type:varchar(32);default:'lively'" json:"personality"`
	InteractionFreq  string                 `gorm:"type:varchar(16);default:'medium'" json:"interaction_freq"`
	DNDStartTime    string                 `gorm:"type:varchar(8);default:'23:00'" json:"dnd_start_time"`
	DNDEndTime      string                 `gorm:"type:varchar(8);default:'08:00'" json:"dnd_end_time"`
	CustomRules     map[string]interface{} `gorm:"type:jsonb" json:"custom_rules"`
	CreatedAt       time.Time              `json:"created_at"`
	UpdatedAt       time.Time              `json:"updated_at"`
}
