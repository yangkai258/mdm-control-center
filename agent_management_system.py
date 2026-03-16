#!/usr/bin/env python3
"""
智能体协作项目管理平台 - 后端服务器
主管：主管智能体
团队：后端、前端、测试、产品、运维智能体
"""

import json
import time
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# 配置
PORT = 8005  # 使用8005端口，避免与MBTI项目冲突
DB_FILE = "agent_management.db"
SECRET_KEY = secrets.token_hex(32)

# 智能体定义
AGENTS = {
    "manager": {"name": "主管智能体", "module": "管理", "color": "#4A90E2"},
    "backend": {"name": "后端智能体", "module": "后端", "color": "#50E3C2"},
    "frontend": {"name": "前端智能体", "module": "前端", "color": "#B8E986"},
    "test": {"name": "测试智能体", "module": "测试", "color": "#F5A623"},
    "product": {"name": "产品智能体", "module": "产品", "color": "#BD10E0"},
    "ops": {"name": "运维智能体", "module": "运维", "color": "#FF6B6B"}
}

class Database:
    """数据库管理类"""
    
    @staticmethod
    def init():
        """初始化数据库"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 创建智能体表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            module TEXT NOT NULL,
            color TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建工作记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT NOT NULL,
            period TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed TEXT,  -- JSON数组
            in_progress TEXT,
            next_tasks TEXT, -- JSON数组
            challenges TEXT,
            notes TEXT,
            FOREIGN KEY (agent_id) REFERENCES agents (agent_id)
        )
        ''')
        
        # 创建项目表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 插入智能体数据
        for agent_id, agent_info in AGENTS.items():
            cursor.execute('''
            INSERT OR IGNORE INTO agents (agent_id, name, module, color)
            VALUES (?, ?, ?, ?)
            ''', (agent_id, agent_info["name"], agent_info["module"], agent_info["color"]))
        
        # 插入当前项目
        cursor.execute('''
        INSERT OR IGNORE INTO projects (name, description)
        VALUES (?, ?)
        ''', ("智能体协作项目管理平台", "可视化展示各智能体工作进展的实时系统"))
        
        conn.commit()
        conn.close()
        print(f"✅ 数据库初始化完成: {DB_FILE}")

class WorkRecord:
    """工作记录管理类"""
    
    @staticmethod
    def add_record(agent_id, period, completed, in_progress, next_tasks, challenges="", notes=""):
        """添加工作记录"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO work_records 
        (agent_id, period, completed, in_progress, next_tasks, challenges, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            agent_id,
            period,
            json.dumps(completed, ensure_ascii=False),
            in_progress,
            json.dumps(next_tasks, ensure_ascii=False),
            challenges,
            notes
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    @staticmethod
    def get_recent_records(limit=10):
        """获取最近的工作记录"""
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT wr.*, a.name as agent_name, a.module, a.color
        FROM work_records wr
        JOIN agents a ON wr.agent_id = a.agent_id
        ORDER BY wr.timestamp DESC
        LIMIT ?
        ''', (limit,))
        
        records = [dict(row) for row in cursor.fetchall()]
        
        # 解析JSON字段
        for record in records:
            if record['completed']:
                record['completed'] = json.loads(record['completed'])
            if record['next_tasks']:
                record['next_tasks'] = json.loads(record['next_tasks'])
        
        conn.close()
        return records
    
    @staticmethod
    def get_agent_records(agent_id, limit=5):
        """获取指定智能体的工作记录"""
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT wr.*, a.name as agent_name, a.module, a.color
        FROM work_records wr
        JOIN agents a ON wr.agent_id = a.agent_id
        WHERE wr.agent_id = ?
        ORDER BY wr.timestamp DESC
        LIMIT ?
        ''', (agent_id, limit))
        
        records = [dict(row) for row in cursor.fetchall()]
        
        # 解析JSON字段
        for record in records:
            if record['completed']:
                record['completed'] = json.loads(record['completed'])
            if record['next_tasks']:
                record['next_tasks'] = json.loads(record['next_tasks'])
        
        conn.close()
        return records

