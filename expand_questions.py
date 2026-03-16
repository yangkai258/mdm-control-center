#!/usr/bin/env python3
"""
MBTI题目库扩展脚本
将题目从16道扩展到100道
"""

import json
import random

# 原始16道题目
original_questions = [
    {
        "id": 1,
        "question": "在聚会中，你通常：",
        "options": [
            {"text": "与很多人交流，包括陌生人", "type": "E", "score_e": 1, "score_i": 0},
            {"text": "只与几个熟悉的人交谈", "type": "I", "score_e": 0, "score_i": 1}
        ]
    },
    {
        "id": 2,
        "question": "你更倾向于：",
        "options": [
            {"text": "通过实践学习", "type": "S", "score_s": 1, "score_n": 0},
            {"text": "通过理论思考学习", "type": "N", "score_s": 0, "score_n": 1}
        ]
    },
    {
        "id": 3,
        "question": "做决定时，你更注重：",
        "options": [
            {"text": "逻辑和客观事实", "type": "T", "score_t": 1, "score_f": 0},
            {"text": "情感和人际关系", "type": "F", "score_t": 0, "score_f": 1}
        ]
    },
    {
        "id": 4,
        "question": "你的生活风格更偏向：",
        "options": [
            {"text": "有计划和组织", "type": "J", "score_j": 1, "score_p": 0},
            {"text": "灵活和随性", "type": "P", "score_j": 0, "score_p": 1}
        ]
    },
    {
        "id": 5,
        "question": "当你感到疲惫时，你更喜欢：",
        "options": [
            {"text": "与朋友一起放松", "type": "E", "score_e": 1, "score_i": 0},
            {"text": "独自休息或阅读", "type": "I", "score_e": 0, "score_i": 1}
        ]
    },
    {
        "id": 6,
        "question": "你更相信：",
        "options": [
            {"text": "具体经验和事实", "type": "S", "score_s": 1, "score_n": 0},
            {"text": "灵感和可能性", "type": "N", "score_s": 0, "score_n": 1}
        ]
    },
    {
        "id": 7,
        "question": "评价他人时，你更看重：",
        "options": [
            {"text": "他们的能力和成就", "type": "T", "score_t": 1, "score_f": 0},
            {"text": "他们的感受和价值观", "type": "F", "score_t": 0, "score_f": 1}
        ]
    },
    {
        "id": 8,
        "question": "处理工作时，你倾向于：",
        "options": [
            {"text": "提前计划并按时完成", "type": "J", "score_j": 1, "score_p": 0},
            {"text": "在压力下工作得更好", "type": "P", "score_j": 0, "score_p": 1}
        ]
    },
    {
        "id": 9,
        "question": "在新环境中，你通常：",
        "options": [
            {"text": "主动认识新朋友", "type": "E", "score_e": 1, "score_i": 0},
            {"text": "先观察再参与", "type": "I", "score_e": 0, "score_i": 1}
        ]
    },
    {
        "id": 10,
        "question": "你更擅长：",
        "options": [
            {"text": "处理具体细节", "type": "S", "score_s": 1, "score_n": 0},
            {"text": "看到整体大局", "type": "N", "score_s": 0, "score_n": 1}
        ]
    },
    {
        "id": 11,
        "question": "当有人批评你时，你更可能：",
        "options": [
            {"text": "分析批评是否有道理", "type": "T", "score_t": 1, "score_f": 0},
            {"text": "感到受伤或不安", "type": "F", "score_t": 0, "score_f": 1}
        ]
    },
    {
        "id": 12,
        "question": "你的书桌通常是：",
        "options": [
            {"text": "整洁有序的", "type": "J", "score_j": 1, "score_p": 0},
            {"text": "有些杂乱但你知道东西在哪", "type": "P", "score_j": 0, "score_p": 1}
        ]
    },
    {
        "id": 13,
        "question": "在社交场合，你通常：",
        "options": [
            {"text": "是谈话的中心", "type": "E", "score_e": 1, "score_i": 0},
            {"text": "倾听多于发言", "type": "I", "score_e": 0, "score_i": 1}
        ]
    },
    {
        "id": 14,
        "question": "学习新东西时，你更喜欢：",
        "options": [
            {"text": "按部就班地学习", "type": "S", "score_s": 1, "score_n": 0},
            {"text": "跳跃式地理解概念", "type": "N", "score_s": 0, "score_n": 1}
        ]
    },
    {
        "id": 15,
        "question": "做重要决定时，你更依赖：",
        "options": [
            {"text": "客观分析和数据", "type": "T", "score_t": 1, "score_f": 0},
            {"text": "个人价值观和感受", "type": "F", "score_t": 0, "score_f": 1}
        ]
    },
    {
        "id": 16,
        "question": "你的假期计划通常是：",
        "options": [
            {"text": "详细安排好的", "type": "J", "score_j": 1, "score_p": 0},
            {"text": "随性而定的", "type": "P", "score_j": 0, "score_p": 1}
        ]
    }
]

