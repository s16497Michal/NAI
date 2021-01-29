'''
Autorzy: Michał Kosiński s16497 i Aleksandra Formela s17402
Instrukcja przygotowania środowiska:
Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install tensorflow, pip install numpy, pip install matplotlib
'''

# import potrzebnych bibliotek
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

fashion_mnist = tf.keras.datasets.fashion_mnist

# ładowanie danych o ubraniach do tablic np
(images_train, train_labels), (images_test, test_labels) = fashion_mnist.load_data()

clothes_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Goat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle '
                                                                                                             'boot']
print(images_train.shape)  # sprawdzamy ile jest obrazów i jak są reprezentowane
print(len(train_labels))  # sprawdzamy ile etykiet jest w zestawie treningowym
print(np.unique(train_labels))  # sprawdzamy jakie etykiety posiadamy
print(images_test.shape)
print(len(test_labels))

# Wstępne przetwarzanie danych
plt.figure()
plt.imshow(images_train[25])
plt.colorbar()
plt.grid(False)
plt.show()  # na wykresie sprawdzamy jak rozkładają się wartości pikseli

images_train = images_train / 255.0
images_test = images_test / 255.0

# sprawdzamy jaki format przyjeły nasze dane korzystając ze 100 obrazków
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(images_train[i], cmap=plt.cm.binary)
    plt.xlabel(clothes_names[train_labels[i]])
plt.show()

# budujemy model i jego warstwy
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),  # formatowanie danych na tablice jednowymiarową
    tf.keras.layers.Dense(256, activation='relu'),  # pierwsza warstwa, posiada 128 neuronów
    tf.keras.layers.Dense(10)  # druga warstwa zawierając punktację, przyporządkowującą do jednej z 10 klas
])

model.compile(optimizer='adam',  # aktualizacja modelu na podstawie widzianych danych i funkcji utraty
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              # minimalizujemy funkcję utraty aby sterować modelem
              metrics=['accuracy'])  # metryka monitoruje etap uczenie i testu

# trenowanie modelu
model.fit(images_train, train_labels, epochs=10)

# ocena dokładności
test_loss, test_accuracy = model.evaluate(images_test, test_labels, verbose=2)
print('\nDokładność testowania: ', test_accuracy)

# prognozowanie

probability_model = tf.keras.Sequential(
    [model, tf.keras.layers.Softmax()])  # warstwa softmaax konwertuje na prawdopodobieńśtwa ?
predictions = probability_model.predict(images_test)
print(predictions[4])  # wyświetlamy przykłądową predykcję
print(np.argmax(predictions[4]))  # sprawdzamy jaka "nazwa" ubrania została przyporządkowana


# dla przykładu implementacja wykresu żeby spojrzeć na większy zestaw danych
def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(clothes_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         clothes_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

# weryfikacja przykładowej prognozy
i = 12
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, images_test)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)
plt.show()

# tworzymy wykres 5 na 3
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions[i], test_labels, images_test)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()
