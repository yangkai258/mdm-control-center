# MEMORY.md - 全局长期记忆

## 项目概述

### MDM 控制中台
- **类型**: 移动设备管理 + 会员管理系统
- **技术栈**: Go + Gin + GORM / Vue 3 + Arco Design
- **路径**: C:\Users\YKing\.openclaw\workspace\mdm-project

## 团队架构

| Agent | 角色 | 目录 |
|-------|------|------|
| zg (主) | 架构师/主管 | workspace |
| agentcp | 产品经理 | mdm-project/docs |
| agenthd | 后端开发 | mdm-project/backend |
| agentqd | 前端开发 | mdm-project/frontend |
| agentcs | 测试工程师 | mdm-project/testing |
| agentyw | 运维工程师 | mdm-project/ops |

## 技能库

已安装以下技能提升团队效率：
- agent-task-tracker
- agent-orchestrate
- team-status-tracker
- skill-vetter
- self-monitor
- task-development-workflow
- product-manager
- requirements-analysis
- memory-setup
- proactive-agent

## 完成的功能

### 设备管理
- 设备注册/绑定/解绑
- 设备状态管理
- OTA 固件管理
- 指令下发

### 会员管理
- 会员 CRUD (9个子模块)
- 会员卡管理
- 优惠券管理
- 会员等级
- 积分规则
- 促销活动
- 店铺管理
- 订单管理

## 访问信息
- 前端: http://localhost:3000
- 后端: http://localhost:8080
- 账号: admin / admin123

## 重要教训

1. **架构师不自己干活** - Agent 超时应该分析原因、重新派任务，不是自己写代码
2. **任务要小而明确** - 避免大任务导致超时
3. **检查点机制** - 监控 Agent 状态，及时干预

---

## 2026-03-20 重大更新

### 团队深度分析
- 4个Agent并行分析MDM项目
- 产出4份分析报告 (PRODUCT/BACKEND/FRONTEND/ARCHITECTURE)

### 识别的核心问题

**P0阻断性 (9个):**
- JWT密钥硬编码
- CORS全开放
- MQTT注入为nil (指令下发失效)
- OTA无后台Worker
- CheckAlerts从未调用
- 回车登录失效
- deleteRecord不删数据
- member.html文件损坏
- Dashboard统计查询错误字段

**P1高优先级 (5个):**
- N+1查询问题
- Redis URL解析失效
- 主色拼写错误(165qff)
- API硬编码localhost
- 无登录限流

### GitHub
- https://github.com/yangkai258/mdm-iot-platform

### 下一步
- 修P0阻断性问题
- 重构后端架构
- 优化前端代码

---

_持续更新，记录项目的成长轨迹。_
