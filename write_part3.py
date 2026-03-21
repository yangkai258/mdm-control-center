# -*- coding: utf-8 -*-
# Part 3: remaining 14.6 + 14.7 + 15-19 + Appendix

part3 = r'''#### 14.6.1 实体字段

| 字段 | 类型 | 说明 |
|------|------|------|
| service_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| service_name | VARCHAR(100) | 服务名称 |
| service_type | ENUM | wechat/dingtalk/feishu/other |
| config | JSONB | 配置信息 |
| is_active | BOOLEAN | 是否启用 |
| updated_at | TIMESTAMPTZ | 更新时间 |

#### 14.6.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/external-services` | 列表 |
| POST | `/api/v1/tenants/{tenant_id}/external-services` | 创建 |
| PUT | `/api/v1/tenants/{tenant_id}/external-services/{id}` | 更新 |
| DELETE | `/api/v1/tenants/{tenant_id}/external-services/{id}` | 删除 |
| POST | `/api/v1/tenants/{tenant_id}/external-services/{id}/test` | 测试连接 |
| POST | `/api/v1/tenants/{tenant_id}/external-services/{id}/sync` | 同步数据 |

### 14.7 系统参数设置

Key-Value 键值对配置。

#### 14.7.1 实体字段

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

#### 14.7.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/params` | 列表 |
| GET | `/api/v1/tenants/{tenant_id}/params/{key}` | 获取单个 |
| POST | `/api/v1/tenants/{tenant_id}/params` | 创建 |
| PUT | `/api/v1/tenants/{tenant_id}/params/{key}` | 更新 |
| DELETE | `/api/v1/tenants/{tenant_id}/params/{key}` | 删除 |

---

## 十五、数据库设计

> **重要说明**：所有业务表统一存放在 public schema，通过 `tenant_id` 字段实现租户隔离。**不创建独立 schema**。

### 15.1 平台级表（无 tenant_id）

#### 15.1.1 tenants（租户台账）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| tenant_code | VARCHAR(20) | UNIQUE, NOT NULL | 租户编码 |
| company_name | VARCHAR(100) | NOT NULL | 企业全称 |
| plan_id | INT | NOT NULL | 套餐ID |
| status | VARCHAR(20) | DEFAULT 'active' | active/suspended/expired |
| expire_time | TIMESTAMPTZ | NOT NULL | 到期时间 |
| logo_url | VARCHAR(500) | NULL | Logo URL |
| custom_domain | VARCHAR(100) | NULL | 自定义域名 |
| contact_name | VARCHAR(50) | NULL | 联系人 |
| contact_phone | VARCHAR(20) | NULL | 联系电话 |
| contact_email | VARCHAR(100) | NULL | 邮箱 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

#### 15.1.2 tenant_applications（租户申请记录）

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
| status | VARCHAR(20) | DEFAULT 'pending' | pending/approved/rejected |
| reject_reason | TEXT | NULL | 拒绝原因 |
| audit_by | UUID | NULL | 审核人 |
| audit_at | TIMESTAMPTZ | NULL | 审核时间 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |

#### 15.1.3 plans（套餐定义）

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
| features | JSONB | DEFAULT '{}' | 功能开关 |
| sort_order | INT | DEFAULT 0 | 排序 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否上架 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |

#### 15.1.4 dicts（公共字典）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | SERIAL | PK | 主键 |
| category | VARCHAR(30) | NOT NULL | 分类标识 |
| item_code | VARCHAR(30) | NOT NULL | 字典项代码 |
| item_name | VARCHAR(50) | NOT NULL | 字典项名称 |
| sort_order | INT | DEFAULT 0 | 排序 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| description | VARCHAR(200) | NULL | 说明 |
| UNIQUE | (category, item_code) | | |

#### 15.1.5 audit_logs（审计日志）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGSERIAL | PK | 主键 |
| tenant_id | UUID | NULL | 所属租户（可跨租户） |
| user_id | UUID | NULL | 操作人 |
| action | VARCHAR(50) | NOT NULL | 操作类型 |
| resource_type | VARCHAR(50) | NULL | 资源类型 |
| resource_id | VARCHAR(36) | NULL | 资源ID |
| detail | JSONB | NULL | 变更详情 |
| ip_address | INET | NULL | IP地址 |
| user_agent | TEXT | NULL | 浏览器UA |
| is_cross_tenant | BOOLEAN | DEFAULT FALSE | 是否跨租户操作 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 操作时间 |

### 15.2 业务表（所有表含 tenant_id 字段实现隔离）

#### 15.2.1 tenant_quotas（租户配额表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | SERIAL | PK | 主键 |
| tenant_id | UUID | FK(tenants), UNIQUE | 所属租户 |
| user_count | INT | DEFAULT 0 | 当前用户数 |
| device_count | INT | DEFAULT 0 | 当前设备数 |
| dept_count | INT | DEFAULT 0 | 当前部门数 |
| store_count | INT | DEFAULT 0 | 当前门店数 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

#### 15.2.2 users（用户表）

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
| role | VARCHAR(20) | NOT NULL DEFAULT 'normal_user' | tenant_admin/normal_user |
| status | VARCHAR(20) | DEFAULT 'active' | active/disabled |
| last_login_at | TIMESTAMPTZ | NULL | 最近登录 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| created_by | UUID | NOT NULL | 创建人 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |
| deleted_at | TIMESTAMPTZ | NULL | 软删除时间 |
| UNIQUE | (tenant_id, username) | | |
| UNIQUE | (tenant_id, phone) | | |

#### 15.2.3 departments（部门表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| tenant_id | UUID | NOT NULL | 所属租户 |
| dept_name | VARCHAR(50) | NOT NULL | 部门名称 |
| parent_id | UUID | NULL | 上级部门 |
| sort_order | INT | DEFAULT 0 | 排序 |
| manager_user_id | UUID | NULL | 部门负责人 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

#### 15.2.4 stores（门店表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| tenant_id | UUID | NOT NULL | 所属租户 |
| dept_id | UUID | NULL | 所属部门 |
| store_name | VARCHAR(100) | NOT NULL | 门店名称 |
| store_code | VARCHAR(20) | NOT NULL | 门店编码 |
| province | VARCHAR(20) | NULL | 省份 |
| city | VARCHAR(20) | NULL | 城市 |
| district | VARCHAR(20) | NULL | 区县 |
| address | VARCHAR(200) | NULL | 详细地址 |
| contact_phone | VARCHAR(20) | NULL | 联系电话 |
| manager_name | VARCHAR(50) | NULL | 店长姓名 |
| manager_user_id | UUID | NULL | 关联用户 |
| device_count | INT | DEFAULT 0 | 设备数（冗余） |
| status | VARCHAR(20) | DEFAULT 'active' | active/suspended |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |
| UNIQUE | (tenant_id, store_code) | | |

#### 15.2.5 devices（设备表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGSERIAL | PK | 主键 |
| tenant_id | UUID | NOT NULL | 所属租户 |
| dept_id | UUID | NULL | 所属部门 |
| store_id | UUID | NULL | 所属门店 |
| device_id | VARCHAR(36) | UNIQUE, NOT NULL | 设备唯一ID |
| mac_address | VARCHAR(17) | NOT NULL | MAC地址 |
| sn_code | VARCHAR(32) | NOT NULL | 序列号 |
| hardware_model | VARCHAR(32) | NOT NULL | 硬件型号 |
| firmware_version | VARCHAR(32) | NOT NULL | 固件版本 |
| lifecycle_status | SMALLINT | DEFAULT 1 | 生命周期状态 |
| created_at | TIMESTAMPTZ | NOT NULL | 创建时间 |
| updated_at | TIMESTAMPTZ | NOT NULL | 更新时间 |

#### 15.2.6 members（会员表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| tenant_id | UUID | NOT NULL | 所属租户 |
| store_id | UUID | NULL | 所属门店 |
| member_name | VARCHAR(50) | NOT NULL | 会员名称 |
| phone | VARCHAR(20) | NOT NULL | 手机号 |
| email | VARCHAR(100) | NULL | 邮箱 |
| status | VARCHAR(20) | DEFAULT 'active' | active/disabled |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | 更新时间 |

### 15.3 GORM 中间件实现

```go
// TenantPlugin 实现 GORM Callback 模式的租户隔离
type TenantPlugin struct{}

func (p *TenantPlugin) Name() string {
    return "tenant_scope"
}

func (p *TenantPlugin) Initialize(db *gorm.DB) error {
    // 创建前回调：注入 tenant_id
    db.Callback().Create().Before("gorm:before_create").Register("tenant:before_create", setTenantID)
    // 查询回调：自动追加 tenant_id 条件
    db.Callback().Query().Before("gorm:query").Register("tenant:before_query", filterByTenant)
    // 更新回调：确保操作仅影响当前租户
    db.Callback().Update().Before("gorm:before_update").Register("tenant:before_update", filterByTenant)
    // 删除回调：确保删除仅影响当前租户
    db.Callback().Delete().Before("gorm:before_delete").Register("tenant:before_delete", filterByTenant)
    return nil
}

func setTenantID(db *gorm.DB) {
    if tenantID, ok := db.Statement.Context.Value("tenant_id").(string); ok {
        if db.Statement.Schema != nil {
            if field := db.Statement.Schema.FieldByName("TenantID"); field != nil {
                db.Statement.SetColumn("tenant_id", tenantID)
            }
        }
    }
}

func filterByTenant(db *gorm.DB) {
    if tenantID, ok := db.Statement.Context.Value("tenant_id").(string); ok {
        if db.Statement.Schema != nil {
            // 只有业务表（有 TenantID 字段）才过滤
            if _, ok := db.Statement.Schema.ModelType.FieldByName("TenantID"); ok {
                db.Statement.Where("tenant_id = ?", tenantID)
            }
        }
    }
}
```

### 15.4 索引设计

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

## 十六、API接口总览

### 16.1 平台管理（超级管理员）

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
| GET | `/api/v1/admin/tenants/applications/{id}` | 申请详情 |
| POST | `/api/v1/admin/tenants/applications/{id}/approve` | 审核通过 |
| POST | `/api/v1/admin/tenants/applications/{id}/reject` | 审核拒绝 |
| GET | `/api/v1/admin/plans` | 套餐列表 |
| POST | `/api/v1/admin/plans` | 新增套餐 |
| PUT | `/api/v1/admin/plans/{id}` | 更新套餐 |
| GET | `/api/v1/admin/dicts` | 字典列表 |
| POST | `/api/v1/admin/dicts` | 新增字典项 |
| PUT | `/api/v1/admin/dicts/{id}` | 更新字典项 |
| DELETE | `/api/v1/admin/dicts/{id}` | 删除字典项 |
| GET | `/api/v1/admin/roles` | 角色列表 |
| POST | `/api/v1/admin/roles` | 创建角色 |
| PUT | `/api/v1/admin/roles/{id}/permissions` | 分配权限 |
| GET | `/api/v1/admin/permissions` | 权限点列表 |
| GET | `/api/v1/admin/post-templates` | 基准岗位模板列表 |
| POST | `/api/v1/admin/post-templates` | 创建基准岗位 |
| PUT | `/api/v1/admin/post-templates/{id}` | 更新基准岗位 |
| DELETE | `/api/v1/admin/post-templates/{id}` | 删除基准岗位 |
| GET | `/api/v1/admin/restricted-users` | 限制用户列表 |
| POST | `/api/v1/admin/restricted-users` | 创建限制用户 |
| PUT | `/api/v1/admin/restricted-users/{id}/toggle` | 切换限制状态 |
| DELETE | `/api/v1/admin/restricted-users/{id}` | 删除限制用户 |

### 16.2 租户管理（租户管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/users` | 用户列表 |
| POST | `/api/v1/tenants/{tenant_id}/users` | 创建用户（含配额校验） |
| GET | `/api/v1/tenants/{tenant_id}/users/{id}` | 用户详情 |
| PUT | `/api/v1/tenants/{tenant_id}/users/{id}` | 更新用户 |
| DELETE | `/api/v1/tenants/{tenant_id}/users/{id}` | 删除用户（软删除） |
| PUT | `/api/v1/tenants/{tenant_id}/users/{id}/reset-password` | 重置密码 |
| PUT | `/api/v1/tenants/{tenant_id}/users/{id}/change-role` | 变更角色 |
| PUT | `/api/v1/tenants/{tenant_id}/users/{id}/roles` | 分配角色 |
| PUT | `/api/v1/tenants/{tenant_id}/users/{id}/permissions` | 分配权限 |
| GET | `/api/v1/tenants/{tenant_id}/departments` | 部门树 |
| POST | `/api/v1/tenants/{tenant_id}/departments` | 新增部门（含配额校验） |
| PUT | `/api/v1/tenants/{tenant_id}/departments/{id}` | 更新部门 |
| DELETE | `/api/v1/tenants/{tenant_id}/departments/{id}` | 删除部门 |
| GET | `/api/v1/tenants/{tenant_id}/stores` | 门店列表 |
| POST | `/api/v1/tenants/{tenant_id}/stores` | 新增门店（含配额校验） |
| GET | `/api/v1/tenants/{tenant_id}/stores/tree` | 门店树形 |
| GET | `/api/v1/tenants/{tenant_id}/stores/{id}` | 门店详情 |
| PUT | `/api/v1/tenants/{tenant_id}/stores/{id}` | 更新门店 |
| DELETE | `/api/v1/tenants/{tenant_id}/stores/{id}` | 删除门店 |
| GET | `/api/v1/tenants/{tenant_id}/company` | 获取公司信息 |
| PUT | `/api/v1/tenants/{tenant_id}/company` | 更新公司信息 |
| GET | `/api/v1/tenants/{tenant_id}/posts` | 岗位列表 |
| POST | `/api/v1/tenants/{tenant_id}/posts` | 创建岗位 |
| GET | `/api/v1/tenants/{tenant_id}/posts/{id}` | 岗位详情 |
| PUT | `/api/v1/tenants/{tenant_id}/posts/{id}` | 更新岗位 |
| DELETE | `/api/v1/tenants/{tenant_id}/posts/{id}` | 删除岗位 |
| GET | `/api/v1/tenants/{tenant_id}/posts/templates` | 岗位模板列表 |
| GET | `/api/v1/tenants/{tenant_id}/employees` | 员工列表 |
| POST | `/api/v1/tenants/{tenant_id}/employees/onboard` | 办理入职 |
| PUT | `/api/v1/tenants/{tenant_id}/employees/{id}/leave` | 办理离职 |
| GET | `/api/v1/tenants/{tenant_id}/employees/stats` | 员工统计 |
| GET | `/api/v1/tenants/{tenant_id}/data-permissions` | 数据权限配置 |
| PUT | `/api/v1/tenants/{tenant_id}/data-permissions` | 更新配置 |
| GET | `/api/v1/tenants/{tenant_id}/data-permissions/users/{id}` | 获取用户数据范围 |
| PUT | `/api/v1/tenants/{tenant_id}/data-permissions/users/{id}` | 设定用户数据范围 |

### 16.3 流程管理 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/workflows` | 流程列表 |
| POST | `/api/v1/tenants/{tenant_id}/workflows` | 创建流程 |
| GET | `/api/v1/tenants/{tenant_id}/workflows/{id}` | 流程详情 |
| PUT | `/api/v1/tenants/{tenant_id}/workflows/{id}` | 更新流程 |
| DELETE | `/api/v1/tenants/{tenant_id}/workflows/{id}` | 删除流程 |
| POST | `/api/v1/tenants/{tenant_id}/workflows/{id}/publish` | 发布流程 |
| GET | `/api/v1/tenants/{tenant_id}/workflows/{id}/bpmn` | 获取BPMN XML |
| GET | `/api/v1/tenants/{tenant_id}/workflows/{id}/versions` | 版本列表 |
| POST | `/api/v1/tenants/{tenant_id}/workflows/{id}/rollback` | 回滚版本 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/todo` | 我的待办 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/complete` | 办理任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/reject` | 拒绝任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/transfer` | 转办任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/delegate` | 委派任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/add-sign` | 加签 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/done` | 我已处理 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/exception` | 异常任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/reassign` | 重新分配 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/terminate` | 终止任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/batch-complete` | 批量同意 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/batch-reject` | 批量拒绝 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/unassigned` | 无办理人任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/claim` | 认领任务 |
| GET | `/api/v1/tenants/{tenant_id}/delegations` | 代理列表 |
| POST | `/api/v1/tenants/{tenant_id}/delegations` | 创建代理 |
| DELETE | `/api/v1/tenants/{tenant_id}/delegations/{id}` | 删除代理 |
| GET | `/api/v1/tenants/{tenant_id}/delegations/received` | 待我代办 |

### 16.4 基础管理 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/archives` | 档案列表 |
| POST | `/api/v1/tenants/{tenant_id}/archives` | 创建档案 |
| GET | `/api/v1/tenants/{tenant_id}/archives/tree` | 档案树形 |
| GET | `/api/v1/tenants/{tenant_id}/jobs` | 任务列表 |
| POST | `/api/v1/tenants/{tenant_id}/jobs` | 创建任务 |
| POST | `/api/v1/tenants/{tenant_id}/jobs/{id}/run-now` | 立即执行 |
| POST | `/api/v1/tenants/{tenant_id}/jobs/{id}/pause` | 暂停任务 |
| POST | `/api/v1/tenants/{tenant_id}/jobs/{id}/resume` | 恢复任务 |
| GET | `/api/v1/tenants/{tenant_id}/jobs/{id}/logs` | 执行日志 |
| GET | `/api/v1/tenants/{tenant_id}/menus` | 菜单列表 |
| POST | `/api/v1/tenants/{tenant_id}/menus` | 创建菜单 |
| GET | `/api/v1/tenants/{tenant_id}/menus/tree` | 菜单树形 |
| GET | `/api/v1/tenants/{tenant_id}/logs` | 日志列表 |
| GET | `/api/v1/tenants/{tenant_id}/logs/stats` | 日志统计 |
| GET | `/api/v1/tenants/{tenant_id}/broadcasts` | 广播列表 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts` | 创建广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/publish` | 发布广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/revoke` | 撤回广播 |
| GET | `/api/v1/tenants/{tenant_id}/validation-rules` | 校验规则列表 |
| POST | `/api/v1/tenants/{tenant_id}/validation-rules` | 创建规则 |
| GET | `/api/v1/tenants/{tenant_id}/pay-channels` | 支付渠道列表 |
| POST | `/api/v1/tenants/{tenant_id}/pay-channels` | 创建渠道 |
| GET | `/api/v1/tenants/{tenant_id}/templates` | 模板列表 |
| POST | `/api/v1/tenants/{tenant_id}/templates` | 上传模板 |
| GET | `/api/v1/tenants/{tenant_id}/test-forms` | 测试表单列表 |
| POST | `/api/v1/tenants/{tenant_id}/test-forms` | 创建表单 |
| GET | `/api/v1/dicts` | 字典列表（所有租户可读） |
| GET | `/api/v1/dicts/{category}` | 指定分类字典 |

### 16.5 门户管理 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/portal-pages` | 门户页面列表 |
| POST | `/api/v1/tenants/{tenant_id}/portal-pages` | 创建门户页面 |
| PUT | `/api/v1/tenants/{tenant_id}/portal-pages/{id}` | 更新页面 |
| DELETE | `/api/v1/tenants/{tenant_id}/portal-pages/{id}` | 删除页面 |
| POST | `/api/v1/tenants/{tenant_id}/portal-pages/{id}/publish` | 发布页面 |
| PUT | `/api/v1/tenants/{tenant_id}/portal-pages/{id}/default` | 设为默认 |
| GET | `/api/v1/tenants/{tenant_id}/news` | 新闻列表 |
| POST | `/api/v1/tenants/{tenant_id}/news` | 创建新闻 |
| GET | `/api/v1/tenants/{tenant_id}/news/{id}` | 新闻详情 |
| PUT | `/api/v1/tenants/{tenant_id}/news/{id}` | 更新新闻 |
| DELETE | `/api/v1/tenants/{tenant_id}/news/{id}` | 删除新闻 |
| POST | `/api/v1/tenants/{tenant_id}/news/{id}/publish` | 发布新闻 |
| GET | `/api/v1/tenants/{tenant_id}/news-categories` | 栏目列表 |
| POST | `/api/v1/tenants/{tenant_id}/news-categories` | 创建栏目 |
| GET | `/api/v1/tenants/{tenant_id}/alert-configs` | 预警配置列表 |
| POST | `/api/v1/tenants/{tenant_id}/alert-configs` | 创建预警配置 |
| PUT | `/api/v1/tenants/{tenant_id}/alert-configs/{id}` | 更新预警配置 |
| DELETE | `/api/v1/tenants/{tenant_id}/alert-configs/{id}` | 删除预警配置 |
| POST | `/api/v1/tenants/{tenant_id}/alert-configs/{id}/test` | 测试预警 |
| GET | `/api/v1/tenants/{tenant_id}/alerts` | 预警列表 |
| POST | `/api/v1/tenants/{tenant_id}/alerts/{id}/acknowledge` | 确认预警 |
| POST | `/api/v1/tenants/{tenant_id}/alerts/{id}/resolve` | 解决预警 |
| POST | `/api/v1/tenants/{tenant_id}/alerts/batch-acknowledge` | 批量确认 |
| GET | `/api/v1/tenants/{tenant_id}/alert-logs` | 预警流水 |

### 16.6 实施工具 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/favorites` | 收藏列表 |
| POST | `/api/v1/tenants/{tenant_id}/favorites` | 添加收藏 |
| DELETE | `/api/v1/tenants/{tenant_id}/favorites/{id}` | 取消收藏 |
| GET | `/api/v1/tenants/{tenant_id}/dashboards/{user_id}` | 首页配置 |
| PUT | `/api/v1/tenants/{tenant_id}/dashboards/{user_id}` | 保存配置 |
| GET | `/api/v1/tenants/{tenant_id}/email-configs` | 邮件配置列表 |
| POST | `/api/v1/tenants/{tenant_id}/email-configs` | 创建邮件配置 |
| POST | `/api/v1/tenants/{tenant_id}/email-configs/{id}/test` | 测试发送 |
| GET | `/api/v1/tenants/{tenant_id}/notifications` | 消息通知 |
| POST | `/api/v1/tenants/{tenant_id}/notifications/{id}/read` | 标记已读 |
| POST | `/api/v1/tenants/{tenant_id}/notifications/mark-all-read` | 全部已读 |
| GET | `/api/v1/tenants/{tenant_id}/external-services` | 外部服务列表 |
| POST | `/api/v1/tenants/{tenant_id}/external-services` | 创建外部服务 |
| POST | `/api/v1/tenants/{tenant_id}/external-services/{id}/test` | 测试连接 |
| POST | `/api/v1/tenants/{tenant_id}/external-services/{id}/sync` | 同步数据 |
| GET | `/api/v1/tenants/{tenant_id}/params` | 系统参数列表 |
| GET | `/api/v1/tenants/{tenant_id}/params/{key}` | 获取单个参数 |
| POST | `/api/v1/tenants/{tenant_id}/params` | 创建参数 |
| PUT | `/api/v1/tenants/{tenant_id}/params/{key}` | 更新参数 |
| DELETE | `/api/v1/tenants/{tenant_id}/params/{key}` | 删除参数 |
| GET | `/api/v1/system/version` | 版本信息 |
| GET | `/api/v1/system/health` | 健康检查 |

---

## 十七、前端页面清单

### 17.1 公开页面

| 页面路径 | 角色 | 功能 |
|----------|------|------|
| `/login` | 公开 | 登录页 |
| `/register` | 公开 | 租户注册申请 |
| `/forgot-password` | 公开 | 找回密码 |

### 17.2 超级管理员页面

| 页面路径 | 功能 |
|----------|------|
| `/admin/tenants` | 租户列表 |
| `/admin/tenants/applications` | 申请审核列表 |
| `/admin/tenants/{id}` | 租户详情/编辑 |
| `/admin/plans` | 套餐管理 |
| `/admin/dicts` | 公共字典管理 |
| `/admin/permissions` | 权限点管理 |
| `/admin/roles` | 角色管理 |
| `/admin/post-templates` | 基准岗位模板 |

### 17.3 租户管理员页面

| 页面路径 | 功能 |
|----------|------|
| `/dashboard` | 首页仪表盘 |
| `/settings/tenant` | 本租户信息配置 |
| `/settings/profile` | 个人信息管理 |
| `/users` | 租户用户列表 |
| `/users/new` | 新建用户 |
| `/users/{id}` | 编辑用户 |
| `/departments` | 组织架构管理 |
| `/stores` | 门店列表 |
| `/stores/new` | 新增门店 |
| `/stores/{id}` | 门店详情/编辑 |
| `/org/company` | 公司信息管理 |
| `/org/posts` | 岗位管理 |
| `/org/employees` | 员工管理 |
| `/org/employees/onboard` | 办理入职 |
| `/org/employees/leave/{id}` | 办理离职 |
| `/permissions/roles` | 角色管理 |
| `/permissions/users` | 用户权限分配 |
| `/permissions/data-scope` | 数据权限配置 |
| `/workflows` | 流程列表 |
| `/workflows/new` | 新建流程 |
| `/workflows/{id}/design` | 流程设计器 |
| `/workflows/{id}/instances` | 流程实例 |
| `/tasks/todo` | 我的待办 |
| `/tasks/done` | 我已处理 |
| `/tasks/exception` | 异常任务 |
| `/system/archives` | 基础档案 |
| `/system/jobs` | 调度任务 |
| `/system/menus` | 菜单设置 |
| `/system/logs` | 业务日志 |
| `/system/broadcasts` | 系统广播 |
| `/system/validation-rules` | 校验规则 |
| `/system/pay-channels` | 支付配置 |
| `/system/templates` | 模板管理 |
| `/system/test-forms` | 测试表单 |

### 17.4 门户页面

| 页面路径 | 角色 | 功能 |
|----------|------|------|
| `/portal` | 全部用户 | 门户首页 |
| `/portal/pages` | 租户管理员 | 门户页面管理 |
| `/portal/news` | 全部用户 | 新闻列表页 |
| `/portal/news/{id}` | 全部