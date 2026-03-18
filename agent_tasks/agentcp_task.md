# Agent CP - 产品经理任务

## 你是核心产品经理兼架构师 (agentcp)
你的任务是输出严格的接口契约，不写具体的业务代码，只定义标准。

## 我们正在开发一个 AI 电子宠物 MDM (移动设备管理) 平台
- 前端是 M5Stack 硬件（采用 Arco Design Vue）
- 后端是 Golang
- 两者通过 MQTT 通信
- Web 管理台通过 HTTP API 与后端通信

## 请严格按照以下要求输出两份规范文档（使用 Markdown 格式，代码块清晰）：

### 任务 1：MQTT Topic 树与 JSON 协议定义

定义设备心跳上报 Topic (如 /device/{device_id}/up/status) 及其 JSON Payload 结构（包含电量、在线状态、当前模式）。

定义云端下发指令 Topic (如 /device/{device_id}/down/cmd) 及其 JSON Payload 结构（包含期望动作、UI 渲染指令）。

### 任务 2：核心 HTTP API 接口规范 (RESTful)

#### 2.1 设备注册/绑定
定义 /api/v1/devices/register (设备注册/绑定) 的请求体和响应体。

#### 2.2 设备列表（分页+筛选）
定义 /api/v1/devices/list (获取设备台账和实时状态列表) 的请求体和响应体。

**必须包含 Arco Table 标准的分页参数：**
- page: 页码
- pageSize: 每页条数
- 返回 total: 总数

**必须包含筛选参数：**
- status: 设备状态 (online/offline)
- lifecycle_status: 生命周期状态

## 约束
- 字段命名统一使用 snake_case
- 所有 JSON 示例必须包含注释
- API 必须支持分页和筛选，以便前端 a-table 配置筛选器
