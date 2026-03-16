# 前端Agent (qd) - 文档库

## 📁 文档库结构

```
docs/agent_qd/
├── projects/          # 项目文档
│   ├── requirements/  # 需求文档
│   ├── designs/       # 设计文档
│   ├── plans/         # 开发计划
│   └── reviews/       # 代码评审
├── technical/         # 技术文档
│   ├── architecture/  # 架构设计
│   ├── components/    # 组件文档
│   ├── apis/          # API文档
│   └── guides/        # 开发指南
├── learning/          # 学习文档
│   ├── tutorials/     # 教程文档
│   ├── notes/         # 学习笔记
│   └── resources/     # 学习资源
├── tools/             # 工具文档
│   ├── configurations/ # 配置文档
│   ├── scripts/       # 脚本文档
│   └── workflows/     # 工作流文档
└── best-practices/    # 最佳实践
    ├── coding/        # 编码规范
    ├── performance/   # 性能优化
    └── security/      # 安全规范
```

## 📋 文档模板

### 1. 前端项目初始化模板
```markdown
# 前端项目初始化文档

## 🎯 项目基本信息
- **项目名称**: 
- **技术栈**: 
- **负责人**: qd (前端Agent)
- **创建日期**: 
- **项目状态**: 初始化中

## 🛠️ 技术选型
### 核心框架
- **主框架**: [React/Vue/Angular]
- **版本**: 
- **选择理由**: 

### UI组件库
- **组件库**: [Ant Design/Element UI/Tailwind UI]
- **版本**: 
- **选择理由**: 

### 状态管理
- **状态库**: [Redux/Vuex/Pinia/MobX]
- **版本**: 
- **选择理由**: 

### 路由管理
- **路由库**: [React Router/Vue Router]
- **版本**: 
- **选择理由**: 

### 构建工具
- **打包工具**: [Webpack/Vite]
- **版本**: 
- **选择理由**: 

## 📁 项目结构
```
src/
├── assets/           # 静态资源
│   ├── images/      # 图片资源
│   ├── fonts/       # 字体文件
│   └── styles/      # 样式文件
├── components/       # 组件目录
│   ├── common/      # 通用组件
│   ├── layout/      # 布局组件
│   └── business/    # 业务组件
├── views/            # 页面组件
│   ├── home/        # 首页
│   ├── user/        # 用户相关
│   └── admin/       # 管理后台
├── router/           # 路由配置
│   ├── index.ts     # 路由入口
│   ├── routes.ts    # 路由定义
│   └── guards.ts    # 路由守卫
├── store/            # 状态管理
│   ├── modules/     # 模块状态
│   ├── actions/     # 动作定义
│   └── getters/     # 获取器
├── api/              # API接口
│   ├── index.ts     # API入口
│   ├── user.ts      # 用户接口
│   └── product.ts   # 产品接口
├── utils/            # 工具函数
│   ├── request.ts   # 请求封装
│   ├── validate.ts  # 验证工具
│   └── helpers.ts   # 辅助函数
├── types/            # 类型定义
│   ├── global.d.ts  # 全局类型
│   ├── api.d.ts     # API类型
│   └── component.d.ts # 组件类型
└── App.tsx           # 应用入口
```

## 🔧 开发环境配置

### 1. 环境要求
- **Node.js**: ≥ 16.0.0
- **npm**: ≥ 8.0.0
- **浏览器**: Chrome ≥ 90, Firefox ≥ 88, Safari ≥ 14

### 2. 安装依赖
```bash
# 安装项目依赖
npm install

# 安装开发依赖
npm install -D typescript eslint prettier

# 安装UI组件库
npm install antd
```

### 3. 开发脚本
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "format": "prettier --write src/",
    "test": "vitest",
    "test:coverage": "vitest --coverage"
  }
}
```

### 4. 配置文件
#### TypeScript配置 (tsconfig.json)
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

#### ESLint配置 (.eslintrc.js)
```javascript
module.exports = {
  env: {
    browser: true,
    es2020: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}
```

## 📝 开发规范

