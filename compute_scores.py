
# Modyfikacja przykladowego rozwiązania z wykładu
# Autorzy: Michał Kosiński s16497 i Aleksandra Formela s17402
# Instrukcja przygotowania środowiska:
# 1. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install numpy
# 2. Używamy konsoli systemowej i wpsiujemy w niej komendę: pip install argparse
# 3. W razie nieaktualnej wersji pip dokunujemy podwyższenia wersji za pomocą komendy: python -m pip install --upgrade pip
# 4. (Warunkowo) Jeśli wersja pip była nieaktualna, to ponownie używamy komend z punktów: 1 i 2.
# Aby odpalić program używamy komendy: python movie_recommender.py --user "user_name", gdzie user_name to Imię i Nazwisko osoby dl aktórej chcemy uzyskać listę polecanych i niepolecancyh filmów.

import argparse
import json
import numpy as np

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--user1', dest='user1', required=True,
            help='First user')
    parser.add_argument('--user2', dest='user2', required=True,
            help='Second user')
    parser.add_argument("--score-type", dest="score_type", required=True, 
            choice=['Euclidean'], help='Similarity metric to be used')
    return parser


def euclidean_score(dataset, user1, user2):
    """
    The function to compute the Euclidean distance score between two users. 
    """
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {} 

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    if len(common_movies) == 0:
        return 0

    squared_diff = [] 

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))
        
    return 1 / (1 + np.sqrt(np.sum(squared_diff))) 

if __name__=='__main__':
    args = build_arg_parser().parse_args()
    user1 = args.user1
    user2 = args.user2
    score_type = args.score_type

    ratings_file = 'ratings.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    if score_type == 'Euclidean':
        print("\nEuclidean score:")
        print(euclidean_score(data, user1, user2))


