#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOL文件工具函数
读取和保存SOL文件
"""

import os
import struct
import json

def read_sol_as_dict(file_path):
    """
    读取SOL文件并返回字典格式的数据
    
    Args:
        file_path (str): SOL文件路径
        
    Returns:
        dict: 解析后的数据字典，如果失败返回空字典
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        print(f"读取SOL文件: {file_path}")
        print(f"文件大小: {len(data)} 字节")
        
        # 尝试解析AMF0格式
        result = parse_amf0(data)
        
        if result:
            print(f"成功解析SOL文件，包含 {len(result)} 个键")
            return result
        else:
            print("无法解析SOL文件，返回空字典")
            return {}
            
    except Exception as e:
        print(f"读取SOL文件失败: {e}")
        return {}

def save_dict_to_sol(data_dict, file_path):
    """
    将字典数据保存为SOL文件
    
    Args:
        data_dict (dict): 要保存的数据字典
        file_path (str): 目标SOL文件路径
        
    Returns:
        bool: 保存成功返回True，失败返回False
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 将字典转换为AMF0格式
        amf_data = encode_amf0(data_dict)
        
        # 写入文件
        with open(file_path, 'wb') as f:
            f.write(amf_data)
        
        print(f"成功保存SOL文件: {file_path}")
        print(f"文件大小: {len(amf_data)} 字节")
        return True
        
    except Exception as e:
        print(f"保存SOL文件失败: {e}")
        return False

def parse_amf0(data):
    """
    解析AMF0格式数据
    """
    result = {}
    pos = 0
    
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
        while pos < len(data):
            if pos >= len(data):
                break
                
            marker = data[pos]
            pos += 1
            
            if marker == AMF0_OBJECT:
                # 解析对象
                obj_data = {}
                while pos < len(data):
                    if data[pos] == AMF0_OBJECT_END:
                        pos += 1
                        break
                    
                    # 读取属性名
                    if data[pos] == AMF0_STRING:
                        pos += 1
                        if pos + 2 <= len(data):
                            name_length = struct.unpack('>H', data[pos:pos+2])[0]
                            pos += 2
                            if pos + name_length <= len(data):
                                name = data[pos:pos+name_length].decode('utf-8', errors='ignore')
                                pos += name_length
                                
                                # 读取属性值
                                if pos < len(data):
                                    value_marker = data[pos]
                                    pos += 1
                                    
                                    if value_marker == AMF0_NUMBER:
                                        if pos + 8 <= len(data):
                                            value = struct.unpack('>d', data[pos:pos+8])[0]
                                            pos += 8
                                            obj_data[name] = value
                                    elif value_marker == AMF0_STRING:
                                        if pos + 2 <= len(data):
                                            value_length = struct.unpack('>H', data[pos:pos+2])[0]
                                            pos += 2
                                            if pos + value_length <= len(data):
                                                value = data[pos:pos+value_length].decode('utf-8', errors='ignore')
                                                pos += value_length
                                                obj_data[name] = value
                                    elif value_marker == AMF0_BOOLEAN:
                                        if pos < len(data):
                                            value = bool(data[pos])
                                            pos += 1
                                            obj_data[name] = value
                                    elif value_marker == AMF0_NULL:
                                        obj_data[name] = None
                                    else:
                                        # 跳过未知类型
                                        pos += 1
                
                result.update(obj_data)
                
            elif marker == AMF0_NUMBER:
                # 8字节双精度浮点数
                if pos + 8 <= len(data):
                    number = struct.unpack('>d', data[pos:pos+8])[0]
                    pos += 8
                    result[f"value_{len(result)}"] = number
                    
            elif marker == AMF0_STRING:
                # 2字节长度 + 字符串
                if pos + 2 <= len(data):
                    length = struct.unpack('>H', data[pos:pos+2])[0]
                    pos += 2
                    if pos + length <= len(data):
                        string = data[pos:pos+length].decode('utf-8', errors='ignore')
                        pos += length
                        result[f"string_{len(result)}"] = string
                        
            else:
                # 跳过未知类型
                pos += 1
                
    except Exception as e:
        print(f"AMF0解析错误: {e}")
    
    return result

def encode_amf0(data_dict):
    """
    将字典编码为AMF0格式
    """
    result = bytearray()
    
    # 开始对象标记
    result.append(0x03)  # AMF0_OBJECT
    
    # 编码每个键值对
    for key, value in data_dict.items():
        # 编码键名
        result.append(0x02)  # AMF0_STRING
        key_bytes = key.encode('utf-8')
        result.extend(struct.pack('>H', len(key_bytes)))
        result.extend(key_bytes)
        
        # 编码值
        if isinstance(value, (int, float)):
            result.append(0x00)  # AMF0_NUMBER
            result.extend(struct.pack('>d', float(value)))
        elif isinstance(value, str):
            result.append(0x02)  # AMF0_STRING
            value_bytes = value.encode('utf-8')
            result.extend(struct.pack('>H', len(value_bytes)))
            result.extend(value_bytes)
        elif isinstance(value, bool):
            result.append(0x01)  # AMF0_BOOLEAN
            result.append(1 if value else 0)
        elif value is None:
            result.append(0x05)  # AMF0_NULL
        else:
            # 默认转换为字符串
            result.append(0x02)  # AMF0_STRING
            value_str = str(value)
            value_bytes = value_str.encode('utf-8')
            result.extend(struct.pack('>H', len(value_bytes)))
            result.extend(value_bytes)
    
    # 对象结束标记
    result.append(0x00)  # 空字符串
    result.append(0x00)  # 长度0
    result.append(0x09)  # AMF0_OBJECT_END
    
    return bytes(result)

def backup_sol_file(file_path):
    """
    备份SOL文件
    
    Args:
        file_path (str): 原文件路径
        
    Returns:
        str: 备份文件路径，失败返回None
    """
    try:
        if not os.path.exists(file_path):
            print(f"原文件不存在: {file_path}")
            return None
            
        backup_path = file_path + '.backup'
        with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
            dst.write(src.read())
        
        print(f"已备份原文件到: {backup_path}")
        return backup_path
        
    except Exception as e:
        print(f"备份文件失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 示例用法
    sol_path = r"C:\Users\weiya\Downloads\FlashBrowser_x64_v1.1.0\Release\Caches\Pepper Data\Shockwave Flash\WritableRoot\#SharedObjects\4NET8CUM\nitrome.com.4399.com\JY1.sol"
    
    # 读取SOL文件
    data = read_sol_as_dict(sol_path)
    breakpoint()
    if data:
        # 显示前几个键值对
        print("\n前10个键值对:")
        for i, (key, value) in enumerate(data.items()):
            if i >= 10:
                break
            print(f"  {key}: {value}")
        
        # 保存为JSON文件以便查看
        with open('sol_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存到 sol_data.json")
        
        # 示例：修改数据并保存
        # data['new_key'] = 'new_value'
        # save_dict_to_sol(data, sol_path + '.modified') 