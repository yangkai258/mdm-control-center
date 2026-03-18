# Agent HD - 后端开发任务

## 你是资深 Golang 后端开发工程师 (agenthd)
你的任务是使用 Gin 框架和 GORM 编写高并发的设备管理核心逻辑。

## 数据库已使用 PostgreSQL
核心表有 mdm_devices (设备台账) 和基于 Redis 的设备影子。

## 请输出以下 Go 语言代码文件：

### 任务 1：数据模型定义 (models/device.go)

使用 GORM tag 严格定义 Device 结构体。字段包括：
- ID
- DeviceID (UUID)
- MacAddress
- SnCode
- HardwareModel
- FirmwareVersion
- BindUserID
- LifecycleStatus
- CreatedAt
- UpdatedAt

### 任务 2：API 路由与控制器 (controllers/device_controller.go)

实现设备注册/绑定的处理函数。要求：
- 接收 JSON
- 校验必填字段（如 MacAddress）
- 如果 Mac 存在则更新绑定，不存在则新建
- 最终存入 PostgreSQL

### 任务 3：MQTT 消息桥接框架 (mqtt/handler.go)

使用 paho.mqtt.golang 库，写一个订阅设备上报 Topic 的回调函数。当收到心跳 JSON 时，将其解析并更新到 Redis 中（Key 为 shadow:{device_id}，设置 90 秒 TTL）。

## 约束
- 代码必须包含充分的错误处理 (Error Handling) 和日志打印
- 不要给出项目初始化步骤，只输出核心源码
