# -*- coding: utf-8 -*-


import re
import openai
from tqdm import tqdm
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import sent_tokenize

import os
import tempfile
import shutil

import configparser

from io import StringIO
import random
import json




import chardet

with open('settings.cfg', 'rb') as f:
    content = f.read()
    encoding = chardet.detect(content)['encoding']
    
with open('settings.cfg', encoding=encoding) as f:
    config_text = f.read()
    config = configparser.ConfigParser()
    config.read_string(config_text)

# 获取openai_apikey和language
openai_apikey = config.get('option', 'openai-apikey')
language_name = config.get('option', 'target-language')

# 设置openai的API密钥
openai.api_key = openai_apikey
import argparse

# 创建参数解析器
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Name of the input file")
parser.add_argument("--test", help="Only translate the first 3 short texts", action="store_true")
args = parser.parse_args()

# 获取命令行参数
filename = args.filename
base_filename, file_extension = os.path.splitext(filename)

new_filenametxt = base_filename + "_translated.srt"
jsonfile = base_filename + "_process.json"
# 从文件中加载已经翻译的文本
translated_dict = {}
try:
    with open(jsonfile, "r", encoding="utf-8") as f:
        translated_dict = json.load(f)
except FileNotFoundError:
    pass



def split_text(text):
    # 使用正则表达式匹配输入文本的每个字幕块（包括空格行）
    blocks = re.split(r'(\n\s*\n)', text)

    # 初始化短文本列表
    short_text_list = []
    # 初始化当前短文本
    short_text = ""
    # 遍历字幕块列表
    for block in blocks:
        # 如果当前短文本加上新的字幕块长度不大于1024，则将新的字幕块加入当前短文本
        if len(short_text + block) <= 1024:
            short_text += block
        # 如果当前短文本加上新的字幕块长度大于1024，则将当前短文本加入短文本列表，并重置当前短文本为新的字幕块
        else:
            short_text_list.append(short_text)
            short_text = block
    # 将最后的短文本加入短文本列表
    short_text_list.append(short_text)
    return short_text_list




# 翻译短文本
def translate_text(text):
    
    # 调用openai的API进行翻译
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    
                    "content": f"Translate the following subtitle text into {language_name}, but keep the subtitle number and timeline unchanged: \n{text}",
                }
            ],
        )
        t_text = (
            completion["choices"][0]
            .get("message")
            .get("content")
            .encode("utf8")
            .decode()
        )
    except Exception as e:
        import time
        # TIME LIMIT for open api please pay
        sleep_time = 60
        time.sleep(sleep_time)
        print(e, f"will sleep  {sleep_time} seconds")
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following subtitle text into {language_name}, but keep the subtitle number and timeline unchanged: \n{text}",
                }
            ],
        )
        t_text = (
            completion["choices"][0]
            .get("message")
            .get("content")
            .encode("utf8")
            .decode()
        )
    
    return t_text

    
def translate_and_store(text):
    

    # 如果文本已经翻译过，直接返回翻译结果
    if text in translated_dict:
        return translated_dict[text]

    # 否则，调用 translate_text 函数进行翻译，并将结果存储在字典中
    translated_text = translate_text(text)
    translated_dict[text] = translated_text

    # 将字典保存为 JSON 文件
    with open(jsonfile, "w", encoding="utf-8") as f:
        json.dump(translated_dict, f, ensure_ascii=False, indent=4)

    return translated_text 


text = ""

# 根据文件类型调用相应的函数

if filename.endswith('.srt'):
    
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
       
           
   
else:
    print("Unsupported file type")


   
# 将多个空格替换为一个空格
import re
#text = re.sub(r"\s+", " ", text)




# 将文本分成不大于1024字符的短文本list
short_text_list = split_text(text)
if args.test:
    short_text_list = short_text_list[:3]
# 初始化翻译后的文本
translated_text = ""

# 遍历短文本列表，依次翻译每个短文本
for short_text in tqdm(short_text_list):
    print((short_text))
    # 翻译当前短文本
    translated_short_text = translate_and_store(short_text)
    
    
    # 将当前短文本和翻译后的文本加入总文本中
        
    translated_text += f"{translated_short_text}\n\n"
    #print(short_text)
    print(translated_short_text)
    



# 将翻译后的文本写入srt文件
with open(new_filenametxt, "w", encoding="utf-8") as f:
    f.write(translated_text)

try:
    os.remove(jsonfile)
    print(f"File '{jsonfile}' has been deleted.")
except FileNotFoundError:
    print(f"File '{jsonfile}' not found. No file was deleted.")