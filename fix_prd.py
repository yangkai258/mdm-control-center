# -*- coding: utf-8 -*-
filepath = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where MMS (old content) starts
mms_pos = content.find('Member Marketing System')
print(f'MMS at: {mms_pos}')
print(f'Total length: {len(content)}')

# Truncate at MMS position (keep everything before it)
truncated = content[:mms_pos]
print(f'Truncated length: {len(truncated)}')

# Write truncated content
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(truncated)

print('File truncated successfully')

# Now append the remaining sections
append_content = r'''

### 11.4 流程多版本管理

#### 11.4.1 版本策略

| 策略 | 说明 |
|------|------|
| 大版本 | 流程结构重大变更，手动发布新版本 |
| 小版本 | 仅表单调整，自动继承 |

#### 11.4.2 版本管理

| 字段 | 类型 | 说明 |
|------|------|------|
| version_id | UUID | 主键 |
| workflow_id | UUID | 所属流程 |
| version | INT | 版本号 |
| bpmn_xml | TEXT | BPMN XML |
| change_log | VARCHAR(500) | 变更说明 |
| status | ENUM | current/history/archived |
| published_at | TIMESTAMPTZ | 发布时间 |
| published_by | UUID | 发布人 |

#### 11.4.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/workflows/{id}/versions` | 版本列表 |
| POST | `/api/v1/tenants/{tenant_id}/workflows/{id}/rollback` | 回滚到历史版本 |
| GET | `/api/v1/tenants/{tenant_id}/workflows/{id}/versions/{vid}` | 版本详情 |

### 11.5 异常任务列表

#### 11.5.1 异常类型

| 异常类型 | 说明 | 处理建议 |
|----------|------|----------|
| timeout | 任务超时未处理 | 提醒办理人/自动转办/终止流程 |
| rejected | 被拒绝的任务 | 查看拒绝原因 |
| no_assignee | 无办理人 | 配置办理人或管理员代处理 |
| error | 执行异常 | 查看错误日志 |

#### 11.5.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/tasks/exception` | 异常任务列表 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/reassign` | 重新分配 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/terminate` | 终止任务 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/{id}/error-log` | 错误日志 |

### 11.6 审批代理

#### 11.6.1 代理规则

| 规则 | 说明 |
|------|------|
| 全部代理 | 所有待办任务自动转发 |
| 部分代理 | 仅指定流程代理 |
| 临时代理 | 设置代理时间段 |

#### 11.6.2 实体字段

| 字段 | 类型 | 说明 |
|------|------|------|
| delegation_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| delegator | UUID | 委托人 |
| delegatee | UUID | 受托人 |
| process_keys | VARCHAR[] | 可代理的流程（NULL表示全部） |
| start_time | TIMESTAMPTZ | 代理开始时间 |
| end_time | TIMESTAMPTZ | 代理结束时间 |
| is_active | BOOLEAN | 是否生效 |

#### 11.6.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/delegations` | 代理列表 |
| POST | `/api/v1/tenants/{tenant_id}/delegations` | 创建代理规则 |
| PUT | `/api/v1/tenants/{tenant_id}/delegations/{id}` | 更新代理规则 |
| DELETE | `/api/v1/tenants/{tenant_id}/delegations/{id}` | 删除代理规则 |
| GET | `/api/v1/tenants/{tenant_id}/delegations/received` | 待我代办的任务 |

### 11.7 待办批处理

#### 11.7.1 批处理限制

| 限制项 | 说明 |
|--------|------|
| 单次最大数量 | 50条 |
| 必须同流程 | 同一流程的任务才能批量处理 |
| 必须同节点 | 同一节点的任务才能批量处理 |

#### 11.7.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/tenants/{tenant_id}/tasks/batch-complete` | 批量同意 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/batch-reject` | 批量拒绝 |
| GET | `/api/v1/tenants/{tenant_id}/tasks/batch-preview` | 预览批处理结果 |

### 11.8 无执行人任务列表

当流程节点配置的办理人为空时，任务进入异常池。

#### 11.8.1 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/tasks/unassigned` | 无执行人任务列表 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/claim` | 认领任务 |
| POST | `/api/v1/tenants/{tenant_id}/tasks/{id}/assign` | 指定办理人 |

---

## 十二、基础管理（档案/调度/字典等）

> **功能路径**：`/system` 模块
> **权限要求**：超级管理员或租户管理员

### 12.1 基础档案

#### 12.1.1 档案实体

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

#### 12.1.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/archives` | 档案列表 |
| POST | `/api/v1/tenants/{tenant_id}/archives` | 创建档案 |
| PUT | `/api/v1/tenants/{tenant_id}/archives/{id}` | 更新档案 |
| DELETE | `/api/v1/tenants/{tenant_id}/archives/{id}` | 删除档案 |
| GET | `/api/v1/tenants/{tenant_id}/archives/tree` | 档案树形 |

### 12.2 调度计划

#### 12.2.1 调度实体

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

#### 12.2.2 API

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

### 12.3 菜单设置

#### 12.3.1 菜单实体

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

#### 12.3.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/menus` | 菜单列表 |
| POST | `/api/v1/tenants/{tenant_id}/menus` | 创建菜单 |
| PUT | `/api/v1/tenants/{tenant_id}/menus/{id}` | 更新菜单 |
| DELETE | `/api/v1/tenants/{tenant_id}/menus/{id}` | 删除菜单 |
| GET | `/api/v1/tenants/{tenant_id}/menus/tree` | 菜单树形 |

### 12.4 业务日志

#### 12.4.1 日志实体

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

#### 12.4.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/logs` | 日志列表 |
| GET | `/api/v1/tenants/{tenant_id}/logs/{id}` | 日志详情 |
| POST | `/api/v1/tenants/{tenant_id}/logs/export` | 导出日志 |
| GET | `/api/v1/tenants/{tenant_id}/logs/stats` | 日志统计 |

### 12.5 系统广播

#### 12.5.1 广播实体

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

#### 12.5.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/broadcasts` | 广播列表 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts` | 创建广播 |
| PUT | `/api/v1/tenants/{tenant_id}/broadcasts/{id}` | 更新广播 |
| DELETE | `/api/v1/tenants/{tenant_id}/broadcasts/{id}` | 删除广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/publish` | 发布广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/revoke` | 撤回广播 |

### 12.6 校验规则配置

#### 12.6.1 规则实体

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

#### 12.6.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/validation-rules` | 规则列表 |
| POST | `/api/v1/tenants/{tenant_id}/validation-rules` | 创建规则 |
| PUT | `/api/v1/tenants/{tenant_id}/validation-rules/{id}` | 更新规则 |
| DELETE | `/api/v1/tenants/{tenant_id}/validation-rules/{id}` | 删除规则 |
| POST | `/api/v1/tenants/{tenant_id}/validation-rules/{id}/test` | 测试规则 |

### 12.7 支付配置

#### 12.7.1 支付渠道实体

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

#### 12.7.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/pay-channels` | 渠道列表 |
| POST | `/api/v1/tenants/{tenant_id}/pay-channels` | 创建渠道 |
| PUT | `/api/v1/tenants/{tenant_id}/pay-channels/{id}` | 更新渠道 |
| DELETE | `/api/v1/tenants/{tenant_id}/pay-channels/{id}` | 删除渠道 |
| POST | `/api/v1/tenants/{tenant_id}/pay-channels/{id}/test` | 测试连接 |

### 12.8 测试表单

#### 12.8.1 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/test-forms` | 表单列表 |
| POST | `/api/v1/tenants/{tenant_id}/test-forms` | 创建表单 |
| GET | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 表单详情 |
| PUT | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 更新表单 |
| DELETE | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 删除表单 |
| POST | `/api/v1/tenants/{tenant_id}/test-forms/{id}/submit` | 提交表单 |

### 12.9 模板管理

#### 12.9.1 模板实体

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

#### 12.9.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/templates` | 模板列表 |
| POST | `/api/v1/tenants/{tenant_id}/templates` | 上传模板 |
| GET | `/api/v1/tenants/{tenant_id}/templates/{id}` | 模板详情 |
| PUT | `/api/v1/tenants/{tenant_id}/templates/{id}` | 更新模板 |
| DELETE | `/api/v1/tenants/{tenant_id}/templates/{id}` | 删除模板 |
| POST | `/api/v1/tenants/{tenant_id}/templates/{id}/preview` | 预览模板 |

### 12.10 数据字典

> 见「八、公共档案 - 8.1 公共数据字典」

---

## 十三、门户管理

> **功能路径**：`/portal` 模块
> **权限要求**：租户管理员

### 13.1 门户页面

可视化页面配置，支持拖拽组件构建门户首页。

#### 13.1.1 门户页面实体

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

#### 13.1.2 页面组件类型

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

#### 13.1.3 门户页面 API

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

### 13.2 新闻公告

#### 13.2.1 新闻栏目实体

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

#### 13.2.2 新闻发布实体

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

#### 13.2.3 新闻 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/news` | 新闻列表（分页+筛选） |
| POST | `/api/v1/tenants/{tenant_id}/news` | 创建新闻 |
| GET | `/api/v1/tenants/{tenant_id}/news/{id}` | 新闻详情 |
| PUT | `/api/v1/tenants/{tenant_id}/news/{id}` | 更新新闻 |
| DELETE | `/api/v1/tenants/{tenant_id}/news/{id}` | 删除新闻 |
| POST | `/api/v1/tenants/{tenant_id}/news/{id}/publish` | 发布新闻 |
| POST | `/api/v1/tenants/{tenant_id}/news/{id}/unpublish` | 下架新闻 |

#### 13.2.4 栏目 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/news-categories` | 栏目列表 |
| POST | `/api/v1/tenants/{tenant_id}/news-categories` | 创建栏目 |
| PUT | `/api/v1/tenants/{tenant_id}/news-categories/{id}` | 更新栏目 |
| DELETE | `/api/v1/tenants/{tenant_id}/news-categories/{id}` | 删除栏目 |

### 13.3 预警消息

#### 13.3.1 预警配置实体

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

#### 13.3.2 预警信息实体

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

#### 13.3.3 预警消息 API

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
| GET | `/api/v1/tenants/{tenant_id}/alert-logs/{alert_id}` | 某预警的流水 |

### 13.4 门户管理页面清单

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

## 十四、实施工具

### 14.1 收藏菜单

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

### 14.2 首页配置

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

### 14.3 邮件配置

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

### 14.4 消息通知

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

### 14.5 系统版本信息

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/system/version` | 版本信息 |
| GET | `/api/v1/system/health` | 健康检查 |
| GET | `/api/v1/system/capabilities` | 系统能力 |

### 14.6 外部服务

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

### 14.7 系统参数设置

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

## 十五、数据库设计

### 15.1 平台级表（无 tenant_id）

#### tenants（租户台账）

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
| status | VARCHAR(20) | DEFAULT 'pending' | pending/approved/rejected |
| reject_reason | TEXT | NULL | 拒绝原因 |
| audit_by | UUID | NULL | 审核人 |
| audit_at | TIMESTAMPTZ | NULL | 审核时间 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | 创建时间 |

#### plans（套餐定义）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | SERIAL | PK | 主键 |
| plan_name | VARCHAR(20) | NOT NULL