# MBTI维度分类
mbti_dimensions = [
    ("E", "I"),  # 外向/内向
    ("S", "N"),  # 实感/直觉
    ("T", "F"),  # 思考/情感
    ("J", "P")   # 判断/感知
]

# 题目模板库
question_templates = {
    "E/I": [
        {"template": "在社交活动中，你通常：", "E": "积极参与并享受热闹", "I": "更喜欢安静的小范围交流"},
        {"template": "当你需要思考问题时，你倾向于：", "E": "通过与人讨论来理清思路", "I": "独自思考并整理想法"},
        {"template": "你的能量主要来自：", "E": "与外界互动和社交", "I": "独处和内省"},
        {"template": "在团队中，你更可能：", "E": "主动发言并带动气氛", "I": "倾听并思考后再表达"},
        {"template": "周末你更喜欢：", "E": "安排丰富的社交活动", "I": "享受安静的私人时间"},
        {"template": "认识新朋友时，你通常：", "E": "主动介绍自己并开启话题", "I": "等待对方先开口或观察"},
        {"template": "当你感到兴奋时，你更想：", "E": "立刻与他人分享", "I": "先自己品味这份感受"},
        {"template": "在工作环境中，你倾向于：", "E": "开放式办公，便于交流", "I": "独立空间，减少干扰"},
        {"template": "学习新技能时，你更喜欢：", "E": "参加培训班与他人一起学习", "I": "自学或一对一指导"},
        {"template": "面对压力时，你更可能：", "E": "找朋友倾诉寻求支持", "I": "独自处理情绪和问题"}
    ],
    "S/N": [
        {"template": "你更关注：", "S": "眼前的具体事实", "N": "未来的可能性"},
        {"template": "描述事物时，你倾向于：", "S": "使用具体细节和实例", "N": "使用比喻和象征"},
        {"template": "解决问题时，你更依赖：", "S": "过去的经验和已知方法", "N": "新的想法和创新方案"},
        {"template": "你更擅长：", "S": "执行具体的任务", "N": "构思抽象的概念"},
        {"template": "看待世界时，你更注重：", "S": "现实和实际存在", "N": "潜力和发展趋势"},
        {"template": "记忆信息时，你更容易记住：", "S": "具体的细节和数据", "N": "整体的模式和联系"},
        {"template": "学习时，你更喜欢：", "S": "按步骤操作练习", "N": "理解背后的原理"},
        {"template": "做计划时，你更关注：", "S": "具体的实施步骤", "N": "整体的愿景目标"},
        {"template": "与人交流时，你更倾向于：", "S": "谈论具体经历和事实", "N": "讨论想法和理论"},
        {"template": "面对新事物时，你首先注意到：", "S": "它的实际功能和外观", "N": "它的象征意义和潜力"}
    ],
    "T/F": [
        {"template": "做决定时，你更重视：", "T": "逻辑和客观标准", "F": "情感和人际关系"},
        {"template": "评价他人时，你更看重：", "T": "能力和效率", "F": "善意和动机"},
        {"template": "面对冲突时，你倾向于：", "T": "就事论事分析问题", "F": "考虑各方感受"},
        {"template": "给予反馈时，你更注重：", "T": "事实和准确性", "F": "方式和语气"},
        {"template": "你的价值观更偏向：", "T": "公正和真理", "F": "和谐和同情"},
        {"template": "处理工作时，你更关注：", "T": "任务完成的质量", "F": "团队合作的氛围"},
        {"template": "学习知识时，你更重视：", "T": "理论的严谨性", "F": "应用的关怀性"},
        {"template": "面对选择时，你更依赖：", "T": "理性的分析", "F": "内心的感受"},
        {"template": "表达观点时，你更注重：", "T": "逻辑的连贯性", "F": "情感的共鸣"},
        {"template": "帮助他人时，你更倾向于：", "T": "提供实际的解决方案", "F": "给予情感的支持"}
    ],
    "J/P": [
        {"template": "你的生活节奏更偏向：", "J": "有计划有规律", "P": "灵活适应变化"},
        {"template": "完成任务时，你倾向于：", "J": "提前完成避免拖延", "P": "在截止日期前完成"},
        {"template": "做决定时，你更愿意：", "J": "尽快做出决定", "P": "保持开放收集信息"},
        {"template": "你的工作环境通常是：", "J": "整洁有序的", "P": "随性但有效率的"},
        {"template": "面对计划时，你更可能：", "J": "严格遵守计划", "P": "根据情况调整"},
        {"template": "你的时间管理风格是：", "J": "详细规划时间", "P": "大致安排灵活应对"},
        {"template": "处理信息时，你倾向于：", "J": "快速分类做决定", "P": "持续收集新信息"},
        {"template": "面对选择时，你更可能：", "J": "做出明确选择", "P": "保留多种可能性"},
        {"template": "你的决策过程更偏向：", "J": "结论导向", "P": "过程导向"},
        {"template": "组织活动时，你更注重：", "J": "结构和流程", "P": "自由和创意"}
    ]
}

