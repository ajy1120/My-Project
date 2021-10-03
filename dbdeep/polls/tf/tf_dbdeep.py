import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
import datetime
import requests
import time
import telegram
import urllib.request as req
import json

from bs4 import BeautifulSoup as bs
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split


def tf_analysis():
    now = datetime.datetime.now()
    seconds_in_day = 24 * 60 * 60

    # 파일 확장자에 맞춰서 불러오기. csv -> pd.read_csv
    train_data = pd.read_csv('polls/tf/train.csv', encoding='cp949')
    train, test = train_test_split(train_data, test_size=0.3, random_state=5)

    # 한글과 공백을 제외하고 모두 제거, 영어까지 제외 하고 전부 제거
    pd.set_option('mode.chained_assignment', None)
    train['공시제목'] = train['공시제목'].str.replace("[^ㄱ-ㅎ ㅏ-ㅣ A-Z a-z 가-힣]", "", regex=True)
    test['공시제목'] = test['공시제목'].str.replace("[^ㄱ-ㅎ ㅏ-ㅣ A-Z a-z 가-힣]", "", regex=True)

    # 불용어
    stopwords = [
        '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '로', '기', '억',
        '등', '년', '만', '천', '적', '억원', '전', '비', '일', '원', '제', '위', '상', '서', '대', '코로나', '분기', '조', '로', '이', '주'
    ]

    x_train = []
    x_test = []

    print("X_train sentence Start")

    for sentence in train['공시제목']:
        temp = Okt().morphs(sentence, stem=True)
        temp = [word for word in temp if not word in stopwords]
        x_train.append(temp)

    print("X_train sentence End")
    time_diff = datetime.datetime.now() - now
    print(divmod(time_diff.days * seconds_in_day + time_diff.seconds, 60))

    print("X_test sentence Start")

    for sentence in test['공시제목']:
        temp = Okt().morphs(sentence, stem=True)
        temp = [word for word in temp if not word in stopwords]
        x_test.append(temp)

    print("X_test sentence End")
    time_diff = datetime.datetime.now() - now
    print(divmod(time_diff.days * seconds_in_day + time_diff.seconds, 60))

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(x_train)

    print("Tokenizer End")
    time_diff = datetime.datetime.now() - now
    print(divmod(time_diff.days * seconds_in_day + time_diff.seconds, 60))
    print("Token Data")

    total = len(tokenizer.word_index)  # 단어의 수
    rare = 0
    for key, value in tokenizer.word_counts.items():
        if value < 5:  # 원래는 3
            rare += 1
    size = total - rare + 2

    tokenizer = Tokenizer(size, oov_token='OOV')
    tokenizer.fit_on_texts(x_train)
    x_train = tokenizer.texts_to_sequences(x_train)
    x_test = tokenizer.texts_to_sequences(x_test)
    y_train = np.array(train['상승하락'])
    y_test = np.array(test['상승하락'])

    drop_train = [index for index, sentence in enumerate(x_train) if len(sentence) < 1]

    x_train = np.delete(x_train, drop_train, axis=0)
    y_train = np.delete(y_train, drop_train, axis=0)

    x_train = pad_sequences(x_train, maxlen=30)
    x_test = pad_sequences(x_test, maxlen=30)

    model = Sequential()
    model.add(Embedding(size, 100))
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
    mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', save_best_only=True)

    model.compile(
        optimizer='rmsprop',
        loss='binary_crossentropy',
        metrics=['acc'])

    history = model.fit(
        x_train,
        y_train,
        epochs=15,
        callbacks=[es, mc],
        batch_size=60,
        validation_split=0.3
    )

    loaded_model = load_model('best_model.h5')
    pre_model = model.predict(x_test)

    # 예측 값 테스트
    def get_predict_per(s):
        new_sentence = Okt().morphs(s, stem=True)  # 토큰화
        new_sentence = [word for word in s if not word in stopwords]  # 불용어 제거
        encoded = tokenizer.texts_to_sequences([s])  # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen=30)  # 패딩
        score = float(loaded_model.predict(pad_new))  # 예측

        if (score > 0.5):
            per = (score * 100)
        else:
            per = ((1 - score) * 100)

        if per > 0:
            per = round(per, 1)

        return per

    print('------------------------------------------------------------')
    str_predict = get_predict_per('트러스트버스, 미국의 제도권 금융블록체인 기업 R3의 프로페셔널 계약 확보')
    print(str_predict)
    print('------------------------------------------------------------')

    def get_news():
        print("Get News Start")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'pragma': 'no-cache',
            'expires': 0
        }

        url = 'https://api.xangle.io/landing-disclosure-list?page=0&offset=10&lang=ko&type=feed&standard_price_type=integrated_price'
        hurl = req.Request(url, headers=headers)
        main = req.urlopen(hurl)
        json_obj = json.load(main)

        old = json_obj[0]['disclosure_id']
        name = json_obj[0]['symbol']
        text = json_obj[0]['title']
        real_name = json_obj[0]['project_name']

        # 텔레그램 봇 토큰
        my_token = '1803012005:AAG0gaidfMB5QymNtau8lruxL7h7PgzWu4A'
        bot = telegram.Bot(token=my_token)

        # 텔레그램 봇 채팅 ID
        chat_id = '1732199293'

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
        temp = []

        main = req.urlopen(hurl)
        json_obj = json.load(main)
        new = json_obj[0]['disclosure_id']  # 공시 분류 아이디

        res = requests.get('https://api.xangle.io/landing-disclosure-list?page=0&offset=10&lang=ko&type=feed')
        # 쟁글 API 주소
        # 구버전 https://api.xangle.io/landing-disclosure?page=0&items_per_page=4&status=public&lang=ko&type=feed
        # XANGLE PRO API 출시 이후 API READ  https://api.xangle.io/landing-disclosure-list?page=0&offset=10&lang=ko&type=feed

        hurl = req.Request(url, headers=headers)
        main = req.urlopen(hurl)
        json_obj = json.load(main)

        for index, obj in enumerate(json_obj):
            json_obj[index]['predict_per'] = get_predict_per(obj['title'])

        print("Get News End")

        return json_obj

    news = get_news()

    return {
        'predict': str_predict,
        'news': news
    }
