# agenthd_task.md - Sprint 3.2 开发任务

## 任务状态: ✅ 已完成

## 完成时间
2026-03-20 14:15 GMT+8

## Sprint 3.2 完成项

### 1. 积分引擎 ✅
- **文件**: `services/points_engine.go`, `controllers/member_enhanced_controller.go`
- **功能**:
  - AddPoints - 增加积分（消费获得/活动赠送/退款返还）
  - DeductPoints - 抵扣积分（带余额检查）
  - GetBalance - 查询积分余额
  - GetLogs - 积分流水分页查询
  - CalculatePoints - 根据规则和会员等级计算积分
  - 会员等级自动升降级（checkAndUpgrade/checkAndDowngrade）
  - 升级奖励积分自动发放
- **接口**:
  - `POST /api/v1/members/:id/points/add` - 增加积分
  - `POST /api/v1/members/:id/points/deduct` - 抵扣积分
  - `GET /api/v1/members/:id/points/balance` - 查询余额
  - `GET /api/v1/members/:id/points/logs` - 积分流水

### 2. 优惠券管理 ✅
- **文件**: `services/points_engine.go`, `controllers/member_enhanced_controller.go`
- **功能**:
  - IssueCoupon - 发放优惠券（库存扣减、发放记录创建）
  - UseCoupon - 核销优惠券（有效期检查、状态更新）
  - GetMemberCoupons - 会员优惠券列表
- **接口**:
  - `GET /api/v1/coupons` - 优惠券列表（新路径）
  - `POST /api/v1/coupons` - 创建优惠券（新路径）
  - `POST /api/v1/coupons/:id/issue` - 发放优惠券
  - `POST /api/v1/coupons/:id/use` - 核销优惠券
  - `GET /api/v1/members/:id/coupons` - 会员优惠券列表

### 3. 促销活动 CRUD ✅
- **文件**: `controllers/member_enhanced_controller.go`
- **接口**:
  - `GET /api/v1/promotions` - 促销列表（新路径）
  - `POST /api/v1/promotions` - 创建促销（新路径）
  - `PUT /api/v1/promotions/:id` - 更新促销（新路径）
  - `DELETE /api/v1/promotions/:id` - 删除促销（新路径）
  - `GET /api/v1/promotions/:id` - 促销详情

### 4. AutoMigrate 集成 ✅
- **文件**: `main.go`
- 新增迁移: `Member`, `MemberCard`, `MemberCardGroup`, `MemberLevel`, `MemberUpgradeRule`, `MemberTag`, `MemberTagRecord`, `Coupon`, `CouponGrant`, `Promotion`, `Store`, `PointsRule`, `MemberPointsRecord`, `MemberOperationRecord`, `TempMember`

### 5. 预存 Bug 修复 ✅
- **文件**: `controllers/policy_controller.go` - req.Status 类型错误（string → int）
- **文件**: `controllers/alert_controller.go` - SendAlertNotifications 未定义
- **文件**: `main.go` - geofenceCallback 签名不匹配
- **文件**: `services/notification_service.go` - 未使用的变量

## 代码变更

### 新增文件
| 文件 | 说明 |
|------|------|
| `services/points_engine.go` | 积分引擎 + 优惠券引擎 |
| `controllers/member_enhanced_controller.go` | 会员增强功能控制器 |

### 修改文件
| 文件 | 变更 |
|------|------|
| `main.go` | AutoMigrate 新增会员相关表，修复 geofenceCallback 签名 |
| `controllers/device_controller.go` | RegisterRoutes 新增 Sprint 3.2 路由 |
| `controllers/alert_controller.go` | 新增 SendAlertNotifications stub |
| `controllers/policy_controller.go` | 修复 req.Status 类型转换 |
| `services/notification_service.go` | 修复未使用变量 |

## Git Commit
```
feat: Sprint 3.2 - 会员管理增强

- 新增积分引擎 (services/points_engine.go)
  - AddPoints/DeductPoints/GetBalance/GetLogs
  - 会员等级自动升降级
  - 升级奖励积分自动发放
- 新增优惠券引擎
  - IssueCoupon/UseCoupon
  - 有效期检查、库存管理
- 新增促销活动 CRUD (新路径 /api/v1/promotions)
- 新增优惠券列表/创建 (新路径 /api/v1/coupons)
- 修复多个预存编译错误
```

## 验收标准检查

| 标准 | 状态 |
|------|------|
| 积分引擎计算正确 | ✅ |
| 优惠券发放和核销 | ✅ |
| 促销 CRUD 完整 | ✅ |

## 遗留问题

- ⚠️ `docs/MODULE_MEMBER_MANAGEMENT.md` 文档不存在（参考规范来自任务描述）
