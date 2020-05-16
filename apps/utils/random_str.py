__author__ = 'jingyuan'
__date__ = '2020/5/13 11:10'

import string
from random import choice

def generate_random(random_length, type):
    """
    :param random_length:
    :param type: 字符串类型（0：纯数字 1：数字+字符 2：数字+字符+特殊字符）
    :return:生成的随机字符串
    """
    if type == 0:
        random_seed = string.digits
    elif type == 1:
        random_seed = string.digits + string.ascii_letters
    elif type == 2:
        random_seed = string.digits + string.ascii_letters + string.punctuation
    random_str = []
    while (len(random_str) < random_length):
        random_str.append(choice(random_seed))
    return ''.join(random_str)

if __name__ == '__main__':
    print(generate_random(4, 0))
