from tensorflow.keras.layers import Input, Dense, concatenate
from tensorflow.keras.models import Model
#pip install keras-visualizer
#pip install graphviz
#pip install pydot
from keras_visualizer import visualizer
from tensorflow.keras.models import Sequential
#pip install keras
#from keras.utils import plot_model
from tensorflow.keras.utils import plot_model


def test_1():
    model = Sequential()
    model.add(Dense(3, input_dim=4, activation='softmax'))
    model.summary()
    plot_model(model, to_file='model.png')
    plot_model(model, to_file='model_shapes.png', show_shapes=True)


def test_2():
    # 두 개의 입력층을 정의
    inputA = Input(shape=(64,))
    inputB = Input(shape=(128,))

    # 첫번째 입력층으로부터 분기되어 진행되는 인공 신경망을 정의
    x = Dense(16, activation="relu")(inputA)
    x = Dense(8, activation="relu")(x)
    x = Model(inputs=inputA, outputs=x)

    # 두번째 입력층으로부터 분기되어 진행되는 인공 신경망을 정의
    y = Dense(64, activation="relu")(inputB)
    y = Dense(32, activation="relu")(y)
    y = Dense(8, activation="relu")(y)
    y = Model(inputs=inputB, outputs=y)

    # 두개의 인공 신경망의 출력을 연결(concatenate)
    result = concatenate([x.output, y.output])

    # 연결된 값을 입력으로 받는 밀집층을 추가(Dense layer)
    z = Dense(2, activation="relu")(result)
    # 선형 회귀를 위해 activation=linear를 설정
    z = Dense(1, activation="linear")(z)

    # 결과적으로 이 모델은 두 개의 입력층으로부터 분기되어 진행된 후 마지막에는 하나의 출력을 예측하는 모델이 됨.
    model = Model(inputs=[x.input, y.input], outputs=z)

    model.summary()

    visualizer(model, format='png', view=True)


def main():
    test_1()
    #test_2()


if __name__ == "__main__":
    main()