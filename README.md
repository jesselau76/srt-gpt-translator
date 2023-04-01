# srt-GPT-translator
[En](https://github.com/jesselau76/srt-gpt-translator/blob/main/README.md) | [中文说明](https://github.com/jesselau76/srt-gpt-translator/blob/main/README-zh.md)

This tool is designed to help users translate srt file into a different language using the OpenAI API (model="gpt-3.5-turbo"). 

## Installation

To use this tool, you will need to have Python 3 installed on your system, as well as the following packages:


You can install these packages by running the following command:
```
pip install -r requirements.txt
```

git clone

```
git clone https://github.com/jesselau76/srt-gpt-translator.git
```

Update to new version
```
cd srt-gpt-translator
git pull
pip install -r requirements.txt
```
## Usage

To use this tool, you need rename settings.cfg.example to settings.cfg at first.
```
cd srt-gpt-translator
mv settings.cfg.example settings.cfg
nano settings.cfg
```

```
openai-apikey = sk-xxxxxxx
```
replace sk-xxxxxxx to your OpenAI api key.
Change others options then press CTRL-X to save.

run the command: 
```
python3 srt_translation.py [-h] [--test] filename

positional arguments:
  filename    Name of the input file

options:
  -h, --help  show this help message and exit
  --test      Only translate the first 3 short texts
```

Simply run the `srt_translation.py` script with the file you want to translate or convert as an argument. For example, to translate a srt file named `example.srt`, you would run the following command:

```
python3 srt_translation.py example.srt
```

By default, the script will attempt to translate the text into the language specified in the `settings.cfg` file under the `target-language` option.
## Feature
- The code reads the OpenAI API key, target language, and other options from a settings.cfg file.
- The code provides a progress bar to show the progress of srt translation
- Test function available. Only translate 3 short texts to save your API usage with --test.

## Configuration

The `settings.cfg` file contains several options that can be used to configure the behavior of the script:

- `openai-apikey`: Your API key for the OpenAI API.
- `target-language`: The language you want to translate the text into (e.g. "English", "Chinese", "Japanese").


## Output


The output of the script will be an srt file with the same name as the input file, but with `_translated` appended to the end. For example, if the input file is `example.srt`, the output file will be `example_translated.srt`.

## License

This tool is released under the MIT License.

## Disclaimer:

This project is intended for use with public domain books and materials only. It is not designed for use with copyrighted content. Users are strongly advised to carefully review copyright information before utilizing this project and to adhere to relevant laws and regulations in order to protect their own rights and the rights of others.

The authors and developers of this project shall not be held responsible for any loss or damage resulting from the use of this project. Users assume all risks associated with its use. It is the responsibility of users to ensure they have obtained permission from the original copyright holder or used open-source PDF, EPUB, or MOBI files before employing this project to avoid potential copyright risks.

If you have any concerns or suggestions about the use of this project, please contact us through the issues section.
