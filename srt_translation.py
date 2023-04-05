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
new_filenametxt2 = base_filename + "_translated_bilingual.srt"

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




def is_translation_valid(original_text, translated_text):
    def get_index_lines(text):
        lines = text.split('\n')
        index_lines = [line for line in lines if re.match(r'^\d+$', line.strip())]
        return index_lines

    original_index_lines = get_index_lines(original_text)
    translated_index_lines = get_index_lines(translated_text)

    print(original_text, original_index_lines)
    print(translated_text, translated_index_lines)

    return original_index_lines == translated_index_lines
def translate_text(text):
    max_retries = 3
    retries = 0
    
    while retries < max_retries:
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
            
            if is_translation_valid(text, t_text):
                return t_text
            else:
                retries += 1
                print(f"Invalid translation format. Retrying ({retries}/{max_retries})")
        
        except Exception as e:
            import time
            sleep_time = 60
            time.sleep(sleep_time)
            retries += 1
            print(e, f"will sleep {sleep_time} seconds, Retrying ({retries}/{max_retries})")

    print(f"Unable to get a valid translation after {max_retries} retries. Returning the original text.")
    return text
    
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
    


    

def replace_text(text1, text2):
    def split_blocks(text):
        blocks = re.split(r'(\n\s*\n)', text.strip())
        return [block.split('\n') for block in blocks if block.strip()]

    blocks1 = split_blocks(text1)
    blocks2 = split_blocks(text2)

    replaced_lines = []

    for block1, block2 in zip(blocks1, blocks2):
        replaced_lines.extend(block1[:2])  # Index and timestamp
        replaced_lines.extend(block2[2:])  # Chinese content
        replaced_lines.append('')  # Add an empty line

    return '\n'.join(replaced_lines).strip()


def merge_text(text1, text2):
    def split_blocks(text):
        blocks = re.split(r'(\n\s*\n)', text.strip())
        return [block.split('\n') for block in blocks if block.strip()]

    blocks1 = split_blocks(text1)
    blocks2 = split_blocks(text2)

    merged_lines = []

    for block1, block2 in zip(blocks1, blocks2):
        merged_lines.extend(block1[:2])  # Index and timestamp
        merged_lines.extend(block1[2:])  # English content
        merged_lines.extend(block2[2:])  # Chinese content
        merged_lines.append('')  # Add an empty line

    return '\n'.join(merged_lines).strip()


result = replace_text(text, translated_text)
# 将翻译后的文本写入srt文件
with open(new_filenametxt, "w", encoding="utf-8") as f:
    f.write(result)

result2 = merge_text(text, translated_text)
# 将翻译后的文本写入srt文件
with open(new_filenametxt2, "w", encoding="utf-8") as f:
    f.write(result2)

try:
    os.remove(jsonfile)
    print(f"File '{jsonfile}' has been deleted.")
except FileNotFoundError:
    print(f"File '{jsonfile}' not found. No file was deleted.")