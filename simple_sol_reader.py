#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的SOL文件读取器
不依赖pyamf，直接读取金庸群侠传3的SOL存档文件
"""

import os
import struct
import json

# 武功名称映射表
SKILL_NAMES = {
    # 基础武功
    1: "基本拳法", 2: "基本掌法", 3: "基本指法", 4: "基本爪法", 5: "基本腿法",
    6: "基本剑法", 7: "基本刀法", 8: "基本棍法", 9: "基本暗器", 10: "基本内功",
    
    # 全真派武功
    11: "全真心法", 12: "全真剑法", 13: "三花聚顶掌", 14: "重阳神掌", 15: "先天功",
    
    # 古墓派武功
    16: "玉女心经", 17: "玉女剑法", 18: "玉女素心剑法", 19: "美女拳法", 20: "天罗地网势",
    21: "捕雀功", 22: "掷针术", 23: "驱蜂术",
    
    # 少林派武功
    24: "少林心法", 25: "罗汉拳", 26: "韦陀掌", 27: "大力金刚掌", 28: "大力金刚指",
    29: "须弥山掌", 30: "拈花指", 31: "易筋经", 32: "洗髓经",
    
    # 武当派武功
    33: "武当心法", 34: "武当长拳", 35: "震山铁掌", 36: "绵掌", 37: "绕指柔剑",
    38: "神门十三剑", 39: "太极拳", 40: "太极剑法",
    
    # 华山派武功
    41: "华山心法", 42: "华山剑法", 43: "独孤九剑", 44: "紫霞神功", 45: "混元功",
    
    # 其他武功
    46: "降龙十八掌", 47: "打狗棒法", 48: "逍遥游", 49: "凌波微步", 50: "北冥神功",
    51: "化功大法", 52: "吸星大法", 53: "神照经", 54: "龟息功", 55: "八荒六合唯我独尊功",
    56: "辟邪剑法", 57: "葵花宝典", 58: "九阴真经", 59: "九阳神功", 60: "太玄经",
    61: "左右互搏", 62: "空明拳", 63: "黯然销魂掌", 64: "弹指神通", 65: "落英神剑掌",
    66: "兰花拂穴手", 67: "天山掌法", 68: "罗汉伏魔功", 69: "万花剑法", 70: "百变千幻云雾剑法",
    71: "金蛇剑法", 72: "冷月宝刀", 73: "君子剑", 74: "淑女剑", 75: "倚天剑",
    76: "屠龙刀", 77: "打狗棒", 78: "金蛇剑", 79: "软猬甲", 80: "女装",
    81: "霹雳雷火弹", 82: "断魂草", 83: "断肠草", 84: "生生造化丸", 85: "九花玉露丸"
}

def read_sol_file(file_path):
    """
    读取SOL文件并尝试提取数据
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        print(f"SOL文件大小: {len(data)} 字节")
        
        # 尝试不同的解析方法
        skills = []
        
        # 方法1: 查找可能的武功ID和经验值模式
        skills.extend(search_for_skill_patterns(data))
        
        # 方法2: 查找数字序列
        skills.extend(search_for_number_sequences(data))
        
        # 方法3: 尝试解析AMF格式（简化版）
        skills.extend(parse_amf_simple(data))
        
        return skills
        
    except Exception as e:
        print(f"读取SOL文件失败: {e}")
        return []

def search_for_skill_patterns(data):
    """
    在二进制数据中搜索可能的武功ID和经验值模式
    """
    skills = []
    
    # 查找可能的武功ID (1-85) 后面跟着经验值
    for i in range(len(data) - 8):
        # 检查是否是有效的武功ID
        if 1 <= data[i] <= 85:
            # 检查后面的字节是否可能是经验值
            exp_bytes = data[i+1:i+5]
            try:
                # 尝试不同的字节序解释
                exp_values = [
                    struct.unpack('<I', exp_bytes)[0],  # 小端序
                    struct.unpack('>I', exp_bytes)[0],  # 大端序
                    struct.unpack('<I', exp_bytes[:3] + b'\x00')[0],  # 3字节
                ]
                
                for exp in exp_values:
                    if 0 < exp < 1000000:  # 合理的经验值范围
                        skill_name = SKILL_NAMES.get(data[i], f"未知武功({data[i]})")
                        skills.append({
                            'id': data[i],
                            'name': skill_name,
                            'experience': exp,
                            'method': 'pattern_search'
                        })
                        break
            except:
                continue
    
    return skills

