# srt-GPT-translator
[En](https://github.com/jesselau76/srt-gpt-translator/blob/main/README.md) | [中文说明](https://github.com/jesselau76/srt-gpt-translator/blob/main/README-zh.md)

这个工具旨在帮助用户使用OpenAI API（model="gpt-3.5-turbo"）将SRT文件翻译成另一种语言。

## 安装

要使用此工具，您需要在系统上安装Python 3，以及以下软件包：

您可以通过运行以下命令来安装这些软件包：

`pip install -r requirements.txt` 

克隆git

`git clone https://github.com/jesselau76/srt-gpt-translator.git` 

更新到新版本

```
cd srt-gpt-translator
git pull
pip install -r requirements.txt
```

## 用法

使用此工具，您需要首先将settings.cfg.example重命名为settings.cfg。

```
cd srt-gpt-translator
mv settings.cfg.example settings.cfg
nano settings.cfg` 
```

`openai-apikey = sk-xxxxxxx` 

将sk-xxxxxxx替换为您的OpenAI API密钥。 更改其他选项，然后按CTRL-X保存。

运行命令：
```
python3 srt_translation.py [-h] [--test] filename

positional arguments:
  filename    输入文件的名称

options:
  -h，--help  显示此帮助消息并退出
  --test      只翻译前3个短文本
```

只需使用要翻译或转换的文件作为参数运行`srt_translation.py`脚本即可。例如，要翻译名为`example.srt`的SRT文件，您将运行以下命令：

`python3 srt_translation.py example.srt` 

默认情况下，脚本将尝试将文本翻译成`settings.cfg`文件中`target-language`选项下指定的语言。

## 特征

-   该代码从settings.cfg文件中读取OpenAI API密钥，目标语言和其他选项。
-   代码提供了进度条，以显示SRT翻译的进度。
-   测试功能可用。只翻译3个短文本以节省API使用情况，使用--test选项。

## 配置

`settings.cfg`文件包含几个选项，可用于配置脚本的行为：

-   `openai-apikey`：您的OpenAI API的API密钥。
-   `target-language`：您要将文本翻译成的语言（例如“英语”，“中文”，“日语”）。

## 输出

脚本的输出将是一个与输入文件同名的SRT文件，但在末尾添加了`_translated`。例如，如果输入文件是`example.srt`，则输出文件将为`example_translated.srt`。

## 许可证

此工具发布在MIT许可下。
## 免责声明：

SRT 翻译器仅供教育和信息目的使用。本工具所使用的 OpenAI API 模型（"gpt-3.5-turbo"）所生成的翻译的准确性、可靠性和完整性不能得到保证。使用 SRT 翻译器的用户应当对所得到的翻译进行准确性和实用性的验证，不应仅凭此进行进一步的依赖和使用。使用 SRT 翻译器工具的风险由用户自行承担，工具的开发人员和贡献者不对其使用所产生的任何损失或损害承担责任。使用 SRT 翻译器工具即表示您同意遵守这些条款和条件。

如果您对本项目的使用有任何疑虑或建议，请通过问题（issues）部分与我们联系。
