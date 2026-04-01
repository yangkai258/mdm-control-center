# 会话快照 - 2026-04-02 00:30

## 状态
- 🔴 后端 8080 ✅
- 🔴 前端 3000 ✅ (Arco Design Pro)
- 🔴 Docker ✅

## 今日完成
1. ✅ 登录系统重构（API路径/代理/响应码）
2. ✅ 切换到新前端 arco-design-pro-vite
3. ✅ 面包屑全局组件
4. ✅ 菜单空白项修复
5. ✅ 菜单 sort 功能定位（旧前端 `frontend/src/views/permissions/Menus.vue`）

## 发现的问题
- 旧前端 `frontend/` 有 **270+ 个文件** 未迁移到新前端
- 菜单 sort 功能在 `permissions/Menus.vue`（sort 数字字段）

## 明日工作：前端迁移

### 文档
- `mdm-project/docs/MIGRATION_MISSING.md` - 完整缺失清单
- `mdm-project/docs/TOMORROW_PLAN.md` - 明日工作计划

### Phase 1 核心页面
Dashboard.vue, DeviceDashboard.vue, DeviceStatus.vue, Member.vue, PetConfig.vue, OtaFirmware.vue, Alert.vue

### 迁移规范
1. 面包屑 `<Breadcrumb>`
2. 三段式布局
3. API `/api/v1/xxx` 通过代理
4. `a-card.general-card` 包裹
5. axios 带 Authorization

## GitHub
- https://github.com/yangkai258/mdm-iot-platform
