"""
爬取豆瓣音乐Top250歌曲信息，并保存为文本文件。

示例：
9.
歌名：旅行的意义
作者：陈绮贞
日期：2004-02-02
风格：流行
"""

import re
import requests
from lxml import etree


# 以追加写方式打开文本文件，若文件不存在会新建
with open('豆瓣音乐Top250.txt', 'a', encoding='utf-8') as file:
    # 音乐编号
    number = 1
    # 排行榜共10页
    for i in range(10):
        # 找规律，构造URL
        url = 'https://music.douban.com/top250?start={}'.format(i * 25)
        # 添加请求头信息，否则请求会返回418错误
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        data = requests.get(url, headers=headers).text
        html = etree.HTML(data)

        # 获取当前页面所有歌曲
        musics = html.xpath('//*[@id="content"]/div/div[1]/div/table')

        for music in musics:
            # 歌名
            music_name = music.xpath('./tr/td[2]/div/a/text()')[0].strip()
            # 歌曲其他信息
            music_info = music.xpath('./tr/td[2]/div/p[1]/text()')[0].strip()

            # 用正则表达式，以'/'为标识符，分别提取歌曲其他信息
            extract = re.findall('[^/]*', music_info)
            # 去掉空字符串
            result = list(filter(None, extract))

            # 作者
            music_author = result[0].strip()
            # 日期
            music_date = result[1].strip()
            # 风格，部分歌曲没有提供该信息
            try:
                music_type = result[4].strip()
            except IndexError:
                music_type = '未知'

            # 写入文本文件
            file.write('{}.\n歌名：{}\n作者：{}\n日期：{}\n风格：{}\n\n'.format(number, music_name, music_author, music_date, music_type))
            number += 1