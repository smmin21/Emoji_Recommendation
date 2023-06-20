## 파이썬 이모지 라이브러리
# 1. pip install 방법
# python -m pip install emoji --upgrade
#
# 2. git clone 방법
# git clone https://github.com/carpedm20/emoji.git
# cd emoji
# python -m pip install .
#

## 구글 변역 라이브러리
# pip install googletrans==4.0.0-rc1

import json
import emoji
from googletrans import Translator

def get_all_emojis():
    translator = Translator()
    all_emojis = {}
    not_available_emojis = {}
    translated_emojis = {}
    not_translated = {}
    for emoji_char, emoji_info in emoji.EMOJI_DATA.items():
        try:
            # 한국어 지원 이모지 저장
            all_emojis[emoji_char] = emoji_info['ko'][1:-1]
        except KeyError:
            # 한국어 지원하지 않는 이모지 영어로 저장
            eng_string = emoji_info['en'][1:-1]
            not_available_emojis[emoji_char] = eng_string
            
            # 영어를 한국어로 변환 후 저장
            eng_string = eng_string.replace('_', ' ')
            try:
                translated = translator.translate(eng_string, src="en", dest="ko").text
                translated_emojis[emoji_char] = translated
            except:
                not_translated[emoji_char] = eng_string
                print(f"not translated : {emoji_char}")
            # print(emoji_char + " : " + eng_string + "->" + translated)
    return all_emojis, not_available_emojis, translated_emojis, not_translated


emojis, not_available_emojis, translated_emojis, not_translated = get_all_emojis()

## txt 파일로 저장
# # 한국어 이모지 출력
# with open('emoji_list.txt', 'w', encoding='utf-8') as f:
#     for emoji_char, emoji_string in emojis.items():
#         f.write(f'{emoji_char}: {emoji_string}\n')
# # 영어 이모지 출력
# with open('emoji_english_list.txt', 'w', encoding='utf-8') as f:
#     for emoji_char, emoji_string in not_available_emojis.items():
#         f.write(f'{emoji_char}: {emoji_string}\n')
# # 번역 이모지 출력
# with open('emoji_translated_list.txt', 'w', encoding='utf-8') as f:
#     for emoji_char, emoji_string in translated_emojis.items():
#         f.write(f'{emoji_char}: {emoji_string}\n')
# # 번역 실패 이모지 출력
# with open('emoji_not_translated_list.txt', 'w', encoding='utf-8') as f:
#     for emoji_char, emoji_string in not_translated.items():
#         f.write(f'{emoji_char}: {emoji_string}\n')
        
# json 파일로 저장 
# 한국어 이모지 출력
with open('emoji_list.json', 'w', encoding='utf-8') as f:
    json.dump(emojis, f, indent=4, ensure_ascii=False)
# 영어 이모지 출력
with open('emoji_english_list.json', 'w', encoding='utf-8') as f:
    json.dump(not_available_emojis, f, indent=4, ensure_ascii=False)
# 번역 이모지 출력
with open('emoji_translated_list.json', 'w', encoding='utf-8') as f:
    json.dump(translated_emojis, f, indent=4, ensure_ascii=False)
# 번역 실패 이모지 출력
with open('emoji_not_translated_list.json', 'w', encoding='utf-8') as f:
    json.dump(not_translated, f, indent=4, ensure_ascii=False)