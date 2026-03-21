# -*- coding: utf-8 -*-
fp = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(fp, 'a', encoding='utf-8') as f:
    f.write('''

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
| GET | `/api/v1/tenants/{tenant_id}/news` | 新闻列表（分页+筛选） |
| POST | `/api/v1/tenants/{tenant_id}/news` | 创建新闻 |
| GET | `/api/v1/tenants/{tenant_id}/news/{id}` | 新闻详情 |
| PUT | `/api/v1/tenants/{tenant_id}/news/{id}` | 更新新闻 |
| DELETE | `/api/v1/tenants/{tenant_id}/news/{id}` | 删除新闻 |
| POST | `/api/v1/tenants/{tenant_id}/news/{id}/publish` | 发布新闻 |
| POST | `/api/v1/tenants/{tenant_id}/news/{id}/unpublish` | 下架新闻 |
| GET | `/api/v1/tenants/{tenant_id}/news-categories` | 栏目列表 |
| POST | `/api/v1/tenants/{tenant_id}/news-categories` | 创建栏目 |
| PUT | `/api/v1/tenants/{tenant_id}/news-categories/{id}` | 更新栏目 |
| DELETE | `/api/v1/tenants/{tenant_id}/news-categories/{id}` | 删除栏目 |

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
| channels | VARCHAR[] | 通知渠道（站内/邮件/SMS） |
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
| GET | `/api/v1/tenants/{tenant_id}/alerts/{id}` | 预警详情 |
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
''')
print('Chapter 14 appended')
