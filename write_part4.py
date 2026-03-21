# -*- coding: utf-8 -*-
# Part 4: remaining 17.4 + 18 + 19 + Appendix

part4 = r'''用户 | 新闻详情页 |
| `/portal/news/manage` | 租户管理员 | 新闻管理后台 |
| `/portal/alerts` | 全部用户 | 预警消息中心 |
| `/portal/alerts/config` | 租户管理员 | 预警配置管理 |
| `/favorites` | 全部用户 | 收藏菜单 |
| `/notifications` | 全部用户 | 消息通知 |

---

## 十八、非功能性需求

### 18.1 性能要求

| 指标 | 要求 |
|------|------|
| 租户开通 | 开通流程 <= 10秒（含租户记录创建、配额初始化） |
| 列表查询 | 1000条数据分页加载 <= 500ms |
| 权限校验 | 中间件额外延迟 <= 5ms |
| 并发租户数 | 单实例支持 >= 500 个活跃租户 |
| 配额校验 | 原子操作，<= 10ms |
| API响应时间 | P95 <= 200ms |

### 18.2 可用性要求

| 要求项 | 说明 |
|--------|------|
| 租户独立性 | 单个租户故障不影响其他租户 |
| 降级策略 | 禁用非核心功能，保证登录和基础设备管理 |
| 数据备份 | 每日全量备份，保留 30 天 |

### 18.3 安全性要求

| 要求项 | 说明 |
|--------|------|
| 密码策略 | 长度>=8位，需包含大小写字母+数字，90天强制更换 |
| JWT 有效期 | Access Token 2小时，Refresh Token 7天 |
| 超级管理员操作 | 所有删除操作需二次确认 |
| 租户隔离 | 跨租户 SQL 执行触发实时告警 |
| 数据传输 | 全链路 TLS 1.2+ 加密 |
| 敏感数据 | 密码、密钥等加密存储（AES-256） |

### 18.4 兼容性要求

| 要求项 | 说明 |
|--------|------|
| 前端兼容 | Chrome/Firefox/Safari/Edge 最新两个版本 |
| 移动端 | 响应式布局，支持 iOS Safari 和 Android Chrome |
| API 版本 | 支持 v1，后续平滑演进 v2 |

### 18.5 审计日志要求

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

## 十九、附录

### 19.1 状态码对照表

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

### 19.2 套餐代码表

| plan_code | 套餐名称 |
|-----------|----------|
| free | 免费版 |
| basic | 基础版 |
| pro | 专业版 |
| enterprise | 企业版 |

### 19.3 角色代码表

| role_code | 角色名称 | 权限级别 |
|-----------|----------|----------|
| super_admin | 超级管理员 | L1 |
| tenant_admin | 租户管理员 | L2 |
| normal_user | 普通用户 | L3 |

### 19.4 配额错误码表

| 错误码 | 说明 | HTTP 状态码 |
|--------|------|-------------|
| QUOTA_USER_EXCEEDED | 用户数已达上限 | 403 |
| QUOTA_DEVICE_EXCEEDED | 设备数已达上限 | 403 |
| QUOTA_DEPT_EXCEEDED | 部门数已达上限 | 403 |
| QUOTA_STORE_EXCEEDED | 门店数已达上限 | 403 |

### 19.5 标准错误响应格式

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
| QUOTA_USER_EXCEEDED | 403 | 用户配额超限 |
| QUOTA_DEVICE_EXCEEDED | 403 | 设备配额超限 |
| QUOTA_DEPT_EXCEEDED | 403 | 部门配额超限 |
| QUOTA_STORE_EXCEEDED | 403 | 门店配额超限 |
| TENANT_DISABLED | 403 | 租户已禁用 |
| TENANT_EXPIRED | 403 | 租户已到期 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

### 19.6 迁移指南

#### 19.6.1 现有单租户系统迁移

将现有单租户 MDM 系统平滑迁移到多租户架构，所有现有数据通过 `tenant_id = 'default'` 标识为默认租户。

#### 19.6.2 迁移步骤

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 执行迁移脚本添加 `tenant_id` 字段 | 为所有业务表添加 `tenant_id` 字段（可NULL） |
| 2 | 设置所有现有数据的 `tenant_id` | 将历史数据迁移到默认租户 |
| 3 | 将 `tenant_id` 字段设为 NOT NULL | 完成后不允许空值 |
| 4 | 创建默认租户记录 | 在 `tenants` 表插入 default 租户 |
| 5 | 初始化默认租户配额 | 在 `tenant_quotas` 表插入配额记录（不限量） |
| 6 | 验证迁移完整性 | 检查数据一致性，确保无数据丢失 |

#### 19.6.3 迁移 SQL 示例

```sql
-- 步骤 1: 添加 tenant_id 字段
ALTER TABLE users ADD COLUMN tenant_id UUID;
ALTER TABLE devices ADD COLUMN tenant_id UUID;
ALTER TABLE departments ADD COLUMN tenant_id UUID;
ALTER TABLE stores ADD COLUMN tenant_id UUID;

-- 步骤 2: 为所有现有数据设置 default 租户
UPDATE users SET tenant_id = '00000000-0000-0000-0000-000000000001';
UPDATE devices SET tenant_id = '00000000-0000-0000-0000-000000000001';
UPDATE departments SET tenant_id = '00000000-0000-0000-0000-000000000001';
UPDATE stores SET tenant_id = '00000000-0000-0000-0000-000000000001';

-- 步骤 3: 设置为 NOT NULL
ALTER TABLE users ALTER COLUMN tenant_id SET NOT NULL;
ALTER TABLE devices ALTER COLUMN tenant_id SET NOT NULL;
ALTER TABLE departments ALTER COLUMN tenant_id SET NOT NULL;
ALTER TABLE stores ALTER COLUMN tenant_id SET NOT NULL;

-- 步骤 4: 创建默认租户记录
INSERT INTO tenants (id, tenant_code, company_name, plan_id, status, expire_time)
VALUES ('00000000-0000-0000-0000-000000000001', 'default', '默认租户', 4, 'active', '2099-12-31');

-- 步骤 5: 初始化默认租户配额（不限量）
INSERT INTO tenant_quotas (tenant_id, user_count, device_count, dept_count, store_count)
VALUES ('00000000-0000-0000-0000-000000000001', 0, 0, 0, 0);
```

#### 19.6.4 迁移验证

```sql
-- 验证所有业务表 tenant_id 已填充
SELECT COUNT(*) FROM users WHERE tenant_id IS NULL;
SELECT COUNT(*) FROM devices WHERE tenant_id IS NULL;
SELECT COUNT(*) FROM departments WHERE tenant_id IS NULL;
SELECT COUNT(*) FROM stores WHERE tenant_id IS NULL;

-- 验证默认租户记录存在
SELECT * FROM tenants WHERE tenant_code = 'default';
SELECT * FROM tenant_quotas WHERE tenant_id = '00000000-0000-0000-0000-000000000001';
```

---

*本文档版本 V1.3，编写日期 2026-03-20*
'''

filepath = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(filepath, 'a', encoding='utf-8') as f:
    f.write(part4)

print(f'Appended part 4, total file size: {open(filepath, "r", encoding="utf-8").read().__len__()} chars')
