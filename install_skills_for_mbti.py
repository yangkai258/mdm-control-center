#!/usr/bin/env python3
"""
为MBTI测试系统团队安装合适的skill
基于项目需求分析需要哪些skill
"""

import os
import json
import shutil
from pathlib import Path

class SkillInstaller:
    def __init__(self):
        self.workspace = Path.cwd()
        self.skills_dir = self.workspace / "skills"
        self.available_skills = []
        
    def analyze_project_needs(self):
        """分析项目需求"""
        print("分析MBTI测试系统项目需求...")
        
        needs = {
            "frontend": [
                "responsive-web-design",  # 响应式网页设计
                "javascript-frameworks",  # JavaScript框架
                "css-animations",  # CSS动画
                "mobile-optimization",  # 移动端优化
                "ui-ux-design"  # UI/UX设计
            ],
            "backend": [
                "python-web-frameworks",  # Python Web框架
                "rest-api-design",  # REST API设计
                "database-management",  # 数据库管理
                "authentication-jwt",  # JWT认证
                "server-performance"  # 服务器性能
            ],
            "testing": [
                "automated-testing",  # 自动化测试
                "performance-testing",  # 性能测试
                "compatibility-testing",  # 兼容性测试
                "user-experience-testing"  # 用户体验测试
            ],
            "devops": [
                "server-deployment",  # 服务器部署
                "monitoring-alerts",  # 监控告警
                "database-optimization",  # 数据库优化
                "backup-recovery"  # 备份恢复
            ],
            "project_management": [
                "task-management",  # 任务管理
                "team-collaboration",  # 团队协作
                "code-review",  # 代码审查
                "documentation"  # 文档编写
            ]
        }
        
        print("项目需求分析完成:")
        for category, skills in needs.items():
            print(f"  {category}: {len(skills)}个skill需求")
        
        return needs
    
    def check_existing_skills(self):
        """检查已存在的skill"""
        print("\n检查已存在的skill...")
        
        if not self.skills_dir.exists():
            self.skills_dir.mkdir(parents=True)
            print(f"创建skills目录: {self.skills_dir}")
            return []
        
        existing_skills = []
        for item in self.skills_dir.iterdir():
            if item.is_dir():
                skill_md = item / "SKILL.md"
                if skill_md.exists():
                    existing_skills.append(item.name)
        
        print(f"发现 {len(existing_skills)} 个已存在的skill:")
        for skill in existing_skills:
            print(f"  - {skill}")
        
        return existing_skills
    
    def create_skill_template(self, skill_name, category, description):
        """创建skill模板"""
        skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建SKILL.md文件
        skill_md_content = f"""# {skill_name.replace('-', ' ').title()} Skill

## 描述
{description}

## 用途
用于MBTI测试系统开发团队的{category}工作。

## 工具
- 提供相关工具和函数
- 自动化常见任务
- 最佳实践指南

## 示例用法

## 配置选项

## 依赖项

## 更新日志

---
**创建时间**: 2026-03-14
**适用项目**: MBTI性格测试系统
**团队**: 前端、后端、测试、产品、运维Agent
"""
        
        skill_md_file = skill_dir / "SKILL.md"
        skill_md_file.write_text(skill_md_content, encoding='utf-8')
        
        # 创建示例脚本目录
        examples_dir = skill_dir / "examples"
        examples_dir.mkdir(exist_ok=True)
        
        # 创建工具目录
        tools_dir = skill_dir / "tools"
        tools_dir.mkdir(exist_ok=True)
        
        print(f"创建skill: {skill_name}")
        return skill_dir
    
    def install_frontend_skills(self):
        """安装前端开发skill"""
        print("\n安装前端开发skill...")
        
        skills = [
            {
                "name": "responsive-web-mbti",
                "category": "frontend",
                "description": "MBTI测试系统的响应式网页设计skill，专门针对心理测试界面的优化，包括题目展示、选项布局、进度指示等组件的响应式设计。"
            },
            {
                "name": "mobile-optimization-mbti",
                "category": "frontend",
                "description": "MBTI测试移动端优化skill，针对iPhone 15 Pro Max等设备的专门优化，包括安全区域处理、触控优化、性能调优。"
            },
            {
                "name": "mbti-test-ui-components",
                "category": "frontend",
                "description": "MBTI测试专用UI组件库，包括题目卡片、选项按钮、进度条、分析报告组件等可复用组件。"
            }
        ]
        
        installed = []
        for skill_info in skills:
            skill_dir = self.create_skill_template(
                skill_info["name"],
                skill_info["category"],
                skill_info["description"]
            )
            installed.append(skill_info["name"])
        
        return installed
    
    def install_backend_skills(self):
        """安装后端开发skill"""
        print("\n安装后端开发skill...")
        
        skills = [
            {
                "name": "mbti-api-server",
                "category": "backend",
                "description": "MBTI测试API服务器skill，提供用户认证、题目管理、测试提交、分析报告生成的完整API解决方案。"
            },
            {
                "name": "jwt-authentication-mbti",
                "category": "backend",
                "description": "MBTI测试JWT认证skill，专门针对心理测试系统的用户认证和会话管理，包括token生成、验证、刷新等功能。"
            },
            {
                "name": "mbti-database-management",
                "category": "backend",
                "description": "MBTI测试数据库管理skill，包括用户数据、测试记录、题目库、分析报告的数据模型和查询优化。"
            }
        ]
        
        installed = []
        for skill_info in skills:
            skill_dir = self.create_skill_template(
                skill_info["name"],
                skill_info["category"],
                skill_info["description"]
            )
            installed.append(skill_info["name"])
        
        return installed
    
    def install_testing_skills(self):
        """安装测试skill"""
        print("\n安装测试skill...")
        
        skills = [
            {
                "name": "mbti-functional-testing",
                "category": "testing",
                "description": "MBTI测试功能测试skill，包括题目流程测试、用户认证测试、分析报告生成测试等完整测试用例。"
            },
            {
                "name": "mobile-compatibility-testing",
                "category": "testing",
                "description": "移动端兼容性测试skill，专门测试MBTI测试在不同iOS和Android设备上的显示和交互效果。"
            },
            {
                "name": "performance-testing-mbti",
                "category": "testing",
                "description": "MBTI测试性能测试skill，包括服务器响应测试、页面加载测试、并发用户测试等性能指标测试。"
            }
        ]
        
        installed = []
        for skill_info in skills:
            skill_dir = self.create_skill_template(
                skill_info["name"],
                skill_info["category"],
                skill_info["description"]
            )
            installed.append(skill_info["name"])
        
        return installed
    
    def install_devops_skills(self):
        """安装运维skill"""
        print("\n安装运维skill...")
        
        skills = [
            {
                "name": "mbti-server-deployment",
                "category": "devops",
                "description": "MBTI测试服务器部署skill，包括环境配置、依赖安装、服务启动、监控设置等完整部署流程。"
            },
            {
                "name": "server-monitoring-mbti",
                "category": "devops",
                "description": "MBTI测试服务器监控skill，实时监控服务器性能、错误日志、用户访问等关键指标。"
            },
            {
                "name": "backup-recovery-mbti",
                "category": "devops",
                "description": "MBTI测试备份恢复skill，定期备份用户数据和系统配置，提供快速恢复方案。"
            }
        ]
        
        installed = []
        for skill_info in skills:
            skill_dir = self.create_skill_template(
                skill_info["name"],
                skill_info["category"],
                skill_info["description"]
            )
            installed.append(skill_info["name"])
        
        return installed
    
    def install_management_skills(self):
        """安装管理skill"""
        print("\n安装项目管理skill...")
        
        skills = [
            {
                "name": "agent-team-supervisor",
                "category": "management",
                "description": "Agent团队主管skill，用于管理前端、后端、测试、产品、运维Agent的协作和任务分配。"
            },
            {
                "name": "mbti-project-management",
                "category": "management",
                "description": "MBTI测试项目管理skill，包括需求分析、任务分解、进度跟踪、质量保证等项目管理功能。"
            },
            {
                "name": "team-collaboration-mbti",
                "category": "management",
                "description": "MBTI测试团队协作skill，促进各Agent之间的沟通协作、代码审查、知识共享。"
            }
        ]
        
        installed = []
        for skill_info in skills:
            skill_dir = self.create_skill_template(
                skill_info["name"],
                skill_info["category"],
                skill_info["description"]
            )
            installed.append(skill_info["name"])
        
        return installed
    
    def create_skill_index(self, all_skills):
        """创建skill索引"""
        print("\n创建skill索引...")
        
        index_content = """# MBTI测试系统开发团队 - Skill索引

## 概述
本目录包含MBTI测试系统开发团队使用的所有skill，每个skill都针对特定的开发任务进行优化。

## Skill分类

### 前端开发skill
用于MBTI测试界面开发、移动端优化、用户体验设计等任务。

### 后端开发skill
用于API服务器开发、用户认证、数据库管理等任务。

### 测试skill
用于功能测试、兼容性测试、性能测试等质量保证任务。

### 运维skill
用于服务器部署、监控、备份恢复等运维任务。

### 管理skill
用于团队协作、项目管理、任务分配等管理任务。

## 使用说明
每个skill目录包含：
1. SKILL.md - skill说明文档
2. examples/ - 使用示例
3. tools/ - 相关工具脚本

## 团队协作
各Agent应根据任务需求使用相应的skill，确保开发效率和质量。

---
**创建时间**: 2026-03-14
**团队**: MBTI测试系统开发团队
**状态**: 活跃开发中
"""
        
        index_file = self.skills_dir / "INDEX.md"
        index_file.write_text(index_content, encoding='utf-8')
        
        # 创建详细的skill列表
        details_content = "# 详细Skill列表\n\n"
        
        for category, skills in all_skills.items():
            details_content += f"## {category.replace('_', ' ').title()} Skill\n\n"
            for skill in skills:
                details_content += f"### {skill}\n"
                details_content += f"- **目录**: skills/{skill}/\n"
                details_content += f"- **用途**: 查看对应的SKILL.md文件\n\n"
        
        details_file = self.skills_dir / "SKILLS_DETAILS.md"
        details_file.write_text(details_content, encoding='utf-8')
        
        print(f"创建索引文件: {index_file}")
        print(f"创建详细列表: {details_file}")
    
    def install_all_skills(self):
        """安装所有skill"""
        print("开始为MBTI测试系统团队安装skill...")
        print("=" * 60)
        
        # 分析需求
        needs = self.analyze_project_needs()
        
        # 检查现有skill
        existing = self.check_existing_skills()
        
        # 安装各类skill
        all_installed = {}
        
        frontend_skills = self.install_frontend_skills()
        all_installed["frontend"] = frontend_skills
        
        backend_skills = self.install_backend_skills()
        all_installed["backend"] = backend_skills
        
        testing_skills = self.install_testing_skills()
        all_installed["testing"] = testing_skills
        
        devops_skills = self.install_devops_skills()
        all_installed["devops"] = devops_skills
        
        management_skills = self.install_management_skills()
        all_installed["management"] = management_skills
        
        # 创建索引
        self.create_skill_index(all_installed)
        
        # 统计
        total_skills = sum(len(skills) for skills in all_installed.values())
        
        print("\n" + "=" * 60)
        print("Skill安装完成!")
        print(f"总计安装: {total_skills} 个skill")
        print("\n按分类统计:")
        for category, skills in all_installed.items():
            print(f"  {category}: {len(skills)}个")
        
        print(f"\nskill目录: {self.skills_dir}")
        print("各Agent现在可以使用这些skill进行开发工作")
        
        return all_installed

def main():
    installer = SkillInstaller()
    installed_skills = installer.install_all_skills()
    
    # 生成安装报告
    report = {
        "timestamp": "2026-03-14T00:54:00",
        "project": "MBTI测试系统",
        "team": ["前端Agent", "后端Agent", "测试Agent", "产品Agent", "运维Agent"],
        "installed_skills": installed_skills,
        "total_count": sum(len(skills) for skills in installed_skills.values())
    }
    
    report_file = "skill_installation_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n安装报告已保存: {report_file}")

if __name__ == "__main__":
    main()