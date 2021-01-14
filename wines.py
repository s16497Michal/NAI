# SVM przykładowa implementacja korzystająca ze zbioru win
# Autorzy: Michał Kosiński s16497 i Aleksandra Formela s17402

import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

wines_set = pd.read_csv('winequality-white.csv', sep=';')

array = wines_set.values
X = array[:, 0:11]
y = array[:, 11]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=10)

svm = svm.SVC(kernel='linear')
svm.fit(X_train, y_train)

Y_predict = svm.predict(X_test)
print('Dokładność wyniku: ' + str(round(accuracy_score(y_test, Y_predict) * 100, 2)))

