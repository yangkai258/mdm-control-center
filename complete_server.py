#!/usr/bin/env python3
"""
MBTI Personality Test Server - Complete Version
支持用户注册、登录、真实题目测试、JWT认证
端口：8004
"""

import sqlite3
import hashlib
import json
import time
import jwt
import secrets
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

# 配置
# 使用固定的SECRET_KEY，避免服务器重启后令牌失效
SECRET_KEY = "mbti_test_fixed_secret_key_2026_03_13_1234567890abcdef"  # 固定JWT密钥
DB_FILE = "mbti_test.db"
PORT = 8004

# 改进的MBTI题目（100道题 - 自然版）
MBTI_QUESTIONS = [
    {
        "id": 1,
        "question": "在聚会中，你通常：",
        "options": [
            {
                "text": "与很多人交流，包括陌生人",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "只与几个熟悉的人交谈",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 2,
        "question": "你更倾向于：",
        "options": [
            {
                "text": "通过实践学习",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "通过理论思考学习",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "id": 3,
        "question": "做决定时，你更注重：",
        "options": [
            {
                "text": "逻辑和客观事实",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "情感和人际关系",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 4,
        "question": "你的生活风格更偏向：",
        "options": [
            {
                "text": "有计划和组织",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "灵活和随性",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 5,
        "question": "当你感到疲惫时，你更喜欢：",
        "options": [
            {
                "text": "与朋友一起放松",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独自休息或阅读",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 6,
        "question": "你更相信：",
        "options": [
            {
                "text": "具体经验和事实",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "灵感和可能性",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "id": 7,
        "question": "评价他人时，你更看重：",
        "options": [
            {
                "text": "他们的能力和成就",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "他们的感受和价值观",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 8,
        "question": "处理工作时，你倾向于：",
        "options": [
            {
                "text": "提前计划并按时完成",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "在压力下工作得更好",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 9,
        "question": "在新环境中，你通常：",
        "options": [
            {
                "text": "主动认识新朋友",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "先观察再参与",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 10,
        "question": "你更擅长：",
        "options": [
            {
                "text": "处理具体细节",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "看到整体大局",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "id": 11,
        "question": "当有人批评你时，你更可能：",
        "options": [
            {
                "text": "分析批评是否有道理",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "感到受伤或不安",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 12,
        "question": "你的书桌通常是：",
        "options": [
            {
                "text": "整洁有序的",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "有些杂乱但你知道东西在哪",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 13,
        "question": "在社交场合，你通常：",
        "options": [
            {
                "text": "是谈话的中心",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "倾听多于发言",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 14,
        "question": "学习新东西时，你更喜欢：",
        "options": [
            {
                "text": "按部就班地学习",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "跳跃式地理解概念",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "id": 15,
        "question": "做重要决定时，你更依赖：",
        "options": [
            {
                "text": "客观分析和数据",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "个人价值观和感受",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 16,
        "question": "你的假期计划通常是：",
        "options": [
            {
                "text": "详细安排好的",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "随性而定的",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 17,
        "question": "在团队中，你更可能：",
        "options": [
            {
                "text": "主动发言并带动气氛",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "倾听并思考后再表达",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "question": "描述一个地方时，你更注重：",
        "options": [
            {
                "text": "具体的环境和细节",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "整体的氛围和感觉",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 18
    },
    {
        "question": "当你需要放松时，你更倾向于：",
        "options": [
            {
                "text": "约朋友出去玩或参加社交活动",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "在家看书、看电影或独自休息",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 19
    },
    {
        "question": "评价工作时，你更看重：",
        "options": [
            {
                "text": "效率和成果质量",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "团队合作和氛围",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 20
    },
    {
        "id": 21,
        "question": "面对冲突时，你倾向于：",
        "options": [
            {
                "text": "就事论事分析问题",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "考虑各方感受",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 22,
        "question": "你的生活节奏更偏向：",
        "options": [
            {
                "text": "有计划有规律",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "灵活适应变化",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "question": "学习新技能时，你更关注：",
        "options": [
            {
                "text": "技术的原理和逻辑",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "应用的价值和意义",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 23
    },
    {
        "question": "学习新知识时，你更喜欢：",
        "options": [
            {
                "text": "按步骤实践掌握",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "理解背后的原理和概念",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 24
    },
    {
        "question": "你的日常生活通常是：",
        "options": [
            {
                "text": "有计划、有规律的",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "灵活、随性的",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 25
    },
    {
        "question": "处理多项任务时，你更擅长：",
        "options": [
            {
                "text": "按优先级顺序完成",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "多任务并行处理",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 26
    },
    {
        "question": "你的工作环境通常是：",
        "options": [
            {
                "text": "整洁有序，物品归位",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "有些杂乱但你知道东西在哪",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 27
    },
    {
        "question": "你的学习方式更偏向：",
        "options": [
            {
                "text": "小组讨论和互动学习",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独立研究和自主学习",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 28
    },
    {
        "question": "你的朋友圈通常是：",
        "options": [
            {
                "text": "广泛而多样，认识很多人",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "小而精，有几个知心好友",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 29
    },
    {
        "id": 30,
        "question": "与人交流时，你更倾向于：",
        "options": [
            {
                "text": "谈论具体经历和事实",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "讨论想法和理论",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "question": "在工作会议中，你通常：",
        "options": [
            {
                "text": "积极发言，表达自己的想法",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "先倾听，思考成熟后再发言",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 31
    },
    {
        "id": 32,
        "question": "面对计划时，你更可能：",
        "options": [
            {
                "text": "严格遵守计划",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "根据情况调整",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "question": "解决问题时，你更依赖：",
        "options": [
            {
                "text": "已知的有效方法",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "创新的解决方案",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 33
    },
    {
        "id": 34,
        "question": "记忆信息时，你更容易记住：",
        "options": [
            {
                "text": "具体的细节和数据",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "整体的模式和联系",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "question": "帮助他人时，你更可能：",
        "options": [
            {
                "text": "提供具体的解决方案",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "给予情感支持和理解",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 35
    },
    {
        "id": 36,
        "question": "学习新技能时，你更喜欢：",
        "options": [
            {
                "text": "参加培训班与他人一起学习",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "自学或一对一指导",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 37,
        "question": "面对新事物时，你首先注意到：",
        "options": [
            {
                "text": "它的实际功能和外观",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "它的象征意义和潜力",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "id": 38,
        "question": "解决问题时，你更依赖：",
        "options": [
            {
                "text": "过去的经验和已知方法",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "新的想法和创新方案",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "question": "面对批评时，你更可能：",
        "options": [
            {
                "text": "理性分析批评的合理性",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "感受批评带来的情绪影响",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 39
    },
    {
        "id": 40,
        "question": "给予反馈时，你更注重：",
        "options": [
            {
                "text": "事实和准确性",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "方式和语气",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 41,
        "question": "你更关注：",
        "options": [
            {
                "text": "眼前的具体事实",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "未来的可能性",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "question": "面对突然的变化时，你更可能：",
        "options": [
            {
                "text": "感到不安，希望恢复原计划",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "灵活适应，享受变化带来的新鲜感",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 42
    },
    {
        "id": 43,
        "question": "在社交活动中，你通常：",
        "options": [
            {
                "text": "积极参与并享受热闹",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "更喜欢安静的小范围交流",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 44,
        "question": "你的工作环境通常是：",
        "options": [
            {
                "text": "整洁有序的",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "随性但有效率的",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 45,
        "question": "你的价值观更偏向：",
        "options": [
            {
                "text": "公正和真理",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "和谐和同情",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "question": "你的时间管理风格是：",
        "options": [
            {
                "text": "严格按时间表执行",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "大致安排，灵活调整",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 46
    },
    {
        "question": "看待问题时，你倾向于：",
        "options": [
            {
                "text": "基于事实和经验分析",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "探索新的可能性和创意",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 47
    },
    {
        "id": 48,
        "question": "面对选择时，你更可能：",
        "options": [
            {
                "text": "做出明确选择",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "保留多种可能性",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "question": "认识新朋友时，你更可能：",
        "options": [
            {
                "text": "主动开启话题，热情交流",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "保持礼貌，等待对方先开口",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 49
    },
    {
        "id": 50,
        "question": "周末你更喜欢：",
        "options": [
            {
                "text": "安排丰富的社交活动",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "享受安静的私人时间",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "question": "面对冲突时，你倾向于：",
        "options": [
            {
                "text": "就事论事，分析问题本质",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "维护和谐，考虑各方感受",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 51
    },
    {
        "question": "处理工作任务时，你倾向于：",
        "options": [
            {
                "text": "提前规划，按时完成",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "灵活应对，在压力下效率更高",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 52
    },
    {
        "id": 53,
        "question": "处理工作时，你更关注：",
        "options": [
            {
                "text": "任务完成的质量",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "团队合作的氛围",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 54,
        "question": "你更擅长：",
        "options": [
            {
                "text": "执行具体的任务",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "构思抽象的概念",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "question": "记忆信息时，你更容易记住：",
        "options": [
            {
                "text": "具体的数字、日期和细节",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "整体的模式和关联",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 55
    },
    {
        "question": "安排假期时，你倾向于：",
        "options": [
            {
                "text": "制定详细的行程计划",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "大致安排，留出自由发挥空间",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 56
    },
    {
        "id": 57,
        "question": "你的能量主要来自：",
        "options": [
            {
                "text": "与外界互动和社交",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独处和内省",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "question": "处理人际关系时，你更倾向于：",
        "options": [
            {
                "text": "明确界限和原则",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "维护和谐和情感联系",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 58
    },
    {
        "question": "做计划时，你更关注：",
        "options": [
            {
                "text": "具体的实施步骤和时间表",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "整体的目标和愿景",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 59
    },
    {
        "id": 60,
        "question": "完成任务时，你倾向于：",
        "options": [
            {
                "text": "提前完成避免拖延",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "在截止日期前完成",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "question": "选择礼物时，你更看重：",
        "options": [
            {
                "text": "实用性和具体功能",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "象征意义和情感价值",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 61
    },
    {
        "question": "与人交流时，你更倾向于：",
        "options": [
            {
                "text": "谈论具体的经历和事实",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "讨论抽象的想法和理论",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 62
    },
    {
        "question": "选择职业时，你更考虑：",
        "options": [
            {
                "text": "发展前景和薪资待遇",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "工作意义和团队氛围",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 63
    },
    {
        "id": 64,
        "question": "做计划时，你更关注：",
        "options": [
            {
                "text": "具体的实施步骤",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "整体的愿景目标",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "id": 65,
        "question": "描述事物时，你倾向于：",
        "options": [
            {
                "text": "使用具体细节和实例",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "使用比喻和象征",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "question": "评价艺术作品时，你更注重：",
        "options": [
            {
                "text": "技巧和细节表现",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "情感表达和深层含义",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 66
    },
    {
        "question": "做决定时，你更愿意：",
        "options": [
            {
                "text": "尽快做出明确决定",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "保持开放，收集更多信息",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 67
    },
    {
        "question": "周末安排活动时，你倾向于：",
        "options": [
            {
                "text": "安排丰富的社交聚会",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "享受安静的私人时光",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 68
    },
    {
        "question": "学习新东西时，你更喜欢：",
        "options": [
            {
                "text": "系统性地按计划学习",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "根据兴趣跳跃式学习",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 69
    },
    {
        "question": "购物时，你更倾向于：",
        "options": [
            {
                "text": "有明确目标，快速完成",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "随意浏览，发现惊喜",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 70
    },
    {
        "id": 71,
        "question": "你的时间管理风格是：",
        "options": [
            {
                "text": "详细规划时间",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "大致安排灵活应对",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 72,
        "question": "当你需要思考问题时，你倾向于：",
        "options": [
            {
                "text": "通过与人讨论来理清思路",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独自思考并整理想法",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "question": "在团队项目中，你更擅长：",
        "options": [
            {
                "text": "协调沟通，带动团队氛围",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "深入研究，提供专业建议",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 73
    },
    {
        "id": 74,
        "question": "评价他人时，你更看重：",
        "options": [
            {
                "text": "能力和效率",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "善意和动机",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 75,
        "question": "学习知识时，你更重视：",
        "options": [
            {
                "text": "理论的严谨性",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "应用的关怀性",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 76,
        "question": "帮助他人时，你更倾向于：",
        "options": [
            {
                "text": "提供实际的解决方案",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "给予情感的支持",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "id": 77,
        "question": "认识新朋友时，你通常：",
        "options": [
            {
                "text": "主动介绍自己并开启话题",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "等待对方先开口或观察",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 78,
        "question": "当你感到兴奋时，你更想：",
        "options": [
            {
                "text": "立刻与他人分享",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "先自己品味这份感受",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "question": "旅行时，你更享受：",
        "options": [
            {
                "text": "体验具体的景点和活动",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "感受当地的文化和氛围",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 79
    },
    {
        "id": 80,
        "question": "面对压力时，你更可能：",
        "options": [
            {
                "text": "找朋友倾诉寻求支持",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独自处理情绪和问题",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "question": "你的社交能量主要来自：",
        "options": [
            {
                "text": "与人互动和外部刺激",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独处和内省的时间",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 81
    },
    {
        "id": 82,
        "question": "组织活动时，你更注重：",
        "options": [
            {
                "text": "结构和流程",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "自由和创意",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "question": "当你遇到有趣的事情时，你第一时间想：",
        "options": [
            {
                "text": "立刻分享给朋友或家人",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "先自己品味和思考",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 83
    },
    {
        "id": 84,
        "question": "在工作环境中，你倾向于：",
        "options": [
            {
                "text": "开放式办公，便于交流",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独立空间，减少干扰",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ]
    },
    {
        "id": 85,
        "question": "做决定时，你更重视：",
        "options": [
            {
                "text": "逻辑和客观标准",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "情感和人际关系",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "question": "面对压力时，你更可能：",
        "options": [
            {
                "text": "找朋友倾诉寻求支持",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "独自思考解决方案",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 86
    },
    {
        "id": 87,
        "question": "表达观点时，你更注重：",
        "options": [
            {
                "text": "逻辑的连贯性",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "情感的共鸣",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "question": "给予他人反馈时，你更注重：",
        "options": [
            {
                "text": "事实的准确性和建设性",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "对方的感受和接受程度",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 88
    },
    {
        "question": "做重要决定时，你更重视：",
        "options": [
            {
                "text": "逻辑分析和客观数据",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "个人感受和人际关系",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 89
    },
    {
        "question": "选择礼物时，你更看重：",
        "options": [
            {
                "text": "实用性和具体功能",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "象征意义和情感价值",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ],
        "id": 90
    },
    {
        "question": "在工作会议中，你通常：",
        "options": [
            {
                "text": "积极发言，表达自己的想法",
                "type": "E",
                "score_e": 1,
                "score_i": 0
            },
            {
                "text": "先倾听，思考成熟后再发言",
                "type": "I",
                "score_e": 0,
                "score_i": 1
            }
        ],
        "id": 91
    },
    {
        "question": "制定规则时，你更注重：",
        "options": [
            {
                "text": "公平和一致性",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "灵活性和人性化",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 92
    },
    {
        "id": 93,
        "question": "面对选择时，你更依赖：",
        "options": [
            {
                "text": "理性的分析",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "内心的感受",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ]
    },
    {
        "question": "制定规则时，你更注重：",
        "options": [
            {
                "text": "公平和一致性",
                "type": "T",
                "score_t": 1,
                "score_f": 0
            },
            {
                "text": "灵活性和人性化",
                "type": "F",
                "score_t": 0,
                "score_f": 1
            }
        ],
        "id": 94
    },
    {
        "id": 95,
        "question": "处理信息时，你倾向于：",
        "options": [
            {
                "text": "快速分类做决定",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "持续收集新信息",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 96,
        "question": "做决定时，你更愿意：",
        "options": [
            {
                "text": "尽快做出决定",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "保持开放收集信息",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 97,
        "question": "学习时，你更喜欢：",
        "options": [
            {
                "text": "按步骤操作练习",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "理解背后的原理",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    },
    {
        "question": "购物时，你更倾向于：",
        "options": [
            {
                "text": "有明确目标，快速完成",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "随意浏览，发现惊喜",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ],
        "id": 98
    },
    {
        "id": 99,
        "question": "你的决策过程更偏向：",
        "options": [
            {
                "text": "结论导向",
                "type": "J",
                "score_j": 1,
                "score_p": 0
            },
            {
                "text": "过程导向",
                "type": "P",
                "score_j": 0,
                "score_p": 1
            }
        ]
    },
    {
        "id": 100,
        "question": "看待世界时，你更注重：",
        "options": [
            {
                "text": "现实和实际存在",
                "type": "S",
                "score_s": 1,
                "score_n": 0
            },
            {
                "text": "潜力和发展趋势",
                "type": "N",
                "score_s": 0,
                "score_n": 1
            }
        ]
    }
]

class MBTIServer(BaseHTTPRequestHandler):
    """MBTI测试服务器处理器"""
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nickname TEXT NOT NULL,
                gender TEXT NOT NULL,
                age INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建测试记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                test_id TEXT NOT NULL,
                mbti_type TEXT,
                status TEXT DEFAULT 'in_progress',
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # 创建答案详情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_record_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                answer TEXT NOT NULL,
                score_e INTEGER DEFAULT 0,
                score_i INTEGER DEFAULT 0,
                score_s INTEGER DEFAULT 0,
                score_n INTEGER DEFAULT 0,
                score_t INTEGER DEFAULT 0,
                score_f INTEGER DEFAULT 0,
                score_j INTEGER DEFAULT 0,
                score_p INTEGER DEFAULT 0,
                FOREIGN KEY (test_record_id) REFERENCES test_records (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password):
        """哈希密码"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password, password_hash):
        """验证密码"""
        return self._hash_password(password) == password_hash
    
    def _generate_token(self, user_id, username):
        """生成JWT令牌"""
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    def _verify_token(self, token):
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except:
            return None
    
    def _get_user_from_token(self):
        """从请求头获取用户信息"""
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        payload = self._verify_token(token)
        if not payload:
            return None
        
        return payload
    
    def _send_response(self, status_code, data=None, message=None):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        response = {}
        if message:
            response['message'] = message
        if data is not None:
            response.update(data)
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
    
    def _send_error(self, status_code, message):
        """发送错误响应"""
        self._send_response(status_code, message=message)
    
    def _send_success(self, data=None, message="操作成功"):
        """发送成功响应"""
        self._send_response(200, data, message)
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 静态文件服务
        if path == '/' or path.endswith('.html') or path.endswith('.js') or path.endswith('.css'):
            self._serve_static_file(path)
            return
        
        # API路由
        if path == '/api/test/questions':
            self._get_questions()
        elif path == '/api/test/instructions':
            self._get_instructions()
        elif path == '/api/test/history':
            self._get_test_history()
        elif path == '/api/test/continue':
            self._get_continue_test()
        elif path == '/api/user/profile':
            self._get_user_profile()
        elif path == '/api/test/analysis':
            self._get_test_analysis()
        elif path == '/api/analytics/overview':
            self._get_analytics_overview()
        elif path == '/api/analytics/mbti-distribution':
            self._get_mbti_distribution()
        elif path == '/api/analytics/dimension-distribution':
            self._get_dimension_distribution()
        elif path == '/api/analytics/question-stats':
            self._get_question_stats()
        elif path == '/api/analytics/trends':
            self._get_analytics_trends()
        elif path == '/api/analytics/completion-rate':
            self._get_completion_rate()
        elif path == '/api/analytics/demographics':
            self._get_demographics()
        else:
            self._send_error(404, "接口不存在")
    
    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
            except:
                data = {}
        else:
            data = {}
        
        if path == '/api/register':
            self._register_user(data)
        elif path == '/api/login':
            self._login_user(data)
        elif path == '/api/test/start':
            self._start_test(data)
        elif path == '/api/test/submit':
            self._submit_test(data)
        else:
            self._send_error(404, "接口不存在")
    
    def do_PUT(self):
        """处理PUT请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
            except:
                data = {}
        else:
            data = {}
        
        if path == '/api/user/profile':
            self._update_user_profile(data)
        else:
            self._send_error(404, "接口不存在")
    
    def _serve_static_file(self, path):
        """提供静态文件"""
        if path == '/':
            file_path = 'index.html'
        else:
            file_path = path.lstrip('/')
        
        # 默认文件
        if not os.path.exists(file_path):
            if path == '/':
                file_path = 'login.html'
            elif path == '/login.html':
                file_path = 'login.html'
            elif path == '/test.html':
                file_path = 'test.html'
            else:
                self._send_error(404, "文件不存在")
                return
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 设置Content-Type
            if file_path.endswith('.html'):
                content_type = 'text/html'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except:
            self._send_error(500, "文件读取失败")
    
    def _register_user(self, data):
        """用户注册"""
        required_fields = ['username', 'password', 'nickname', 'gender', 'age']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                self._send_error(400, f"缺少必填字段: {field}")
                return
        
        username = data['username'].strip()
        password = data['password']
        nickname = data['nickname'].strip()
        gender = data['gender'].strip()
        
        try:
            age = int(data['age'])
            if age < 1 or age > 120:
                raise ValueError
        except:
            self._send_error(400, "年龄必须是1-120之间的整数")
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 检查用户名是否已存在
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                self._send_error(400, "用户名已存在")
                return
            
            # 插入新用户
            password_hash = self._hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, nickname, gender, age)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, nickname, gender, age))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # 生成令牌
            token = self._generate_token(user_id, username)
            
            self._send_success({
                'user_id': user_id,
                'username': username,
                'nickname': nickname,
                'token': token
            }, "注册成功")
        except Exception as e:
            self._send_error(500, f"注册失败: {str(e)}")
        finally:
            conn.close()
    
    def _login_user(self, data):
        """用户登录"""
        if 'username' not in data or 'password' not in data:
            self._send_error(400, "需要用户名和密码")
            return
        
        username = data['username'].strip()
        password = data['password']
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, username, password_hash, nickname, gender, age 
                FROM users WHERE username = ?
            ''', (username,))
            user = cursor.fetchone()
            
            if not user:
                self._send_error(401, "用户名或密码错误")
                return
            
            user_id, db_username, password_hash, nickname, gender, age = user
            
            if not self._verify_password(password, password_hash):
                self._send_error(401, "用户名或密码错误")
                return
            
            # 生成令牌
            token = self._generate_token(user_id, username)
            
            self._send_success({
                'user_id': user_id,
                'username': username,
                'nickname': nickname,
                'gender': gender,
                'age': age,
                'token': token
            }, "登录成功")
        except Exception as e:
            self._send_error(500, f"登录失败: {str(e)}")
        finally:
            conn.close()
    
    def _get_questions(self):
        """获取测试题目"""
        # 检查认证
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        # 返回题目（简化版，只返回必要信息）
        questions_for_client = []
        for q in MBTI_QUESTIONS:
            question_data = {
                'id': q['id'],
                'question': q['question'],
                'options': [{'text': opt['text'], 'type': opt['type']} for opt in q['options']]
            }
            questions_for_client.append(question_data)
        
        self._send_success({
            'questions': questions_for_client,
            'total': len(questions_for_client)
        })
    
    def _get_instructions(self):
        """获取测试说明"""
        instructions = {
            'title': 'MBTI性格测试',
            'description': '本测试基于经典的MBTI理论，通过16道题目帮助您了解自己的性格类型。',
            'steps': [
                '仔细阅读每道题目',
                '选择最符合您实际情况的选项',
                '请根据第一感觉选择，不要过多思考',
                '完成所有题目后提交，查看您的MBTI类型和分析'
            ],
            'duration': '约5-10分钟',
            'questions_count': len(MBTI_QUESTIONS)
        }
        self._send_success(instructions)
    
    def _get_test_history(self):
        """获取测试历史"""
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        user_id = user['user_id']
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, test_id, mbti_type, status, start_time, end_time
                FROM test_records 
                WHERE user_id = ? 
                ORDER BY start_time DESC
                LIMIT 10
            ''', (user_id,))
            
            records = []
            for row in cursor.fetchall():
                record_id, test_id, mbti_type, status, start_time, end_time = row
                records.append({
                    'id': record_id,
                    'test_id': test_id,
                    'mbti_type': mbti_type,
                    'status': status,
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': self._calculate_duration(start_time, end_time) if end_time else None
                })
            
            self._send_success({'records': records})
        except Exception as e:
            self._send_error(500, f"获取历史失败: {str(e)}")
        finally:
            conn.close()
    
    def _get_continue_test(self):
        """继续未完成的测试"""
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        user_id = user['user_id']
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 查找未完成的测试
            cursor.execute('''
                SELECT tr.id, tr.test_id, tr.start_time
                FROM test_records tr
                WHERE tr.user_id = ? AND tr.status = 'in_progress'
                ORDER BY tr.start_time DESC
                LIMIT 1
            ''', (user_id,))
            
            record = cursor.fetchone()
            
            if record:
                record_id, test_id, start_time = record
                
                # 获取已答题目
                cursor.execute('''
                    SELECT question_id, answer 
                    FROM answers 
                    WHERE test_record_id = ?
                    ORDER BY question_id
                ''', (record_id,))
                
                answered = {row[0]: row[1] for row in cursor.fetchall()}
                
                self._send_success({
                    'test_id': test_id,
                    'record_id': record_id,
                    'start_time': start_time,
                    'answered': answered,
                    'can_continue': True
                })
            else:
                self._send_success({
                    'can_continue': False,
                    'message': '没有未完成的测试'
                })
        except Exception as e:
            self._send_error(500, f"检查继续测试失败: {str(e)}")
        finally:
            conn.close()
    
    def _get_user_profile(self):
        """获取用户信息"""
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        user_id = user['user_id']
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT username, nickname, gender, age, created_at
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user_data = cursor.fetchone()
            if user_data:
                username, nickname, gender, age, created_at = user_data
                
                # 获取测试统计
                cursor.execute('''
                    SELECT COUNT(*) as total_tests,
                           COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tests,
                           COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_tests
                    FROM test_records WHERE user_id = ?
                ''', (user_id,))
                
                stats = cursor.fetchone()
                total_tests, completed_tests, in_progress_tests = stats
                
                self._send_success({
                    'username': username,
                    'nickname': nickname,
                    'gender': gender,
                    'age': age,
                    'created_at': created_at,
                    'stats': {
                        'total_tests': total_tests,
                        'completed_tests': completed_tests,
                        'in_progress_tests': in_progress_tests
                    }
                })
            else:
                self._send_error(404, "用户不存在")
        except Exception as e:
            self._send_error(500, f"获取用户信息失败: {str(e)}")
        finally:
            conn.close()
    
    def _update_user_profile(self, data):
        """更新用户信息"""
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        user_id = user['user_id']
        
        # 检查可更新字段
        updatable_fields = ['nickname', 'gender', 'age']
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                if field == 'age':
                    try:
                        age = int(data[field])
                        if age < 1 or age > 120:
                            raise ValueError
                        update_data[field] = age
                    except:
                        self._send_error(400, "年龄必须是1-120之间的整数")
                        return
                else:
                    value = str(data[field]).strip()
                    if value:
                        update_data[field] = value
        
        if not update_data:
            self._send_error(400, "没有可更新的字段")
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 构建更新语句
            set_clause = ', '.join([f"{field} = ?" for field in update_data.keys()])
            values = list(update_data.values())
            values.append(user_id)
            
            cursor.execute(f'''
                UPDATE users SET {set_clause} WHERE id = ?
            ''', values)
            
            if cursor.rowcount > 0:
                conn.commit()
                self._send_success(message="用户信息更新成功")
            else:
                self._send_error(404, "用户不存在")
        except Exception as e:
            self._send_error(500, f"更新用户信息失败: {str(e)}")
        finally:
            conn.close()
    
    def _start_test(self, data):
        """开始测试"""
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        user_id = user['user_id']
        
        # 生成测试ID
        test_id = f"test_{int(time.time())}_{secrets.token_hex(4)}"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 创建测试记录
            cursor.execute('''
                INSERT INTO test_records (user_id, test_id, status)
                VALUES (?, ?, 'in_progress')
            ''', (user_id, test_id))
            
            record_id = cursor.lastrowid
            conn.commit()
            
            self._send_success({
                'test_id': test_id,
                'record_id': record_id,
                'questions_count': len(MBTI_QUESTIONS),
                'message': '测试已开始'
            })
        except Exception as e:
            self._send_error(500, f"开始测试失败: {str(e)}")
        finally:
            conn.close()
    
    def _submit_test(self, data):
        """提交测试答案"""
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        user_id = user['user_id']
        
        if 'record_id' not in data or 'answers' not in data:
            self._send_error(400, "需要测试记录ID和答案")
            return
        
        record_id = data['record_id']
        answers = data['answers']
        
        # 验证答案格式
        if not isinstance(answers, dict):
            self._send_error(400, "答案格式不正确")
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 验证测试记录属于当前用户
            cursor.execute('''
                SELECT id, status FROM test_records 
                WHERE id = ? AND user_id = ?
            ''', (record_id, user_id))
            
            record = cursor.fetchone()
            if not record:
                self._send_error(404, "测试记录不存在")
                return
            
            if record[1] == 'completed':
                self._send_error(400, "测试已完成，不能重复提交")
                return
            
            # 计算MBTI类型
            scores = {
                'E': 0, 'I': 0,
                'S': 0, 'N': 0,
                'T': 0, 'F': 0,
                'J': 0, 'P': 0
            }
            
            # 保存答案并计算分数
            for question_id_str, answer in answers.items():
                try:
                    question_id = int(question_id_str)
                except:
                    continue
                
                # 查找题目
                question = None
                for q in MBTI_QUESTIONS:
                    if q['id'] == question_id:
                        question = q
                        break
                
                if not question:
                    continue
                
                # 查找选项
                option = None
                for opt in question['options']:
                    if opt['text'] == answer:
                        option = opt
                        break
                
                if not option:
                    continue
                
                # 保存答案
                cursor.execute('''
                    INSERT INTO answers (
                        test_record_id, question_id, answer,
                        score_e, score_i, score_s, score_n,
                        score_t, score_f, score_j, score_p
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record_id, question_id, answer,
                    option.get('score_e', 0), option.get('score_i', 0),
                    option.get('score_s', 0), option.get('score_n', 0),
                    option.get('score_t', 0), option.get('score_f', 0),
                    option.get('score_j', 0), option.get('score_p', 0)
                ))
                
                # 累加分数
                for key in scores.keys():
                    score_key = f'score_{key.lower()}'
                    if score_key in option:
                        scores[key] += option[score_key]
            
            # 确定MBTI类型
            mbti_type = ''
            mbti_type += 'E' if scores['E'] > scores['I'] else 'I'
            mbti_type += 'S' if scores['S'] > scores['N'] else 'N'
            mbti_type += 'T' if scores['T'] > scores['F'] else 'F'
            mbti_type += 'J' if scores['J'] > scores['P'] else 'P'
            
            # 更新测试记录
            cursor.execute('''
                UPDATE test_records 
                SET mbti_type = ?, status = 'completed', end_time = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (mbti_type, record_id))
            
            conn.commit()
            
            # 获取分析报告
            analysis = self._generate_analysis(mbti_type, scores)
            
            self._send_success({
                'mbti_type': mbti_type,
                'scores': scores,
                'analysis': analysis,
                'record_id': record_id,
                'message': '测试提交成功'
            })
        except Exception as e:
            self._send_error(500, f"提交测试失败: {str(e)}")
        finally:
            conn.close()
    
    def _get_test_analysis(self):
        """获取测试分析"""
        user = self._get_user_from_token()
        if not user:
            self._send_error(401, "需要登录")
            return
        
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        record_id = query_params.get('record_id', [None])[0]
        if not record_id:
            self._send_error(400, "需要测试记录ID")
            return
        
        try:
            record_id = int(record_id)
        except:
            self._send_error(400, "测试记录ID格式不正确")
            return
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 验证测试记录属于当前用户
            cursor.execute('''
                SELECT tr.mbti_type, tr.start_time, tr.end_time
                FROM test_records tr
                WHERE tr.id = ? AND tr.user_id = ? AND tr.status = 'completed'
            ''', (record_id, user['user_id']))
            
            record = cursor.fetchone()
            if not record:
                self._send_error(404, "测试记录不存在或未完成")
                return
            
            mbti_type, start_time, end_time = record
            
            # 获取分数详情
            cursor.execute('''
                SELECT 
                    SUM(score_e) as total_e,
                    SUM(score_i) as total_i,
                    SUM(score_s) as total_s,
                    SUM(score_n) as total_n,
                    SUM(score_t) as total_t,
                    SUM(score_f) as total_f,
                    SUM(score_j) as total_j,
                    SUM(score_p) as total_p
                FROM answers WHERE test_record_id = ?
            ''', (record_id,))
            
            score_row = cursor.fetchone()
            scores = {
                'E': score_row[0] or 0, 'I': score_row[1] or 0,
                'S': score_row[2] or 0, 'N': score_row[3] or 0,
                'T': score_row[4] or 0, 'F': score_row[5] or 0,
                'J': score_row[6] or 0, 'P': score_row[7] or 0
            }
            
            # 生成分析报告
            analysis = self._generate_analysis(mbti_type, scores)
            
            self._send_success({
                'mbti_type': mbti_type,
                'scores': scores,
                'analysis': analysis,
                'start_time': start_time,
                'end_time': end_time,
                'duration': self._calculate_duration(start_time, end_time)
            })
        except Exception as e:
            self._send_error(500, f"获取分析失败: {str(e)}")
        finally:
            conn.close()
    
    def _generate_analysis(self, mbti_type, scores):
        """生成MBTI分析报告"""
        # MBTI类型描述
        type_descriptions = {
            'ISTJ': '检查员型 - 安静、严肃，通过全面性和可靠性获得成功。实际，有责任感。',
            'ISFJ': '照顾者型 - 安静、友好，有责任感和良知。坚定地致力于完成他们的义务。',
            'INFJ': '提倡者型 - 寻求思想、关系、物质等之间的意义和联系。有洞察力，对于如何更好地服务大众有清晰的远景。',
            'INTJ': '建筑师型 - 在实现自己的想法和达成自己的目标时有创新的想法和非凡的动力。',
            'ISTP': '鉴赏家型 - 灵活、忍耐力强，是个安静的观察者直到有问题发生，就会马上行动，找到实用的解决方法。',
            'ISFP': '探险家型 - 安静、友好、敏感、和善。享受当前。喜欢有自己的空间，喜欢能按照自己的时间表工作。',
            'INFP': '调解员型 - 理想主义，对于自己的价值观和自己觉得重要的人非常忠诚。希望外部的生活和自己内心的价值观是统一的。',
            'INTP': '逻辑学家型 - 对于自己感兴趣的任何事物都寻求找到合理的解释。喜欢理论和抽象的事情，喜欢理念思维多于社交活动。',
            'ESTP': '企业家型 - 灵活、忍耐力强，实际，注重结果。觉得理论和抽象的解释非常无趣。喜欢积极地采取行动解决问题。',
            'ESFP': '表演者型 - 外向、友好、接受力强。热爱生活、人类和物质上的享受。喜欢和别人一起将事情做成功。',
            'ENFP': '竞选者型 - 热情洋溢、富有想象力。认为人生有很多的可能性。能很快地将事情和信息联系起来，然后很自信地根据自己的判断解决问题。',
            'ENTP': '辩论家型 - 反应快、睿智，有激励别人的能力，警觉性强、直言不讳。',
            'ESTJ': '总经理型 - 实际、现实主义。果断，一旦下决心就会马上行动。善于将项目和人组织起来将事情完成，并尽可能用最有效率的方法得到结果。',
            'ESFJ': '执政官型 - 热心肠、有责任心、合作。希望周边的环境温馨而和谐，并为此果断地执行。喜欢和他人一起精确并及时地完成任务。',
            'ENFJ': '主人公型 - 热情、为他人着想、易感应、有责任心。非常注重他人的感情、需求和动机。善于发现他人的潜能，并希望能帮助他们实现。',
            'ENTJ': '指挥官型 - 坦诚、果断，有天生的领导能力。能很快看到公司/组织程序和政策中的不合理性和低效能性，发展并实施有效和全面的系统来解决问题。'
        }
        
        # 维度分析
        dimensions = []
        
        # E/I维度
        e_score = scores.get('E', 0)
        i_score = scores.get('I', 0)
        if e_score > i_score:
            dimensions.append({
                'dimension': '外向(E) vs 内向(I)',
                'result': '外向(E)',
                'score': f'E:{e_score} vs I:{i_score}',
                'description': '您更倾向于从外部世界获取能量，喜欢社交和表达。'
            })
        else:
            dimensions.append({
                'dimension': '外向(E) vs 内向(I)',
                'result': '内向(I)',
                'score': f'E:{e_score} vs I:{i_score}',
                'description': '您更倾向于从内心世界获取能量，喜欢独处和思考。'
            })
        
        # S/N维度
        s_score = scores.get('S', 0)
        n_score = scores.get('N', 0)
        if s_score > n_score:
            dimensions.append({
                'dimension': '实感(S) vs 直觉(N)',
                'result': '实感(S)',
                'score': f'S:{s_score} vs N:{n_score}',
                'description': '您更关注具体事实和细节，注重实际经验。'
            })
        else:
            dimensions.append({
                'dimension': '实感(S) vs 直觉(N)',
                'result': '直觉(N)',
                'score': f'S:{s_score} vs N:{n_score}',
                'description': '您更关注可能性和模式，注重想象和理论。'
            })
        
        # T/F维度
        t_score = scores.get('T', 0)
        f_score = scores.get('F', 0)
        if t_score > f_score:
            dimensions.append({
                'dimension': '思考(T) vs 情感(F)',
                'result': '思考(T)',
                'score': f'T:{t_score} vs F:{f_score}',
                'description': '您做决定时更注重逻辑和客观分析。'
            })
        else:
            dimensions.append({
                'dimension': '思考(T) vs 情感(F)',
                'result': '情感(F)',
                'score': f'T:{t_score} vs F:{f_score}',
                'description': '您做决定时更注重价值观和人际关系。'
            })
        
        # J/P维度
        j_score = scores.get('J', 0)
        p_score = scores.get('P', 0)
        if j_score > p_score:
            dimensions.append({
                'dimension': '判断(J) vs 感知(P)',
                'result': '判断(J)',
                'score': f'J:{j_score} vs P:{p_score}',
                'description': '您更喜欢有计划、有条理的生活方式。'
            })
        else:
            dimensions.append({
                'dimension': '判断(J) vs 感知(P)',
                'result': '感知(P)',
                'score': f'J:{j_score} vs P:{p_score}',
                'description': '您更喜欢灵活、适应性强的生活方式。'
            })
        
        return {
            'type': mbti_type,
            'description': type_descriptions.get(mbti_type, '未知类型'),
            'dimensions': dimensions,
            'career_suggestions': self._get_career_suggestions(mbti_type),
            'relationship_advice': self._get_relationship_advice(mbti_type)
        }
    
    def _get_career_suggestions(self, mbti_type):
        """获取职业建议"""
        suggestions = {
            'ISTJ': ['会计', '审计师', '行政人员', '工程师', '律师'],
            'ISFJ': ['护士', '教师', '社工', '图书馆员', '行政助理'],
            'INFJ': ['心理咨询师', '作家', '艺术家', '教师', '人力资源'],
            'INTJ': ['科学家', '工程师', '律师', '大学教授', '战略规划师'],
            'ISTP': ['技工', '工程师', '运动员', '警察', '飞行员'],
            'ISFP': ['艺术家', '设计师', '音乐家', '兽医', '园丁'],
            'INFP': ['作家', '心理咨询师', '艺术家', '社工', '编辑'],
            'INTP': ['科学家', '哲学家', '研究员', '程序员', '建筑师'],
            'ESTP': ['销售', '企业家', '运动员', '警察', '急救人员'],
            'ESFP': ['演员', '主持人', '销售', '旅游顾问', '活动策划'],
            'ENFP': ['记者', '心理咨询师', '教师', '公关', '创意总监'],
            'ENTP': ['企业家', '律师', '记者', '营销总监', '顾问'],
            'ESTJ': ['经理', '警察', '军官', '教师', '行政主管'],
            'ESFJ': ['护士', '教师', '社工', '人力资源', '客户服务'],
            'ENFJ': ['教师', '心理咨询师', '人力资源', '公关', '教练'],
            'ENTJ': ['CEO', '律师', '经理', '顾问', '政治家']
        }
        return suggestions.get(mbti_type, [])
    
    def _get_relationship_advice(self, mbti_type):
        """获取人际关系建议"""
        advice = {
            'ISTJ': '在关系中需要稳定和可靠性，表达感情时可能比较含蓄。',
            'ISFJ': '非常体贴和关心他人，但需要被感激和认可。',
            'INFJ': '寻求深层次的精神连接，需要独处时间来充电。',
            'INTJ': '重视智慧和能力，在关系中需要智力刺激和独立性。',
            'ISTP': '喜欢自由和冒险，需要空间和实际行动而非空谈。',
            'ISFP': '敏感而艺术，需要被理解和欣赏其独特性。',
            'INFP': '理想主义且忠诚，需要价值观的一致性和情感深度。',
            'INTP': '理性而独立，需要智力自由和尊重其思考空间。',
            'ESTP': '活跃而实际，喜欢新鲜刺激，需要行动和自由。',
            'ESFP': '热情而友好，喜欢社交，需要被关注和欣赏。',
            'ENFP': '热情而有创意，需要变化和深层次的情感连接。',
            'ENTP': '聪明而好奇，需要智力挑战和辩论的机会。',
            'ESTJ': '务实而有组织，需要效率和明确的期望。',
            'ESFJ': '温暖而负责，需要和谐和相互支持的关系。',
            'ENFJ': '富有同情心和领导力，需要被需要和情感连接。',
            'ENTJ': '果断而有远见，需要尊重和共同成长的机会。'
        }
        return advice.get(mbti_type, '')
    
    def _calculate_duration(self, start_time, end_time):
        """计算持续时间"""
        if not start_time or not end_time:
            return None
        
        try:
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            duration = end - start
            
            # 转换为分钟
            total_seconds = duration.total_seconds()
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            
            return f"{minutes}分{seconds}秒"
        except:
            return None


    def _get_analytics_overview(self):
        """概览统计"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 总用户数
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            # 总测试次数
            cursor.execute("SELECT COUNT(*) FROM test_records")
            total_tests = cursor.fetchone()[0]
            
            # 已完成测试次数
            cursor.execute("SELECT COUNT(*) FROM test_records WHERE status = 'completed'")
            completed_tests = cursor.fetchone()[0]
            
            # 平均完成时间（秒）
            cursor.execute("""
                SELECT AVG(
                    (julianday(end_time) - julianday(start_time)) * 86400
                ) FROM test_records 
                WHERE status = 'completed' AND end_time IS NOT NULL
            """)
            avg_duration = cursor.fetchone()[0]
            avg_duration_str = f"{int(avg_duration // 60)}分{int(avg_duration % 60)}秒" if avg_duration else "0 分 0 秒"
            
            # 今日新增用户
            cursor.execute("""
                SELECT COUNT(*) FROM users 
                WHERE DATE(created_at) = DATE('now', 'localtime')
            """)
            today_new_users = cursor.fetchone()[0]
            
            # 今日测试次数
            cursor.execute("""
                SELECT COUNT(*) FROM test_records 
                WHERE DATE(start_time) = DATE('now', 'localtime')
            """)
            today_tests = cursor.fetchone()[0]
            
            self._send_success({
                'total_users': total_users,
                'total_tests': total_tests,
                'completed_tests': completed_tests,
                'avg_completion_time': avg_duration_str,
                'today_new_users': today_new_users,
                'today_tests': today_tests
            })
        except Exception as e:
            self._send_error(500, f"获取概览统计失败：{str(e)}")
        finally:
            conn.close()
    
    def _get_mbti_distribution(self):
        """MBTI 类型分布"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            
            start_date = query_params.get('start_date', [None])[0]
            end_date = query_params.get('end_date', [None])[0]
            
            # 构建查询条件
            where_clause = "WHERE status = 'completed' AND mbti_type IS NOT NULL"
            if start_date:
                where_clause += f" AND DATE(end_time) >= DATE('{start_date}')"
            if end_date:
                where_clause += f" AND DATE(end_time) <= DATE('{end_date}')"
            
            # 获取总数
            cursor.execute(f"SELECT COUNT(*) FROM test_records {where_clause}")
            total = cursor.fetchone()[0]
            
            # 获取各类型分布
            cursor.execute(f"""
                SELECT mbti_type, COUNT(*) as count 
                FROM test_records 
                {where_clause}
                GROUP BY mbti_type 
                ORDER BY count DESC
            """)
            
            distribution = []
            mbti_types = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP',
                         'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']
            
            type_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            for mbti_type in mbti_types:
                count = type_counts.get(mbti_type, 0)
                percentage = round(count / total * 100, 2) if total > 0 else 0
                distribution.append({
                    'type': mbti_type,
                    'count': count,
                    'percentage': percentage
                })
            
            self._send_success({
                'total': total,
                'distribution': distribution,
                'filter': {
                    'start_date': start_date,
                    'end_date': end_date
                }
            })
        except Exception as e:
            self._send_error(500, f"获取 MBTI 分布失败：{str(e)}")
        finally:
            conn.close()
    
    def _get_dimension_distribution(self):
        """四维度分布"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 计算各维度分数总和
            cursor.execute("""
                SELECT 
                    SUM(score_e) as total_e,
                    SUM(score_i) as total_i,
                    SUM(score_s) as total_s,
                    SUM(score_n) as total_n,
                    SUM(score_t) as total_t,
                    SUM(score_f) as total_f,
                    SUM(score_j) as total_j,
                    SUM(score_p) as total_p
                FROM answers
            """)
            
            row = cursor.fetchone()
            total_e = row[0] or 0
            total_i = row[1] or 0
            total_s = row[2] or 0
            total_n = row[3] or 0
            total_t = row[4] or 0
            total_f = row[5] or 0
            total_j = row[6] or 0
            total_p = row[7] or 0
            
            # 计算各维度总数
            ei_total = total_e + total_i
            sn_total = total_s + total_n
            tf_total = total_t + total_f
            jp_total = total_j + total_p
            
            distribution = {
                'E_I': {
                    'E': {'count': total_e, 'percentage': round(total_e / ei_total * 100, 2) if ei_total > 0 else 0},
                    'I': {'count': total_i, 'percentage': round(total_i / ei_total * 100, 2) if ei_total > 0 else 0}
                },
                'S_N': {
                    'S': {'count': total_s, 'percentage': round(total_s / sn_total * 100, 2) if sn_total > 0 else 0},
                    'N': {'count': total_n, 'percentage': round(total_n / sn_total * 100, 2) if sn_total > 0 else 0}
                },
                'T_F': {
                    'T': {'count': total_t, 'percentage': round(total_t / tf_total * 100, 2) if tf_total > 0 else 0},
                    'F': {'count': total_f, 'percentage': round(total_f / tf_total * 100, 2) if tf_total > 0 else 0}
                },
                'J_P': {
                    'J': {'count': total_j, 'percentage': round(total_j / jp_total * 100, 2) if jp_total > 0 else 0},
                    'P': {'count': total_p, 'percentage': round(total_p / jp_total * 100, 2) if jp_total > 0 else 0}
                }
            }
            
            self._send_success({'distribution': distribution})
        except Exception as e:
            self._send_error(500, f"获取维度分布失败：{str(e)}")
        finally:
            conn.close()
    
    def _get_question_stats(self):
        """题目分析"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 获取每道题的选项分布
            cursor.execute("""
                SELECT question_id, answer, COUNT(*) as count 
                FROM answers 
                GROUP BY question_id, answer 
                ORDER BY question_id, count DESC
            """)
            
            question_stats = {}
            for row in cursor.fetchall():
                question_id = row[0]
                answer = row[1]
                count = row[2]
                
                if question_id not in question_stats:
                    question_stats[question_id] = {'question_id': question_id, 'options': []}
                
                question_stats[question_id]['options'].append({
                    'answer': answer,
                    'count': count
                })
            
            # 添加题目文本
            for q_id in question_stats:
                for q in MBTI_QUESTIONS:
                    if q['id'] == q_id:
                        question_stats[q_id]['question'] = q['question']
                        break
            
            self._send_success({
                'total_questions': len(question_stats),
                'stats': list(question_stats.values())
            })
        except Exception as e:
            self._send_error(500, f"获取题目统计失败：{str(e)}")
        finally:
            conn.close()
    
    def _get_analytics_trends(self):
        """时间趋势"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            
            days = int(query_params.get('days', ['7'])[0])
            
            # 获取每日趋势
            cursor.execute(f"""
                SELECT DATE(start_time) as date, COUNT(*) as count 
                FROM test_records 
                WHERE DATE(start_time) >= DATE('now', 'localtime', '-{days} days')
                GROUP BY DATE(start_time)
                ORDER BY date
            """)
            
            test_trends = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # 获取每日注册趋势
            cursor.execute(f"""
                SELECT DATE(created_at) as date, COUNT(*) as count 
                FROM users 
                WHERE DATE(created_at) >= DATE('now', 'localtime', '-{days} days')
                GROUP BY DATE(created_at)
                ORDER BY date
            """)
            
            register_trends = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # 获取每日完成趋势
            cursor.execute(f"""
                SELECT DATE(end_time) as date, COUNT(*) as count 
                FROM test_records 
                WHERE status = 'completed' 
                AND DATE(end_time) >= DATE('now', 'localtime', '-{days} days')
                GROUP BY DATE(end_time)
                ORDER BY date
            """)
            
            completion_trends = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            self._send_success({
                'days': days,
                'register_trends': register_trends,
                'test_trends': test_trends,
                'completion_trends': completion_trends
            })
        except Exception as e:
            self._send_error(500, f"获取趋势数据失败：{str(e)}")
        finally:
            conn.close()
    
    def _get_completion_rate(self):
        """完成率分析"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 总测试数
            cursor.execute("SELECT COUNT(*) FROM test_records")
            total_tests = cursor.fetchone()[0] or 0
            
            # 完成测试数
            cursor.execute("SELECT COUNT(*) FROM test_records WHERE status = 'completed'")
            completed_tests = cursor.fetchone()[0] or 0
            
            # 未完成测试数
            in_progress_tests = total_tests - completed_tests
            
            # 完成率
            completion_rate = round(completed_tests / total_tests * 100, 2) if total_tests > 0 else 0
            
            # 未完成测试的平均答题数
            cursor.execute("""
                SELECT AVG(answer_count) FROM (
                    SELECT test_record_id, COUNT(*) as answer_count 
                    FROM answers 
                    GROUP BY test_record_id
                ) WHERE test_record_id IN (
                    SELECT id FROM test_records WHERE status = 'in_progress'
                )
            """)
            avg_answers_incomplete = cursor.fetchone()[0] or 0
            
            # 放弃率（未完成的比例）
            abandonment_rate = round(in_progress_tests / total_tests * 100, 2) if total_tests > 0 else 0
            
            self._send_success({
                'total_tests': total_tests,
                'completed_tests': completed_tests,
                'in_progress_tests': in_progress_tests,
                'completion_rate': completion_rate,
                'avg_answers_incomplete': round(avg_answers_incomplete, 2),
                'abandonment_rate': abandonment_rate
            })
        except Exception as e:
            self._send_error(500, f"获取完成率分析失败：{str(e)}")
        finally:
            conn.close()
    
    def _get_demographics(self):
        """用户画像"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # 年龄分布
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN age < 18 THEN '18 岁以下'
                        WHEN age BETWEEN 18 AND 24 THEN '18-24 岁'
                        WHEN age BETWEEN 25 AND 34 THEN '25-34 岁'
                        WHEN age BETWEEN 35 AND 44 THEN '35-44 岁'
                        WHEN age BETWEEN 45 AND 54 THEN '45-54 岁'
                        WHEN age BETWEEN 55 AND 64 THEN '55-64 岁'
                        ELSE '65 岁以上'
                    END as age_group,
                    COUNT(*) as count
                FROM users
                GROUP BY age_group
                ORDER BY age_group
            """)
            
            age_distribution = [{'age_group': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            # 性别分布
            cursor.execute("""
                SELECT gender, COUNT(*) as count 
                FROM users 
                GROUP BY gender
            """)
            
            total_users = sum(row[1] for row in cursor.fetchall())
            
            # 重新查询以获取详细数据
            cursor.execute("""
                SELECT gender, COUNT(*) as count 
                FROM users 
                GROUP BY gender
            """)
            
            gender_distribution = []
            for row in cursor.fetchall():
                gender_distribution.append({
                    'gender': row[0],
                    'count': row[1],
                    'percentage': round(row[1] / total_users * 100, 2) if total_users > 0 else 0
                })
            
            self._send_success({
                'age_distribution': age_distribution,
                'gender_distribution': gender_distribution,
                'total_users': total_users
            })
        except Exception as e:
            self._send_error(500, f"获取用户画像失败：{str(e)}")
        finally:
            conn.close()

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nickname TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建测试记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            test_id TEXT NOT NULL,
            mbti_type TEXT,
            status TEXT DEFAULT 'in_progress',
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 创建答案详情表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_record_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            score_e INTEGER DEFAULT 0,
            score_i INTEGER DEFAULT 0,
            score_s INTEGER DEFAULT 0,
            score_n INTEGER DEFAULT 0,
            score_t INTEGER DEFAULT 0,
            score_f INTEGER DEFAULT 0,
            score_j INTEGER DEFAULT 0,
            score_p INTEGER DEFAULT 0,
            FOREIGN KEY (test_record_id) REFERENCES test_records (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("数据库表创建完成")

def main():
    """主函数"""
    print(f"正在启动MBTI测试服务器...")
    print(f"端口: {PORT}")
    print(f"数据库: {DB_FILE}")
    
    # 初始化数据库
    init_database()
    
    print("数据库初始化完成")
    print(f"题目数量: {len(MBTI_QUESTIONS)}")
    print("服务器正在启动...")
    
    try:
        httpd = HTTPServer(('0.0.0.0', PORT), MBTIServer)
        print(f"服务器已启动，访问 http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")

if __name__ == '__main__':
    main()
