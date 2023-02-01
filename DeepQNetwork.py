import numpy as np
import pandas as pd
import collections

import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D


class DeepQNetwork:
    def __init__(self, train):
        self.train = train
        self.test = not train

        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.00013629
        self.epsilon = 1
        self.actual = []
        self.first_layer = 200
        self.second_layer = 20
        self.third_layer = 50
        self.memory_size = 2500
        self.episodes = 250
        self.batch_size = 1000
        self.memory = collections.deque(maxlen=self.memory_size)
        self.weights = 'weights/weights.h5'
        self.load_weights = self.test
        self.optimizer = None
        self.network()

    def network(self):

        tf.random.set_seed(1)

        keras = tf.keras
        model = keras.models.Sequential()
        l1 = keras.layers.Dense(self.first_layer, activation=tf.nn.relu)
        l2 = keras.layers.Dense(self.second_layer, activation=tf.nn.relu)
        l3 = keras.layers.Dense(self.third_layer, activation=tf.nn.relu)
        l4 = keras.layers.Dense(3, activation=tf.nn.softmax)

        model.add(l1)
        model.add(l2)
        model.add(l3)
        model.add(l4)

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        # model.fit(x=x_train, y=y_train, epochs=20, batch_size=64, validation_data=(x_test, y_test))
