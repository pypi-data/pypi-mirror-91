

from family_name import family_name
from boy import single_name, double_name
import random


def gen_name(length=1):
    if length == 1:
        return random.choice(family_name) + random.choice(single_name)
    elif length == 2:
        return random.choice(family_name) + random.choice(double_name)
    else:
        raise ValueError('暂不支持2字以上的名字!')

if __name__ == '__main__':
    a = gen_name()
    print(a)