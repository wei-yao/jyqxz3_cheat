#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金庸群侠传3 武功名称映射表
包含所有武功的ID和名称对应关系
"""

# 武功名称映射表 (根据游戏数据)
SKILL_NAMES = {
    # 暗器
    2: "弹指神通", 3: "腐尸毒", 4: "基本暗器", 5: "满天星", 6: "漫天花雨", 7: "慕容暗器", 8: "掷针术", 9: "青字九打",
    
    # 刀法
    10: "柴刀十八路", 11: "胡家残刀", 12: "胡家刀法", 13: "火焰刀", 14: "基本刀法", 15: "狂风刀法", 16: "慕容刀法", 17: "奇门三才刀", 18: "燃木刀法", 19: "五虎断刀门", 20: "修罗刀法", 21: "玄虚刀法", 22: "血刀刀法",
    
    # 棍法
    23: "打狗棍法", 24: "伏魔杖法", 25: "基本棍法", 26: "叫化棍法", 27: "金刚降魔杵", 28: "灵蛇杖法", 29: "慕容棍法", 30: "太祖棍", 31: "韦陀杖法", 32: "无上大力杵法",
    
    # 剑法
    33: "百变千幻云雾剑法", 34: "辟邪剑法", 35: "冰雪剑法", 36: "达摩剑法", 37: "独孤九剑", 38: "段家剑法", 39: "夺命连环三仙剑", 40: "华山剑法", 41: "回风拂柳剑", 42: "回风落雁剑", 43: "基本剑法", 44: "金蛇剑法", 45: "快慢十七路", 46: "狂风剑法", 47: "苗家剑法", 48: "灭绝剑法", 49: "慕容剑法", 50: "宁氏一剑", 51: "全真剑法", 52: "绕指柔剑", 53: "神门十三剑", 54: "松风剑法", 55: "太极剑法", 56: "太岳三青峰", 57: "躺尸剑法", 58: "万花剑法", 59: "五大夫剑", 60: "五岳剑法", 61: "玄铁剑法", 62: "玉女剑法", 63: "玉女素心剑", 64: "玉萧剑法", 65: "越女剑法",
    
    # 掌拳
    66: "黯然销魂掌", 67: "白虹掌", 68: "白驼雪山掌", 69: "般若掌", 70: "碧波清掌", 71: "冰蚕神掌", 72: "长拳", 73: "长拳", 74: "长拳", 75: "长拳", 76: "赤炼神掌", 77: "抽髓掌", 78: "春蚕掌法", 79: "摧心掌", 80: "大力金刚掌", 81: "寒冰绵掌", 82: "化骨绵掌", 83: "火焰刀", 84: "基本拳掌", 85: "降龙十八掌", 86: "金蛇游身掌", 87: "空明拳", 88: "灵蛇拳", 89: "罗汉拳", 90: "落英神剑掌", 91: "美女拳法", 92: "美女三招", 93: "绵掌", 94: "南山掌法", 95: "劈空掌", 96: "七伤拳", 97: "如来千叶手", 98: "三化聚顶掌", 99: "太极拳", 100: "天长掌法", 101: "天罗地网掌", 102: "天山六阳掌", 103: "天山折梅手", 104: "铁掌", 105: "铜锤手", 106: "五罗轻烟掌", 107: "五行六合掌", 108: "逍遥游(掌法)", 109: "须弥山掌", 110: "野狐拳法", 111: "英雄三招(拳法)", 112: "震山铁掌", 113: "重阳神掌",
    
    # 指法
    114: "参合指", 115: "大力金刚指", 116: "分筋错骨手(指法)", 117: "虎爪绝户手(指法)", 118: "基本指法", 119: "九阴白骨爪(指法)", 120: "兰花拂穴手", 121: "六脉神剑", 122: "龙爪功", 123: "拈花指", 124: "凝血神抓", 125: "千蛛万毒手", 126: "三阴蜈蚣爪", 127: "锁喉擒拿手", 128: "无相劫指", 129: "一阳指", 130: "鹰爪擒拿手",
    
    # 内功
    131: "八荒六合唯我独尊功", 132: "北冥真气", 133: "蛤蟆功", 134: "龟息功", 135: "化功大法", 136: "混元功", 137: "金刚不坏神功", 138: "九阳神功", 139: "自创", 140: "葵花神功", 141: "龙象般若功(13)", 142: "乾坤大挪移(6)", 143: "神龙心法", 144: "神照经", 145: "狮吼功", 146: "太玄经", 147: "吸星大法", 148: "小无相功", 149: "紫霞神功", 150: "闭穴术", 151: "纯阳无极功", 152: "斗转星移", 153: "段氏心法", 154: "峨眉九阳功", 155: "华山心法", 156: "叫化内功", 157: "逆转经脉", 158: "九阴真经心法", 159: "罗汉伏魔功", 160: "密宗内功", 161: "全真心法", 162: "少林九阳功", 163: "太极劲", 164: "桃花岛心法", 165: "武当功", 166: "先天功", 167: "易筋经", 168: "玉女心经", 169: "紫薇心法",
    
    # 身法/轻功
    170: "八步赶蟾", 171: "北斗仙踪", 172: "捕雀功", 173: "飞檐走壁", 174: "华山身法", 175: "金雁功", 176: "凌波微步", 177: "少林身法", 178: "神行百变", 179: "四象步法", 180: "踏雪无痕", 181: "梯云纵", 182: "一苇渡江"
}

# 按类别组织的武功列表，便于查询
SKILL_CATEGORIES = {
    "暗器": [2, 3, 4, 5, 6, 7, 8, 9],
    "刀法": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "棍法": [23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
    "剑法": [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65],
    "掌拳": [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
    "指法": [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130],
    "内功": [131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169],
    "身法/轻功": [170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182]
}

def get_skill_name(skill_id):
    """获取武功名称"""
    return SKILL_NAMES.get(skill_id, f"未知武功({skill_id})")

def get_skill_category(skill_id):
    """获取武功类别"""
    for category, skill_ids in SKILL_CATEGORIES.items():
        if skill_id in skill_ids:
            return category
    return "未知类别"

def get_skills_by_category(category):
    """根据类别获取武功列表"""
    skill_ids = SKILL_CATEGORIES.get(category, [])
    return {skill_id: SKILL_NAMES[skill_id] for skill_id in skill_ids if skill_id in SKILL_NAMES} 