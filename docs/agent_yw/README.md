# 运维Agent (yw) - 文档库

## 📁 文档库结构

```
docs/agent_yw/
├── deployments/       # 部署文档
│   ├── procedures/   # 部署流程
│   ├── configurations/ # 配置文档
│   ├── scripts/      # 部署脚本
│   └── rollbacks/    # 回滚方案
├── monitoring/        # 监控文档
│   ├── dashboards/   # 监控面板
│   ├── alerts/       # 告警配置
│   ├── metrics/      # 监控指标
│   └── tools/        # 监控工具
├── security/          # 安全文档
│   ├── policies/     # 安全策略
│   ├── audits/       # 安全审计
│   ├── vulnerabilities/ # 漏洞管理
│   └── compliance/   # 合规文档
├── infrastructure/    # 基础设施
│   ├── servers/      # 服务器配置
│   ├── networks/     # 网络配置
│   ├── storage/      # 存储配置
│   └── backups/      # 备份方案
├── troubleshooting/   # 故障排查
│   ├── procedures/   # 故障处理流程
│   ├── knowledge/    # 故障知识库
│   ├── incidents/    # 故障事件记录
│   └── postmortems/  # 故障复盘
└── templates/        # 文档模板
    ├── deployment/   # 部署文档模板
    ├── monitoring/   # 监控文档模板
    ├── security/     # 安全文档模板
    └── incident/     # 故障报告模板
```

## 📋 核心文档模板

### 1. 系统部署文档模板
```markdown
# 系统部署文档

## 🎯 部署概述
- **系统名称**: 
- **部署版本**: v1.0.0
- **部署负责人**: yw (运维Agent)
- **部署时间**: 
- **部署环境**: [开发/测试/生产]

## 🛠️ 部署环境

### 1. 服务器配置
| 服务器 | 角色 | 配置 | IP地址 | 状态 |
|--------|------|------|--------|------|
| web-01 | Web服务器 | 4核8G 100GB | 192.168.1.101 | 就绪 |
| app-01 | 应用服务器 | 8核16G 200GB | 192.168.1.102 | 就绪 |
| db-01 | 数据库服务器 | 16核32G 500GB | 192.168.1.103 | 就绪 |
| redis-01 | 缓存服务器 | 4核8G 50GB | 192.168.1.104 | 就绪 |

### 2. 软件版本
| 软件 | 版本 | 安装路径 | 配置状态 |
|------|------|----------|----------|
| **操作系统** | Ubuntu 22.04 LTS | - | 已配置 |
| **Nginx** | 1.22.0 | /usr/local/nginx | 已配置 |
| **Node.js** | 18.16.0 | /usr/local/node | 已安装 |
| **MySQL** | 8.0.33 | /usr/local/mysql | 已配置 |
| **Redis** | 7.0.11 | /usr/local/redis | 已配置 |
| **Docker** | 24.0.2 | /usr/bin/docker | 已安装 |

### 3. 网络配置
- **域名**: app.example.com
- **SSL证书**: Let's Encrypt (自动续期)
- **负载均衡**: Nginx + Keepalived
- **防火墙**: UFW (只开放必要端口)
- **网络拓扑**: 
  ```
  互联网 → 负载均衡器 → Web服务器 → 应用服务器 → 数据库
                           ↓
                        缓存服务器
  ```

## 🔧 部署步骤

### 阶段1: 环境准备 (1小时)
```bash
# 1. 系统更新和安全配置
sudo apt update && sudo apt upgrade -y
sudo apt install -y ufw fail2ban

# 2. 配置防火墙
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# 3. 创建部署用户
sudo useradd -m -s /bin/bash deployer
sudo usermod -aG sudo deployer
```

### 阶段2: 软件安装 (2小时)
```bash
# 1. 安装Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 2. 安装MySQL
sudo apt install -y mysql-server
sudo mysql_secure_installation

# 3. 安装Redis
sudo apt install -y redis-server
sudo systemctl enable redis-server

# 4. 安装Nginx
sudo apt install -y nginx
sudo systemctl enable nginx
```

### 阶段3: 应用部署 (1小时)
```bash
# 1. 创建应用目录
sudo mkdir -p /var/www/app
sudo chown -R deployer:deployer /var/www/app

