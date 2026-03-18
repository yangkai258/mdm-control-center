package controllers

import (
	"net/http"
	"strings"
	"time"

	"mdm/backend/models"
	"mdm/backend/utils"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

// DeviceController 设备管理控制器
type DeviceController struct {
	DB  *gorm.DB
	Redis *utils.RedisClient
}

// RegisterRequest 设备注册请求
type RegisterRequest struct {
	DeviceID        string `json:"device_id" binding:"omitempty"`
	MacAddress      string `json:"mac_address" binding:"required"`
	SnCode         string `json:"sn_code" binding:"required"`
	HardwareModel   string `json:"hardware_model" binding:"required"`
	FirmwareVersion string `json:"firmware_version" binding:"required"`
}

// BindRequest 绑定请求
type BindRequest struct {
	BindUserID string `json:"bind_user_id" binding:"required"`
}

// Register 设备注册/绑定
func (c *DeviceController) Register(ctx *gin.Context) {
	var req RegisterRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"code":      4005,
			"message":   "参数校验失败: " + err.Error(),
			"error_code": "ERR_VALIDATION",
		})
		return
	}

	// 校验 MAC 地址格式
	if !isValidMAC(req.MacAddress) {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"code":      4005,
			"message":   "无效的MAC地址格式",
			"error_code": "ERR_VALIDATION",
		})
		return
	}

	var device models.Device
	result := c.DB.Where("mac_address = ?", req.MacAddress).First(&device)

	if result.Error == nil {
		// 设备已存在，更新绑定
		device.FirmwareVersion = req.FirmwareVersion
		device.UpdatedAt = time.Now()
		if err := c.DB.Save(&device).Error; err != nil {
			ctx.JSON(http.StatusInternalServerError, gin.H{
				"code":      5001,
				"message":   "服务器内部错误",
				"error_code": "ERR_INTERNAL",
			})
			return
		}
		ctx.JSON(http.StatusOK, gin.H{
			"code":    0,
			"message": "success",
			"data": gin.H{
				"device_id":        device.DeviceID,
				"lifecycle_status": device.LifecycleStatus,
				"created_at":       device.CreatedAt,
			},
		})
		return
	}

	// 新建设备
	device = models.Device{
		MacAddress:      req.MacAddress,
		SnCode:         req.SnCode,
		HardwareModel:   req.HardwareModel,
		FirmwareVersion: req.FirmwareVersion,
		LifecycleStatus: 1, // 待激活
	}

	if err := c.DB.Create(&device).Error; err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"code":      5001,
			"message":   "设备注册失败",
			"error_code": "ERR_INTERNAL",
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"code":    0,
		"message": "success",
		"data": gin.H{
			"device_id":        device.DeviceID,
			"lifecycle_status": device.LifecycleStatus,
			"created_at":       device.CreatedAt,
		},
	})
}

// Bind 扫码绑定设备
func (c *DeviceController) Bind(ctx *gin.Context) {
	snCode := ctx.Param("sn_code")
	var req BindRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"code":      4005,
			"message":   "参数校验失败",
			"error_code": "ERR_VALIDATION",
		})
		return
	}

	var device models.Device
	if err := c.DB.Where("sn_code = ?", snCode).First(&device).Error; err != nil {
		ctx.JSON(http.StatusNotFound, gin.H{
			"code":      4002,
			"message":   "设备不存在",
			"error_code": "ERR_DEVICE_002",
		})
		return
	}

	// 检查状态
	if device.LifecycleStatus != 1 && device.LifecycleStatus != 2 {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"code":      4003,
			"message":   "非法设备状态，无法绑定",
			"error_code": "ERR_DEVICE_003",
		})
		return
	}

	// 更新绑定
	device.BindUserID = &req.BindUserID
	device.LifecycleStatus = 2 // 服役中
	device.UpdatedAt = time.Now()

	if err := c.DB.Save(&device).Error; err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"code":      5001,
			"message":   "绑定失败",
			"error_code": "ERR_INTERNAL",
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"code":    0,
		"message": "success",
		"data": gin.H{
			"device_id":        device.DeviceID,
			"bind_user_id":     *device.BindUserID,
			"lifecycle_status": device.LifecycleStatus,
			"message":          "绑定成功",
		},
	})
}

