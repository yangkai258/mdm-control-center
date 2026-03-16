#!/usr/bin/env python3
"""
改进MBTI题目质量
移除不自然的"表现出X特质"题目，替换为更自然的选项
"""

import json
import random

# 读取现有的100道题
with open("mbti_questions_100.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

print(f"读取到 {len(all_questions)} 道题目")

# 更自然的题目模板库
natural_templates = {
    "E/I": [
        {"question": "当你需要放松时，你更倾向于：", "E": "约朋友出去玩或参加社交活动", "I": "在家看书、看电影或独自休息"},
        {"question": "在工作会议中，你通常：", "E": "积极发言，表达自己的想法", "I": "先倾听，思考成熟后再发言"},
        {"question": "认识新朋友时，你更可能：", "E": "主动开启话题，热情交流", "I": "保持礼貌，等待对方先开口"},
        {"question": "你的社交能量主要来自：", "E": "与人互动和外部刺激", "I": "独处和内省的时间"},
        {"question": "周末安排活动时，你倾向于：", "E": "安排丰富的社交聚会", "I": "享受安静的私人时光"},
        {"question": "当你遇到有趣的事情时，你第一时间想：", "E": "立刻分享给朋友或家人", "I": "先自己品味和思考"},
        {"question": "在团队项目中，你更擅长：", "E": "协调沟通，带动团队氛围", "I": "深入研究，提供专业建议"},
        {"question": "你的学习方式更偏向：", "E": "小组讨论和互动学习", "I": "独立研究和自主学习"},
        {"question": "面对压力时，你更可能：", "E": "找朋友倾诉寻求支持", "I": "独自思考解决方案"},
        {"question": "你的朋友圈通常是：", "E": "广泛而多样，认识很多人", "I": "小而精，有几个知心好友"}
    ],
    "S/N": [
        {"question": "描述一个地方时，你更注重：", "S": "具体的环境和细节", "N": "整体的氛围和感觉"},
        {"question": "学习新知识时，你更喜欢：", "S": "按步骤实践掌握", "N": "理解背后的原理和概念"},
        {"question": "做计划时，你更关注：", "S": "具体的实施步骤和时间表", "N": "整体的目标和愿景"},
        {"question": "看待问题时，你倾向于：", "S": "基于事实和经验分析", "N": "探索新的可能性和创意"},
        {"question": "记忆信息时，你更容易记住：", "S": "具体的数字、日期和细节", "N": "整体的模式和关联"},
        {"question": "选择礼物时，你更看重：", "S": "实用性和具体功能", "N": "象征意义和情感价值"},
        {"question": "旅行时，你更享受：", "S": "体验具体的景点和活动", "N": "感受当地的文化和氛围"},
        {"question": "解决问题时，你更依赖：", "S": "已知的有效方法", "N": "创新的解决方案"},
        {"question": "与人交流时，你更倾向于：", "S": "谈论具体的经历和事实", "N": "讨论抽象的想法和理论"},
        {"question": "评价艺术作品时，你更注重：", "S": "技巧和细节表现", "N": "情感表达和深层含义"}
    ],
    "T/F": [
        {"question": "做重要决定时，你更重视：", "T": "逻辑分析和客观数据", "F": "个人感受和人际关系"},
        {"question": "给予他人反馈时，你更注重：", "T": "事实的准确性和建设性", "F": "对方的感受和接受程度"},
        {"question": "面对冲突时，你倾向于：", "T": "就事论事，分析问题本质", "F": "维护和谐，考虑各方感受"},
        {"question": "评价工作时，你更看重：", "T": "效率和成果质量", "F": "团队合作和氛围"},
        {"question": "帮助他人时，你更可能：", "T": "提供具体的解决方案", "F": "给予情感支持和理解"},
        {"question": "学习新技能时，你更关注：", "T": "技术的原理和逻辑", "F": "应用的价值和意义"},
        {"question": "制定规则时，你更注重：", "T": "公平和一致性", "F": "灵活性和人性化"},
        {"question": "面对批评时，你更可能：", "T": "理性分析批评的合理性", "F": "感受批评带来的情绪影响"},
        {"question": "选择职业时，你更考虑：", "T": "发展前景和薪资待遇", "F": "工作意义和团队氛围"},
        {"question": "处理人际关系时，你更倾向于：", "T": "明确界限和原则", "F": "维护和谐和情感联系"}
    ],
    "J/P": [
        {"question": "你的日常生活通常是：", "J": "有计划、有规律的", "P": "灵活、随性的"},
        {"question": "处理工作任务时，你倾向于：", "J": "提前规划，按时完成", "P": "灵活应对，在压力下效率更高"},
        {"question": "做决定时，你更愿意：", "J": "尽快做出明确决定", "P": "保持开放，收集更多信息"},
        {"question": "你的工作环境通常是：", "J": "整洁有序，物品归位", "P": "有些杂乱但你知道东西在哪"},
        {"question": "面对突然的变化时，你更可能：", "J": "感到不安，希望恢复原计划", "P": "灵活适应，享受变化带来的新鲜感"},
        {"question": "安排假期时，你倾向于：", "J": "制定详细的行程计划", "P": "大致安排，留出自由发挥空间"},
        {"question": "学习新东西时，你更喜欢：", "J": "系统性地按计划学习", "P": "根据兴趣跳跃式学习"},
        {"question": "处理多项任务时，你更擅长：", "J": "按优先级顺序完成", "P": "多任务并行处理"},
        {"question": "你的时间管理风格是：", "J": "严格按时间表执行", "P": "大致安排，灵活调整"},
        {"question": "购物时，你更倾向于：", "J": "有明确目标，快速完成", "P": "随意浏览，发现惊喜"}
    ]
}

def find_and_replace_bad_questions(questions):
    """查找并替换不自然的题目"""
    bad_question_patterns = [
        "表现出E特质",
        "表现出I特质", 
        "表现出S特质",
        "表现出N特质",
        "表现出T特质",
        "表现出F特质",
        "表现出J特质",
        "表现出P特质",
        "在E/I维度上",
        "在S/N维度上",
        "在T/F维度上",
        "在J/P维度上"
    ]
    
    bad_questions = []
    for i, q in enumerate(questions):
        question_text = q["question"]
        options = q["options"]
        
        # 检查题目文本是否包含不自然模式
        is_bad_question = False
        for pattern in bad_question_patterns:
            if pattern in question_text:
                is_bad_question = True
                break
        
        # 检查选项是否包含不自然模式
        if not is_bad_question:
            for option in options:
                if any(pattern in option["text"] for pattern in bad_question_patterns):
                    is_bad_question = True
                    break
        
        if is_bad_question:
            bad_questions.append((i, q))
    
    return bad_questions

def get_dimension_from_question(question):
    """从题目中提取MBTI维度"""
    options = question["options"]
    if len(options) >= 2:
        type1 = options[0].get("type", "")
        type2 = options[1].get("type", "")
        
        # 确定维度对
        dimension_pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
        for dim1, dim2 in dimension_pairs:
            if (type1 == dim1 and type2 == dim2) or (type1 == dim2 and type2 == dim1):
                return (dim1, dim2)
    
    return None

def generate_natural_question(dimension, used_templates):
    """生成自然的题目"""
    dim_key = f"{dimension[0]}/{dimension[1]}"
    templates = natural_templates.get(dim_key, [])
    
    if not templates:
        return None
    
    # 选择未使用过的模板
    available_templates = [t for t in templates if t not in used_templates]
    if not available_templates:
        available_templates = templates  # 如果都用过了，重新使用
    
    template = random.choice(available_templates)
    used_templates.append(template)
    
    question = {
        "question": template["question"],
        "options": [
            {
                "text": template[dimension[0]],
                "type": dimension[0],
                f"score_{dimension[0].lower()}": 1,
                f"score_{dimension[1].lower()}": 0
            },
            {
                "text": template[dimension[1]],
                "type": dimension[1],
                f"score_{dimension[0].lower()}": 0,
                f"score_{dimension[1].lower()}": 1
            }
        ]
    }
    
    return question

def improve_questions():
    """改进题目质量"""
    print("开始改进题目质量...")
    
    # 查找需要替换的题目
    bad_questions = find_and_replace_bad_questions(all_questions)
    print(f"找到 {len(bad_questions)} 道需要改进的题目")
    
    if not bad_questions:
        print("没有发现需要改进的题目")
        return all_questions
    
    # 记录已使用的模板
    used_templates_by_dimension = {
        "E/I": [],
        "S/N": [],
        "T/F": [],
        "J/P": []
    }
    
    improved_questions = all_questions.copy()
    
    # 替换不自然的题目
    replacement_count = 0
    for idx, bad_q in bad_questions:
        dimension = get_dimension_from_question(bad_q)
        if not dimension:
            print(f"警告：无法确定题目 {idx+1} 的维度，跳过")
            continue
        
        dim_key = f"{dimension[0]}/{dimension[1]}"
        new_question = generate_natural_question(dimension, used_templates_by_dimension[dim_key])
        
        if new_question:
            # 保持原有的ID和其他属性
            new_question["id"] = bad_q["id"]
            improved_questions[idx] = new_question
            replacement_count += 1
            
            print(f"替换题目 {idx+1}:")
            print(f"  原题: {bad_q['question']}")
            print(f"  选项: {bad_q['options'][0]['text']} / {bad_q['options'][1]['text']}")
            print(f"  新题: {new_question['question']}")
            print(f"  选项: {new_question['options'][0]['text']} / {new_question['options'][1]['text']}")
            print()
    
    print(f"成功替换 {replacement_count} 道题目")
    return improved_questions

def update_server_file(questions):
    """更新服务器文件"""
    # 读取原始服务器文件
    with open("complete_server.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 找到题目定义的位置
    start_marker = "# 扩展MBTI题目（100道题）"
    end_marker = "]"
    
    start_index = content.find(start_marker)
    if start_index == -1:
        print("错误：找不到题目定义开始标记")
        return
    
    # 找到MBTI_QUESTIONS列表的结束位置
    bracket_count = 0
    in_list = False
    end_index = start_index
    
    for i in range(start_index, len(content)):
        if content[i] == '[':
            bracket_count += 1
            in_list = True
        elif content[i] == ']' and in_list:
            bracket_count -= 1
            if bracket_count == 0:
                end_index = i
                break
    
    # 生成新的题目定义
    new_questions_def = f"""# 改进的MBTI题目（100道题 - 自然版）
MBTI_QUESTIONS = {json.dumps(questions, ensure_ascii=False, indent=4)}"""
    
    # 替换内容
    new_content = content[:start_index] + new_questions_def + content[end_index+1:]
    
    # 写回文件
    with open("complete_server.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("服务器文件已更新")
    
    # 保存改进后的题目到文件
    with open("mbti_questions_improved.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print("改进后的题目已保存到 mbti_questions_improved.json")

if __name__ == "__main__":
    print("开始改进MBTI题目质量...")
    
    # 改进题目
    improved_questions = improve_questions()
    
    # 更新服务器文件
    update_server_file(improved_questions)
    
    print("题目质量改进完成！")
    print("下一步：重启服务器以应用改进后的题目")