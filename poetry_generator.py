'''
Autorzy: Michał Kosiński s16497 i Aleksandra Formela s17402
Instrukcja przygotowania środowiska:
Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install tensorflow, pip install numpy
Materiały pomocnicze:
https://medium.com/predict/creating-a-poem-writer-ai-using-keras-and-tensorflow-16eac157cba6
https://towardsdatascience.com/creating-poems-from-ones-own-poems-neural-networks-and-life-paradoxes-a9cffd2b07e3
https://www.youtube.com/watch?v=ZMudJXhsUpY
'''
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np

# obróbka danych przed procesowaniem
tokenizer = Tokenizer()
data = open('mickiewicz_poetry.txt', encoding='utf-8').read()
corpus = data.lower().split('\n')
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1

# obróbka danych (dodanie do sekwencji oraz nadanie tokenów)
input_sequence = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequence.append(n_gram_sequence)

# tworzenie sekwencji słów wejściowych jako baza do uczenia sieci
max_sequence_len = max([len(x) for x in input_sequence])
input_sequence = np.array(pad_sequences(input_sequence, maxlen=max_sequence_len, padding='pre'))

xs, labels = input_sequence[:, :-1], input_sequence[:, -1]

ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

# tworzenie modelu
model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(Bidirectional(LSTM(150)))
model.add(Dense(total_words, activation='softmax'))
adam = Adam(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
history = model.fit(xs, ys, epochs=100, verbose=1)

# generowanie wiersza z określeniem ile ma zawierać słów i od jakiego słowa się zaczynać
seed_text = "Okryła rzeki ramiona"
next_words = 100

for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted = model.predict_classes(token_list, verbose=0)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    seed_text += " " + output_word
print(seed_text)