# Agent QD - 前端开发任务

## 你是高级前端开发工程师 (agentqd)
你的任务是使用 Vue 3 (Composition API) + TypeScript + Arco Design 构建 MDM 管控台页面。

## UI 框架变更通知
**我们决定弃用 Element Plus，全量采用 Arco Design Vue (@arco-design/web-vue) 作为 UI 框架。**

## 我们需要一个"设备大盘"页面
供管理员实时查看全球 M5Stack 设备的在线状态和基本信息。

## 请输出一个完整的单文件组件 (DeviceDashboard.vue)

### 具体要求：

1. **整体布局**
   - 使用 a-layout 结构
   - 侧边栏展示菜单
   - 主区域使用 a-card 包裹设备列表

2. **数据表格**
   - 使用 a-table

3. **"在线状态"列**
   - 使用 a-badge 组件
   - status="processing" 代表在线
   - status="danger" 代表离线

4. **"电量"列**
   - 使用 a-progress 的线条模式
   - 根据数值动态调整颜色（低于20%显示红色）

5. **操作项**
   - 每一行添加一个"指令控制"按钮
   - 点击弹出 a-drawer（抽屉）
   - 用于发送手动指令

6. **统计看板**
   - 页面顶部使用 a-grid 和 a-statistic 组件
   - 展示：设备总数、在线数、警告数
   - 配上相应的图标（icon-robot, icon-check-circle）

7. **核心逻辑**
   - 在 onMounted 中使用 Axios 请求 /api/v1/devices/list 获取初始数据

8. **实时刷新**
   - 编写一个基于 setInterval 的轮询函数（或预留 WebSocket 接收逻辑）
   - 每隔 10 秒刷新一次列表中的"在线状态"和"电量"字段

9. **分页支持**
   - 支持 page, pageSize 分页参数

10. **筛选支持**
    - 支持 status 筛选

## 约束
- 严格使用 <script setup lang="ts"> 语法
- 为设备对象定义清晰的 interface Device {...}
- UI 布局力求简洁专业
- 保持 Arco Design 的默认深蓝色系风格
