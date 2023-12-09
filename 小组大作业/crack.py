import hashlib
import raw


def reduction_function(data, n):
    # 将字符串转换为整数，以便进行更复杂的处理
    value = int(data, 16)  # 假设 data 是十六进制字符串

    # 使用一些复杂的运算，例如位运算、取模等，以增加非线性性
    value = (value * 137 + 53) % (2**32)

    # 将处理后的整数转换回字符串，并取前 n 位
    new_data = hex(value)[2:]
    return new_data[:n]


def load_rainbow_table(filename):
    """从文件加载彩虹表"""
    rainbow_table = {}
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(':')
            start, end = parts[0], parts[1]
            rainbow_table[end] = start
    return rainbow_table


def crack_password(chain_length, hash_to_crack, rainbow_table):
    """破解密码"""
    start=''
    hash_value1=hash_to_crack
    for i in range(chain_length):
        plaintext = reduction_function(hash_value1, 2)
        if plaintext in rainbow_table:
            start = rainbow_table[plaintext]
            break
        else:
            hash_value1=hashlib.md5(plaintext.encode()).hexdigest()

    plaintext=start
    for _ in range(chain_length):
        hash_value2 = hashlib.md5(plaintext.encode()).hexdigest()
        if hash_value2 == hash_to_crack:
            return plaintext
        else:
            plaintext = reduction_function(hash_value2, 2)

    return "Password not found in rainbow table"


# def serarch_last(hash_to_crack, start, rainbow_table, chain_length):
#     plaintext = start
#     print(plaintext)
#     for j in range(chain_length):
#         # 计算 MD5 哈希值
#         hash_value = hashlib.md5(plaintext.encode()).hexdigest()
#         if hash_value == hash_to_crack:
#             return plaintext
#         # 缩减哈希值，准备下一轮循环
#         plaintext = reduce_hash(hash_value, len(start))
#     return "no search!"


def main():

    # 加载彩虹表
    loaded_rainbow_table = load_rainbow_table("table.txt")

    # 要破解的哈希值
    hash_to_crack = hashlib.md5("".encode()).hexdigest()

    # r_function_set = generate_r_function_set(chain_length, n)
    # 破解密码
    cracked_password = crack_password(100,hash_to_crack, loaded_rainbow_table)
    print(f"Hash to crack: {hash_to_crack}")
    print(f"Cracked password: {cracked_password}")


if __name__ == "__main__":
    main()
