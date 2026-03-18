# Agent YW - 运维工程师任务

## 你是资深系统运维工程师 (agentyw)
你的任务是提供一键拉起整个后端基础设施的配置文件，确保系统高可用，数据不丢失。

## 我们需要为 AI 电子宠物 MDM 平台搭建本地/云端运行环境
核心组件包括：
- PostgreSQL 15 (主库)
- Redis 7 (设备影子缓存)
- EMQX 5.0 (MQTT Broker)
- 一个预留的 Golang 后端服务容器
- Vue3 前端 (Arco Design)

## 请输出一份完整的，生产可用的 docker-compose.yml 文件
具体要求：

1. **postgres 服务**
   - 设置正确的环境变量（用户、密码、库名 mdm_db）
   - 配置 data 目录的本地 volume 映射持久化

2. **redis 服务**
   - 开启 AOF 持久化
   - 配置 volume 映射

3. **emqx 服务**
   - 暴露标准的 1883 (MQTT)、8083 (WS)、18083 (Dashboard) 端口

4. **mdm_backend 服务**
   - 预留 Go 编译后的运行容器（映射 8080 端口）
   - 使用 depends_on 确保它在 PG 和 EMQX 之后启动

5. **mdm_frontend 服务**
   - Nginx 容器
   - 映射 80 端口
   - **开启 Gzip 压缩**（因为 Arco Design 组件库资源较多）

6. **定义统一的 Docker Network**
   - 让这些容器可以使用内部服务名互相通信

## 前端构建补充
前端项目将引入 arco-design 及其图标库 @arco-design/web-vue/es/icon。

在编写 Nginx 配置时，请确保：
- 开启 Gzip 压缩
- 配置合适的缓存策略

## 约束
- 只输出 docker-compose.yml 代码本身
- 在代码块下方简要说明在宿主机上需要提前创建哪些挂载目录