def generate_questions():
    """生成100道MBTI题目"""
    all_questions = []
    question_id = 1
    
    # 保留原始16道题
    for q in original_questions:
        q_copy = q.copy()
        q_copy["id"] = question_id
        all_questions.append(q_copy)
        question_id += 1
    
    # 生成额外题目（84道）
    for dimension in mbti_dimensions:
        dim_key = f"{dimension[0]}/{dimension[1]}"
        templates = question_templates.get(dim_key, [])
        
        # 每个维度生成21道题（共84道）
        for i in range(21):
            if i < len(templates):
                template = templates[i]
            else:
                # 如果模板不够，使用通用模板
                template = {
                    "template": f"在{dim_key}维度上，你更倾向于：",
                    dimension[0]: f"表现出{dimension[0]}特质",
                    dimension[1]: f"表现出{dimension[1]}特质"
                }
            
            question = {
                "id": question_id,
                "question": template["template"],
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
            all_questions.append(question)
            question_id += 1
    
    # 随机打乱题目顺序（但保留前16题）
    first_16 = all_questions[:16]
    rest_84 = all_questions[16:]
    random.shuffle(rest_84)
    all_questions = first_16 + rest_84
    
    # 重新编号
    for i, q in enumerate(all_questions):
        q["id"] = i + 1
    
    return all_questions

def update_server_file():
    """更新服务器文件中的题目"""
    expanded_questions = generate_questions()
    
    # 读取原始服务器文件
    with open("complete_server.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 找到题目定义的位置
    start_marker = "# 标准MBTI题目（16道题）"
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
    new_questions_def = f"""# 扩展MBTI题目（100道题）
MBTI_QUESTIONS = {json.dumps(expanded_questions, ensure_ascii=False, indent=4)}"""
    
    # 替换内容
    new_content = content[:start_index] + new_questions_def + content[end_index+1:]
    
    # 写回文件
    with open("complete_server.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"成功扩展题目库到 {len(expanded_questions)} 道题")
    print(f"题目分布：")
    print(f"   - E/I维度：{len([q for q in expanded_questions if any(opt['type'] in ['E','I'] for opt in q['options'])])} 题")
    print(f"   - S/N维度：{len([q for q in expanded_questions if any(opt['type'] in ['S','N'] for opt in q['options'])])} 题")
    print(f"   - T/F维度：{len([q for q in expanded_questions if any(opt['type'] in ['T','F'] for opt in q['options'])])} 题")
    print(f"   - J/P维度：{len([q for q in expanded_questions if any(opt['type'] in ['J','P'] for opt in q['options'])])} 题")
    
    # 保存题目到独立文件
    with open("mbti_questions_100.json", "w", encoding="utf-8") as f:
        json.dump(expanded_questions, f, ensure_ascii=False, indent=2)
    
    print(f"题目已保存到 mbti_questions_100.json")

if __name__ == "__main__":
    print("开始扩展MBTI题目库...")
    update_server_file()
    print("题目库扩展完成！")
    print("下一步：重启服务器以应用新的题目库")