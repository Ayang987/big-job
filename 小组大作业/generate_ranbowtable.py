import hashlib
import random
import string


def hash_function(data):
    """计算哈希值"""
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()

#另一种R函数
# def reduction_function(data, n):
#     # 将字符串转换为整数，以便进行更复杂的处理
#     value = int(data, 16)  # 假设 data 是十六进制字符串
#
#     # 使用一些复杂的运算，例如位运算、取模等，以增加非线性性
#     value = (value * 137 + 53) % (2 ** 32)
#
#     # 将处理后的整数转换回字符串，并取前 n 位
#     new_data = hex(value)[2:]
#     return new_data[:n]

def reduction_function(data, n):
    """R函数，返回与明文格式一样的字符串"""
    return data[:n]

def generate_random_starting_value(length):
    """随机生成每条哈希链的起始点"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_hash_chain(starting_value, chain_length, n):
    """
    生成哈希链
    :param starting_value: 起始节点
    :param chain_length: 末节点
    :param n: 明文长度
    :return: （末节点和起始节点）
    """
    current_value = starting_value

    for _ in range(chain_length):
        # 第一步：计算哈希值
        hashed_value = hash_function(current_value)
        # 第二步：使用 reduction 函数
        current_value = reduction_function(hashed_value, n)
    #返回（）
    return ( starting_value,current_value)


def generate_ranbow_table(table_size, chain_length, n):
    """
    由哈希链组成彩虹表，彩虹表由字典存储
    :param table_size: 需要生成的彩虹表的链条数
    :param chain_length: 链条长度
    :param n: 明文长度
    :return: 返回彩虹表
    """
    table = {}#彩虹表
    while len(table) <= table_size:#实际表大小小于预生成大小时
        random_starting_value = generate_random_starting_value(n)#链条起始节点随机生成
        starting_value,end_value  = generate_hash_chain(random_starting_value, chain_length, n)#得到链条
        table[starting_value] = end_value#键值为起始点

    return table


# 示例用法

def save_rainbow_table(rainbow_table, filename):
    """保存彩虹表到文件"""
    with open(filename, 'w', encoding='utf-8') as file:
        for start, end in rainbow_table.items():
            file.write(f"{start}:{end}\n")#以起始：末节点保存

def main():
    table_size = 100
    chain_length = 100
    n = 1

    #生成彩虹表
    ranbow_table = generate_ranbow_table(table_size, chain_length, n)
    #保存彩虹表
    save_rainbow_table(ranbow_table, "table.txt")

if __name__ == "__main__":
    main()