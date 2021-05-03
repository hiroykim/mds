import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer


def test_1():
    texts = ['먹고 싶은 사과', '먹고 싶은 바나나', '길고 노란 바나나 바나나', '저는 과일이 좋아요']

    t = Tokenizer()
    t.fit_on_texts(texts)
    print(t.word_index)

    #총 4개의 모드를 지원하는데 각 모드는 'binary', 'count', 'freq', 'tfidf'로 총 4개
    print(t.texts_to_matrix(texts, mode = 'count')) # texts_to_matrix의 입력으로 texts를 넣고, 모드는 'count'
    print(t.texts_to_matrix(texts, mode = 'binary'))
    print(t.texts_to_matrix(texts, mode = 'tfidf').round(2)) # 둘째 자리까지 반올림하여 출력
    print(t.texts_to_matrix(texts, mode = 'freq').round(2)) # 둘째 자리까지 반올림하여 출력


def main():
    test_1()

if __name__ == "__main__":
    main()