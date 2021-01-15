# SVM przykładowa implementacja korzystająca ze zbioru win
# Autorzy: Michał Kosiński s16497 i Aleksandra Formela s17402

# Instrukcja przygotowania środowiska:
# 1. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install numpy
# 2. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install pandas
# 3. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install sklearn
# Do uruchomienia programu wykorzystujemy komendę w terminalu: python wines.py

# Na podstawie danych dotyczących wina jesteśmy w stanie przewidzieć jego jakość
# Przykładowe wino generowane jest za pomocą funkcji make_random_wine z uwagi na dużą liczbę parametrów,
# których użytkownicy nie są w stanie znaleźć na etykiecie produktu :)

import pandas as pd
import numpy as np
import random
from sklearn import svm
from sklearn.model_selection import train_test_split


class SvmWines:
    def __init__(self):
        self.svmclassifier = svm.SVC(kernel='linear')

    # generate random wine
    def make_random_wine(self):
        fixed_acidity = random.uniform(0, 10)
        volatile_acidity = random.uniform(0, 1)
        citric_acid = random.uniform(0, 1)
        residual_sugar = random.uniform(0, 20)
        chlorides = random.uniform(0, 0.06)
        free_sulfur_dioxide = random.uniform(95, 100)
        total_sulfur_dioxide = random.uniform(0, 370)
        density = random.uniform(0, 1)
        pH = random.uniform(0, 4)
        sulphates = random.uniform(0, 1)
        alcohol = random.uniform(6, 20)

        return np.array([fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide,
                         total_sulfur_dioxide, density, pH, sulphates, alcohol])

    # loading data
    def getData(self):
        wines_set = pd.read_csv('winequality-white.csv', sep=';')
        array = wines_set.values
        X = array[:, 0:11]
        y = array[:, 11]
        # preprocesing data and training
        self.svmclassifier.fit(X, y)
        # training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        self.svmclassifier.fit(X_train, y_train)

    def getResult(self, random_wine):
        return self.svmclassifier.predict([random_wine])


svmTest = SvmWines()
svmTest.getData()

random_wine = svmTest.make_random_wine()
print("\nPredicted quality: ")
print(svmTest.getResult(random_wine))

# Y_predict = svm.predict(X_test)
# print('Dokładność wyniku: ' + str(round(accuracy_score(y_test, Y_predict) * 100, 2)))
