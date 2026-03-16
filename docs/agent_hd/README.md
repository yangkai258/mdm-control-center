# 后端Agent (hd) - 文档库

## 📁 文档库结构

```
docs/agent_hd/
├── projects/          # 项目文档
│   ├── architectures/ # 架构设计
│   ├── apis/          # API文档
│   ├── databases/     # 数据库设计
│   └── deployments/   # 部署文档
├── technical/         # 技术文档
│   ├── frameworks/    # 框架文档
│   ├── libraries/     # 库文档
│   ├── patterns/      # 设计模式
│   └── standards/     # 开发标准
├── operations/        # 运维文档
│   ├── monitoring/    # 监控配置
│   ├── performance/   # 性能优化
│   ├── security/      # 安全配置
│   └── troubleshooting/ # 故障排查
├── learning/          # 学习文档
│   ├── tutorials/     # 教程文档
│   ├── notes/         # 学习笔记
│   └── resources/     # 学习资源
└── templates/         # 文档模板
    ├── api-design/    # API设计模板
    ├── db-design/     # 数据库设计模板
    ├── tech-design/   # 技术设计模板
    └── deployment/    # 部署文档模板
```

## 📋 核心文档模板

### 1. API设计文档模板
```markdown
# API设计文档

## 🎯 API基本信息
- **API名称**: 
- **版本**: v1.0
- **负责人**: hd (后端Agent)
- **创建日期**: 
- **状态**: 设计中/开发中/已上线

## 📋 接口列表
### 用户管理接口
| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| GET | `/api/v1/users` | 获取用户列表 | 管理员 |
| POST | `/api/v1/users` | 创建用户 | 管理员 |
| GET | `/api/v1/users/{id}` | 获取用户详情 | 用户本人/管理员 |
| PUT | `/api/v1/users/{id}` | 更新用户 | 用户本人/管理员 |
| DELETE | `/api/v1/users/{id}` | 删除用户 | 管理员 |

### 认证接口
| 方法 | 路径 | 描述 | 权限 |
|------|------|------|------|
| POST | `/api/v1/auth/login` | 用户登录 | 公开 |
| POST | `/api/v1/auth/register` | 用户注册 | 公开 |
| POST | `/api/v1/auth/logout` | 用户登出 | 登录用户 |
| POST | `/api/v1/auth/refresh` | 刷新令牌 | 登录用户 |

## 📊 数据模型

### 用户模型 (User)
```typescript
interface User {
  id: string;           // 用户ID
  username: string;     // 用户名
  email: string;        // 邮箱
  phone?: string;       // 手机号（可选）
  role: 'admin' | 'user'; // 角色
  status: 'active' | 'inactive' | 'suspended'; // 状态
  createdAt: Date;      // 创建时间
  updatedAt: Date;      // 更新时间
}
```

### 请求/响应格式
#### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {},           // 业务数据
  "timestamp": "2026-03-13T02:01:00Z"
}
```

#### 错误响应
```json
{
  "code": 400,
  "message": "请求参数错误",
  "errors": [           // 错误详情（可选）
    {
      "field": "email",
      "message": "邮箱格式不正确"
    }
  ],
  "timestamp": "2026-03-13T02:01:00Z"
}
```

## 🔐 认证授权

### 1. 认证方式
- **JWT令牌**: Bearer Token认证
- **Token格式**: `Bearer <jwt-token>`
- **Token有效期**: 访问令牌1小时，刷新令牌7天

### 2. 权限控制
- **公开接口**: 无需认证即可访问
- **用户权限**: 需要登录，只能访问自己的数据
- **管理员权限**: 需要管理员角色

### 3. 安全要求
- **HTTPS**: 所有API必须使用HTTPS
- **输入验证**: 所有输入必须验证
- **输出过滤**: 敏感信息不返回
- **限流防护**: API调用频率限制

## 📈 性能要求

### 1. 响应时间
- **简单查询**: < 100ms
- **复杂查询**: < 500ms
- **数据写入**: < 200ms
- **批量操作**: < 1000ms

### 2. 并发能力
- **预期QPS**: 1000
- **最大连接数**: 10000
- **连接超时**: 30秒
- **请求超时**: 10秒

### 3. 数据量
- **单表数据量**: ≤ 1000万条
- **单次查询返回**: ≤ 100条
- **分页大小**: 默认20，最大100

## 🔧 开发指南

### 1. 环境配置
```bash
# 安装依赖
npm install

# 开发环境启动
npm run dev

# 生产环境构建
npm run build

# 运行测试
npm test
```

### 2. 数据库配置
```yaml
# database.yml
development:
  host: localhost
  port: 3306
  database: app_dev
  username: root
  password: password

test:
  host: localhost
  port: 3306
  database: app_test
  username: root
  password: password

production:
  host: db.production.com
  port: 3306
  database: app_prod
  username: ${DB_USERNAME}
  password: ${DB_PASSWORD}
```

### 3. API开发示例
```typescript
// src/routes/user.routes.ts
import { Router } from 'express';
import { UserController } from '../controllers/user.controller';
import { authMiddleware } from '../middlewares/auth.middleware';
import { validate } from '../middlewares/validate.middleware';
import { createUserSchema, updateUserSchema } from '../schemas/user.schema';

const router = Router();
const userController = new UserController();

// 获取用户列表
router.get('/', authMiddleware('admin'), userController.getUsers);

// 创建用户
router.post('/', 
  authMiddleware('admin'),
  validate(createUserSchema),
  userController.createUser
);

// 获取用户详情
router.get('/:id', 
  authMiddleware(),
  userController.getUser
);

// 更新用户
router.put('/:id', 
  authMiddleware(),
  validate(updateUserSchema),
  userController.updateUser
);

// 删除用户
router.delete('/:id', 
  authMiddleware('admin'),
  userController.deleteUser
);

export default router;
```

## 🚀 部署配置

### 1. Docker配置
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm ci --only=production

# 复制源码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["npm", "start"]
```

### 2. Kubernetes配置
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
      - name: api-server
        image: api-server:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: db.host
```

### 3. 监控配置
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'api-server'
    static_configs:
      - targets: ['api-server:3000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

## 🔒 安全规范

### 1. 代码安全
- **SQL注入防护**: 使用参数化查询或ORM
- **XSS防护**: 输入验证和输出转义
- **CSRF防护**: CSRF Token验证
- **敏感信息**: 不在日志中记录敏感信息

### 2. API安全
- **认证**: 所有非公开API必须认证
- **授权**: 基于角色的访问控制
- **限流**: 防止API滥用
- **审计**: 记录所有重要操作

### 3. 数据安全
- **加密**: 敏感数据加密存储
- **备份**: 定期数据备份
- **恢复**: 数据恢复演练
- **清理**: 定期清理过期数据

## 📝 质量保证

### 1. 测试策略
- **单元测试**: 覆盖核心业务逻辑
- **集成测试**: 测试API接口和数据库
- **性能测试**: 测试系统性能指标
- **安全测试**: 测试安全漏洞

### 2. 代码质量
- **代码审查**: Pull Request代码审查
- **静态分析**: ESLint、TypeScript检查
- **测试覆盖率**: ≥ 85%代码覆盖率
- **文档完整**: API文档和开发文档

### 3. 监控告警
- **性能监控**: 响应时间、错误率
- **业务监控**: 关键业务指标
- **安全监控**: 安全事件和攻击
- **容量监控**: 资源使用情况

---
**文档版本**: v1.0  
**创建时间**: 2026-03-13  
**创建人**: hd (后端Agent)  
**更新记录**: 初始版本创建