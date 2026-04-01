# HEARTBEAT.md - 凌晨状态 (2026-04-02 00:30)

## 服务状态 ✅
| 服务 | 端口 | 状态 |
|------|------|------|
| 后端 | 8080 | ✅ 运行中 |
| 前端 | 3000 | ✅ 运行中 (Arco Design Pro) |
| PostgreSQL | 5432 | ✅ Docker healthy |
| Redis | 6379 | ✅ Docker healthy |
| EMQX | 1883/8083/18083 | ✅ Docker healthy |

## 2026-04-02 凌晨完成

### 登录系统修复 ✅
- 删除 `.env.development` 中的 `VITE_API_BASE_URL`
- `vite.config.dev.ts` 代理 rewrite：`/api` → `/api/v1`
- 修复 `user.ts` API 路径：`/api/user/login` → `/api/auth/login`
- 后端新增 `/logout`、`/me`、`/menu` 接口，响应码统一 `code: 20000`
- 修复 `getUserInfo()` / `getMenuList()` 为 GET 方法

### 前端迁移 ✅
- 切换到 `mdm-frontend-new/arco-design-pro-vite/`
- 旧 `frontend/` 保留（待迁移功能）

### 面包屑全局组件 ✅
- `page-layout.vue` 全局加入 `<Breadcrumb>`

### 菜单空白项修复 ✅
- 12 个 redirect 路由加 `hideInMenu: true`
- `menu/index.vue` 菜单 locale fallback

### 国际化修复 ✅
- 清除 `zh-CN.ts` 重复 key

## 明日工作计划

### 文档
- 迁移清单：`mdm-project/docs/MIGRATION_MISSING.md`
- 明日计划：`mdm-project/docs/TOMORROW_PLAN.md`

### Phase 1 核心页面迁移
- Dashboard.vue, DeviceDashboard.vue, DeviceStatus.vue
- Member.vue, PetConfig.vue, OtaFirmware.vue, Alert.vue

### 迁移标准
- 面包屑 + 三段式布局
- API 通过 `/api` 代理
- Arco Design 组件
- Authorization header

## 访问信息
- 前端: http://localhost:3000 （admin / admin123）
- 后端: http://localhost:8080
- EMQX: http://localhost:18083 （admin/public）

## GitHub
- https://github.com/yangkai258/mdm-iot-platform

## 待处理
- [ ] Phase 1 核心页面迁移
- [ ] 后端稳定性优化
