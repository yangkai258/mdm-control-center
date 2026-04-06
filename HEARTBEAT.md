# HEARTBEAT.md - 服务状态 (2026-04-06 15:40)

## 当前状态
- ✅ Docker Desktop 运行中（PostgreSQL/Redis/EMQX healthy）
- ✅ 后端 http://localhost:8080 运行中
- ✅ 前端 Preview http://localhost:3003 运行中

## 今日完成
1. ✅ 统一菜单模块 - 删掉重复的 MDMMenu，将所有功能合并到单一 mdm.ts
2. ✅ 路由嵌套结构 - 每个模块作为父路由，子路由嵌套在父路由下
3. ✅ 补全缺失的 locale 翻译（51个菜单键）
4. ✅ 修复 API proxy 配置（preview 模式可正常登录）
5. ✅ Git commit: `f8c7e8a` feat(frontend): unify all menu modules into single mdm.ts

## Git Commits（今日）
- `92eb45e` fix(frontend): replace a-chart with placeholder divs
- `f5addad` fix(frontend): add business routes, fix build issues
- `a2b2a5b` fix(frontend): register 80+ business routes as top-level menu items
- `b3e81b2` fix(frontend): complete missing zh-CN locale translations
- `fa49637` fix(frontend): restructure routes as nested children under parent modules
- `7a3fa04` chore(frontend): remove business.ts (merged into mdm.ts)
- `f8c7e8a` feat(frontend): unify all menu modules into single mdm.ts

## 待处理
- 菜单仍有少量 fallback 到 route.name 的项（locale 键未注册）
- Vite chunk 缓存问题（硬刷新 Ctrl+Shift+R）

## 访问信息
- 新前端：http://localhost:3003 （admin / admin123）
- 后端：http://localhost:8080
- EMQX：http://localhost:18083 （admin/public）

## GitHub
- https://github.com/yangkai258/mdm-iot-platform