# 2. 拉取代码
cd /var/www/app
git clone https://github.com/example/app.git .
git checkout v1.0.0

# 3. 安装依赖
npm ci --only=production

# 4. 配置环境变量
cp .env.example .env
nano .env  # 编辑配置文件
```

### 阶段4: 数据库部署 (30分钟)
```sql
-- 创建数据库
CREATE DATABASE app_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户并授权
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON app_prod.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;

-- 导入数据
mysql -u app_user -p app_prod < database/schema.sql
mysql -u app_user -p app_prod < database/seed.sql
```

### 阶段5: 服务配置 (30分钟)
```nginx
# /etc/nginx/sites-available/app
server {
    listen 80;
    server_name app.example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # SSL配置 (Certbot自动配置)
}
```

```bash
# 创建systemd服务
sudo nano /etc/systemd/system/app.service

[Unit]
Description=App Service
After=network.target

[Service]
Type=simple
User=deployer
WorkingDirectory=/var/www/app
Environment=NODE_ENV=production
ExecStart=/usr/bin/node src/index.js
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 阶段6: 启动服务 (15分钟)
```bash
# 1. 启用Nginx配置
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 2. 启动应用服务
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl start app.service

# 3. 配置SSL证书
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d app.example.com
```

### 阶段7: 验证部署 (15分钟)
```bash
# 1. 检查服务状态
sudo systemctl status app.service
sudo systemctl status nginx
sudo systemctl status mysql

# 2. 检查应用健康
curl -f http://localhost:3000/health
curl -f https://app.example.com/health

# 3. 检查日志
sudo journalctl -u app.service -f
sudo tail -f /var/log/nginx/access.log
```

## 📊 监控配置

### 1. 监控指标
| 指标类型 | 具体指标 | 告警阈值 | 监控工具 |
|----------|----------|----------|----------|
| **系统指标** | CPU使用率 | > 80% 持续5分钟 | Prometheus |
| | 内存使用率 | > 85% | Node Exporter |
| | 磁盘使用率 | > 90% | Node Exporter |
| | 系统负载 | > 5 (1分钟平均) | Node Exporter |
| **应用指标** | 响应时间 | P95 > 500ms | Blackbox Exporter |
| | 错误率 | > 1% | Application |
| | 请求量 | 异常波动 | Nginx Logs |
| | 服务状态 | HTTP状态码 != 200 | Blackbox Exporter |
| **业务指标** | 用户活跃 | 日活下降30% | Custom Metrics |
| | 交易量 | 异常下降 | Business Logic |
| | 收入指标 | 异常波动 | Business Logic |

### 2. 告警规则
```yaml
# prometheus/rules/alerts.yml
groups:
  - name: system_alerts
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "高CPU使用率"
          description: "实例 {{ $labels.instance }} CPU使用率持续5分钟超过80%"
          
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "高内存使用率"
          description: "实例 {{ $labels.instance }} 内存使用率超过85%"
          
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "服务下线"
          description: "服务 {{ $labels.job }} 在实例 {{ $labels.instance }} 上已下线"
```

### 3. 监控面板
```json
// grafana/dashboards/app-dashboard.json
{
  "dashboard": {
    "title": "应用监控面板",
    "panels": [
      {
        "title": "系统资源",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg by(instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{instance}} CPU使用率"
          },
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
            "legendFormat": "{{instance}} 内存使用率"
          }
        ]
      },
      {
        "title": "应用性能",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P95响应时间"
          },
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
            "legendFormat": "错误率"
          }
        ]
      }
    ]
  }
}
```

## 🔒 安全配置

### 1. 系统安全
```bash
# 1. 系统更新
sudo apt update && sudo apt upgrade -y
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades

# 2. SSH安全配置
sudo nano /etc/ssh/sshd_config
# 修改以下配置:
Port 2222                      # 修改SSH端口
PermitRootLogin no            # 禁止root登录
PasswordAuthentication no     # 禁用密码认证
MaxAuthTries 3                # 最大尝试次数
ClientAliveInterval 300       # 客户端活跃间隔
ClientAliveCountMax 2         # 客户端活跃计数

# 3. 防火墙配置
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp       # SSH
sudo ufw allow 80/tcp         # HTTP
sudo ufw allow 443/tcp        # HTTPS
sudo ufw enable

# 4. Fail2ban配置
sudo apt install -y fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

### 2. 应用安全
```nginx
# Nginx安全配置
server {
    # 隐藏Nginx版本
    server_tokens off;
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # CSP策略
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;
    
    # 限制请求大小
    client_max_body_size 10m;
    
    # 限制请求速率
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://app_backend;
    }
}
```

### 3. 数据安全
```bash
# 1. 数据库备份
#!/bin/bash
# backup-mysql.sh
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="app_prod"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u root -p$DB_PASSWORD $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# 保留最近7天备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

