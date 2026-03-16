#!/usr/bin/env python3
"""
简化版主管Agent巡检系统
"""

import time
import json
import os
from datetime import datetime, timedelta

class SupervisorAgent:
    def __init__(self):
        self.agents = {
            "qd": {"name": "前端开发Agent", "status": "idle", "current_task": None},
            "hd": {"name": "后端开发Agent", "status": "idle", "current_task": None},
            "cs": {"name": "测试Agent", "status": "idle", "current_task": None},
            "cp": {"name": "产品Agent", "status": "busy", "current_task": "社交功能规划"},
            "yw": {"name": "运维Agent", "status": "idle", "current_task": None},
        }
        self.task_queue = []
        
    def check_status(self):
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始巡检agent状态")
        print("=" * 60)
        
        idle_count = 0
        busy_count = 0
        
        for agent_id, agent in self.agents.items():
            print(f"\n{agent['name']} ({agent_id}):")
            print(f"  状态: {agent['status']}")
            print(f"  任务: {agent['current_task'] or '无'}")
            
            if agent['status'] == 'idle':
                idle_count += 1
                print(f"  -> 空闲，准备分配任务")
                self.assign_task(agent_id)
            elif agent['status'] == 'busy':
                busy_count += 1
                print(f"  -> 忙碌中: {agent['current_task']}")
        
        print(f"\n" + "=" * 60)
        print(f"统计: 空闲 {idle_count}个, 忙碌 {busy_count}个")
        
        return idle_count, busy_count
    
    def assign_task(self, agent_id):
        agent = self.agents[agent_id]
        role = agent['name']
        
        # 根据角色分配任务
        task = self.get_task_for_role(role)
        if task:
            agent['current_task'] = task['name']
            agent['status'] = 'busy'
            
            self.task_queue.append({
                'agent': agent_id,
                'task': task['name'],
                'assigned_time': datetime.now().isoformat()
            })
            
            print(f"  已分配: {task['name']}")
            print(f"  描述: {task['description']}")
            print(f"  预计: {task['estimated_time']}")
    
    def get_task_for_role(self, role):
        tasks = {
            "前端开发Agent": [
                {
                    "name": "社交分享界面开发",
                    "description": "开发用户分享测试结果的界面",
                    "estimated_time": "4小时",
                    "priority": "high"
                }
            ],
            "后端开发Agent": [
                {
                    "name": "社交分享API开发",
                    "description": "开发分享相关的API接口",
                    "estimated_time": "3小时",
                    "priority": "high"
                }
            ],
            "测试Agent": [
                {
                    "name": "社交功能测试",
                    "description": "测试社交分享功能的所有用例",
                    "estimated_time": "4小时",
                    "priority": "high"
                }
            ],
            "产品Agent": [
                {
                    "name": "社交功能需求细化",
                    "description": "细化社交功能的需求文档",
                    "estimated_time": "3小时",
                    "priority": "high"
                }
            ],
            "运维Agent": [
                {
                    "name": "服务器性能监控优化",
                    "description": "优化服务器性能监控系统",
                    "estimated_time": "3小时",
                    "priority": "high"
                }
            ]
        }
        
        role_tasks = tasks.get(role, [])
        return role_tasks[0] if role_tasks else None
    
    def generate_report(self):
        report = {
            "timestamp": datetime.now().isoformat(),
            "agents": self.agents,
            "task_queue": self.task_queue
        }
        
        filename = f"supervisor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已生成: {filename}")
        return filename
    
    def setup_hourly_check(self):
        """设置每小时自动检查"""
        print("\n设置每小时自动巡检...")
        print(f"下次检查时间: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S')}")
        
        # 创建cron任务
        cron_content = f"""# 主管Agent每小时巡检
0 * * * * cd {os.getcwd()} && python {__file__} --check
"""
        
        cron_file = "supervisor_cron.txt"
        with open(cron_file, 'w', encoding='utf-8') as f:
            f.write(cron_content)
        
        print(f"Cron配置已保存到: {cron_file}")
        print("请手动添加到crontab中")

def main():
    supervisor = SupervisorAgent()
    
    print("主管Agent巡检系统")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行检查
    idle, busy = supervisor.check_status()
    
    # 生成报告
    report_file = supervisor.generate_report()
    
    # 设置定时检查
    supervisor.setup_hourly_check()
    
    print(f"\n巡检完成!")
    print(f"- 空闲Agent: {idle}个")
    print(f"- 忙碌Agent: {busy}个")
    print(f"- 报告文件: {report_file}")

if __name__ == "__main__":
    main()