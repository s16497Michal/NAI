# Autorzy: Aleksandra Formela s17402 i Michał Kosiński s16497
# Dane wykorzystane w zadaniu pobrane ze strony: https://archive.ics.uci.edu/ml/datasets/Early+stage+diabetes+risk+prediction+dataset.
# Opis problemu: wykrywanie cukrzycy we wczesnym stadium na podstawie 16 czynników wejściowych.
# Dane z pliku csv zostały delikatnie zmodyfikowane - zamiana małych liter na wielkie i połączenie dwuyrazowwych symptomów za pomocą "_"

# Instrukcja przygotowania środowiska:
# 1. Upewniamy się, że posiadamy 64-bitową wersję Pythona 3.8.0
# 2. Używamy terminala i wpsiujemy w nim komendę: python -m pip install numpy
# 3. Używamy konsoli systemowej i wpsiujemy w niej komendę: python -m pip install pandas
# 4. Używamy konsoli systemowej i wpsiujemy w niej komendę: python -m pip install tensorflow
# Do uruchomienia programu wykorzystujemy komendę w terminalu: python diabetes_different_size.py

# Słownik trudniejszych terminów medycznych:
# Polyuria - wielomocz
# Polydipsia - polidypsja (nadmierne pragnienie)
# Polyphagia - polifagia (nadmierne zwiększenie łaknienia)
# Genital thrush - pleśniawki narządów rozrodczych
# Visual blurring - rozmycie wizualne (pogorszenie wzroku)
# Partial paresis - częściowy paraliż
# Alopecia - łysienie

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import feature_column
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
import pathlib

"""
Import of the csv file.
"""
diabetes_csv = "diabetes_data_upload_v2.csv"
dataframe = pd.read_csv("diabetes_data_upload_v2.csv")

print(dataframe)

dataframe['target'] = np.where(dataframe['Class']=='Negative', 0, 1)
dataframe = dataframe.drop(columns=['Class'])

"""
Splitting the dataset into test and valuation datasets and
printing lenghts of train, valuation and test examples.
"""

train, test = train_test_split(dataframe, test_size=0.4)
train, val = train_test_split(train, test_size=0.2)
print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')



def df_to_dataset(dataframe, shuffle=True, batch_size=64):
    """
    used to create a tf.data dataset from Pandas dataframe.
    """
    dataframe = dataframe.copy()
    labels = dataframe.pop('target')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds

feature_columns = []

indicator_column_names = ['Age', 'Polyuria', 'Polydipsia', 'Sudden_weight_loss', 'Polyphagia', 'Genital_thrush', 'Visual_blurring', 'Itching', 'Irritability', 'Delayed_healing', 'Partial_paresis', 'Muscle_stiffness', 'Alopecia', 'Obesity']
for col_name in indicator_column_names:
  categorical_column = feature_column.categorical_column_with_vocabulary_list(
      col_name, dataframe[col_name].unique())
  indicator_column = feature_column.indicator_column(categorical_column)
  feature_columns.append(indicator_column)


"""
Creation of the feature column and their transforamtion of columns into dataframe.
"""   
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

batch_size = 64
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

for feature_batch, label_batch in train_ds.take(1):
    print('Every feature:', list(feature_batch.keys()))
    print('A batch of ages:', feature_batch['Age'])
    print('A batch of targets:', label_batch )

model = tf.keras.Sequential([
  feature_layer,
  layers.Dense(128, activation='relu'), # first layer with 256 neurons
  layers.Dense(10, activation='relu'), # second layer attaching to one of classes
  layers.Dropout(.1),
  layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_ds,
          validation_data=val_ds,
          epochs=20)

loss, accuracy = model.evaluate(test_ds)

print("Accuracy", accuracy)