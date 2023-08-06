#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : poetry
# @Time         : 2020-01-09 12:53
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :hiddenpoem

"""
1. 去重
2. 结果为空字符串
3. 含有非中文字符

"""
from meutils.pipe import *
from meutils.path_utils import get_module_path
from fastapi import FastAPI

data_cache = Path(get_module_path("./data_cache", __file__))

reg_chinese = re.compile('[^\u4e00-\u9fa5]+')

new_chars = list('好闪高神强嗨迷靓甜纯萌恒酷美靓真帅纯柔惠慧雅倩秀亲')


def get_poem_map():
    dfs = []
    for file in ['poem_ext.txt', 'cangtoushi7.txt', 'cangtoushi5.txt']:
        df = pd.read_csv(data_cache / file, '\t', names=['char', 'poems'])
        if file == 'cangtoushi5.txt':
            df['poems'] = df['poems'].str.split().str[0]
        dfs.append(df)
    df = (
        pd.concat(dfs)
            .assign(poems=lambda df: df.poems.str.split())
            .explode('poems')
            .assign(poems=lambda df: df.poems.map(lambda x: reg_chinese.sub('', x)))
            .assign(poems=lambda df: (df.poems + df.poems.str[-1] * 10).str[:7])
        # reg_chinese.sub(np.random.choice(new_chars)
    ).groupby('char').agg({'poems': set}).reset_index()
    return dict(zip(df.char, df.poems))


poem_map = get_poem_map()


def poem_gen(sent):
    r = []
    for char in sent:
        poems = poem_map.get(char, set())
        poems -= set(r)  # 去重
        if poems:
            poem = np.random.choice(list(poems))  # 造诗
        else:
            poem = char + "".join(np.random.choice(new_chars, 6))
        r.append(poem)
    return r


# print(poem_gen("啊哈哈哈哈哈哈哈哈哈哈"))
app = FastAPI()


@app.get("/{title}")
async def read_item(title):
    title = reg_chinese.sub('', title)
    return {"title": title, "poem": poem_gen(title)}


# if __name__ == '__main__':
#     import os
#     import socket
#
#     me = socket.gethostname() == 'yuanjie-Mac.local'
#     gunicorn = "gunicorn" if me else "/opt/soft/python3/bin/gunicorn"
#
#     main_file = __file__.split('/')[-1].split('.')[0]
#     os.system(f"{gunicorn} -c gun.py {main_file}:app")

# gunicorn main:app -b 0.0.0.0:8000  -w 4 -k uvicorn.workers.UvicornH11Worker --daemon
