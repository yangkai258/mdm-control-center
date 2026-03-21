# -*- coding: utf-8 -*-
# Write the complete new chapter 13-19 and appendix for PRD
# This script writes UTF-8 content directly to avoid encoding issues

fp = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'

ch13_ch19 = """

---

## 十三、基础管理（档案/调度/字典等）

> **功能路径**：`/system` 模块
> **权限要求**：超级管理员或租户管理员

### 13.1 基础档案

#### 13.1.1 档案实体

| 字段 | 类型 | 说明 |
|------|------|------|
| archive_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| archive_type | VARCHAR(50) | 档案类型编码 |
| archive_name | VARCHAR(100) | 档案名称 |
| archive_code | VARCHAR(50) | 档案编码 |
| parent_id | UUID | 上级档案 |
| sort_order | INT | 排序 |
| status | ENUM | active/disabled |
| extra_data | JSONB | 扩展字段 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.1.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/archives` | 档案列表 |
| POST | `/api/v1/tenants/{tenant_id}/archives` | 创建档案 |
| PUT | `/api/v1/tenants/{tenant_id}/archives/{id}` | 更新档案 |
| DELETE | `/api/v1/tenants/{tenant_id}/archives/{id}` | 删除档案 |
| GET | `/api/v1/tenants/{tenant_id}/archives/tree` | 档案树形 |

### 13.2 调度计划

#### 13.2.1 调度实体

| 字段 | 类型 | 说明 |
|------|------|------|
| job_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| job_name | VARCHAR(100) | 任务名称 |
| job_code | VARCHAR(50) | 任务编码 |
| job_type | ENUM | http/bean-script/http-spring |
| cron_expression | VARCHAR(50) | Cron表达式 |
| endpoint | VARCHAR(200) | 调用地址/Bean名 |
| params | JSONB | 调用参数 |
| status | ENUM | running/paused/stopped |
| last_run_at | TIMESTAMPTZ | 上次执行时间 |
| next_run_at | TIMESTAMPTZ | 下次执行时间 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.2.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/jobs` | 任务列表 |
| POST | `/api/v1/tenants/{tenant_id}/jobs` | 创建任务 |
| PUT | `/api/v1/tenants/{tenant_id}/jobs/{id}` | 更新任务 |
| DELETE | `/api/v1/tenants/{tenant_id}/jobs/{id}` | 删除任务 |
| POST | `/api/v1/tenants/{tenant_id}/jobs/{id}/run-now` | 立即执行 |
| POST | `/api/v1/tenants/{tenant_id}/jobs/{id}/pause` | 暂停任务 |
| POST | `/api/v1/tenants/{tenant_id}/jobs/{id}/resume` | 恢复任务 |
| GET | `/api/v1/tenants/{tenant_id}/jobs/{id}/logs` | 执行日志 |

### 13.3 菜单设置

#### 13.3.1 菜单实体

| 字段 | 类型 | 说明 |
|------|------|------|
| menu_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| parent_id | UUID | 上级菜单 |
| menu_name | VARCHAR(50) | 菜单名称 |
| menu_code | VARCHAR(50) | 菜单编码 |
| menu_type | ENUM | directory/menu/button |
| path | VARCHAR(200) | 路由路径 |
| component | VARCHAR(200) | 组件路径 |
| icon | VARCHAR(50) | 图标 |
| sort_order | INT | 排序 |
| visible | BOOLEAN | 是否显示 |
| status | ENUM | active/disabled |
| permissions | VARCHAR[] | 权限标识 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.3.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/menus` | 菜单列表 |
| POST | `/api/v1/tenants/{tenant_id}/menus` | 创建菜单 |
| PUT | `/api/v1/tenants/{tenant_id}/menus/{id}` | 更新菜单 |
| DELETE | `/api/v1/tenants/{tenant_id}/menus/{id}` | 删除菜单 |
| GET | `/api/v1/tenants/{tenant_id}/menus/tree` | 菜单树形 |

### 13.4 业务日志

#### 13.4.1 日志实体

| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | BIGSERIAL | 主键 |
| tenant_id | UUID | 所属租户 |
| user_id | UUID | 操作人 |
| user_name | VARCHAR(50) | 操作人姓名 |
| module | VARCHAR(50) | 操作模块 |
| action | VARCHAR(50) | 操作类型 |
| resource_type | VARCHAR(50) | 资源类型 |
| resource_id | VARCHAR(50) | 资源ID |
| detail | JSONB | 变更详情 |
| ip_address | VARCHAR(50) | IP地址 |
| user_agent | VARCHAR(200) | 浏览器UA |
| created_at | TIMESTAMPTZ | 操作时间 |

#### 13.4.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/logs` | 日志列表 |
| GET | `/api/v1/tenants/{tenant_id}/logs/{id}` | 日志详情 |
| POST | `/api/v1/tenants/{tenant_id}/logs/export` | 导出日志 |
| GET | `/api/v1/tenants/{tenant_id}/logs/stats` | 日志统计 |

### 13.5 系统广播

#### 13.5.1 广播实体

| 字段 | 类型 | 说明 |
|------|------|------|
| broadcast_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| title | VARCHAR(100) | 标题 |
| content | TEXT | 内容 |
| broadcast_type | ENUM | popup/notice/urgent |
| target_type | ENUM | all/dept/role/user |
| target_ids | UUID[] | 目标范围 |
| publish_at | TIMESTAMPTZ | 发布时间 |
| expire_at | TIMESTAMPTZ | 过期时间 |
| status | ENUM | draft/published/revoked |
| created_by | UUID | 创建人 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.5.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/broadcasts` | 广播列表 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts` | 创建广播 |
| PUT | `/api/v1/tenants/{tenant_id}/broadcasts/{id}` | 更新广播 |
| DELETE | `/api/v1/tenants/{tenant_id}/broadcasts/{id}` | 删除广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/publish` | 发布广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/revoke` | 撤回广播 |

### 13.6 校验规则配置

#### 13.6.1 规则实体

| 字段 | 类型 | 说明 |
|------|------|------|
| rule_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| rule_name | VARCHAR(50) | 规则名称 |
| rule_code | VARCHAR(50) | 规则编码 |
| field_type | ENUM | string/number/date/regex/custom |
| rule_expr | VARCHAR(200) | 正则表达式或规则表达式 |
| error_message | VARCHAR(100) | 错误提示 |
| is_active | BOOLEAN | 是否启用 |

#### 13.6.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/validation-rules` | 规则列表 |
| POST | `/api/v1/tenants/{tenant_id}/validation-rules` | 创建规则 |
| PUT | `/api/v1/tenants/{tenant_id}/validation-rules/{id}` | 更新规则 |
| DELETE | `/api/v1/tenants/{tenant_id}/validation-rules/{id}` | 删除规则 |
| POST | `/api/v1/tenants/{tenant_id}/validation-rules/{id}/test` | 测试规则 |

### 13.7 支付配置

#### 13.7.1 支付渠道实体

| 字段 | 类型 | 说明 |
|------|------|------|
| channel_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| channel_name | VARCHAR(50) | 渠道名称 |
| channel_type | ENUM | alipay/wechat/unionpay |
| app_id | VARCHAR(100) | 应用ID |
| merchant_id | VARCHAR(100) | 商户号 |
| config | JSONB | 渠道配置（密钥等） |
| status | ENUM | active/disabled/test |
| is_default | BOOLEAN | 是否默认 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.7.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/pay-channels` | 渠道列表 |
| POST | `/api/v1/tenants/{tenant_id}/pay-channels` | 创建渠道 |
| PUT | `/api/v1/tenants/{tenant_id}/pay-channels/{id}` | 更新渠道 |
| DELETE | `/api/v1/tenants/{tenant_id}/pay-channels/{id}` | 删除渠道 |
| POST | `/api/v1/tenants/{tenant_id}/pay-channels/{id}/test` | 测试连接 |

### 13.8 测试表单

#### 13.8.1 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/test-forms` | 表单列表 |
| POST | `/api/v1/tenants/{tenant_id}/test-forms` | 创建表单 |
| GET | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 表单详情 |
| PUT | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 更新表单 |
| DELETE | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 删除表单 |
| POST | `/api/v1/tenants/{tenant_id}/test-forms/{id}/submit` | 提交表单 |

### 13.9 模板管理

#### 13.9.1 模板实体

| 字段 | 类型 | 说明 |
|------|------|------|
| template_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| template_name | VARCHAR(100) | 模板名称 |
| template_type | ENUM | word/excel/pdf/custom |
| template_path | VARCHAR(500) | 存储路径 |
| variables | JSONB | 变量定义 |
| preview_url | VARCHAR(500) | 预览URL |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.9.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/templates` | 模板列表 |
| POST | `/api/v1/tenants/{tenant_id}/templates` | 上传模板 |
| GET | `/api/v1/tenants/{tenant_id}/templates/{id}` | 模板详情 |
| PUT | `/api/v1/tenants/{tenant_id}/templates/{id}` | 更新模板 |
| DELETE | `/api/v1/tenants/{tenant_id}/templates/{id}` | 删除模板 |
| POST | `/api/v1/tenants/{tenant_id}/templates/{id}/preview` | 预览模板 |

### 13.10 数据字典

> 见「八、公共档案 - 8.1 公共数据字典」

---

## 十四、门户管理

### 14.1 门户页面

#### 14.1.1 门户页面实体

| 字段 | 类型 | 说明 |
|------|------|------|
| page_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| page_code | VARCHAR(50) | 页面编码 |
| page_name | VARCHAR(100) | 页面名称 |
| layout | JSONB | 布局配置 |
| components | JSONB | 组件列表 |
| is_published | BOOLEAN | 是否发布 |
| is_default | BOOLEAN | 是否默认首页 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 14.1.2 页面组件类型

| 组件类型 | 说明 |
|----------|------|
| banner | 图片轮播 |
| news_list | 新闻列表 |
| quick_entry | 快捷入口 |
| data_stat | 数据统计卡片 |
| task_todo | 待办任务数 |
| device_status | 设备状态概览 |
| announcement | 系统公告 |
| weather | 天气预报 |

#### 14.1.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/portal-pages` | 门户页面列表 |
| POST | `/api/v1/tenants/{tenant_id}/portal-pages` | 创建门户页面 |
| GET | `/api/v1/tenants/{tenant_id}/portal-pages/{id}` | 页面详情 |
| PUT | `/api/v1/tenants/{tenant_id}/portal-pages/{id}` | 更新页面 |
| DELETE | `/api/v1/tenants/{tenant_id}/portal-pages/{id}` | 删除页面 |
| POST | `/api/v1/tenants/{tenant_id}/portal-pages/{id}/publish` | 发布页面 |
| GET | `/api/v1/tenants/{tenant_id}/portal-pages/{id}/preview` | 预览页面 |
| PUT | `/api/v1/tenants/{tenant_id}/portal-pages/{id}/default` | 设为默认首页 |

### 14.2 新闻公告

#### 14.2.1 新闻栏目实体

| 字段 | 类型 | 说明 |
|------|------|------|
| category_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| category_name | VARCHAR(100) | 栏目名称 |
| category_code | VARCHAR(50) | 栏目编码 |
| parent_id | UUID | 父级栏目 |
| sort_order | INT | 排序 |
| is_active | BOOLEAN | 是否启用 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 14.2.2 新闻发布实体

| 字段 | 类型 | 说明 |
|------|------|------|
| news_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| category_id | UUID | 所属栏目 |
| title | VARCHAR(200) | 标题 |
| content | TEXT | 内容（富文本） |
| summary | VARCHAR(500) | 摘要 |
| author | VARCHAR(50) | 作者 |
| source | VARCHAR(100) | 来源 |
| cover_image | VARCHAR(500) | 封面图 |
| tags | VARCHAR[] | 标签 |
| status | ENUM | draft/published/archived |
| publish_time | TIMESTAMPTZ | 发布时间 |
| view_count | INT | 浏览次数 |
| created_at | TIMESTAMPTZ | 创建时间 |
| updated_at | TIMESTAMPTZ | 更新时间 |

#### 14.2.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/news` | 新闻列表 |
| POST | `/api/v1/tenants/{tenant_id}/news` | 创建新闻 |
| GET | `/api/v1/tenants/{tenant_id}/news/{id}` | 新闻详情 |
| PUT | `/api/v1/tenants/{tenant_id}/news/{id}` | 更新新闻 |
| DELETE | `/api/v1/tenants/{tenant_id}/news/{id}` | 删除新闻 |
| POST | `/api/v1/tenants/{tenant_id}/news/{id}/publish` | 发布新闻 |
| GET | `/api/v1/tenants/{tenant_id}/news-categories` | 栏目列表 |
| POST | `/api/v1/tenants/{tenant_id}/news-categories` | 创建栏目 |

### 14.3 预警消息

#### 14.3.1 预警配置实体

| 字段 | 类型 | 说明 |
|------|------|------|
| alert_config_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| alert_name | VARCHAR(100) | 预警名称 |
| alert_type | ENUM | threshold/schedule/event |
| condition | JSONB | 触发条件 |
| severity | ENUM | info/warning/critical |
| channels | VARCHAR[] | 通知渠道 |
| is_active | BOOLEAN | 是否启用 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 14.3.2 预警信息实体

| 字段 | 类型 | 说明 |
|------|------|------|
| alert_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| config_id | UUID | 关联配置ID |
| alert_time | TIMESTAMPTZ | 预警时间 |
| severity | ENUM | info/warning/critical |
| title | VARCHAR(200) | 预警标题 |
| content | TEXT | 预警内容 |
| status | ENUM | triggered/acknowledged/resolved |
| acknowledged_by | UUID | 确认人 |
| acknowledged_at | TIMESTAMPTZ | 确认时间 |
| resolved_at | TIMESTAMPTZ | 解决时间 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 14.3.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
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

### 14.4 门户管理页面清单

| 页面路径 | 角色 | 功能 |
|----------|------|------|
| `/portal` | 全部用户 | 门户首页（默认页） |
| `/portal/pages` | 租户管理员 | 门户页面管理 |
| `/portal/news` | 全部用户 | 新闻列表页 |
| `/portal/news/{id}` | 全部用户 | 新闻详情页 |
| `/portal/news/manage` | 租户管理员 | 新闻管理后台 |
| `/portal/alerts` | 全部用户 | 预警消息中心 |
| `/portal/alerts/config` | 租户管理员 | 预警配置管理 |

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

**API**：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/favorites` | 收藏列表 |
| POST | `/api/v1/tenants/{tenant_id}/favorites` | 添加收藏 |
| DELETE | `/api/v1/tenants/{tenant_id}/favorites/{id}` | 取消收藏 |
| PUT | `/api/v1/tenants/{tenant_id}/favorites/reorder` | 重新排序 |

### 15.2 首页配置

| 字段 | 类型 | 说明 |
|------|------|------|
| dashboard_id | UUID | 主键 |
| user_id | UUID | 用户ID |
| layout | JSONB | 布局配置 |
| widgets | JSONB | 组件列表 |
| updated_at | TIMESTAMPTZ | 更新时间 |

**API**：

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

**API**：

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

**API**：

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

**API**：

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

**API**：

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
| UNIQUE | (category, item_code) | | |

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
| dept_count | INT |