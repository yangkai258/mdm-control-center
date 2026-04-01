# HEARTBEAT.md - 凌晨状态 (2026-04-02 00:04)

## 服务状态 ✅
| 服务 | 端口 | 状态 |
|------|------|------|
| 后端 | 8080 | ✅ 运行中 |
| 前端 | 3000 | ✅ 运行中 (Arco Design Pro) |
| PostgreSQL | 5432 | ✅ Docker healthy |
| Redis | 6379 | ✅ Docker healthy |
| EMQX | 1883/8083/18083 | ✅ Docker healthy |

## 2026-04-01 晚间完成

### 登录系统修复 ✅
- **问题**：前端调用 `/api/user/login`，后端路由 `/api/v1/auth/login`
- **修复**：
  1. 删除了 `.env.development` 中的 `VITE_API_BASE_URL`（绕过代理直连8080）
  2. 配置 `vite.config.dev.ts` 代理 rewrite：`/api` → `/api/v1`
  3. 修复 `user.ts` API 路径：`/api/user/login` → `/api/auth/login`
  4. 后端 `auth_controller.go` 新增 `/logout`、`/me`、`/menu` 接口
  5. 后端响应码统一改为 `code: 20000`
  6. 修复 `getUserInfo()` / `getMenuList()` 为 GET 方法
  7. 注册 `/api/v1/auth/me`、`/api/v1/auth/menu` 路由

### 前端迁移 ✅
- 切换到 `mdm-frontend-new/arco-design-pro-vite/`（新的 Arco Design Pro）
- 旧 `frontend/` 不再使用

### 面包屑全局组件 ✅
- 修改 `page-layout.vue`：全局加入 `<Breadcrumb>` 组件
- 从路由 `matched` 提取 `locale` 显示面包屑路径

### 国际化修复 ✅
- 清除 `zh-CN.ts` 重复 key：`menu.orders`、`menu.system.settings`
- `menu.pets.health` 与 `menu.system.health` 冲突，保留 `menu.pets.health`

### 菜单空白项修复 ✅
- **问题**：子菜单里出现空白项，点击无反应
- **原因**：所有 redirect 空路由（如 `{ path: '', redirect: '/xxx' }`）没有 `component` 但被菜单渲染出来了
- **修复**：
  1. 12 个 redirect 路由统一加 `meta: { hideInMenu: true }`
  2. `menu/index.vue` 菜单组件添加 fallback：`locale` 为空时显示 `route.name`
  3. 清除 `.vite` 缓存 + 重启 Vite

## 访问信息
- 前端: http://localhost:3000 （admin / admin123）
- 后端: http://localhost:8080
- EMQX: http://localhost:18083 （admin/public）

## GitHub
- https://github.com/yangkai258/mdm-iot-platform

## 待处理
- [ ] 后端稳定性优化（进程管理/自动重启）
- [ ] 前端 API 联调验证（各页面数据接口对接）
- [ ] 部署文档完善
