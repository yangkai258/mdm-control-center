# -*- coding: utf-8 -*-
fp = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(fp, 'a', encoding='utf-8') as f:
    f.write('''

---

## 十五、实施工具

### 15.1 收藏菜单

| 字段 | 类型 | 说明 |
|------|------|------|
| favorite_id | UUID | 主键 |
| user_id | UUID | 用户ID |
| menu_id | UUID | 菜单ID |
| sort_order | INT | 排序 |
| created_at | TIMESTAMPTZ | 创建时间 |

**API**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/favorites` | 收藏列表 |
| POST | `/api/v1/tenants/{tenant_id}/favorites` | 添加收藏 |
| DELETE | `/api/v1/tenants/{tenant_id}/favorites/{id}` | 取消收藏 |
| PUT | `/api/v1/tenants/{tenant_id}/favorites/reorder` | 重新排序 |

### 15.2 首页配置

**API**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/dashboards/{user_id}` | 获取配置 |
| PUT | `/api/v1/tenants/{tenant_id}/dashboards/{user_id}` | 保存配置 |
| POST | `/api/v1/tenants/{tenant_id}/dashboards/{user_id}/reset` | 重置为默认 |

### 15.3 邮件配置

| 字段 | 类型 | 说明 |
|------|------|------|
| email_config_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| smtp_host | VARCHAR(100) | SMTP服务器 |
| smtp_port | INT | 端口 |
| smtp_username | VARCHAR(100) | 用户名 |
| smtp_password | VARCHAR(100) | 密码（加密存储） |
| from_address | VARCHAR(100) | 发件人地址 |
| is_default | BOOLEAN | 是否默认 |
| updated_at | TIMESTAMPTZ | 更新时间 |

**API**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/email-configs` | 列表 |
| POST | `/api/v1/tenants/{tenant_id}/email-configs` | 创建 |
| PUT | `/api/v1/tenants/{tenant_id}/email-configs/{id}` | 更新 |
| DELETE | `/api/v1/tenants/{tenant_id}/email-configs/{id}` | 删除 |
| POST | `/api/v1/tenants/{tenant_id}/email-configs/{id}/test` | 测试发送 |

### 15.4 消息通知

| 字段 | 类型 | 说明 |
|------|------|------|
| notification_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| user_id | UUID | 接收用户 |
| title | VARCHAR(100) | 标题 |
| content | TEXT | 内容 |
| type | ENUM | system/task/alert |
| is_read | BOOLEAN | 是否已读 |
| created_at | TIMESTAMPTZ | 创建时间 |

**API**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/notifications` | 我的消息 |
| GET | `/api/v1/tenants/{tenant_id}/notifications/{id}` | 详情 |
| POST | `/api/v1/tenants/{tenant_id}/notifications/{id}/read` | 标记已读 |
| POST | `/api/v1/tenants/{tenant_id}/notifications/mark-all-read` | 全部已读 |
| DELETE | `/api/v1/tenants/{tenant_id}/notifications/{id}` | 删除 |

### 15.5 系统版本信息

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/system/version` | 版本信息 |
| GET | `/api/v1/system/health` | 健康检查 |
| GET | `/api/v1/system/capabilities` | 系统能力 |

### 15.6 外部服务

| 字段 | 类型 | 说明 |
|------|------|------|
| service_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| service_name | VARCHAR(100) | 服务名称 |
| service_type | ENUM | wechat/dingtalk/feishu/other |
| config | JSONB | 配置信息 |
| is_active | BOOLEAN | 是否启用 |
| updated_at | TIMESTAMPTZ | 更新时间 |

**API**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/external-services` | 列表 |
| POST | `/api/v1/tenants/{tenant_id}/external-services` | 创建 |
| PUT | `/api/v1/tenants/{tenant_id}/external-services/{id}` | 更新 |
| DELETE | `/api/v1/tenants/{tenant_id}/external-services/{id}` | 删除 |
| POST | `/api/v1/tenants/{tenant_id}/external-services/{id}/test` | 测试连接 |
| POST | `/api/v1/tenants/{tenant_id}/external-services/{id}/sync` | 同步数据 |

### 15.7 系统参数设置

| 字段 | 类型 | 说明 |
|------|------|------|
| param_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| param_key | VARCHAR(100) | 参数键 |
| param_value | TEXT | 参数值 |
| param_type | ENUM | string/number/boolean/json |
| description | VARCHAR(200) | 说明 |
| is_system | BOOLEAN | 是否系统参数 |
| updated_at | TIMESTAMPTZ | 更新时间 |

**API**:

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/params` | 列表 |
| GET | `/api/v1/tenants/{tenant_id}/params/{key}` | 获取单个 |
| POST | `/api/v1/tenants/{tenant_id}/params` | 创建 |
| PUT | `/api/v1/tenants/{tenant_id}/params/{key}` | 更新 |
| DELETE | `/api/v1/tenants/{tenant_id}/params/{key}` | 删除 |

---

## 十六、数据库设计

### 16.1 平台级表（无 tenant_id）

#### tenants（租户台账）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| tenant_code | VARCHAR(20) | UNIQUE, NOT NULL | 租户编码 |
| company_name | VARCHAR(100) | NOT NULL | 企业全称 |
| plan_id | INT | NOT NULL | 套餐ID |
| status | VARCHAR(20) | DEFAULT | active/suspended/expired |
| expire_time | TIMESTAMPTZ | NOT NULL | 到期时间 |
| logo_url | VARCHAR(500) | NULL | Logo URL |
| custom_domain | VARCHAR(100) | NULL | 自定义域名 |
| contact_name | VARCHAR(50) | NULL | 联系人 |
| contact_phone | VARCHAR(20) | NULL | 联系电话 |
| contact_email | VARCHAR(100) | NULL | 邮箱 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

#### tenant_applications（租户申请记录）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | SERIAL | PK | 主键 |
| app_no | VARCHAR(20) | UNIQUE, NOT NULL | 申请编号 |
| company_name | VARCHAR(100) | NOT NULL | 企业名称 |
| contact_name | VARCHAR(50) | NOT NULL | 联系人 |
| contact_phone | VARCHAR(20) | NOT NULL | 联系电话 |
| contact_email | VARCHAR(100) | NOT NULL | 邮箱 |
| industry | VARCHAR(50) | NULL | 行业 |
| company_size | VARCHAR(20) | NULL | 规模 |
| plan_id | INT | NOT NULL | 申请套餐 |
| use_case | TEXT | NULL | 使用场景 |
| status | VARCHAR(20) | DEFAULT | pending/approved/rejected |
| reject_reason | TEXT | NULL | 拒绝原因 |
| audit_by | UUID | NULL | 审核人 |
| audit_at | TIMESTAMPTZ | NULL | 审核时间 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |

#### plans（套餐定义）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | SERIAL | PK | 主键 |
| plan_name | VARCHAR(20) | NOT NULL | 套餐名称 |
| plan_code | VARCHAR(20) | UNIQUE, NOT NULL | 套餐代码 |
| price_monthly | DECIMAL(10,2) | NULL | 月费 |
| price_yearly | DECIMAL(10,2) | NULL | 年费 |
| user_quota | INT | NOT NULL | 用户数上限 |
| device_quota | INT | NOT NULL | 设备数上限 |
| dept_quota | INT | NOT NULL | 部门数上限 |
| store_quota | INT | NOT NULL | 门店数上限 |
| features | JSONB | DEFAULT | 功能开关 |
| sort_order | INT | DEFAULT 0 | 排序 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否上架 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |

#### dicts（公共字典）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | SERIAL | PK | 主键 |
| category | VARCHAR(30) | NOT NULL | 分类标识 |
| item_code | VARCHAR(30) | NOT NULL | 字典项代码 |
| item_name | VARCHAR(50) | NOT NULL | 字典项名称 |
| sort_order | INT | DEFAULT 0 | 排序 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| description | VARCHAR(200) | NULL | 说明 |

#### audit_logs（审计日志）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGSERIAL | PK | 主键 |
| tenant_id | UUID | NULL | 所属租户 |
| user_id | UUID | NULL | 操作人 |
| action | VARCHAR(50) | NOT NULL | 操作类型 |
| resource_type | VARCHAR(50) | NULL | 资源类型 |
| resource_id | VARCHAR(36) | NULL | 资源ID |
| detail | JSONB | NULL | 变更详情 |
| ip_address | INET | NULL | IP地址 |
| user_agent | TEXT | NULL | 浏览器UA |
| is_cross_tenant | BOOLEAN | DEFAULT FALSE | 是否跨租户操作 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 操作时间 |

### 16.2 业务表（所有表含 tenant_id 字段）

#### tenant_quotas（租户配额表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | SERIAL | PK | 主键 |
| tenant_id | UUID | FK(tenants), UNIQUE | 所属租户 |
| user_count | INT | DEFAULT 0 | 当前用户数 |
| device_count | INT | DEFAULT 0 | 当前设备数 |
| dept_count | INT | DEFAULT 0 | 当前部门数 |
| store_count | INT | DEFAULT 0 | 当前门店数 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

#### users（用户表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| tenant_id | UUID | NOT NULL | 所属租户 |
| dept_id | UUID | NULL | 所属部门 |
| username | VARCHAR(50) | NOT NULL | 用户名 |
| password_hash | VARCHAR(255) | NOT NULL | 密码（bcrypt） |
| real_name | VARCHAR(50) | NOT NULL | 真实姓名 |
| phone | VARCHAR(20) | NOT NULL | 手机号 |
| email | VARCHAR(100) | NULL | 邮箱 |
| role | VARCHAR(20) | NOT NULL | tenant_admin/normal_user |
| status | VARCHAR(20) | DEFAULT | active/disabled |
| last_login_at | TIMESTAMPTZ | NULL | 最近登录 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| created_by | UUID | NOT NULL | 创建人 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |
| deleted_at | TIMESTAMPTZ | NULL | 软删除时间 |

### 16.3 GORM中间件实现

TenantPlugin（GORM Callback模式的租户隔离）:

```go
func (p *TenantPlugin) Name() string { return "tenant_scope" }
func (p *TenantPlugin) Initialize(db *gorm.DB) error {
    db.Callback().Create().Before("gorm:before_create").Register("tenant:before_create", setTenantID)
    db.Callback().Query().Before("gorm:query").Register("tenant:before_query", filterByTenant)
    db.Callback().Update().Before("gorm:before_update").Register("tenant:before_update", filterByTenant)
    db.Callback().Delete().Before("gorm:before_delete").Register("tenant:before_delete", filterByTenant)
    return nil
}
```

### 16.4 索引设计

| 表名 | 索引字段 | 类型 | 说明 |
|------|----------|------|------|
| users | tenant_id | B-Tree | 租户用户查询 |
| users | (tenant_id, username) | B-Tree | 唯一约束 |
| users | (tenant_id, phone) | B-Tree | 唯一约束 |
| departments | tenant_id | B-Tree | 租户部门查询 |
| departments | parent_id | B-Tree | 树形查询 |
| stores | tenant_id | B-Tree | 租户门店查询 |
| stores | (tenant_id, store_code) | B-Tree | 唯一约束 |
| devices | tenant_id | B-Tree | 租户设备查询 |
| devices | device_id | B-Tree | 设备查询 |
| audit_logs | tenant_id | B-Tree | 租户审计 |
| audit_logs | created_at | B-Tree | 时间范围查询 |
| tenant_quotas | tenant_id | B-Tree | 唯一约束 |

---

## 十七、API接口总览

### 17.1 平台管理（超级管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/tenants` | 租户列表 |
| GET | `/api/v1/admin/tenants/{id}` | 租户详情 |
| PUT | `/api/v1/admin/tenants/{id}` | 更新租户 |
| DELETE | `/api/v1/admin/tenants/{id}` | 删除租户 |
| PUT | `/api/v1/admin/tenants/{id}/suspend` | 禁用租户 |
| PUT | `/api/v1/admin/tenants/{id}/activate` | 启用租户 |
| PUT | `/api/v1/admin/tenants/{id}/extend` | 延长租期 |
| POST | `/api/v1/admin/tenants/{id}/change-plan` | 变更套餐 |
| GET | `/api/v1/admin/tenants/applications` | 申请列表 |
| POST | `/api/v1/admin/tenants/applications/{id}/approve` | 审核通过 |
| POST | `/api/v1/admin/tenants/applications/{id}/reject` | 审核拒绝 |
| GET | `/api/v1/admin/plans` | 套餐列表 |
| POST | `/api/v1/admin/plans` | 新增套餐 |
| PUT | `/api/v1/admin/plans/{id}` | 更新套餐 |
| GET | `/api/v1/admin/dicts` | 字典列表 |
| POST | `/api/v1/admin/dicts` | 新增字典项 |
| GET | `/api/v1/admin/roles` | 角色列表 |
| POST | `/api/v1/admin/roles` | 创建角色 |
| PUT | `/api/v1/admin/roles/{id}/permissions` | 分配权限 |
| GET | `/api/v1/admin/permissions` | 权限点列表 |

### 17.2 租户管理（租户管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/users` | 用户列表 |
| POST | `/api/v1/tenants/{tenant_id}/users` | 创建用户（含配额校验） |
| GET | `/api/v1/tenants/{tenant_id}/users/{id}` | 用户详情 |
| PUT | `/api/v1/tenants/{tenant_id}/users/{id}` | 更新用户 |
| DELETE | `/api/v1/tenants/{tenant_id}/users/{id}` | 删除用户（软删除） |
| PUT | `/api/v1/tenants/{tenant_id}/users/{id}/reset-password` | 重置密码 |
| GET | `/api/v1/tenants/{tenant_id}/departments` | 部门树 |
| POST | `/api/v1/tenants/{tenant_id}/departments` | 新增部门 |
| GET | `/api/v1/tenants/{tenant_id}/stores` | 门店列表 |
| POST | `/api/v1/tenants/{tenant_id}/stores` | 新增门店 |
| GET | `/api/v1/tenants/{tenant_id}/company` | 获取公司信息 |
| PUT | `/api/v1/tenants/{tenant_id}/company` | 更新公司信息 |

### 17.3 流程管理API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/workflows` | 流程列表 |
| POST | `/api/v1/tenants/{tenant_id}/workflows` | 创建流程 |
| GET | `/api/v1/tenants/{tenant_id}/workflows/{id}` | 流程详情 |
| PUT | `/api/v1/tenants/{tenant_id}/workflows/{id}` | 更新流程 |
| DELETE | `/api/v1/tenants/{tenant_id}/workflows/{id}` | 删除流程 |
| POST | `/api/v1/tenants/{tenant_id}/workflows/{id}/publish` | 发布流程 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/todo` | 我的待办 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/complete` | 办理任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/reject` | 拒绝任务 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/done` | 我已处理 |

### 17.4 会员营销API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/members` | 会员列表 |
| POST | `/api/v1/tenants/{tenant_id}/members` | 创建会员 |
| GET | `/api/v1/tenants/{tenant_id}/members/{id}` | 会员详情 |
| PUT | `/api/v1/tenants/{tenant_id}/members/{id}` | 更新会员 |
| GET | `/api/v1/tenants/{tenant_id}/member-cards` | 会员卡列表 |
| POST | `/api/v1/tenants/{tenant_id}/member-cards` | 创建会员卡 |
| GET | `/api/v1/tenants/{tenant_id}/coupons` | 优惠券列表 |
| POST | `/api/v1/tenants/{tenant_id}/coupons` | 创建优惠券 |
| POST | `/api/v1/tenants/{tenant_id}/coupons/{id}/grant` | 发放优惠券 |
| GET | `/api/v1/tenants/{tenant_id}/member-tags` | 会员标签列表 |
| POST | `/api/v1/tenants/{tenant_id}/member-tags` | 创建标签 |
| GET | `/api/v1/tenants/{tenant_id}/member-points` | 积分流水 |
| POST | `/api/v1/tenants/{tenant_id}/member-points/adjust` | 调整积分 |

---

## 十八、前端页面清单

### 18.1 公开页面

| 页面路径 | 角色 | 功能 |
|----------|------|------|
| `/login` | 公开 | 登录页 |
| `/register` | 公开 | 租户注册申请 |
| `/forgot-password` | 公开 | 找回密码 |

### 18.2 超级管理员页面

| 页面路径 | 功能 |
|----------|------|
| `/admin/tenants` | 租户列表 |
| `/admin/tenants/applications` | 申请审核列表 |
| `/admin/plans` | 套餐管理 |
| `/admin/dicts` | 公共字典管理 |
| `/admin/permissions` | 权限点管理 |
| `/admin/roles` | 角色管理 |

### 18.3 租户管理员页面

| 页面路径 | 功能 |
|----------|------|
| `/dashboard` | 首页仪表盘 |
| `/settings/tenant` | 本租户信息配置 |
| `/settings/profile` | 个人信息管理 |
| `/users` | 租户用户列表 |
| `/departments` | 组织架构管理 |
| `/stores` | 门店列表 |
| `/org/company` | 公司信息管理 |
| `/org/posts` | 岗位管理 |
| `/permissions/roles` | 角色管理 |
| `/workflows` | 流程列表 |
| `/tasks/todo` | 我的待办 |
| `/tasks/done` | 我已处理 |

### 18.4 会员营销页面

| 页面路径 | 功能 |
|----------|------|
| `/member/members` | 会员列表 |
| `/member/members/{id}` | 会员详情 |
| `/member/cards` | 会员卡管理 |
| `/member/coupons` | 优惠券管理 |
| `/member/tags` | 会员标签 |
| `/member/points` | 积分管理 |
| `/member/activities` | 促销活动 |
| `/member/gifts` | 礼包管理 |
| `/member/services` | 会员服务 |

---

## 十九、非功能性需求

### 19.1 性能要求

| 指标 | 要求 |
|------|------|
| 租户开通 | 开通流程 <= 10秒 |
| 列表查询 | 1000条数据分页加载 <= 500ms |
| 权限校验 | 中间件额外延迟 <= 5ms |
| 并发租户数 | 单实例支持 >= 500 个活跃租户 |
| 配额校验 | 原子操作，<= 10ms |
| API响应时间 | P95 <= 200ms |

### 19.2 可用性要求

| 要求项 | 说明 |
|--------|------|
| 租户独立性 | 单个租户故障不影响其他租户 |
| 降级策略 | 禁用非核心功能，保证登录和基础设备管理 |
| 数据备份 | 每日全量备份，保留 30 天 |

### 19.3 安全性要求

| 要求项 | 说明 |
|--------|------|
| 密码策略 | 长度>=8位，需包含大小写字母+数字，90天强制更换 |
| JWT 有效期 | Access Token 2小时，Refresh Token 7天 |
| 超级管理员操作 | 所有删除操作需二次确认 |
| 租户隔离 | 跨租户 SQL 执行触发实时告警 |
| 数据传输 | 全链路 TLS 1.2+ 加密 |
| 敏感数据 | 密码、密钥等加密存储（AES-256） |

### 19.4 兼容性要求

| 要求项 | 说明 |
|--------|------|
| 前端兼容 | Chrome/Firefox/Safari/Edge 最新两个版本 |
| 移动端 | 响应式布局，支持 iOS Safari 和 Android Chrome |
| API 版本 | 支持 v1，后续平滑演进 v2 |

### 19.5 审计日志要求

| 操作类型 | 日志记录 | 详情字段 |
|----------|----------|----------|
| 租户开通/禁用 | 是 | 操作人、时间、原因 |
| 套餐变更 | 是 | 原套餐->新套餐、操作人 |
| 用户创建/删除 | 是 | 用户ID、类型、操作人 |
| 权限变更 | 是 | 用户、角色、操作人 |
| 跨租户数据访问 | 是 | 访问者、目标租户、资源类型 |
| 登录/登出 | 是 | IP、UA、登录结果 |
| 配额超限操作 | 是 | 租户ID、操作类型、错误码 |

---

## 附录

### 附录A：状态码对照表

| 状态码 | 英文 | 中文 | 说明 |
|--------|------|------|------|
| 1 | pending | 待审核 | 租户申请待审核 |
| 2 | approved | 审核通过 | 审核通过 |
| 3 | rejected | 审核拒绝 | 审核拒绝 |
| 4 | activating | 开通中 | 租户开通流程中 |
| 5 | active | 已开通 | 租户已开通正常使用 |
| 6 | suspended | 已禁用 | 租户被禁用 |
| 7 | expired | 已到期 | 租户到期 |
| 8 | activation_failed | 开通失败 | 租户开通流程异常 |

### 附录B：套餐代码表

| plan_code | 套餐名称 |
|-----------|----------|
| free | 免费版 |
| basic | 基础版 |
| pro | 专业版 |
| enterprise | 企业版 |

### 附录C：角色代码表

| role_code | 角色名称 | 权限级别 |
|-----------|----------|----------|
| super_admin | 超级管理员 | L1 |
| tenant_admin | 租户管理员 | L2 |
| normal_user | 普通用户 | L3 |

### 附录D：配额错误码表

| 错误码 | 说明 | HTTP 状态码 |
|--------|------|-------------|
| QUOTA_USER_EXCEEDED | 用户数已达上限 | 403 |
| QUOTA_DEVICE_EXCEEDED | 设备数已达上限 | 403 |
| QUOTA_DEPT_EXCEEDED | 部门数已达上限 | 403 |
| QUOTA_STORE_EXCEEDED | 门店数已达上限 | 403 |

### 附录E：标准错误响应格式

```json
{
  "code": "ERROR_CODE",
  "message": "错误信息描述",
  "data": null,
  "trace_id": "uuid"
}
```

**错误码说明**：

| code | HTTP | 说明 |
|------|------|------|
| SUCCESS | 200 | 成功 |
| BAD_REQUEST | 400 | 请求参数错误 |
| UNAUTHORIZED | 401 | 未登录或Token过期 |
| FORBIDDEN | 403 | 无权限 |
| NOT_FOUND | 404 | 资源不存在 |
| TENANT_DISABLED | 403 | 租户已禁用 |
| TENANT_EXPIRED | 403 | 租户已到期 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

---

*本文档版本 V1.3，编写日期 2026-03-20*
''')
print('Chapters 15-19 and appendix appended successfully')