### 1. 代码规范
#### 命名规范
- **组件命名**: PascalCase (如: UserProfile)
- **文件命名**: kebab-case (如: user-profile.tsx)
- **变量命名**: camelCase (如: userName)
- **常量命名**: UPPER_SNAKE_CASE (如: API_URL)

#### 组件规范
```typescript
// 组件示例
import React from 'react';
import { User } from '@/types';

interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  onDelete?: (userId: string) => void;
}

const UserCard: React.FC<UserCardProps> = ({ user, onEdit, onDelete }) => {
  // 组件逻辑
  
  return (
    <div className="user-card">
      {/* 组件内容 */}
    </div>
  );
};

export default UserCard;
```

#### 样式规范
```css
/* BEM命名规范 */
.user-card {}
.user-card__header {}
.user-card__body {}
.user-card__footer {}
.user-card--active {}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-card {
    /* 移动端样式 */
  }
}
```

### 2. 状态管理规范
#### Redux示例
```typescript
// store/modules/user.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  userInfo: User | null;
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  userInfo: null,
  loading: false,
  error: null,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.userInfo = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
    },
  },
});

export const { setUser, setLoading, setError } = userSlice.actions;
export default userSlice.reducer;
```

### 3. API调用规范
```typescript
// api/user.ts
import request from '@/utils/request';
import { User, LoginParams, RegisterParams } from '@/types';

export const userApi = {
  // 用户登录
  login: (params: LoginParams): Promise<User> => {
    return request.post('/api/auth/login', params);
  },
  
  // 获取用户信息
  getUserInfo: (userId: string): Promise<User> => {
    return request.get(`/api/users/${userId}`);
  },
  
  // 更新用户信息
  updateUser: (userId: string, data: Partial<User>): Promise<User> => {
    return request.put(`/api/users/${userId}`, data);
  },
  
  // 删除用户
  deleteUser: (userId: string): Promise<void> => {
    return request.delete(`/api/users/${userId}`);
  },
};
```

## 🚀 部署配置

### 1. 构建配置
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['antd'],
        },
      },
    },
  },
});
```

### 2. Docker配置
```dockerfile
# Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. CI/CD配置
```yaml
# .github/workflows/deploy.yml
name: Deploy Frontend

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build
      run: npm run build
      
    - name: Deploy to Server
      uses: appleboy/scp-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        source: "dist/*"
        target: "/var/www/html"
```

## 📊 性能监控

### 1. 性能指标
- **首次内容绘制 (FCP)**: < 1.5s
- **最大内容绘制 (LCP)**: < 2.5s
- **首次输入延迟 (FID)**: < 100ms
- **累积布局偏移 (CLS)**: < 0.1

### 2. 监控工具
- **Lighthouse**: 性能评分和优化建议
- **Web Vitals**: 核心Web指标监控
- **Sentry**: 错误监控和性能追踪
- **Google Analytics**: 用户行为分析

### 3. 优化策略
1. **代码分割**: 路由级和组件级分割
2. **图片优化**: 压缩、懒加载、响应式图片
3. **缓存策略**: 静态资源长期缓存
4. **CDN加速**: 静态资源CDN分发

## 🔒 安全规范

### 1. 前端安全
- **XSS防护**: 输入验证、输出转义
- **CSRF防护**: Token验证、SameSite Cookie
- **CSP配置**: 内容安全策略
- **HTTPS强制**: 所有请求使用HTTPS

### 2. 数据安全
- **敏感信息**: 不在前端存储敏感数据
- **本地存储**: 合理使用localStorage和sessionStorage
- **加密传输**: 敏感数据加密传输
- **隐私保护**: 遵守隐私保护法规

## 📈 质量保证

### 1. 测试策略
- **单元测试**: 组件和工具函数测试
- **集成测试**: 组件交互测试
- **E2E测试**: 完整用户流程测试
- **性能测试**: 页面性能测试

### 2. 代码质量
- **代码审查**: Pull Request代码审查
- **自动化检查**: ESLint、Prettier、TypeScript
- **测试覆盖率**: ≥ 80%代码覆盖率
- **文档完整**: 组件和API文档完整

---
**文档版本**: v1.0  
**创建时间**: 2026-03-13  
**创建人**: qd (前端Agent)  
**更新记录**: 初始版本创建