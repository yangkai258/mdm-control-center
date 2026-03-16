#!/usr/bin/env python3
"""
主管Agent巡检系统
每1小时巡检其他agent是否空闲，如果空闲则安排下一项工作
"""

import time
import json
import os
from datetime import datetime, timedelta
import subprocess
import sys

class AgentStatus:
    """Agent状态类"""
    def __init__(self, name, role, current_task=None, status="idle", last_check=None):
        self.name = name
        self.role = role
        self.current_task = current_task
        self.status = status  # idle, busy, blocked, completed
        self.last_check = last_check or datetime.now()
        self.next_task = None
        self.performance_metrics = {
            "tasks_completed": 0,
            "avg_completion_time": 0,
            "success_rate": 1.0
        }
    
    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "current_task": self.current_task,
            "status": self.status,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "next_task": self.next_task,
            "performance": self.performance_metrics
        }

class SupervisorAgent:
    """主管Agent类"""
    def __init__(self):
        self.agents = {}
        self.task_queue = []
        self.completed_tasks = []
        self.check_interval = 3600  # 1小时
        self.last_check_time = datetime.now()
        self.status_file = "agent_status.json"
        self.task_history_file = "task_history.json"
        
        # 初始化agents
        self._initialize_agents()
        
    def _initialize_agents(self):
        """初始化agent团队"""
        self.agents = {
            "qd": AgentStatus("qd", "前端开发Agent", status="idle"),
            "hd": AgentStatus("hd", "后端开发Agent", status="idle"),
            "cs": AgentStatus("cs", "测试Agent", status="idle"),
            "cp": AgentStatus("cp", "产品Agent", status="busy", current_task="社交功能规划"),
            "yw": AgentStatus("yw", "运维Agent", status="idle"),
        }
        
        # 加载历史状态
        self._load_status()
    
    def _load_status(self):
        """加载agent状态"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for agent_id, agent_data in data.items():
                        if agent_id in self.agents:
                            self.agents[agent_id].last_check = datetime.fromisoformat(agent_data.get("last_check"))
                            self.agents[agent_id].performance_metrics = agent_data.get("performance", {})
        except Exception as e:
            print(f"加载状态失败: {e}")
    
    def _save_status(self):
        """保存agent状态"""
        try:
            data = {agent_id: agent.to_dict() for agent_id, agent in self.agents.items()}
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存状态失败: {e}")
    
    def check_agent_status(self):
        """检查所有agent状态"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始巡检agent状态...")
        
        current_time = datetime.now()
        
        # 检查每个agent的状态
        for agent_id, agent in self.agents.items():
            print(f"\n检查 {agent.role} ({agent_id}):")
            print(f"  当前状态: {agent.status}")
            print(f"  当前任务: {agent.current_task or '无'}")
            print(f"  上次检查: {agent.last_check.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 判断是否空闲
            if agent.status == "idle":
                print(f"  {agent.role} 空闲，准备分配任务...")
                self._assign_task(agent_id)
            elif agent.status == "busy":
                # 检查任务是否超时（假设任务最长8小时）
                time_diff = (current_time - agent.last_check).total_seconds()
                if time_diff > 28800:  # 8小时
                    print(f"  {agent.role} 任务可能超时，需要检查")
                    self._check_task_progress(agent_id)
            elif agent.status == "completed":
                print(f"  {agent.role} 任务已完成")
                self._record_completion(agent_id)
    
    def _assign_task(self, agent_id):
        """为空闲agent分配任务"""
        agent = self.agents[agent_id]
        
        # 根据agent角色分配任务
        tasks = self._get_available_tasks(agent.role)
        
        if tasks:
            task = tasks[0]  # 分配第一个可用任务
            agent.current_task = task["name"]
            agent.status = "busy"
            agent.last_check = datetime.now()
            
            print(f"  🎯 分配任务: {task['name']}")
            print(f"  📝 任务描述: {task['description']}")
            print(f"  ⏱️ 预计时间: {task['estimated_time']}")
            
            # 记录到任务队列
            self.task_queue.append({
                "agent": agent_id,
                "task": task["name"],
                "assigned_time": datetime.now().isoformat(),
                "status": "assigned"
            })
        else:
            print(f"  ℹ️ 暂无适合 {agent.role} 的任务")
    
    def _get_available_tasks(self, role):
        """根据角色获取可用任务"""
        # MBTI测试系统开发任务池
        task_pool = {
            "前端开发Agent": [
                {
                    "name": "社交分享界面开发",
                    "description": "开发用户分享测试结果的界面，包括分享按钮、分享卡片、社交媒体集成",
                    "estimated_time": "4小时",
                    "priority": "high",
                    "skills": ["HTML", "CSS", "JavaScript", "响应式设计"]
                },
                {
                    "name": "好友对比功能界面",
                    "description": "开发好友MBTI类型对比界面，包括对比图表、相似度分析、建议",
                    "estimated_time": "6小时",
                    "priority": "medium",
                    "skills": ["图表库", "数据可视化", "UI设计"]
                },
                {
                    "name": "社区功能界面",
                    "description": "开发用户社区界面，包括帖子列表、评论、点赞、用户资料",
                    "estimated_time": "8小时",
                    "priority": "low",
                    "skills": ["前端框架", "状态管理", "组件设计"]
                }
            ],
            "后端开发Agent": [
                {
                    "name": "社交分享API开发",
                    "description": "开发分享相关的API接口，包括生成分享链接、分享统计、分享内容",
                    "estimated_time": "3小时",
                    "priority": "high",
                    "skills": ["Python", "Flask", "REST API", "数据库"]
                },
                {
                    "name": "好友对比数据API",
                    "description": "开发好友对比相关的API，包括用户关系管理、对比算法、数据查询",
                    "estimated_time": "5小时",
                    "priority": "medium",
                    "skills": ["算法", "数据库设计", "API设计"]
                },
                {
                    "name": "社区功能API",
                    "description": "开发社区功能相关的API，包括帖子管理、评论系统、用户互动",
                    "estimated_time": "7小时",
                    "priority": "low",
                    "skills": ["后端架构", "消息队列", "缓存"]
                }
            ],
            "测试Agent": [
                {
                    "name": "社交功能测试",
                    "description": "测试社交分享、好友对比、社区功能的所有用例",
                    "estimated_time": "4小时",
                    "priority": "high",
                    "skills": ["功能测试", "集成测试", "用户体验测试"]
                },
                {
                    "name": "性能压力测试",
                    "description": "对社交功能进行性能测试和压力测试，确保系统稳定性",
                    "estimated_time": "3小时",
                    "priority": "medium",
                    "skills": ["性能测试", "压力测试", "监控"]
                },
                {
                    "name": "兼容性测试扩展",
                    "description": "扩展设备兼容性测试，覆盖更多iOS和Android设备",
                    "estimated_time": "5小时",
                    "priority": "low",
                    "skills": ["兼容性测试", "设备测试", "自动化测试"]
                }
            ],
            "产品Agent": [
                {
                    "name": "社交功能需求细化",
                    "description": "细化社交功能的需求文档，包括用户故事、功能规格、验收标准",
                    "estimated_time": "3小时",
                    "priority": "high",
                    "skills": ["需求分析", "产品设计", "文档编写"]
                },
                {
                    "name": "用户反馈分析",
                    "description": "分析用户对新功能的反馈，提出改进建议和优化方案",
                    "estimated_time": "2小时",
                    "priority": "medium",
                    "skills": ["数据分析", "用户研究", "产品优化"]
                },
                {
                    "name": "竞品分析",
                    "description": "分析竞品的社交功能，提取最佳实践和改进点",
                    "estimated_time": "4小时",
                    "priority": "low",
                    "skills": ["市场分析", "竞品研究", "策略规划"]
                }
            ],
            "运维Agent": [
                {
                    "name": "服务器性能监控优化",
                    "description": "优化服务器性能监控系统，增加更多指标和告警",
                    "estimated_time": "3小时",
                    "priority": "high",
                    "skills": ["监控", "运维", "性能优化"]
                },
                {
                    "name": "数据库性能优化",
                    "description": "优化数据库查询性能，建立索引，优化表结构",
                    "estimated_time": "4小时",
                    "priority": "medium",
                    "skills": ["数据库", "性能调优", "SQL优化"]
                },
                {
                    "name": "部署自动化",
                    "description": "实现自动化部署流程，减少人工干预",
                    "estimated_time": "5小时",
                    "priority": "low",
                    "skills": ["自动化", "部署", "CI/CD"]
                }
            ]
        }
        
        return task_pool.get(role, [])
    
    def _check_task_progress(self, agent_id):
        """检查任务进度"""
        agent = self.agents[agent_id]
        print(f"  🔍 检查 {agent.role} 的任务进度: {agent.current_task}")
        
        # 这里可以添加实际检查任务进度的逻辑
        # 例如：检查代码提交、测试结果、文档更新等
        
        # 模拟进度检查
        import random
        progress = random.randint(50, 90)
        print(f"  📊 任务进度: {progress}%")
        
        if progress >= 90:
            print(f"  ⏳ 任务即将完成，预计剩余时间: 30分钟")
        elif progress >= 70:
            print(f"  ⏳ 任务进行中，预计剩余时间: 2小时")
        else:
            print(f"  ⏳ 任务进行中，预计剩余时间: 4小时")
    
    def _record_completion(self, agent_id):
        """记录任务完成"""
        agent = self.agents[agent_id]
        
        # 更新性能指标
        agent.performance_metrics["tasks_completed"] += 1
        
        # 添加到完成列表
        self.completed_tasks.append({
            "agent": agent_id,
            "task": agent.current_task,
            "completion_time": datetime.now().isoformat(),
            "status": "completed"
        })
        
        # 重置agent状态
        agent.current_task = None
        agent.status = "idle"
        
        print(f"  ✅ 已记录 {agent.role} 的任务完成")
    
    def generate_report(self):
        """生成巡检报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "agents_status": {agent_id: agent.to_dict() for agent_id, agent in self.agents.items()},
            "idle_agents": [agent_id for agent_id, agent in self.agents.items() if agent.status == "idle"],
            "busy_agents": [agent_id for agent_id, agent in self.agents.items() if agent.status == "busy"],
            "task_queue": self.task_queue,
            "completed_tasks": self.completed_tasks[-10:]  # 最近10个完成的任务
        }
        
        # 保存报告
        report_file = f"supervisor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📋 巡检报告已生成: {report_file}")
        return report_file
    
    def run_hourly_check(self):
        """运行每小时巡检"""
        while True:
            current_time = datetime.now()
            time_since_last_check = (current_time - self.last_check_time).total_seconds()
            
            if time_since_last_check >= self.check_interval:
                print(f"\n{'='*60}")
                print(f"🕐 开始每小时巡检 - {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print('='*60)
                
                self.check_agent_status()
                self.generate_report()
                self._save_status()
                
                self.last_check_time = current_time
                
                print(f"\n✅ 巡检完成，下次巡检时间: {(current_time + timedelta(seconds=self.check_interval)).strftime('%H:%M:%S')}")
                print('='*60)
            
            # 等待1分钟再检查
            time.sleep(60)
    
    def run_once(self):
        """运行单次巡检"""
        print(f"\n{'='*60}")
        print(f"🕐 运行单次巡检 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print('='*60)
        
        self.check_agent_status()
        report_file = self.generate_report()
        self._save_status()
        
        print(f"\n✅ 单次巡检完成")
        print('='*60)
        
        return report_file

def main():
    """主函数"""
    supervisor = SupervisorAgent()
    
    print("主管Agent巡检系统启动")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"巡检间隔: 1小时")
    print(f"管理Agent数量: {len(supervisor.agents)}")
    
    # 运行单次巡检
    supervisor.run_once()
    
    # 如果要运行持续巡检，取消下面的注释
    # print("\n开始持续巡检（每小时一次）...")
    # supervisor.run_hourly_check()

if __name__ == "__main__":
    main()