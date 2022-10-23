import flask
from flask import Flask, render_template, request
import json
from transliterate.base import TranslitLanguagePack, registry
from transliterate import get_available_language_codes, translit, get_translit_function
from transliterate.discover import autodiscover
import nltk
import language_tool_python



class KBDLanguagePack(TranslitLanguagePack):
    language_code = "kbd"
    language_name = "KeyBoard"
    mapping = (
       'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
       'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,йцукенгшщзхъфывапролджэячсмитьбю.',
    )



autodiscover()
registry.register(KBDLanguagePack)

translit_ru = get_translit_function('ru')
translit_kbd = get_translit_function('kbd')

tool = language_tool_python.LanguageTool('en-US')
tool = language_tool_python.LanguageTool('ru-RU')


def normalize_text(src: str):
    src_str = src
    kbd_str_ru = translit_kbd(src)
    kbd_str_en = translit_kbd(src, reversed=True)
    str_ru = translit_ru(src)
    str_en = translit_ru(src, reversed=True)
    return [src_str, kbd_str_ru, kbd_str_en, str_ru, str_en]


app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search', methods=['POST'])
def query_example():
    text = request.get_data(as_text=True)
    print(text)
    normed_text = normalize_text(text)
    return json.dumps(normed_text)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


