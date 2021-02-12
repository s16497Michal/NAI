# Autorzy: Aleksandra Formela s17402 i Michał Kosiński s16497
# Materiały pomocnicze: 
# https://gym.openai.com/envs/Taxi-v3/
# https://gym.openai.com/docs/
# Opis problemu: Nauczanie ze wzmocnieniem na przykładzie gry Taxi-v3

# Instrukcja przygotowania środowiska:
# 1. Upewniamy się, że posiadamy 64-bitową wersję Pythona 3.8.0
# 2. Używamy terminala i wpsiujemy w nim komendę: python -m pip install numpy
# 3. Używamy konsoli systemowej i wpsiujemy w niej komendę: python -m pip install gym
# 4. Używamy konsoli systemowej i wpsiujemy w niej komendę: python -m pip install IPython
# 5. Używamy konsoli systemowej i wpsiujemy w niej komendę: python -m pip install display
# 6. Używamy konsoli systemowej i wpsiujemy w niej komendę: python -m pip install random

# Opis rozwiązania:
# Taksówka na planszy o wymiarach 5x5 ma za zadanie zabranie pasażera z jednego punktu (zaznaczonego na niebiesko) i wysadzenie go w drugim punkcie (zaznaczonym na różowo).
# Na planszy istnieją ściany - przeszkody, których taksówka nie może przekroczyć (|).
# Taksówka na planszy oznaczona jest jako żółty kwadrat.
# Istnieje 5 akcji dla taksówki: 0 - ruch na południe, 1 - ruch na północ, 2 - ruch na wschód, 3 - ruch na zachód, 4 - zabranie pasażera, 5 - wysadzenie pasażera.
# Jeden epizod składa się z tury od wzięcia pasażera na pokład do wysadzenia go w miejscu docelowym.


import gym
import numpy as np
import time, pickle, os
from IPython.display import clear_output
import random

# Użycie gym do wyrenederowania środowiska gry
env = gym.make('Taxi-v3')

for i in range(0,100):
    clear_output(wait=True)
    env.reset()
    env.render()
    time.sleep(0.5)

env.s = 328
env.render()
print(env.step(2))
time.sleep(10)
clear_output(wait=True)
env.render()

# Macierz z wierszem dla każdego stanu i kolumną dla kązdej akcji: 500 x 6
q_table = np.zeros([env.observation_space.n, env.action_space.n])

### Rozpoczęcie uczenia

# Parametry alfa - szybkość uczenia, gamma - waga nagrody (od "chciwości" do oczekiwania na długoterminową nagrodę) epsilon - wksaźnik "eksploracji"
alpha = 0.2
gamma = 0.7
epsilon = 0.1

# Do określenia metryk
all_epochs = []
all_penalties = []

# Algorytm do update'u naszej macierzy na podstawie podanej liczby epizodów.

for i in range(1, 100501):
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False
    
    # W pierwszej części porównujemy wartości epsilonu do wyniku funkcji random.uniform(0, 1) i na tej podstawie decydujemy, czy: 
    # wybrać randomową wartość, 
    # czy wykorzystać już obliczoną Q -value.

    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Wybranie randomowej wartości - poszukiwanie nowych rozwiązań
        else:
            action = np.argmax(q_table[state]) # Wykorzystanie już poznanych wartości

        next_state, reward, done, info = env.step(action) 
        
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        if reward == -10:
            penalties += 1

        state = next_state
        epochs += 1
        
    if i % 100 == 0:
        clear_output(wait=True)
        print(f"Episode: {i}")

print("Training finished.\n")


# Ocena wydajności po wytrenowaniu - na podstawie 100 epizodów (od załadowania pasażera do wysadzenia go w jego destynacji)
total_epochs, total_penalties = 0, 0
episodes = 100
frames = []

for ep in range(episodes):
    state = env.reset()
    epochs, penalties, reward = 0, 0, 0
    
    done = False
    
    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)

        if reward == -10:
            penalties += 1
        
        # Animacja
        frames.append({
            'frame': env.render(mode='ansi'),
            'episode': ep, 
            'state': state,
            'action': action,
            'reward': reward
            }
        )
        epochs += 1

    total_penalties += penalties
    total_epochs += epochs


    # Wydajność oceniamy na podstawie:
    # 1. Średniej liczby kar na jeden epizod
    # 2. Średniej liczby timestepów na jeden epizod - im mniej tym krótsza droga do wygranej = lepsza efektywność
    # 3. Średniej wygranej z epizodu

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")

    # Animacja

def print_frames(frames):
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'])
        print(f"Episode: {frame['episode']}")
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        time.sleep(1)

print_frames(frames)
