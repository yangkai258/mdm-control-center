# HEARTBEAT.md - Proactive Agent 检查

# 🚀 项目就绪 - 等待用户指令

## 用户指令
用户关机前说: "明天开机再做后续的内容，我要怎么跟你说，你会立即执行"

## 触发条件
用户发送**任何消息** = 立即执行明日计划

## 立即执行清单
当用户发消息时，自动执行以下（无需询问）:

### 1. 启动服务
```bash
# 1. 检查 Docker 状态
docker ps

# 2. 如果容器未运行，启动
cd C:\Users\YKing\.openclaw\workspace\mdm-project
docker-compose up -d

# 3. 等待后端就绪
docker exec mdm_backend curl http://localhost:8080/health
```

### 2. 执行明日计划 (docs/SPRINT_TOMORROW.md)
按计划分配 5 个 Agent:
1. **agenthd** - 后端开发 (5h): stores API + ai/model/shards
2. **agentqd** - 前端验收 (5h)
3. **agentcp** - PRD 补充 (4h)
4. **agentcs** - 全面测试 (4h)
5. **agentyw** - CI/CD (2h)

### 3. 监控进度
- 每 30 分钟检查 Agent 状态
- 阻塞时及时汇报

## 无需主动提醒用户
系统会等待用户消息，用户发消息即触发执行。
