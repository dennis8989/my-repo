import requests
from bs4 import BeautifulSoup
import os
import psycopg2
import json
DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a dennis89linebot').read()[:-1]
# DATABASE_URL = os.environ['DATABASE_URL'] #on heroku

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

def postgre_inssert_data(list_word):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    # headword = list_word[0]
    # voice_us = list_word[0]
    dict_data = list_word[2]
    json_data = json.dumps(dict_data)
    list_word[2] = json_data
    table_columns = '(word, pronounce, data)'
    postgres_insert_query = f"""BEGIN;
    INSERT INTO english_dict {table_columns} VALUES (%s, %s, %s);
    COMMIT;"""

    cursor.executemany(postgres_insert_query, [list_word])  # use executemany for mulitple, but execute for single
    conn.commit()

    count = cursor.rowcount
    print(count, "Record inserted successfully into english_dict")

    cursor.close()
    conn.close()


def check_word_exist(word):
    url = f'https://dictionary.cambridge.org/dictionary/english-chinese-traditional/{word}'
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    return  soup

def cambridge_dict(soup):
    list_word = []
    headword = soup.select('.headword')[0].get_text()  # the word you look up
    list_word.append(headword)

    audios = soup.select('amp-audio')
    voice_uk = 'https://dictionary.cambridge.org' + audios[0].select('source')[0].get('src')  # UK Pronounce
    voice_us = 'https://dictionary.cambridge.org' + audios[1].select('source')[1].get('src')  # US Pronounce
    list_word.append(voice_us)

    entrys = soup.select(".entry-body__el")
    dict_data = {}
    for entry in entrys[:]:
        part_of_speech = entry.select('.pos')[0].get_text() if len(entry.select('.pos')) > 0 else ''  # 詞性
        meanings = entry.select(".dsense")
        list_easmples = []
        for meaning in meanings:
            # chinese_definition
            word_def_en_short = meaning.select(".guideword")[0].get_text().strip() if len(
                meaning.select(".guideword")) > 0 else ''
            # english_definition
            word_def_en = meaning.select(".ddef_d")[0].get_text() if len(meaning.select(".ddef_d")) > 0 else ''
            # chinese_definition
            word_def_zh = meaning.select(".def-body")[0].span.get_text() if len(meaning.select(".def-body")) > 0 else ''

            word_exams = meaning.select(".examp")  # example
            if word_exams != []:
                for word_exam in word_exams[:1]:
                    word_exam_en = word_exam.span.get_text() if word_exam.find('span') is not None else ''
                    word_exam_zh = word_exam.find(class_='trans').get_text() if word_exam.find(
                        class_='trans') is not None else ''
            else:
                word_exam_en = ''
                word_exam_zh = ''
            dict_exam = {"word_def_en_short": word_def_en_short, "word_def_zh": word_def_zh,
                         "word_exam_en": word_exam_en, "word_exam_zh": word_exam_zh}
            list_easmples.append(dict_exam)
            dict_data[f'{part_of_speech}'] = list_easmples

    list_word.append(dict_data)
    return list_word



def main():
    word = input('word')
    soup = check_word_exist(word)
    if soup.select('.headword') == []:
        print('find nothing!')
        exit()

    list_word = cambridge_dict(soup)
    print(list_word)

    text = list_word[0].upper() + '\n' + list_word[1]
    dict_data = list_word[2]
    for part_of_speech, list_examles in dict_data.items():
        text = text + part_of_speech
        for dict_example in list_examles:
            text = text + f"\n[{dict_example['word_def_en_short']} {dict_example['word_def_zh']}]"
            text = text + f"\n{dict_example['word_exam_en']}\n{dict_example['word_exam_zh']}"
    print(text)
    try:
        postgre_inssert_data(list_word)
    except Exception as e:
        print(e)


while True:
    main()

