#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金庸群侠传3 武功经验读取器
使用 pyamf 读取 SOL 存档文件，列出所有经验不为0的武功
"""

import os
import sys
import pdb
from unittest import case
from itemp_map import ITEM_NAMES
from pyamf import sol
from skill_names import SKILL_NAMES, get_skill_name, get_skill_category


def find_sol_file():
    """
    查找金庸群侠传3的SOL存档文件
    返回可能的文件路径列表
    """
    # 硬编码的特定路径
    specific_path = r"C:\Users\weiya\Downloads\FlashBrowser_x64_v1.1.0\Release\Caches\Pepper Data\Shockwave Flash\WritableRoot\#SharedObjects\4NET8CUM\nitrome.com.4399.com\JY2.sol"

    if os.path.exists(specific_path):
        return [specific_path]
    else:
        print(f"指定的存档文件不存在: {specific_path}")
        return []


def load_sol_file(file_path):
    """
    加载SOL文件
    """
    try:
        data = sol.load(file_path)
        return data
    except Exception as e:
        print(f"加载SOL文件失败: {e}")
        return None


def extract_skills(data):
    """
    从游戏数据中提取武功经验信息
    """
    skills_with_exp = []

    if not data:
        return skills_with_exp

    skill_list = ["o", "p", "q", "r", "s", "t", "u", "v_1", "w"]
    KEY_EXP = "v"

    # 也可能在其他键中，尝试查找
    for key, value in data.items():
        if key in skill_list and isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, (int)) and sub_value > 0:
                    # 检查是否是武功ID
                    skill_id = sub_value
                    if skill_id in SKILL_NAMES:
                        skill_name = get_skill_name(skill_id)
                        skill_category = get_skill_category(skill_id)
                        experience = data.get(KEY_EXP, {}).get(skill_id, 0)
                        skills_with_exp.append(
                            {
                                "id": skill_id,
                                "name": skill_name,
                                "category": skill_category,
                                "experience": experience,
                            }
                        )

    return skills_with_exp


def set_all_skills_experience_max(data):
    skills = extract_skills(data)
    candidates = []
    candidates_name = []
    for skill in skills:
        level = skill["experience"]
        if isinstance(level, int) and level < 999:
            candidates.append(skill)
            candidates_name.append(skill["name"])

    confirm = (
        input(f"确认将 {candidates_name} 武功的经验值全部设置为 999 吗？(y/n): ")
        .strip()
        .lower()
    )
    if confirm != "y":
        print("操作已取消，不修改经验值。")
        return
    for skill in candidates:
        data["v"][skill["id"]] = 999
        print(f"set  {skill['name']} level to max")


def print_skills(skills):
    """
    打印武功列表，按类别分组显示
    """
    if not skills:
        print("未找到任何经验不为0的武功")
        return

    # 按类别组织武功
    skills_by_category = {}
    for skill in skills:
        category = skill["category"]
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)

    print(f"\n找到 {len(skills)} 个经验不为0的武功:")
    print("=" * 70)

    # 按类别打印
    for category in sorted(skills_by_category.keys()):
        print(f"\n【{category}】")

        for skill in skills_by_category[category]:
            print(skill)

    print("\n" + "=" * 70)


def set_skill_levels(data, start_id=14, end_id=37, level=100):
    """
    设置武功等级
    Args:
        data: SOL存档数据
        start_id: 起始武功ID
        end_id: 结束武功ID
        level: 要设置的等级值
    """
    if "m" not in data:
        data["m"] = {}

    # 确保使用字符串作为键
    for skill_id in range(start_id, end_id + 1):
        data["m"][str(skill_id)] = level

    return data


def save_sol_file(file_path, data):
    """
    保存SOL文件
    """
    backup_path = file_path + ".bak"
    try:
        import shutil

        shutil.copy2(file_path, backup_path)
        print(f"已创建备份文件: {backup_path}")
    except Exception as e:
        print(f"创建备份失败: {e}")
        return
    try:
        sol.save(data, file_path)
        print("存档保存成功!")
        return True
    except Exception as e:
        print(f"保存存档失败: {e}")
        return False


def enable_all_jingmai(data):
    table = data.get("n", {})
    for key in table:
        table[key] = 1


def get_item_list(data):
    nm = data.get("f", {})
    count_m = data.get("g", {})
    for key, value in nm.items():
        itemKey = int(value)
        itemCount = count_m.get(itemKey, 0)
        itemName = ITEM_NAMES.get(itemKey, "未知物品")
        if itemCount >= 0:
            print(f"{key} 物品ID: {itemKey}, 名称: {itemName}, 数量: {itemCount}")


def change_belonging(data):
    """
    修改门派归属和相关技能
    belonging: str, 可选值: "1.武当", "2.华山", "3.全真", "4.少林"
    """
    if "m" not in data:
        data["m"] = {}
    choice = (
        input("请选择门派: 1.武当, 2.华山, 3.全真, 4.少林 (默认: 武当): ")
        .strip()
        .lower()
    )
    choice = int(choice)
    if choice == 1:
        data["m"][139] = "初入武当"
        data["m"][140] = "武当派"
        data["m"][10] = "侠义"
    elif choice == 2:
        data["m"][139] = "初入华山"
        data["m"][140] = "华山派"
        data["m"][10] = "儒风"
    elif choice == 3:
        data["m"][139] = "初入全真"
        data["m"][140] = "全真教"
        # data["m"][140] = "古 墓.找小龙女学美女拳法。"
    elif choice == 4:
        data["m"][139] = "初入少林"
        data["m"][140] = "少林派"
        data["m"][10] = "佛法"
    else:
        print("未知门派类型，只支持：武当、华山、全真、少林")


def update_skill_experience(data, skill_id, experience):
    skill_name = get_skill_name(skill_id)
    confirm = (
        input(
            f"确认将武功 '{skill_name}' (ID: {skill_id}) 的经验设置为 {experience} 吗？(y/n): "
        )
        .strip()
        .lower()
    )
    if confirm == "y":
        data["v"][skill_id] = experience
    else:
        print("操作已取消，不修改经验值。")


def display_attribute_list(data):
    """
    显示所有属性列表
    """
    al = """
    14 名望
    15 侠义
    16 力道 （16-37 100 封顶）
    17 根骨
    18 悟性
    19 福缘
    20 灵敏
    21 定力
    22 拳掌之功
    23 弹指之力
    24 御剑之术
    25 耍刀之法
    26 舞棍之能
    27 内功修为
    28 拆招卸力
    29 搏击格斗
    30 闪躲纵跃
    31 轻身之法
    32 施毒之术
    33 医疗之术
    34 暗器技法
    35 读书识字
    36 交易之道
    37 烹饪之道
    """

    print(al)
    print("修改请使用 s m id value 的格式")

def enable_all_jingmai(data):
    """
    启用所有经脉
    """
    for key in data['n'].keys():
        data['n'][key] = 1
def main():
    """
    主函数
    """
    print("金庸群侠传3 武功经验读取器")
    print("=" * 30)

    # 查找SOL文件
    sol_files = find_sol_file()

    if not sol_files:
        print("未找到金庸群侠传3的存档文件")
        return

    # 尝试加载第一个文件
    if sol_files:
        file_path = sol_files[0]
        data = load_sol_file(file_path)
        if not data:
            print("未能加载存档文件，请检查文件路径或格式")
            return
        print("成功加载存档文件!")
        # print(f"存档数据包含 {len(data)} 个键")

        # print(
        #     "please input the option: 1 to read skill, 2 to 设置所有属性为100, 3 to exit"
        # )
        # 备份原始文件
        # breakpoint()
        while True:
            command = (
                input(
                    "\n请输入命令:\n"
                    "  g  : 获取武功经验\n"
                    "  s  : 设置武功经验\n"
                    "  gi : 获取物品列表\n"
                    "  si : 添加物品\n"
                    "  c  : 改门派时期\n"
                    "  w  : 查看武功\n"
                    "  ue : 修改武功经验\n"
                    "  ms : 所有武功经验满级\n"
                    "  a  : 查看属性列表\n"
                    "  jm : 经脉全通\n"
                    "  q  : 退出\n"
                    ">> "
                )
                .strip()
                .lower()
            )
            if command == "q":
                print("退出程序")
                break
            elif command == "gi":
                # 获取物品列表
                get_item_list(data)
                continue
            elif command == "si":
                # 添加物品
                # 输入格式: si key value
                # 例如: si v 100
                print("物品 列表: " + ITEM_NAMES.__str__())
                inputValue = input("请输入 key value:").strip().split()
                # breakpoint()
                if len(inputValue) != 2:
                    print("输入格式错误，请输入 'key value'")
                    continue
                try:
                    key = int(inputValue[0])
                    value = int(inputValue[1])
                except ValueError:
                    print("输入格式错误，key 和 value 必须为整数")
                    continue

                if key not in ITEM_NAMES:
                    print(f"未知物品ID: {key}")
                    continue
                if value <= 0:
                    print(f"物品数量必须大于0: {value}")
                    continue
                name = ITEM_NAMES.get(key)

                existing_value = data.get("g", {}).get(key, None)
                if existing_value:
                    print(f"已存在 {name} 数量: {existing_value} 增加数量: {value}")
                    data["g"][key] += value
                else:
                    print(f"添加物品 {name}，数量: {value}")
                    count_ = len(data["f"])
                    data["f"][count_] = key
                    data["g"][key] = value
                save_sol_file(file_path, data)
                continue
            elif command == "g":
                # 查看数值
                inputValue = input("请输入 key1 key2 or key1:").strip().split()
                if len(inputValue) > 2:
                    print("输入格式错误，请输入 'key1 key2' or 'key1'")
                    continue
                if len(inputValue) == 1:
                    # 只输入了key1
                    key1 = inputValue[0]
                    value = data.get(key1, None)
                    if value is None:
                        print(f"{key1} 的值为: None")
                    else:
                        print(f"{key1} 的值为: {value}")
                    continue
                key1, key2 = inputValue[0], int(inputValue[1])
                value = data.get(key1, {}).get(key2, None)
                print(f"{key1}[{key2}] 的值为: {value}")
                continue
            elif command == "s":
                # 设置value
                # 输入格式: s key1 key2 value
                # 例如: s v 14 100
                inputValue = input("请输入 key1 key2 value:").strip().split()
                if len(inputValue) != 3:
                    print("输入格式错误，请输入 'key1 key2  value'")
                    continue
                try:
                    key1, key2, value = (
                        inputValue[0],
                        int(inputValue[1]),
                        int(inputValue[2]),
                    )
                except ValueError:
                    print("key2 和 value 必须为整数")
                    continue

                existing_value = data.get(key1, {}).get(key2, None)
                if existing_value is not None:
                    print(f"已存在 {key1}[{key2}] 的值: {existing_value}")
                # breakpoint
                data.setdefault(key1, {})[key2] = value
                save_sol_file(file_path, data)
            elif command == "c":
                # 修改门派归属
                change_belonging(data)
                save_sol_file(file_path, data)
            elif command == "w":
                # 查看武功
                skills = extract_skills(data)
                print_skills(skills)
            elif command == "ue":
                # 修改武功经验
                skill_id = int(input("请输入武功ID: ").strip())
                if skill_id not in SKILL_NAMES:
                    print(f"未知武功ID: {skill_id}")
                    continue
                experience = int(input("请输入新的经验值: ").strip())
                update_skill_experience(data, skill_id, experience)
                save_sol_file(file_path, data)
            elif command == "ms":
                # 设置所有武功经验为满级
                set_all_skills_experience_max(data)
                save_sol_file(file_path, data)
            elif command == "a":
                # 查看属性列表
                display_attribute_list(data)
            elif command == "jm":
                # 经脉全通
                enable_all_jingmai(data)
                save_sol_file(file_path, data)
                print("已启用所有经脉")
            else:
                print("未知命令，请输入 'g', 's', 'gi' 或 'q' 退出")
                continue
        # enable_all_jingmai(data)
        # 设置武功等级
        # data = set_skill_levels(data)
        # print("\n已设置武功技能 14-37 为 100")

        # 保存修改后的存档
        # save_sol_file(file_path, data)

        # 提取武功信息
        # skills = extract_skills(data)
        # print_skills(skills)


if __name__ == "__main__":
    main()
