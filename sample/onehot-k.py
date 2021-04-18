from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

text="나랑 점심 먹으러 갈래 점심 메뉴는 햄버거 갈래 갈래 햄버거 최고야"

t = Tokenizer()
t.fit_on_texts([text])
print(t.word_index) # 각 단어에 대한 인코딩 결과 출력.

sub_text="점심 먹으러 갈래 메뉴는 햄버거 최고야"
sub_text2="점심 먹으러 갈래 메뉴는 누구나 최고야"
encoded=t.texts_to_sequences([sub_text, sub_text2])[0]
print(encoded)

one_hot = to_categorical(encoded)
print(one_hot)