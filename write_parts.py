# -*- coding: utf-8 -*-
# Write new chapters content files

# Chapter 13: 基础管理
ch13 = """## 十三、基础管理（档案/调度/菜单/日志/字典等）

> **功能路径**：`/system` 模块
> **权限要求**：租户管理员（tenant_admin）
> **套餐要求**：基础版及以上

### 13.1 基础档案

#### 13.1.1 功能描述
基础档案用于管理企业的通用业务档案数据，支持树形层级结构和标准 CRUD 操作。档案类型由管理员自定义，每种档案可维护独立的字段结构。

#### 13.1.2 数据表
档案分类表（archive_category）：

| 字段 | 类型 | 说明 |
|------|------|------|
| category_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| category_name | VARCHAR(50) | 分类名称 |
| category_code | VARCHAR(30) | 分类编码（唯一） |
| parent_id | UUID | 上级分类（NULL表示根） |
| icon | VARCHAR(50) | 图标 |
| sort_order | INT | 排序 |
| field_schema | JSONB | 字段定义 JSON Schema |
| status | ENUM | active / disabled |
| created_at | TIMESTAMPTZ | 创建时间 |

档案数据表（archive_record）：

| 字段 | 类型 | 说明 |
|------|------|------|
| record_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| category_id | UUID | 档案分类 |
| parent_id | UUID | 上级档案（树形） |
| record_code | VARCHAR(50) | 档案编码 |
| record_name | VARCHAR(100) | 档案名称 |
| data | JSONB | 档案数据（动态字段） |
| status | ENUM | active / disabled |
| created_at | TIMESTAMPTZ | 创建时间 |
| updated_at | TIMESTAMPTZ | 更新时间 |

#### 13.1.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/archives/categories` | 获取档案分类树 |
| POST | `/api/v1/tenants/{tenant_id}/archives/categories` | 新建档案分类 |
| PUT | `/api/v1/tenants/{tenant_id}/archives/categories/{id}` | 更新档案分类 |
| DELETE | `/api/v1/tenants/{tenant_id}/archives/categories/{id}` | 删除档案分类 |
| GET | `/api/v1/tenants/{tenant_id}/archives/records` | 档案数据列表（分页+树形） |
| POST | `/api/v1/tenants/{tenant_id}/archives/records` | 新建档案数据 |
| GET | `/api/v1/tenants/{tenant_id}/archives/records/{id}` | 档案数据详情 |
| PUT | `/api/v1/tenants/{tenant_id}/archives/records/{id}` | 更新档案数据 |
| DELETE | `/api/v1/tenants/{tenant_id}/archives/records/{id}` | 删除档案数据 |

#### 13.1.4 按钮定义
**页面路径**: `/system/archives`
**布局**: 左侧树 + 右侧列表

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「新建档案」 | 打开全屏模态 | tenant_admin |
| 操作栏（右） | 「新建分类」 | 打开抽屉 | tenant_admin |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

### 13.2 调度计划

#### 13.2.1 功能描述
调度计划管理 Cron 定时任务，支持可视化配置执行周期、任务脚本和告警规则。

#### 13.2.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| job_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| job_name | VARCHAR(100) | 任务名称 |
| job_code | VARCHAR(50) | 任务编码（唯一） |
| job_type | ENUM | http / script / mq |
| cron_expression | VARCHAR(50) | Cron 表达式 |
| endpoint | VARCHAR(500) | HTTP 接口地址（HTTP类型） |
| script_content | TEXT | 脚本内容（Script类型） |
| params | JSONB | 任务参数 |
| timeout_seconds | INT | 超时时间（秒） |
| retry_count | INT | 重试次数 |
| status | ENUM | active / paused / stopped |
| last_run_at | TIMESTAMPTZ | 上次执行时间 |
| last_run_status | ENUM | success / failed / running |
| next_run_at | TIMESTAMPTZ | 下次执行时间 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.2.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/jobs` | 任务列表 |
| POST | `/api/v1/tenants/{tenant_id}/jobs` | 创建任务 |
| GET | `/api/v1/tenants/{tenant_id}/jobs/{id}` | 任务详情 |
| PUT | `/api/v1/tenants/{tenant_id}/jobs/{id}` | 更新任务 |
| DELETE | `/api/v1/tenants/{tenant_id}/jobs/{id}` | 删除任务 |
| POST | `/api/v1/tenants/{tenant_id}/jobs/{id}/execute` | 手动执行一次 |
| PUT | `/api/v1/tenants/{tenant_id}/jobs/{id}/pause` | 暂停任务 |
| PUT | `/api/v1/tenants/{tenant_id}/jobs/{id}/resume` | 恢复任务 |
| GET | `/api/v1/tenants/{tenant_id}/jobs/{id}/logs` | 执行日志 |
| GET | `/api/v1/tenants/{tenant_id}/jobs/cron/validate` | 验证 Cron 表达式 |

#### 13.2.4 按钮定义
**页面路径**: `/system/scheduler`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「新建任务」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「立即执行」 | 确认弹窗 | tenant_admin |
| 表格行 | 「暂停」 | 确认弹窗 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |
| 表格行 | 「日志」 | 路由跳转日志页 | all |

### 13.3 菜单设置

#### 13.3.1 功能描述
前端动态菜单管理，支持租户自定义菜单结构、图标、路由和权限标识。

#### 13.3.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| menu_id | UUID | 主键 |
| tenant_id | UUID | 所属租户（NULL表示平台级） |
| parent_id | UUID | 上级菜单（NULL表示根） |
| menu_name | VARCHAR(50) | 菜单名称 |
| menu_code | VARCHAR(50) | 菜单编码 |
| path | VARCHAR(200) | 路由路径 |
| component | VARCHAR(200) | 组件路径 |
| icon | VARCHAR(50) | 图标 |
| sort_order | INT | 排序 |
| visible | BOOLEAN | 是否显示 |
| status | ENUM | active / disabled |
| permission | VARCHAR(50) | 权限标识 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.3.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/menus` | 获取菜单树 |
| POST | `/api/v1/tenants/{tenant_id}/menus` | 新建菜单 |
| GET | `/api/v1/tenants/{tenant_id}/menus/{id}` | 菜单详情 |
| PUT | `/api/v1/tenants/{tenant_id}/menus/{id}` | 更新菜单 |
| DELETE | `/api/v1/tenants/{tenant_id}/menus/{id}` | 删除菜单 |
| PUT | `/api/v1/tenants/{tenant_id}/menus/reorder` | 批量排序 |

#### 13.3.4 按钮定义
**页面路径**: `/system/menus`
**布局**: 左侧树 + 右侧表单

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「刷新」 | 刷新树 | all |
| 操作栏（右） | 「新增菜单」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「新增子菜单」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

### 13.4 业务日志

#### 13.4.1 功能描述
业务操作日志记录和查询，支持按时间、模块、操作人等维度筛选和导出。

#### 13.4.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| user_id | UUID | 操作用户 |
| user_name | VARCHAR(50) | 操作用户名（冗余） |
| module | VARCHAR(50) | 操作模块 |
| action | VARCHAR(50) | 操作动作（create/update/delete） |
| resource_type | VARCHAR(50) | 资源类型 |
| resource_id | UUID | 资源ID |
| detail | JSONB | 操作详情（旧值/新值） |
| ip_address | VARCHAR(50) | IP 地址 |
| user_agent | VARCHAR(200) | 浏览器标识 |
| created_at | TIMESTAMPTZ | 操作时间 |

#### 13.4.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/logs` | 日志列表（分页+筛选） |
| GET | `/api/v1/tenants/{tenant_id}/logs/{id}` | 日志详情 |
| GET | `/api/v1/tenants/{tenant_id}/logs/statistics` | 日志统计 |
| POST | `/api/v1/tenants/{tenant_id}/logs/export` | 导出日志（异步） |

#### 13.4.4 按钮定义
**页面路径**: `/system/audit-logs`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（左） | 「时间范围」 | 日期范围选择器 | all |
| 操作栏（右） | 「导出」 | 导出Excel | tenant_admin |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 表格行 | 「详情」 | 打开抽屉 | all |

### 13.5 系统广播

#### 13.5.1 功能描述
向租户内所有用户发送全员通知，支持定时发送和撤回。

#### 13.5.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| broadcast_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| title | VARCHAR(100) | 广播标题 |
| content | TEXT | 广播内容 |
| broadcast_type | ENUM | all / dept / role |
| target_scope | JSONB | 发送范围配置 |
| send_time | TIMESTAMPTZ | 发送时间（NULL为立即） |
| published_at | TIMESTAMPTZ | 发布时间 |
| status | ENUM | draft / published / cancelled |
| created_by | UUID | 创建人 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.5.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/broadcasts` | 广播列表 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts` | 创建广播 |
| GET | `/api/v1/tenants/{tenant_id}/broadcasts/{id}` | 广播详情 |
| PUT | `/api/v1/tenants/{tenant_id}/broadcasts/{id}` | 更新广播 |
| DELETE | `/api/v1/tenants/{tenant_id}/broadcasts/{id}` | 删除广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/publish` | 发布广播 |
| POST | `/api/v1/tenants/{tenant_id}/broadcasts/{id}/cancel` | 撤回广播 |

#### 13.5.4 按钮定义
**页面路径**: `/system/broadcasts`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「新建广播」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「发布」 | 确认弹窗 | tenant_admin |
| 表格行 | 「撤回」 | 确认弹窗 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

### 13.6 校验规则配置

#### 13.6.1 功能描述
管理表单字段的校验规则，支持正则表达式和自定义错误消息。

#### 13.6.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| rule_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| rule_name | VARCHAR(50) | 规则名称 |
| rule_code | VARCHAR(30) | 规则编码 |
| field_type | ENUM | string / number / date / phone / email / idcard |
| pattern | VARCHAR(200) | 正则表达式 |
| min_length | INT | 最小长度 |
| max_length | INT | 最大长度 |
| error_message | VARCHAR(200) | 错误提示消息 |
| status | ENUM | active / disabled |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.6.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/validation-rules` | 规则列表 |
| POST | `/api/v1/tenants/{tenant_id}/validation-rules` | 新建规则 |
| GET | `/api/v1/tenants/{tenant_id}/validation-rules/{id}` | 规则详情 |
| PUT | `/api/v1/tenants/{tenant_id}/validation-rules/{id}` | 更新规则 |
| DELETE | `/api/v1/tenants/{tenant_id}/validation-rules/{id}` | 删除规则 |
| POST | `/api/v1/tenants/{tenant_id}/validation-rules/{id}/test` | 测试规则 |

#### 13.6.4 按钮定义
**页面路径**: `/system/validation-rules`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「新建规则」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「测试」 | 打开抽屉 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

### 13.7 支付配置

#### 13.7.1 功能描述
配置支付渠道，包括微信支付、支付宝等第三方支付通道。

#### 13.7.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| channel_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| channel_name | VARCHAR(50) | 渠道名称 |
| channel_type | ENUM | wechat / alipay / unionpay |
| app_id | VARCHAR(100) | 应用ID |
| merchant_id | VARCHAR(50) | 商户号 |
| api_key | VARCHAR(200) | API密钥（加密存储） |
| cert_path | VARCHAR(500) | 证书路径 |
| status | ENUM | active / disabled / testing |
| is_default | BOOLEAN | 是否默认渠道 |
| created_at | TIMESTAMPTZ | 创建时间 |
| updated_at | TIMESTAMPTZ | 更新时间 |

#### 13.7.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/payment-channels` | 支付渠道列表 |
| POST | `/api/v1/tenants/{tenant_id}/payment-channels` | 新建支付渠道 |
| GET | `/api/v1/tenants/{tenant_id}/payment-channels/{id}` | 渠道详情 |
| PUT | `/api/v1/tenants/{tenant_id}/payment-channels/{id}` | 更新渠道配置 |
| DELETE | `/api/v1/tenants/{tenant_id}/payment-channels/{id}` | 删除渠道 |
| POST | `/api/v1/tenants/{tenant_id}/payment-channels/{id}/test` | 测试支付通道 |

#### 13.7.4 按钮定义
**页面路径**: `/system/payment-channels`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「新建渠道」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「测试」 | 确认弹窗后测试 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

### 13.8 测试表单

#### 13.8.1 功能描述
为开发测试阶段提供临时表单数据录入，支持提交后查看数据。

#### 13.8.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| form_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| form_name | VARCHAR(50) | 表单名称 |
| form_schema | JSONB | 表单 Schema |
| submissions | JSONB[] | 提交记录数组 |
| total_count | INT | 提交次数 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.8.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/test-forms` | 表单列表 |
| POST | `/api/v1/tenants/{tenant_id}/test-forms` | 创建测试表单 |
| GET | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 表单详情 |
| PUT | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 更新表单 |
| DELETE | `/api/v1/tenants/{tenant_id}/test-forms/{id}` | 删除表单 |
| POST | `/api/v1/tenants/{tenant_id}/test-forms/{id}/submit` | 提交表单数据 |

#### 13.8.4 按钮定义
**页面路径**: `/system/test-forms`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「新建表单」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「填写」 | 打开全屏模态 | all |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

### 13.9 模板管理

#### 13.9.1 功能描述
文档模板管理，支持上传、预览和下载各类文档模板（Word/Excel/PDF）。

#### 13.9.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| template_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| template_name | VARCHAR(100) | 模板名称 |
| template_code | VARCHAR(50) | 模板编码 |
| template_type | ENUM | word / excel / pdf |
| file_url | VARCHAR(500) | 文件存储地址 |
| file_size | INT | 文件大小（字节） |
| variables | JSONB | 模板变量定义 |
| description | VARCHAR(200) | 模板描述 |
| status | ENUM | active / disabled |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.9.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/templates` | 模板列表 |
| POST | `/api/v1/tenants/{tenant_id}/templates` | 上传模板 |
| GET | `/api/v1/tenants/{tenant_id}/templates/{id}` | 模板详情 |
| PUT | `/api/v1/tenants/{tenant_id}/templates/{id}` | 更新模板信息 |
| DELETE | `/api/v1/tenants/{tenant_id}/templates/{id}` | 删除模板 |
| GET | `/api/v1/tenants/{tenant_id}/templates/{id}/preview` | 预览模板 |

#### 13.9.4 按钮定义
**页面路径**: `/system/templates`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（左） | 「类型筛选」 | 下拉筛选 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「上传模板」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「预览」 | 打开新窗口 | all |
| 表格行 | 「下载」 | 触发下载 | all |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

### 13.10 效率套件

#### 13.10.1 功能描述
内置效率工具集，包括二维码生成、条形码生成、随机抽签、批量编号生成等常用工具。

#### 13.10.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| tool_id | UUID | 主键 |
| tenant_id | UUID | 所属租户 |
| tool_name | VARCHAR(50) | 工具名称 |
| tool_code | VARCHAR(30) | 工具编码 |
| tool_type | ENUM | qrcode / barcode / random / batchno |
| config | JSONB | 工具配置参数 |
| usage_count | INT | 使用次数 |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.10.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/efficiency-tools` | 工具列表 |
| POST | `/api/v1/tenants/{tenant_id}/efficiency-tools/{code}/generate` | 生成结果 |
| GET | `/api/v1/tenants/{tenant_id}/efficiency-tools/{code}/history` | 使用历史 |

#### 13.10.4 按钮定义
**页面路径**: `/system/efficiency-tools`
**布局**: 工具卡片网格

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 工具卡片 | 「使用」 | 打开对话框 | all |
| 工具卡片 | 「使用历史」 | 打开抽屉 | all |

### 13.11 数据字典

#### 13.11.1 功能描述
通用数据字典，支持租户自定义业务编码体系和维护常用选项列表。

#### 13.11.2 数据表
| 字段 | 类型 | 说明 |
|------|------|------|
| dict_id | UUID | 主键 |
| tenant_id | UUID | 所属租户（NULL为平台级） |
| dict_name | VARCHAR(50) | 字典名称 |
| dict_code | VARCHAR(30) | 字典编码 |
| description | VARCHAR(200) | 说明 |
| items | JSONB | 字典项列表 |
| status | ENUM | active / disabled |
| created_at | TIMESTAMPTZ | 创建时间 |

#### 13.11.3 API接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tenants/{tenant_id}/dicts` | 字典列表 |
| POST | `/api/v1/tenants/{tenant_id}/dicts` | 新建字典 |
| GET | `/api/v1/tenants/{tenant_id}/dicts/{id}` | 字典详情（含字典项） |
| PUT | `/api/v1/tenants/{tenant_id}/dicts/{id}` | 更新字典 |
| DELETE | `/api/v1/tenants/{tenant_id}/dicts/{id}` | 删除字典 |
| POST | `/api/v1/tenants/{tenant_id}/dicts/{id}/items` | 新增字典项 |
| PUT | `/api/v1/tenants/{tenant_id}/dicts/{id}/items/{item_id}` | 更新字典项 |
| DELETE | `/api/v1/tenants/{tenant_id}/dicts/{id}/items/{item_id}` | 删除字典项 |

#### 13.11.4 按钮定义
**页面路径**: `/system/data-dicts`
**布局**: 列表页

**按钮定义**:
| 位置 | 按钮名称 | 动作 | 权限 |
|------|----------|------|------|
| 操作栏（左） | 「搜索」 | 展开筛选面板 | all |
| 操作栏（右） | 「刷新」 | 刷新列表 | all |
| 操作栏（右） | 「新建字典」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「编辑」 | 打开全屏模态 | tenant_admin |
| 表格行 | 「字典项」 | 打开抽屉 | tenant_admin |
| 表格行 | 「删除」 | 删除确认弹窗 | tenant_admin |

with open(r"C:\Users\YKing\.openclaw\workspace\new_ch13.txt", "w", encoding="utf-8") as f:
    f.write(ch13)
print(f"Ch13 written: {len(ch13)} chars")
