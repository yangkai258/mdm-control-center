# 项目架构规划

## 概述
工作区下有两个独立项目，分别存放在不同目录。

## 项目结构

```
C:\Users\YKing\.openclaw\workspace\
│
├── mbti-project/          # MBTI测试项目
│   ├── test.html           # 前端页面
│   ├── login.html          # 登录页面
│   ├── complete_server.py  # 后端服务
│   ├── mbti_questions_100.json  # 题目数据
│   └── mbti_test.db      # SQLite数据库
│
├── mdm-project/           # MDM控制中台项目
│   ├── backend/           # Golang后端
│   │   ├── models/       # 数据模型
│   │   ├── controllers/  # 控制器
│   │   ├── mqtt/        # MQTT处理
│   │   └── utils/       # 工具类
│   ├── frontend/         # Vue3前端
│   │   └── src/views/   # 页面组件
│   ├── agent_tasks/     # Agent任务定义
│   ├── test_scripts/   # 测试脚本
│   ├── docker-compose.yml
│   └── PRD_*.md         # 项目文档
│
├── AGENTS.md             # Agent配置文件（根目录）
├── SESSION-STATE.md      # 当前会话状态
├── HEARTBEAT.md         # 心跳检查
└── memory/              # 每日工作日志
```

## GitHub仓库

| 项目 | 仓库 | 说明 |
|------|------|------|
| MBTI测试 | https://github.com/yangkai258/mbti-web | 已在master分支 |
| MDM控制中台 | https://github.com/yangkai258/mdm-control-center | 已在main分支 |

## 开发原则

1. **项目隔离**：不同项目的文件必须存放在各自目录
2. **依赖明确**：每个项目有独立的依赖和环境配置
3. **文档归属**：项目文档随项目走，不放在根目录
4. **Agent配置**：全局Agent配置在根目录，项目特定配置在各项目目录

## 架构师职责

- 规划项目目录结构
- 确保项目文件不混淆
- 维护项目间依赖关系
- 定期审查文件位置
