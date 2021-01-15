# Autorzy: Aleksandra Formela s17402 i Michał Kosiński s16497
# Dane wykorzystane w zadaniu pobrane ze strony: https://archive.ics.uci.edu/ml/datasets/Early+stage+diabetes+risk+prediction+dataset.
# Opis problemu: wykrywanie cukrzycy we wczesnym stadium na podstawie 16 czynników wejściowych.
# Dane z pliku csv zostały przekształcone na potrzeby klasyfikacji - zmiana stringów w danych wejściowych na typ int.
# Najlepsze predykcje osiągnięte zostały przy użyciu liniowego(linear) Kernela.

# Instrukcja przygotowania środowiska:
# 1. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install numpy
# 2. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install pandas
# 3. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install sklearn
# Do uruchomienia programu wykorzystujemy komendę w terminalu: python DiabetesDataSVC.py

# Słownik trudniejszych terminów medycznych:
# Polyuria - wielomocz
# Polydipsia - polidypsja (nadmierne pragnienie)
# Polyphagia - polifagia (nadmierne zwiększenie łaknienia)
# Genital thrush - pleśniawki narządów rozrodczych
# Visual blurring - rozmycie wizualne (pogorszenie wzroku)
# Partial paresis - częściowy paraliż
# Alopecia - łysienie

import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier

class SvnModel:
    def __init__(self):
        """
        The constructor of the SvmModel class.

        In here we pass "linear" as value for the Kernel parameter.
        """
        self.svclassifier = SVC(kernel='linear')

    #Import dataset
    def importData(self):
        """
        The function for dataset import from the .csv file.

        In here we also preprocess data and train the test split.
        """
        dataset = open('diabetes_data_upload.csv')
        data = np.genfromtxt(fname = dataset, delimiter = ',', dtype=str, encoding=None)
        X = data[:, :-1]
        X = X.astype(float)
        y = data[:, -1]

        self.svclassifier.fit(X, y)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

        self.svclassifier.fit(X_train, y_train)

    def getInput(self):
        """
        The function for demanding input from user.

        In here we specify parameters demanded from the user to make prediction.
        """
        age = int(input("Enter age: "))
        gender = int(input("Enter gender where 0 = male, 1 = female: "))
        polyuria = int(input("Enter if has polyuria, where 0 = No, 1 = Yes: "))
        polydipsia = int(input("Enter if has polydipsia, where 0 = No, 1 = Yes: "))
        sudden_weight_loss = int(input("Enter if had sudden weight loss, where 0 = No, 1 = Yes: "))
        weakness = int(input("Enter if feels weakness, where 0 = No, 1 = Yes: "))
        polyphagia = int(input("Enter if has polyphagia, where 0 = No, 1 = Yes: "))
        genital_thrush = int(input("Enter if has genital thrush, where 0 = No, 1 = Yes: "))
        visual_blurring = int(input("Enter if has visual blurring, where 0 = No, 1 = Yes: "))
        itching = int(input("Enter if suffers from itching, where 0 = No, 1 = Yes: "))
        irritability = int(input("Enter if feeling unusually irritable, where 0 = No, 1 = Yes: "))
        delayed_healing = int(input("Enter if suffers from delayed wound healing, where 0 = No, 1 = Yes: "))
        partial_paresis = int(input("Enter if has partial paresis, where 0 = No, 1 = Yes: "))
        muscle_stiffness = int(input("Enter if feels frequent muscle stiffness, where 0 = No, 1 = Yes: "))
        alopecia = int(input("Enter if suffers from alopecia, where 0 = No, 1 = Yes: "))
        obesity = int(input("Enter if is obese, where 0 = No, 1 = Yes: "))

        self.input = np.array([age, gender, polyuria, polydipsia, sudden_weight_loss, weakness, polyphagia, genital_thrush, visual_blurring, itching, irritability, delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity])

    def getOutput(self):
        """
        The function for returning the predicttion made on the user input data
        """
        return self.svclassifier.predict([self.input])

svn = SvnModel()
svn.importData()
svn.getInput()
print(svn.getOutput())