def search_for_number_sequences(data):
    """
    搜索数字序列，可能包含武功数据
    """
    skills = []
    
    # 查找连续的数值
    for i in range(len(data) - 16):
        # 尝试读取连续的数值
        try:
            values = []
            for j in range(8):
                if i + j * 2 < len(data):
                    val = struct.unpack('<H', data[i+j*2:i+j*2+2])[0]
                    values.append(val)
            
            # 检查是否有合理的武功ID和经验值组合
            for k in range(len(values) - 1):
                if 1 <= values[k] <= 85 and 0 < values[k+1] < 100000:
                    skill_name = SKILL_NAMES.get(values[k], f"未知武功({values[k]})")
                    skills.append({
                        'id': values[k],
                        'name': skill_name,
                        'experience': values[k+1],
                        'method': 'sequence_search'
                    })
        except:
            continue
    
    return skills

def parse_amf_simple(data):
    """
    简化的AMF解析器
    """
    skills = []
    
    # AMF0 类型标记
    AMF0_NUMBER = 0x00
    AMF0_BOOLEAN = 0x01
    AMF0_STRING = 0x02
    AMF0_OBJECT = 0x03
    AMF0_NULL = 0x05
    AMF0_UNDEFINED = 0x06
    AMF0_REFERENCE = 0x07
    AMF0_ARRAY = 0x08
    AMF0_OBJECT_END = 0x09
    AMF0_STRICT_ARRAY = 0x0A
    AMF0_DATE = 0x0B
    AMF0_LONG_STRING = 0x0C
    
    try:
        pos = 0
        while pos < len(data):
            if pos >= len(data):
                break
                
            marker = data[pos]
            pos += 1
            
            if marker == AMF0_NUMBER:
                # 8字节双精度浮点数
                if pos + 8 <= len(data):
                    number = struct.unpack('>d', data[pos:pos+8])[0]
                    pos += 8
                    # 检查是否是合理的武功经验值
                    if 0 < number < 1000000 and number.is_integer():
                        # 可能是武功经验值
                        pass
                        
            elif marker == AMF0_STRING:
                # 2字节长度 + 字符串
                if pos + 2 <= len(data):
                    length = struct.unpack('>H', data[pos:pos+2])[0]
                    pos += 2
                    if pos + length <= len(data):
                        string = data[pos:pos+length].decode('utf-8', errors='ignore')
                        pos += length
                        
            elif marker == AMF0_OBJECT:
                # 对象开始，继续解析
                continue
                
            elif marker == AMF0_OBJECT_END:
                # 对象结束
                continue
                
            else:
                # 跳过未知类型
                pos += 1
                
    except Exception as e:
        print(f"AMF解析错误: {e}")
    
    return skills

def find_sol_file():
    """
    查找金庸群侠传3的SOL存档文件
    """
    # 硬编码的特定路径
    specific_path = r"C:\Users\weiya\Downloads\FlashBrowser_x64_v1.1.0\Release\Caches\Pepper Data\Shockwave Flash\WritableRoot\#SharedObjects\4NET8CUM\nitrome.com.4399.com\JY1.sol"
    
    if os.path.exists(specific_path):
        return [specific_path]
    else:
        print(f"指定的存档文件不存在: {specific_path}")
        return []

def print_skills(skills):
    """
    打印武功列表
    """
    if not skills:
        print("未找到任何经验不为0的武功")
        return
    
    # 去重，保留经验值最高的
    unique_skills = {}
    for skill in skills:
        skill_id = skill['id']
        if skill_id not in unique_skills or skill['experience'] > unique_skills[skill_id]['experience']:
            unique_skills[skill_id] = skill
    
    skills_list = list(unique_skills.values())
    
    print(f"\n找到 {len(skills_list)} 个经验不为0的武功:")
    print("=" * 60)
    print(f"{'ID':<4} {'武功名称':<15} {'经验值':<10} {'方法':<15}")
    print("-" * 60)
    
    # 按经验值排序
    skills_list.sort(key=lambda x: x['experience'], reverse=True)
    
    for skill in skills_list:
        print(f"{skill['id']:<4} {skill['name']:<15} {skill['experience']:<10} {skill['method']:<15}")
    
    print("=" * 60)

def main():
    """
    主函数
    """
    print("金庸群侠传3 武功经验读取器 (简化版)")
    print("=" * 40)
    
    # 查找SOL文件
    sol_files = find_sol_file()
    
    if not sol_files:
        print("未找到金庸群侠传3的存档文件")
        return
    
    print(f"找到存档文件: {sol_files[0]}")
    
    # 读取SOL文件
    skills = read_sol_file(sol_files[0])
    
    # 显示结果
    print_skills(skills)
    
    # 保存结果到JSON文件
    if skills:
        with open('skills_output.json', 'w', encoding='utf-8') as f:
            json.dump(skills, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到 skills_output.json")

if __name__ == "__main__":
    main() 