// ListRequest 设备列表请求
type ListRequest struct {
	Page            int    `form:"page"`
	PageSize        int    `form:"page_size"`
	Status          string `form:"status"`
	LifecycleStatus int    `form:"lifecycle_status"`
	HardwareModel   string `form:"hardware_model"`
	Search          string `form:"search"`
}

// List 获取设备列表（带分页和筛选）
func (c *DeviceController) List(ctx *gin.Context) {
	var req ListRequest
	if err := ctx.ShouldBindQuery(&req); err != nil {
		req.Page = 1
		req.PageSize = 20
	}

	if req.Page < 1 {
		req.Page = 1
	}
	if req.PageSize < 1 || req.PageSize > 100 {
		req.PageSize = 20
	}

	query := c.DB.Model(&models.Device{})

	// 筛选条件
	if req.LifecycleStatus > 0 {
		query = query.Where("lifecycle_status = ?", req.LifecycleStatus)
	}
	if req.HardwareModel != "" {
		query = query.Where("hardware_model = ?", req.HardwareModel)
	}
	if req.Search != "" {
		search := "%" + req.Search + "%"
		query = query.Where("device_id LIKE ? OR sn_code LIKE ?", search, search)
	}

	// 获取总数
	var total int64
	query.Count(&total)

	// 查询列表
	var devices []models.Device
	offset := (req.Page - 1) * req.PageSize
	if err := query.Offset(offset).Limit(req.PageSize).Order("created_at DESC").Find(&devices).Error; err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"code":      5001,
			"message":   "查询失败",
			"error_code": "ERR_INTERNAL",
		})
		return
	}

	// 获取在线状态（从 Redis）
	type DeviceWithShadow struct {
		models.Device
		IsOnline      bool `json:"is_online"`
		BatteryLevel  int  `json:"battery_level"`
	}

	result := make([]DeviceWithShadow, len(devices))
	for i, d := range devices {
		result[i].Device = d
		// 从 Redis 获取设备影子
		shadow, err := c.Redis.GetDeviceShadow(d.DeviceID)
		if err == nil && shadow != nil {
			result[i].IsOnline = shadow.IsOnline
			result[i].BatteryLevel = shadow.BatteryLevel
		}
	}

	// 如果有 status 筛选，内存过滤
	if req.Status != "" {
		filtered := make([]DeviceWithShadow, 0)
		for _, d := range result {
			if req.Status == "online" && d.IsOnline {
				filtered = append(filtered, d)
			} else if req.Status == "offline" && !d.IsOnline {
				filtered = append(filtered, d)
			}
		}
		result = filtered
	}

	ctx.JSON(http.StatusOK, gin.H{
		"code":    0,
		"message": "success",
		"data": gin.H{
			"list": result,
			"pagination": gin.H{
				"page":        req.Page,
				"page_size":   req.PageSize,
				"total":       total,
				"total_pages": (int(total) + req.PageSize - 1) / req.PageSize,
			},
		},
	})
}

// Get 获取单个设备详情
func (c *DeviceController) Get(ctx *gin.Context) {
	deviceID := ctx.Param("device_id")

	var device models.Device
	if err := c.DB.Where("device_id = ?", deviceID).First(&device).Error; err != nil {
		ctx.JSON(http.StatusNotFound, gin.H{
			"code":      4002,
			"message":   "设备不存在",
			"error_code": "ERR_DEVICE_002",
		})
		return
	}

	// 获取设备影子
	shadow, _ := c.Redis.GetDeviceShadow(deviceID)
	
	// 获取宠物配置
	var petProfile models.PetProfile
	c.DB.Where("device_id = ?", deviceID).First(&petProfile)

	ctx.JSON(http.StatusOK, gin.H{
		"code":    0,
		"message": "success",
		"data": gin.H{
			"device_id":         device.DeviceID,
			"mac_address":      device.MacAddress,
			"sn_code":          device.SnCode,
			"hardware_model":   device.HardwareModel,
			"firmware_version": device.FirmwareVersion,
			"bind_user_id":     device.BindUserID,
			"lifecycle_status": device.LifecycleStatus,
			"shadow":          shadow,
			"pet_profile":     petProfile,
			"created_at":      device.CreatedAt,
			"updated_at":      device.UpdatedAt,
		},
	})
}

// 校验 MAC 地址格式
func isValidMAC(mac string) bool {
	parts := strings.Split(mac, ":")
	if len(parts) != 6 {
		return false
	}
	for _, p := range parts {
		if len(p) != 2 {
			return false
		}
	}
	return true
}