# 上传到云存储
aws s3 sync $BACKUP_DIR s3://backup-bucket/mysql/ --delete

# 2. 文件备份
rsync -avz --delete /var/www/app/ backup-server:/backup/app/
```

## 🚨 故障处理

### 1. 故障处理流程
```mermaid
graph TD
    A[故障发现] --> B[故障确认]
    B --> C{故障等级}
    C -->|P0 严重| D[紧急响应]
    C -->|P1 重要| E[优先处理]
    C -->|P2 一般| F[计划处理]
    D --> G[故障恢复]
    E --> G
    F --> G
    G --> H[故障分析]
    H --> I[改进措施]
    I --> J[流程优化]
```

### 2. 常见故障处理
#### 数据库连接失败
```bash
# 1. 检查数据库服务状态
sudo systemctl status mysql

# 2. 检查数据库连接
mysql -u app_user -p -e "SHOW STATUS LIKE 'Threads_connected';"

# 3. 检查连接数限制
mysql -u root -p -e "SHOW VARIABLES LIKE 'max_connections';"

# 4. 检查磁盘空间
df -h /var/lib/mysql

# 5. 检查数据库日志
sudo tail -f /var/log/mysql/error.log
```

#### 应用响应缓慢
```bash
# 1. 检查系统资源
top -c
free -h
df -h

# 2. 检查应用日志
sudo journalctl -u app.service --since "10 minutes ago"

# 3. 检查网络连接
netstat -an | grep :3000
ss -tlnp | grep :3000

# 4. 检查数据库性能
mysql -u root -p -e "SHOW PROCESSLIST;"
mysql -u root -p -e "SHOW ENGINE INNODB STATUS\G"
```

#### 服务不可用
```bash
# 1. 快速恢复步骤
sudo systemctl restart app.service
sudo systemctl restart nginx

# 2. 检查端口监听
sudo lsof -i :3000
sudo lsof -i :80
sudo lsof -i :443

# 3. 检查防火墙
sudo ufw status verbose

# 4. 检查DNS解析
nslookup app.example.com
dig app.example.com

# 5. 回滚到上一个版本
cd /var/www/app
git log --oneline -5
git reset --hard <previous_commit>
sudo systemctl restart app.service
```

### 3. 故障报告模板
```markdown
# 故障报告

## 故障基本信息
- **故障标题**: 
- **故障等级**: [P0/P1/P2]
- **发生时间**: 
- **恢复时间**: 
- **影响范围**: 
- **报告人**: yw (运维Agent)

## 故障描述
[详细描述故障现象]

## 故障时间线
| 时间 | 事件 | 处理人 |
|------|------|--------|
| 10:00 | 监控告警触发 | 系统自动 |
| 10:02 | 值班人员确认故障 | yw |
| 10:05 | 开始故障排查 | yw |
| 10:20 | 定位故障原因 | yw |
| 10:30 | 实施修复方案 | yw |
| 10:35 | 验证修复效果 | yw |
| 10:40 | 故障恢复 | yw |

## 根本原因分析
[分析故障的根本原因]

## 影响评估
- **用户影响**: 
- **业务影响**: 
- **财务影响**: 
- **声誉影响**: 

## 处理过程
[详细描述处理过程]

## 改进措施
### 短期措施 (1周内)
1. 
2. 
3. 

### 中期措施 (1个月内)
1. 
2. 
3. 

### 长期措施 (3个月内)
1. 
2. 
3. 

## 经验教训
1. 
2. 
3. 

## 责任人跟进
| 改进措施 | 责任人 | 完成时间 | 状态 |
|----------|--------|----------|------|
| | | | |
| | | | |
```

---
**文档版本**: v1.0  
**创建时间**: 2026-03-13  
**创建人**: yw (运维Agent)  
**更新记录**: 初始版本创建