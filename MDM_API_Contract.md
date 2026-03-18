# MDM 控制中台 - 接口契约规范
**版本:** V1.0  
**编写:** agentcp (产品经理)  
**日期:** 2026-03-18

---

## 一、MQTT Topic 树与 JSON 协议定义

### 1.1 设备上行消息 (Device → Cloud)

#### 心跳上报 Topic
```
/mdm/device/{device_id}/up/status
```

**JSON Payload 结构：**
```json
{
  "device_id": "string (UUID, 必填) - 设备唯一标识",
  "timestamp": "string (ISO8601, 必填) - 消息时间戳",
  "connection_status": "string (枚举: online|offline|poor_network, 必填) - 网络连接状态",
  "battery_level": "integer (0-100, 必填) - 当前电量百分比",
  "charging_status": "boolean, 必填 - 是否正在充电",
  "current_mode": "string (枚举: sleeping|roaming|listening|talking|idle, 必填) - 宠物当前模式",
  "rssi": "integer (可选) - Wi-Fi信号强度，单位dBm"
}
```

#### 设备属性上报 Topic
```
/mdm/device/{device_id}/up/property
```

**JSON Payload 结构：**
```json
{
  "device_id": "string (UUID, 必填)",
  "firmware_version": "string (必填) - 当前固件版本",
  "hardware_model": "string (必填) - 硬件型号",
  "last_ip_address": "string (可选) - 最后一次公网IP"
}
```

---

### 1.2 云端下行消息 (Cloud → Device)

#### 指令下发 Topic
```
/mdm/device/{device_id}/down/cmd
```

**JSON Payload 结构：**
```json
{
  "cmd_id": "string (UUID, 必填) - 命令唯一ID",
  "cmd_type": "string (枚举: action|display|config|ota, 必填) - 命令类型",
  "action": "string (可选) - 具体动作指令",
  "display": "object (可选) - UI渲染指令",
  "config": "object (可选) - 配置更新",
  "ota": "object (可选) - OTA升级指令",
  "timestamp": "string (ISO8601, 必填)"
}
```

#### 配置下发 Topic
```
/mdm/device/{device_id}/down/config
```

**JSON Payload 结构：**
```json
{
  "desired_sleep_time": "string (可选) - 期望就寝时间，如 22:00",
  "desired_firmware": "string (可选) - 期望固件版本",
  "dnd_mode": "object (可选) - 免打扰配置",
  "timestamp": "string (ISO8601, 必填)"
}
```

---

### 1.3 MQTT Topic 树结构

```
/mdm
  ├── device
  │   ├── {device_id}
  │   │   ├── up
  │   │   │   ├── status        # 心跳上报
  │   │   │   └── property      # 属性上报
  │   │   ├── down
  │   │   │   ├── cmd           # 指令下发
  │   │   │   └── config        # 配置下发
  │   │   └── broadcast         # 广播消息
  │   └── gateway
  │       └── status            # 网关状态
  └── ota
      ├── {device_id}
      │   ├── progress          # 升级进度
      │   └── result            # 升级结果
```

---

## 二、核心 HTTP API 接口规范 (RESTful)

### 2.1 设备注册/绑定

#### POST /api/v1/devices/register

**功能说明：** 新设备首次连网上报身份，完成注册

**请求头：**
```
Content-Type: application/json
Authorization: Bearer {token} (可选，首次注册无需token)
```

**请求体：**
```json
{
  "device_id": "string (UUID v4, 必填) - 系统生成的全局唯一设备标识符",
  "mac_address": "string (必填) - M5Stack物理网卡MAC地址，格式: XX:XX:XX:XX:XX:XX",
  "sn_code": "string (必填) - 产品序列号，用于扫码绑定",
  "hardware_model": "string (必填) - 硬件型号，如 M5_CoreS3",
  "firmware_version": "string (必填) - 当前运行固件版本"
}
```

**成功响应 (200)：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "device_id": "string - 注册后的设备ID",
    "lifecycle_status": 1,
    "created_at": "string (ISO8601) - 注册时间"
  }
}
```

**错误响应 (400)：**
```json
{
  "code": 4001,
  "message": "设备ID或MAC地址已存在",
  "error_code": "ERR_DEVICE_001"
}
```

---

#### POST /api/v1/devices/{sn_code}/bind

**功能说明：** 用户扫码绑定设备

**请求头：**
```
Content-Type: application/json
Authorization: Bearer {token} (必填)
```

**请求体：**
```json
{
  "bind_user_id": "string (必填) - 绑定的用户ID"
}
```

**成功响应 (200)：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "device_id": "string",
    "bind_user_id": "string",
    "lifecycle_status": 2,
    "message": "绑定成功"
  }
}
```

---

### 2.2 设备列表（分页+筛选）

#### GET /api/v1/devices/list

**功能说明：** 获取设备台账和实时状态列表，支持分页和筛选

**请求头：**
```
Authorization: Bearer {token} (必填)
```

**Query 参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页条数，默认20 |
| status | string | 否 | 设备在线状态筛选：online/offline |
| lifecycle_status | integer | 否 | 生命周期状态筛选：1-5 |
| hardware_model | string | 否 | 硬件型号筛选 |
| search | string | 否 | 关键词搜索（设备ID/SN码） |

**成功响应 (200)：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "device_id": "string - 设备唯一ID",
        "mac_address": "string - MAC地址",
        "sn_code": "string - 序列号",
        "hardware_model": "string - 硬件型号",
        "firmware_version": "string - 固件版本",
        "bind_user_id": "string - 绑定用户ID",
        "lifecycle_status": 2,
        "is_online": true,
        "battery_level": 85,
        "current_mode": "idle",
        "last_heartbeat": "string (ISO8601) - 最后心跳时间",
        "created_at": "string (ISO8601) - 注册时间",
        "updated_at": "string (ISO8601) - 更新时间"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 150,
      "total_pages": 8
    }
  }
}
```

**分页响应字段说明：**
- `page`: 当前页码
- `page_size`: 每页条数
- `total`: 总记录数
- `total_pages`: 总页数

---

### 2.3 设备详情

#### GET /api/v1/devices/{device_id}

**成功响应 (200)：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "device_id": "string",
    "mac_address": "string",
    "sn_code": "string",
    "hardware_model": "string",
    "firmware_version": "string",
    "bind_user_id": "string",
    "lifecycle_status": 2,
    "shadow": {
      "is_online": true,
      "battery_level": 85,
      "current_mode": "idle",
      "last_ip": "string",
      "rssi": -60,
      "last_heartbeat": "string (ISO8601)",
      "desired_config": {}
    },
    "pet_profile": {
      "pet_name": "Mimi",
      "personality": "lively",
      "dnd_start_time": "23:00",
      "dnd_end_time": "08:00"
    },
    "created_at": "string (ISO8601)",
    "updated_at": "string (ISO8601)"
  }
}
```

---

## 三、错误码规范

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 4001 | 设备已存在 |
| 4002 | 设备不存在 |
| 4003 | 非法设备状态 |
| 4004 | 绑定失败 |
| 4005 | 参数校验失败 |
| 5001 | 服务器内部错误 |

---

**文档状态：** 已完成  
**下一步：** 交付给 agenthd (后端) 和 agentqd (前端) 进行开发
