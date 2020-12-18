
# Modyfikacja przykladowego rozwiazania z wykładu
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

from compute_scores import euclidean_score

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Find the movie recommendations for the given user')
    parser.add_argument('--user', dest='user', required=True,
            help='Input user')
    return parser
    """
    Function demanding the input of the selected user
    Retruns: parser
    """

def get_recommendations(dataset, input_user):
    """
    Function for finding the list of recommendations for the input User.
    Returns: sorted list of movie recommendations
    """
    if input_user not in dataset:
        raise TypeError('Cannot find ' + input_user + ' in the dataset')

    overall_scores = {}
    similarity_scores = {}

    for user in [x for x in dataset if x != input_user]:
        similarity_score = euclidean_score(dataset, input_user, user)

        if similarity_score <= 0:
            continue
        
        filtered_list = [x for x in dataset[user] if x not in \
                dataset[input_user] or dataset[input_user][x] == 0]

        for item in filtered_list: 
            overall_scores.update({item: dataset[user][item] * similarity_score})
            similarity_scores.update({item: similarity_score})

    if len(overall_scores) == 0:
        return ['No recommendations possible']

    movie_scores = np.array([[score/similarity_scores[item], item] 
            for item, score in overall_scores.items()])

    movie_scores = movie_scores[np.argsort(movie_scores[:, 0])[::-1]]

    movie_recommendations = [movie for _, movie in movie_scores]

    return movie_recommendations

 
if __name__=='__main__':
    args = build_arg_parser().parse_args()
    user = args.user

    ratings_file = 'ratings.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    print("\n5 best movie recommendations for " + user + ":")
    """
    Print function for printing 5 best movie reccomendations
    """
    movies = get_recommendations(data, user)
    for i, movie in enumerate(movies[0:5]):
        print(str(i+1) + '. ' + movie)



    print("\n5 worst movie recommendations for " + user + ":")
    """
    Print function for printing 5 worst movie reccomendations
    """
    movies = get_recommendations(data, user)
    N = 5
    res = movies[-5:]

    for i, movie in enumerate(res):
        print(str(i+1) + '. ' + movie)