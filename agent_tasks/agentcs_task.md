# Agent CS - 测试工程师任务

## 你是高级自动化测试工程师 (agentcs)
你的任务是确保后端服务和 MQTT Broker 能够承受海量设备的并发冲击。

## 后端使用 EMQX 接收 MQTT 消息，Golang 处理业务
我们需要验证系统在弱网和多设备情况下的健壮性。

## 请使用 Python 编写一个高并发模拟压测脚本 (mqtt_stress_test.py)

### 具体要求：

1. 使用 paho-mqtt 库

2. 脚本需要利用多线程或 asyncio
   - 一次性虚拟生成 1000 个不同的 device_id

3. 让这 1000 个虚拟设备同时连接到指定的 EMQX Broker
   - 支持从环境变量读取 IP 和端口

4. 连接成功后，每个设备进入死循环
   - 每隔 30 秒向 /device/{device_id}/up/status 发送包含随机电量（0-100）和状态（online）的 JSON 心跳包

5. 打印实时的
   - 连接成功数
   - 消息发送成功数
   - 丢包数

## 约束
- 代码必须健壮，能优雅处理连接被服务器拒绝等异常
- 给出明确的 pip install 依赖项
