# 全局技术栈与存储方案选型

## 技术栈

### 后端核心 (agenthd)
- **Golang** (使用 Gin 框架)
- Go 语言极其适合处理 IoT 场景下海量设备的高并发心跳包和 WebSocket/MQTT 长连接

### 前端后台 (agentqd)
- **Vue3 + TypeScript**
- 使用 Element Plus UI 库
- 快速构建 MDM 管理控制台

### 消息中间件 (agentyw)
- **EMQX** (开源的企业级 MQTT Broker)
- 专门负责与所有 M5Stack 终端保持长连接，处理 Pub/Sub 消息流转

### 主数据库 (agenthd & agentyw)
- **PostgreSQL 15+**
- 负责存储绝对不能丢失的设备台账、固件版本和用户资产数据

### 状态缓存与影子 (agenthd)
- **Redis 7.0**
- 存储设备的实时高频心跳、电量、当前在线状态（设备影子）
- 避免高频读写击穿 PostgreSQL

### 数据交换格式
- 前后端及端云之间均使用 **JSON**

---

## 核心数据库表结构设计

### 1. 设备资产主表 mdm_devices

```sql
CREATE TABLE mdm_devices (
    id BIGSERIAL PRIMARY KEY,
    device_id VARCHAR(36) UNIQUE NOT NULL,
    mac_address VARCHAR(17) UNIQUE NOT NULL,
    sn_code VARCHAR(32) UNIQUE NOT NULL,
    hardware_model VARCHAR(32) NOT NULL,
    firmware_version VARCHAR(32) NOT NULL,
    bind_user_id VARCHAR(36),
    lifecycle_status SMALLINT DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
```

| 字段 | 类型 | 约束 | 描述 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| device_id | VARCHAR(36) | UNIQUE, NOT NULL | 全局唯一设备 ID (UUID v4) |
| mac_address | VARCHAR(17) | UNIQUE, NOT NULL | 硬件网卡 MAC 地址 |
| sn_code | VARCHAR(32) | UNIQUE, NOT NULL | 产品序列号 |
| hardware_model | VARCHAR(32) | NOT NULL | 硬件型号 |
| firmware_version | VARCHAR(32) | NOT NULL | 当前运行固件版本 |
| bind_user_id | VARCHAR(36) | INDEX | 绑定的主人用户 ID |
| lifecycle_status | SMALLINT | DEFAULT 1 | 状态: 1待激活, 2服役中, 3维修, 4报废 |
| created_at | TIMESTAMPTZ | NOT NULL | 出厂录入时间 |
| updated_at | TIMESTAMPTZ | NOT NULL | 最后更新时间 |

### 2. 设备影子表 mdm_device_shadows

此表的高频更新在 Redis 中进行，后台通过定时任务（Cron）每 5 分钟向 PostgreSQL 此表持久化一次。

```sql
CREATE TABLE mdm_device_shadows (
    device_id VARCHAR(36) PRIMARY KEY,
    is_online BOOLEAN DEFAULT FALSE,
    battery_level SMALLINT CHECK (battery_level >= 0 AND battery_level <= 100),
    current_mode VARCHAR(20) DEFAULT 'idle',
    last_ip VARCHAR(45),
    last_heartbeat TIMESTAMPTZ,
    desired_config JSONB
);
```

| 字段 | 类型 | 约束 | 描述 |
|------|------|------|------|
| device_id | VARCHAR(36) | PRIMARY KEY | 关联 mdm_devices |
| is_online | BOOLEAN | DEFAULT FALSE | MQTT 是否处于连接状态 |
| battery_level | SMALLINT | CHECK (0-100) | 当前剩余电量百分比 |
| current_mode | VARCHAR(20) | DEFAULT 'idle' | 宠物当前状态 |
| last_ip | VARCHAR(45) | | 最后一次上报心跳的 IP 地址 |
| last_heartbeat | TIMESTAMPTZ | INDEX | 最后心跳时间戳 |
| desired_config | JSONB | | 期望状态配置 |

### 3. 固件包 OTA 管理表 mdm_ota_packages

