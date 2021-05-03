import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def test_1():
  sentences = [
    'I love my dog',
    'I love my cat'
  ]
  print(sentences)
  tokenizer = Tokenizer(num_words=100)
  print(type(tokenizer))
  tokenizer.fit_on_texts(sentences)
  print(type(tokenizer))
  word_index = tokenizer.word_index
  print(word_index)

def test_2():
  sentences = [
    'I love my dog',
    'I love my cat',
    'You love my dog!'
  ]
  tokenizer = Tokenizer(num_words=100)
  tokenizer.fit_on_texts(sentences)
  word_index = tokenizer.word_index
  print(word_index)

def test_3():
  sentences = [
    'I love my dog',
    'I love my cat',
    'You love my dog!',
    'Do you think my dog is amazing?'
  ]
  tokenizer = Tokenizer(num_words=100)
  tokenizer.fit_on_texts(sentences)
  word_index = tokenizer.word_index
  sequences = tokenizer.texts_to_sequences(sentences)

  print(word_index)
  print(sequences)

def test_4():
  sentences = [
    'I love my dog',
    'I love my cat',
    'You love my dog!',
    'Do you think my dog is amazing?'
  ]
  tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
  tokenizer.fit_on_texts(sentences)
  word_index = tokenizer.word_index
  sequences = tokenizer.texts_to_sequences(sentences)
  print(sequences)
  print(word_index)

  test_sentences = [
    'i really love my dog',
    'my dog loves my friend'
  ]
  test_sequences = tokenizer.texts_to_sequences(test_sentences)
  print(test_sequences)
  print(word_index)

def test_5():
  sentences = [
    'I love my dog',
    'I love my cat',
    'You love my dog!',
    'Do you think my dog is amazing?'
  ]

  tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
  tokenizer.fit_on_texts(sentences)
  word_index = tokenizer.word_index

  sequences = tokenizer.texts_to_sequences(sentences)
  padded = pad_sequences(sequences, padding='pre', maxlen=6, truncating='post')

  print(word_index)
  print(sequences)
  print(padded)

def main():
  print("1-----------------------------------------")
  test_1()
  print("2-----------------------------------------")
  test_2()
  print("3-----------------------------------------")
  test_3()
  print("4-----------------------------------------")
  test_4()
  print("5-----------------------------------------")
  test_5()

if __name__ =="__main__":
  main()