'''
Autorzy: Michał Kosiński s16497 i Aleksandra Formela s17402
Instrukcja przygotowania środowiska:
Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install tensorflow, pip install numpy, pip install matplotlib
'''
import tensorflow as tf
import numpy as np

digits = tf.keras.datasets.mnist  # importujemy zestaw danych odręcznie napisanych liczb

# przygotowujemy zestawy z powyższego zbioru
(training_digits, training_labels), (test_digits, test_labels) = digits.load_data()

# dzielimy zestawy na 255 przez po uzyskamy większą skuteczność uczenia
training_digits, test_digits = training_digits / 255, test_digits / 255

# budujemy model i jego warstwy
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),  # formatowanie danych na tablice jednowymiarową
    tf.keras.layers.Dense(256, activation=tf.nn.relu),  # pierwsza warstwa, posiada 128 neuronów
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)  # druga warstwa zawierając punktację, przyporządkowującą do jednej z 10 klas
])

model.compile(optimizer='adam',  # aktualizacja modelu na podstawie widzianych danych i funkcji utraty
              loss='sparse_categorical_crossentropy',  # minimalizujemy funkcję utraty aby sterować modelem
              metrics='accuracy')  # metryka monitoruje etap uczenie i testu

# trenowanie modelu
model.fit(training_digits, training_labels, epochs=5)

# ocena dokładności
model.evaluate(test_digits, test_labels)

# przewidywanie
prediction = model.predict(test_digits)
np.set_printoptions(suppress=True)
print(test_labels[0])
print(prediction[0])
