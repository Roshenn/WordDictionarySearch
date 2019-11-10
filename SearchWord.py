import requests
import time
from bs4 import BeautifulSoup
import re
import sys
import random

# 修改递深限制
sys.setrecursionlimit(100000)

# 单词文件所在位置
# 单词间回车分隔,例:
# achieve
# acquisition
# administration
# affect
# appropriate
# aspects
# assistance
# categories
# chapter
# commission
WORDS_PATH = './Word.txt'
# 网页头
URL = 'http://dict.cn/'
# 单词列表
WORDS = []
# 内容列表
CONTENT = []
# 输入时候注释
# SELECT_NUM = 4
SELECT_NUM_DICT = {
    1: 'Definition',
    2: 'WordFamily',
    3: 'Synonym',
    4: 'Antonym',
    5: 'ContextualSentence'
}
# 正则表达式
STR_MATCH_DICT = {
    1: r'.?([a-zA-z].*)\;',
    2: r'\/(\b[a-zA-Z]+\b)\"',
    3: r'\/(\b[a-zA-Z]+\b)\"',
    4: r'\/(\b[a-zA-Z]+\b)\"',
    5: r'\<li\>(.*?)\<br\/\>',
}
# 搜索规则
QUERY_RULE_DICT = {
    1: '.section.def .layout.en ol[slider="3"] li',
    2: '.section.rel .layout.nwd a',
    3: '.section.rel .layout.nfo ul[slider="12"] li a',
    4: '.section.rel .layout.nfo ul[slider="12"] li a',
    5: '.section.sent .layout.sort ol[slider="2"] li'
}


# 5: '.section.def .layout.en ol[slider="3"] li'

def run(str_match, query_rule):
    '''遍历获得每个单词的相应属性'''

    # 获取网站元素
    # 创建链接
    rs = requests.Session()

    # 遍历获得每个单词的元素
    for word in WORDS:
        word_url = URL + word

        res = rs.get(word_url)

        # 获取链接源代码
        soup = BeautifulSoup(res.text, 'lxml')

        # 查询内容
        element = soup.select(query_rule)
        element = str(element)
        element = re.findall(str_match, element)

        # element = str(element)
        if element:
            # 句子选最短
            if SELECT_NUM == 5:
                element = min(element, key=len)
            # 近义词选最前
            elif SELECT_NUM == 1 or SELECT_NUM == 2 or SELECT_NUM == 3:
                element = element[0]
            # 反义词选最后
            elif SELECT_NUM == 4:
                element = element[-1]

        else:
            element = ''

        # 添加任意字符串, 以区分单词是否找到相关释义,如不需要字符串为空''即可
        sign = 'SSS:'
        content = sign + str(element)
        CONTENT.append(content)


def show():
    '''显示选择菜单'''
    print('请选择需要产生的单词内容:\n'
          '\n1.Definition(单词定义)\n'
          '\n2.WordFamily(形近词)\n'
          '\n3.Synonym(同义词)\n'
          '\n4.Antonym(反义词)\n'
          '\n5.ContextualSentence(句子)\n'
          '\n6.ALL\n'
          '')
    try:
        select_num = int(input('请输入你的选择:'))
    except Exception as e:
        print('输入错误')
    return select_num


def write():
    '''写入保存的内容'''
    file = SELECT_NUM_DICT[SELECT_NUM]

    date = time.strftime('%Y%m%d%H')

    file_name = file + date + '.txt'
    print('写入')
    jump = str('\r')
    # 写入
    with open(file_name, 'w+') as f:
        for i in CONTENT:
            f.writelines(i)
            f.write(jump)
        CONTENT.clear()


def select(select_num):
    global SELECT_NUM
    SELECT_NUM = select_num
    print(select_num)
    # 对应相关正则表达式
    str_match = STR_MATCH_DICT[SELECT_NUM]
    query_rule = QUERY_RULE_DICT[SELECT_NUM]

    run(str_match, query_rule)
    # 写入内容
    write()
    print('任务结束___%s' % select_num)


def mean():
    '''获取单词'''
    # 获取单词
    with open(WORDS_PATH) as f:
        for word in f.readlines():
            word = word.replace('\n', '')
            WORDS.append(word)

    if len(WORDS) < 1:
        print('无法获取单词')
        return
    while True:
        # 显示选择菜单
        try:
            select_num = show()
        except Exception as e:
            print(e)
            continue
        # 修改全局变量

        # 默认选择5
        # if SELECT_NUM:
        select_list = range(1, 6)

        if select_num == 6:
            for i in select_list:
                select(i)

        elif select_num in select_list:
            select(select_num)

        else:
            print('输入错误,请重新输入')
            continue


if __name__ == '__main__':
    mean()