class AgentHandler:
    """智能体工作模拟器"""
    
    @staticmethod
    def simulate_work(agent_id, current_time):
        """模拟智能体工作并生成工作记录"""
        agent = AGENTS.get(agent_id)
        if not agent:
            return None
        
        # 生成工作周期标识
        period_start = current_time.replace(minute=(current_time.minute // 30) * 30, second=0, microsecond=0)
        period_end = period_start + timedelta(minutes=30)
        period = f"{period_start.strftime('%H:%M')}-{period_end.strftime('%H:%M')}"
        
        # 根据智能体类型生成不同的工作内容
        if agent_id == "manager":
            completed = [
                "协调各智能体工作分配",
                "监控项目整体进度",
                "解决跨智能体协作问题"
            ]
            in_progress = "准备第一次进度更新报告"
            next_tasks = [
                "收集各智能体工作成果",
                "更新项目管理软件展示",
                "调整任务优先级"
            ]
            
        elif agent_id == "backend":
            completed = [
                "分析后端需求和技术选型",
                "设计数据库表结构",
                "规划API接口规范"
            ]
            in_progress = "实现核心数据模型和API"
            next_tasks = [
                "完成数据库初始化脚本",
                "实现工作记录API",
                "添加数据验证逻辑"
            ]
            
        elif agent_id == "frontend":
            completed = [
                "分析UI/UX需求",
                "设计6模块布局方案",
                "规划组件库结构"
            ]
            in_progress = "创建HTML/CSS框架"
            next_tasks = [
                "实现实时更新显示",
                "添加时间线组件",
                "优化响应式设计"
            ]
            
        elif agent_id == "test":
            completed = [
                "制定测试策略和计划",
                "定义质量标准",
                "规划测试环境"
            ]
            in_progress = "设计测试用例模板"
            next_tasks = [
                "创建自动化测试框架",
                "准备测试数据",
                "设计质量报告模板"
            ]
            
        elif agent_id == "product":
            completed = [
                "分析用户需求和痛点",
                "规划核心功能模块",
                "设计用户工作流程"
            ]
            in_progress = "完善产品需求文档"
            next_tasks = [
                "创建用户故事和用例",
                "确定功能优先级",
                "设计产品路线图"
            ]
            
        elif agent_id == "ops":
            completed = [
                "分析系统架构需求",
                "设计部署方案",
                "规划监控策略"
            ]
            in_progress = "设计监控和日志系统"
            next_tasks = [
                "创建部署脚本",
                "实现系统监控",
                "规划性能优化"
            ]
        
        # 添加工作记录
        record_id = WorkRecord.add_record(
            agent_id=agent_id,
            period=period,
            completed=completed,
            in_progress=in_progress,
            next_tasks=next_tasks,
            challenges="暂无重大挑战",
            notes=f"自动生成的工作记录 - {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        return {
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "module": agent["module"],
            "color": agent["color"],
            "period": period,
            "timestamp": current_time.isoformat(),
            "completed": completed,
            "in_progress": in_progress,
            "next_tasks": next_tasks,
            "record_id": record_id
        }

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 设置CORS头
        self.send_cors_headers()
        
        if path == "/":
            self.serve_static_file("index.html")
        elif path == "/api/agents":
            self.get_agents()
        elif path == "/api/records":
            self.get_records()
        elif path == "/api/progress":
            self.get_progress()
        elif path == "/api/simulate":
            self.simulate_work()
        elif path.endswith(".html") or path.endswith(".css") or path.endswith(".js"):
            self.serve_static_file(path[1:])  # 移除前导斜杠
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        self.send_cors_headers()
        
        if path == "/api/records":
            self.add_record()
        else:
            self.send_error(404, "Not Found")
    
    def send_cors_headers(self):
        """发送CORS头"""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
    
    def serve_static_file(self, filename):
        """提供静态文件"""
        try:
            if filename == "index.html":
                content = self.generate_index_html()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            else:
                # 尝试读取文件
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                
                content_type = "text/plain"
                if filename.endswith(".html"):
                    content_type = "text/html"
                elif filename.endswith(".css"):
                    content_type = "text/css"
                elif filename.endswith(".js"):
                    content_type = "application/javascript"
                
                self.send_response(200)
                self.send_header("Content-type", f"{content_type}; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, f"File not found: {filename}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def generate_index_html(self):
        """生成首页HTML"""
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能体协作项目管理平台</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #f0f0f0;
        }}
        
        .header h1 {{
            color: #333;
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-top: 10px;
        }}
        
        .time-display {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            font-size: 1.1em;
            color: #555;
            border: 2px solid #e9ecef;
        }}
        
        .time-display .current-time {{
            font-weight: bold;
            color: #667eea;
            font-size: 1.3em;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .module-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            border: 2px solid #f0f0f0;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .module-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }}
        
        .module-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .module-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 15px;
        }}
        
        .module-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
            flex-grow: 1;
        }}
        
        .module-agent {{
            background: #f8f9fa;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            color: #666;
        }}
        
        .work-period {{
            background: #e9ecef;
            padding: 8px 15px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #495057;
        }}
        
        .work-content h4 {{
            color: #495057;
            margin: 15px 0 8px 0;
            font-size: 1.1em;
        }}
        
        .task-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .task-list li {{
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            align-items: center;
        }}
        
        .task-list li:before {{
            content: "✓";
            color: #28a745;
            margin-right: 10px;
            font-weight: bold;
        }}
        
        .in-progress {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #ffc107;
        }}
        
        .next-tasks {{
            background: #d1ecf1;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #17a2b8;
        }}
        
        .controls {{
            text-align: center;
            margin-top: 40px;
            padding-top: 30px;
            border-top: 3px solid #f0f0f0;
        }}
        
        .btn {{
            background: linear-gradient(90deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            margin: 0 10px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }}
        
        .btn:active {{
            transform: translateY(0);
        }}
        
        .btn-secondary {{
            background: #6c757d;
        }}
        
        .status-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #f8f9fa;
            padding: 15px 25px;
            border-radius: 10px;
            margin-top: 30px;
            font-size: 0.9em;
            color: #666;
        }}
        
        .status-item {{
            display: flex;
            align-items: center;
        }}
        
        .status-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .status-active {{ background: #28a745; }}
        .status-inactive {{ background: #dc3545; }}
        
        @media (max-width: 768px) {{
            .dashboard {{
                grid-template-columns: 1fr;
            }}
            
            .container {{
                padding: 15px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 智能体协作项目管理平台</h1>
            <div class="subtitle">实时展示6个智能体的工作进展 - 每30分钟更新</div>
        </div>
        
        <div class="time-display">
            当前时间: <span class="current-time" id="currentTime">加载中...</span> | 
            当前周期: <span id="currentPeriod">22:39-23:09</span> | 
            下次更新: <span id="nextUpdate">23:09</span>
        </div>
        
        <div class="dashboard" id="dashboard">
            <!-- 各模块内容将通过JavaScript动态加载 -->
        </div>
        
        <div class="controls">
            <button class="btn" onclick="simulateWork()">🔄 模拟智能体工作</button>
            <button class="btn btn-secondary" onclick="refreshData()">🔄 刷新数据</button>
            <button class="btn" onclick="exportReport()">📥 导出工作报告</button>
        </div>
        
        <div class="status-bar">
            <div class="status-item">
                <div class="status-dot status-active"></div>
                <span>6个智能体工作中</span>
            </div>
            <div class="status-item">
                <span>更新周期: 30分钟</span>
            </div>
            <div class="status-item">
                <span>记忆整理: 每4小时</span>
            </div>
            <div class="status-item">
                <span>服务器: <span id="serverStatus">运行中</span></span>
            </div>
        </div>
    </div>
    
    <script>
        // 全局变量
        let agentsData = [];
        let workRecords = [];
        
        // 页面加载时初始化
        window.addEventListener('load', function() {
            updateTimeDisplay();
            loadAgentsData();
            setInterval(updateTimeDisplay, 1000);
            setInterval(loadAgentsData, 30000); // 每30秒刷新一次
        });
        
        // 更新时间显示
        function updateTimeDisplay() {{
            const now = new Date();
            const timeStr = now.toLocaleString('zh-CN', {{
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }});
            
            document.getElementById('currentTime').textContent = timeStr;
            
            // 计算当前周期
            const minutes = now.getMinutes();
            const periodStart = new Date(now);
            periodStart.setMinutes(Math.floor(minutes / 30) * 30, 0, 0);
            
            const periodEnd = new Date(periodStart);
            periodEnd.setMinutes(periodStart.getMinutes() + 30);
            
            const periodStr = `${{periodStart.getHours().toString().padStart(2, '0')}}:${{periodStart.getMinutes().toString().padStart(2, '0')}}-${{periodEnd.getHours().toString().padStart(2, '0')}}:${{periodEnd.getMinutes().toString().padStart(2, '0')}}`;
            document.getElementById('currentPeriod').textContent = periodStr;
            
            // 计算下次更新时间
            const nextUpdate = new Date(periodEnd);
            document.getElementById('nextUpdate').textContent = `${{nextUpdate.getHours().toString().padStart(2, '0')}}:${{nextUpdate.getMinutes().toString().padStart(2, '0')}}`;
        }}
        
        // 加载智能体数据
        async function loadAgentsData() {{
            try {{
                // 加载智能体信息
                const agentsResponse = await fetch('/api/agents');
                agentsData = await agentsResponse.json();
                
                // 加载工作记录
                const recordsResponse = await fetch('/api/records?limit=20');
                workRecords = await recordsResponse.json();
                
                // 更新仪表板
                updateDashboard();
                
                // 更新服务器状态
                document.getElementById('serverStatus').textContent = '运行中';
                document.getElementById('serverStatus').style.color = '#28a745';
            }} catch (error) {{
                console.error('加载数据失败:', error);
                document.getElementById('serverStatus').textContent = '连接失败';
                document.getElementById('serverStatus').style.color = '#dc3545';
            }}
        }}
        
        // 更新仪表板
        function updateDashboard() {{
            const dashboard = document.getElementById('dashboard');
            dashboard.innerHTML = '';
            
            // 按模块分组记录
            const recordsByAgent = {{}};
            workRecords.forEach(record => {{
                if (!recordsByAgent[record.agent_id]) {{
                    recordsByAgent[record.agent_id] = [];
                }}
                recordsByAgent[record.agent_id].push(record);
            }});
            
            // 为每个智能体创建模块卡片
            agentsData.forEach(agent => {{
                const agentRecords = recordsByAgent[agent.agent_id] || [];
                const latestRecord = agentRecords[0]; // 最新的记录
                
                const card = document.createElement('div');
                card.className = 'module-card';
                card.style.borderColor = agent.color;
                
                card.innerHTML = `
                    <div class="module-header">
                        <div class="module-color" style="background: ${{agent.color}}"></div>
                        <div class="module-title">${{agent.module}}模块</div>
                        <div class="module-agent">${{agent.name}}</div>
                    </div>
                    
                    ${{latestRecord ? `
                        <div class="work-period">工作周期: ${{latestRecord.period}}</div>
                        
                        <div class="work-content">
                            <h4>✅ 已完成工作</h4>
                            <ul class="task-list">
                                ${{latestRecord.completed ? latestRecord.completed.map(task => `<li>${{task}}</li>`).join('') : '<li>暂无记录</li>'}}
                            </ul>
                            
                            <h4>🔄 进行中工作</h4>
                            <div class="in-progress">
                                ${{latestRecord.in_progress || '暂无记录'}}
                            </div>
                            
                            <h4>📅 后续工作安排</h4>
                            <div class="next-tasks">
                                ${{latestRecord.next_tasks ? latestRecord.next_tasks.map(task => `<div>• ${{task}}</div>`).join('') : '暂无安排'}}
                            </div>
                            
                            <div style="margin-top: 15px; color: #666; font-size: 0.9em;">
                                记录时间: ${{new Date(latestRecord.timestamp).toLocaleString('zh-CN')}}
                            </div>
                        </div>
                    ` : `
                        <div class="work-content">
                            <p style="color: #666; text-align: center; padding: 30px;">
                                等待${{agent.name}}提交工作记录...
                            </p>
                        </div>
                    `}}
                `;
                
                dashboard.appendChild(card);
            }});
        }}
        
        // 模拟智能体工作
        async function simulateWork() {{
            try {{
                const response = await fetch('/api/simulate');
                const result = await response.json();
                
                if (result.success) {{
                    alert('✅ 智能体工作模拟成功！已生成新的工作记录。');
                    loadAgentsData();
                }} else {{
                    alert('❌ 模拟失败: ' + result.message);
                }}
            }} catch (error) {{
                alert('❌ 请求失败: ' + error.message);
            }}
        }}
        
        // 刷新数据
        function refreshData() {{
            loadAgentsData();
            alert('🔄 数据已刷新！');
        }}
        
        // 导出工作报告
        function exportReport() {{
            const now = new Date();
            const dateStr = now.toISOString().split('T')[0];
            const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
            
            const report = {{
                export_time: now.toISOString(),
                agents: agentsData,
                records: workRecords,
                summary: {{
                    total_agents: agentsData.length,
                    total_records: workRecords.length,
                    latest_update: workRecords[0]?.timestamp || '无记录'
                }}
            }};
            
            const blob = new Blob([JSON.stringify(report, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `agent-work-report-${{dateStr}}-${{timeStr}}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            alert('📥 工作报告已导出！');
        }}
    </script>
</body>
</html>'''
    
    def get_agents(self):
        """获取智能体列表"""
        try:
            agents_list = []
            for agent_id, agent_info in AGENTS.items():
                agents_list.append({
                    "agent_id": agent_id,
                    "name": agent_info["name"],
                    "module": agent_info["module"],
                    "color": agent_info["color"]
                })
            
            self.send_json_response(200, agents_list)
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
    def get_records(self):
        """获取工作记录"""
        try:
            query = parse_qs(urlparse(self.path).query)
            limit = int(query.get("limit", [10])[0])
            
            records = WorkRecord.get_recent_records(limit)
            self.send_json_response(200, records)
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
    def get_progress(self):
        """获取项目进度"""
        try:
            # 获取各智能体的最新记录
            progress = {}
            for agent_id in AGENTS.keys():
                records = WorkRecord.get_agent_records(agent_id, 1)
                if records:
                    progress[agent_id] = {
                        "latest_record": records[0],
                        "total_records": len(WorkRecord.get_agent_records(agent_id, 100))
                    }
            
            self.send_json_response(200, {
                "total_agents": len(AGENTS),
                "active_agents": len(progress),
                "progress": progress,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
    def simulate_work(self):
        """模拟智能体工作"""
        try:
            current_time = datetime.now()
            results = []
            
            # 为每个智能体生成工作记录
            for agent_id in AGENTS.keys():
                if agent_id != "manager":  # 主管智能体不自动生成
                    result = AgentHandler.simulate_work(agent_id, current_time)
                    if result:
                        results.append(result)
            
            # 主管智能体生成管理记录
            manager_result = AgentHandler.simulate_work("manager", current_time)
            if manager_result:
                results.append(manager_result)
            
            self.send_json_response(200, {
                "success": True,
                "message": f"成功生成{len(results)}个智能体的工作记录",
                "results": results,
                "timestamp": current_time.isoformat()
            })
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
    def add_record(self):
        """添加工作记录"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            required_fields = ["agent_id", "period", "completed", "in_progress", "next_tasks"]
            for field in required_fields:
                if field not in data:
                    self.send_json_response(400, {"error": f"缺少必要字段: {field}"})
                    return
            
            record_id = WorkRecord.add_record(
                agent_id=data["agent_id"],
                period=data["period"],
                completed=data["completed"],
                in_progress=data["in_progress"],
                next_tasks=data["next_tasks"],
                challenges=data.get("challenges", ""),
                notes=data.get("notes", "")
            )
            
            self.send_json_response(201, {
                "success": True,
                "message": "工作记录添加成功",
                "record_id": record_id
            })
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})
    
    def send_json_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

def start_server():
    """启动服务器"""
    # 初始化数据库
    Database.init()
    
    # 创建服务器
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    
    print("=" * 60)
    print("🏢 智能体协作项目管理平台")
    print("=" * 60)
    print(f"📍 服务器地址: http://localhost:{PORT}")
    print(f"📁 数据库文件: {DB_FILE}")
    print(f"👥 智能体数量: {len(AGENTS)}个")
    print(f"⏰ 更新周期: 每30分钟")
    print(f"🧠 记忆整理: 每4小时")
    print("=" * 60)
    print("🚀 服务器启动中...")
    print("📊 访问 http://localhost:8005 查看实时工作看板")
    print("🔄 使用模拟功能生成智能体工作记录")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器错误: {e}")

if __name__ == "__main__":
    start_server()