```sql
CREATE TABLE mdm_ota_packages (
    id BIGSERIAL PRIMARY KEY,
    version_code VARCHAR(32) UNIQUE NOT NULL,
    hardware_model VARCHAR(32) NOT NULL,
    bin_url VARCHAR(255) NOT NULL,
    md5_hash VARCHAR(32) NOT NULL,
    is_mandatory BOOLEAN DEFAULT FALSE,
    release_status SMALLINT DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL
);
```

| 字段 | 类型 | 约束 | 描述 |
|------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| version_code | VARCHAR(32) | UNIQUE, NOT NULL | 版本号 |
| hardware_model | VARCHAR(32) | NOT NULL | 适配的硬件型号 |
| bin_url | VARCHAR(255) | NOT NULL | 固件 .bin 文件 CDN 链接 |
| md5_hash | VARCHAR(32) | NOT NULL | 文件的 MD5 校验码 |
| is_mandatory | BOOLEAN | DEFAULT FALSE | 是否强制升级 |
| release_status | SMALLINT | DEFAULT 0 | 0:测试中, 1:灰度发布, 2:全量发布 |

### 4. 宠物设定与偏好表 pet_profiles

```sql
CREATE TABLE pet_profiles (
    device_id VARCHAR(36) PRIMARY KEY,
    pet_name VARCHAR(64) DEFAULT 'Mimi',
    personality VARCHAR(32) DEFAULT 'lively',
    interaction_freq VARCHAR(16) DEFAULT 'medium',
    dnd_start_time TIME DEFAULT '23:00',
    dnd_end_time TIME DEFAULT '08:00',
    custom_rules JSONB,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
```

| 字段 | 类型 | 约束 | 描述 |
|------|------|------|------|
| device_id | VARCHAR(36) | PRIMARY KEY | 关联的设备 ID |
| pet_name | VARCHAR(64) | DEFAULT 'Mimi' | 用户给宠物取的名字 |
| personality | VARCHAR(32) | DEFAULT 'lively' | 核心性格设定 |
| interaction_freq | VARCHAR(16) | DEFAULT 'medium' | 互动频率 |
| dnd_start_time | TIME | DEFAULT '23:00' | 免打扰开始时间 |
| dnd_end_time | TIME | DEFAULT '08:00' | 免打扰结束时间 |
| custom_rules | JSONB | | 用户的特殊指令集 |

---

## 各 Agent 任务拆解

### 1. agentcp (产品经理)
- 产出全部 RESTful API 的 Swagger 文档和 MQTT Topic 规范定义
- 必须定义清楚设备注册流、心跳上报流、OTA 升级流的业务状态机逻辑

### 2. agenthd (后端开发)
- 根据表结构使用 GORM (Golang) 完成数据访问层开发
- 实现 HTTP API 接口
- 编写 MQTT WebHook 回调服务
- 标准：所有接口响应时间必须小于 200ms

### 3. agentqd (前端开发)
- 开发 MDM 网页端：设备大盘监控页、设备详情页、OTA 任务发布与进度监控页
- 必须接入 WebSocket，实现设备状态实时变绿

### 4. agentyw (运维/DevOps)
- 编写一键部署的 docker-compose.yml
- 一键拉起 PostgreSQL、Redis、EMQX、后端 Go 服务和前端 Nginx
- 必须为 PostgreSQL 配置数据卷持久化
- 必须为 EMQX 配置鉴权插件

### 5. agentcs (测试/QA)
- 编写 Python 压力测试脚本
- 模拟 10,000 个虚拟设备同时向 EMQX 发送 MQTT 心跳包
- 模拟弱网环境下心跳超时的状态反转测试
- 出具压测报告，确保每秒 500 次心跳并发下系统稳定

---

## 时间预估 (5 个 Agent 24小时连轴转)

| 阶段 | 时间 | 内容 |
|------|------|------|
| 基建期 | 第 1-12 小时 | agentcp 输出 API 契约；agentyw 跑通 Docker；agenthd 完成建表与 ORM |
| 核心业务开发 | 第 13-36 小时 | agenthd 完成后台逻辑和 MQTT 集成；agentqd 完成前端面板 |
| 前后端联调 | 第 37-48 小时 | 接口字段对齐、跨域问题、WebSocket 实时推送 |
| 高并发压测 | 第 49-72 小时 | agentcs 压测，agenthd 修复内存泄漏和死锁 |

**极限效率预估：60-72 小时 (2.5-3 天)**
