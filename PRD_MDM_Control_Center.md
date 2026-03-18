# 产品需求文档 (PRD)：AI 电子宠物 MDM 控制中台

版本号： V1.0 - 核心架构与设备管控

目标读者： 架构师、后端研发、前端研发、测试、运维

---

## 一、 产品概述

MDM (Mobile Device Management) 中台是整个"端云协同"架构的核心骨干（部署于 Mac mini 或云端服务器）。它负责统一管理分布在全球的 M5Stack 硬件终端，维护设备的生命周期（注册、在线、离线、升级、报废），并作为 OpenClaw 多智能体中枢与物理设备之间的"状态缓冲池"与"指令路由器"。

---

## 二、 核心模块与功能详情（精确到字段）

### 模块一：设备资产与生命周期管理 (Device Asset Management)

业务目标： 建立全局设备台账，实现设备从出厂烧录到用户绑定、报废的全链路追踪。

#### 1. 设备台账列表 (Device Registry)

| 字段 | 类型 | 说明 |
|------|------|------|
| device_id | String (主键) | 系统生成的全局唯一设备标识符（UUID） |
| mac_address | String (唯一索引) | M5Stack 物理网卡的 MAC 地址 |
| sn_code | String (唯一索引) | 贴在设备底部的产品序列号 |
| hardware_model | String | 硬件型号（如 CoreS3_Rover、StickC_Plus） |
| firmware_version | String | 当前运行的 MimiClaw 固件版本号 |
| activation_time | Datetime | 首次连网激活时间 |
| bind_user_id | String | 绑定的系统用户 ID |
| lifecycle_status | Enum [1-5] | 设备状态 [1:待激活, 2:正常服役, 3:维修中, 4:已挂失, 5:已报废] |

#### 2. 用户绑定与解绑接口

- 扫码绑定：校验 sn_code 和当前 lifecycle_status，通过后更新 bind_user_id，并触发 OpenClaw 初始化该用户的"专属宠物记忆库"。

---

### 模块二：设备影子与状态监控 (Device Shadow & Monitoring)

业务目标： 解决网络高延迟或断网问题，在服务器端保留一份设备的"最新物理快照"。

#### 1. 实时状态机 (State Snapshot)

终端通过 MQTT/WebSocket 每隔 30 秒（或状态变化时）上报：

| 字段 | 类型 | 说明 |
|------|------|------|
| connection_status | Enum [online, offline, poor_network] | 网络状态 |
| battery_level | Int | 0-100，电量百分比 |
| charging_status | Boolean | 是否正在充电 |
| current_mode | Enum [sleeping, roaming, listening, talking, idle] | 宠物当前模式 |
| last_ip_address | String | 最后公网 IP |
| rssi | Int | Wi-Fi 信号强度（负值，如 -60dBm） |

MDM 若 90 秒未收到心跳包，自动标记为 offline。低于 15% 触发低电量警报。

#### 2. 期望状态控制 (Desired State)

OpenClaw 修改 MDM 里的"期望状态"，设备上线后自行拉取：

| 字段 | 类型 | 说明 |
|------|------|------|
| desired_sleep_time | String | 设定的就寝时间（如 "22:00"） |
| desired_firmware | String | 期望升级到的目标固件版本 |

---

### 模块三：OTA 固件静默升级中心 (Over-The-Air Updates)

业务目标： 支撑全球设备的持续进化，支持灰度发布与异常自动回滚。

#### 1. 固件包管理 (Firmware Packages)

| 字段 | 类型 | 说明 |
|------|------|------|
| package_id | String | 固件包唯一 ID |
| version_name | String | 版本号（如 v2.0_Major） |
| bin_file_url | String | CDN 上的下载链接 |
| md5_checksum | String | 文件 MD5 校验码 |
| release_notes | Text | 更新日志 |
| force_update | Boolean | 是否强制升级 |

#### 2. 发布任务与灰度管控 (Deployment Tasks)

| 字段 | 类型 | 说明 |
|------|------|------|
| target_hardware | String | 指定升级的硬件型号 |
| rollout_strategy | Enum [全量, 百分比, 白名单] | 发布策略 |
| success_rate | Float | 升级成功率，低于 90% 自动暂停 |

---

### 模块四：宠物性格与管控策略 (Pet Configuration & Rules)

业务目标： 连接 MDM 与大模型，为每个设备存储个性化边界和规则。

#### 1. 宠物系统设定 (System Profile)

作为 System Prompt 变量注入：

| 字段 | 类型 | 说明 |
|------|------|------|
| pet_name | String | 用户自定义的宠物名字 |
| personality_base | Enum [活泼, 高冷, 暴躁, 粘人] | 基础性格底色 |
| interaction_frequency | Enum [高, 中, 低] | 偶发事件频率 |
| do_not_disturb_mode | JSON | 免打扰时间段 {"start": "23:00", "end": "08:00"} |

---

## 三、 研发团队任务分配

| Agent | 任务 |
|-------|------|
| **agenthd** | 设计 MySQL/PostgreSQL 数据库表结构，搭建 Redis 设备影子缓存层，提供设备激活、状态上报的 RESTful API |
| **agentqd** | 开发 Web 端管理控制台：设备列表分页查询、在线状态 Dashboard、OTA 固件上传和灰度配置 |
| **agentyw** | 规划 MQTT Broker (EMQX) 或 WebSocket 网关部署，配置 CDN 域名 |
| **agentcs** | 编写后端接口自动化测试，重点模拟网络环境测试心跳超时 |
| **agentcp** | 监控整体 API 规范，确保 OpenClaw 调用 MDM 接口逻辑顺畅 |
