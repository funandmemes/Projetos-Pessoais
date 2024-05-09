#!/usr/bin/env python3
'''
Jogo baseado no jogo da forca

Modo de utilização:

python3 guessme.py

É necessário o arquivo 'words.txt' estar presente na mesma pasta que
o programa, contendo uma lista de palavras separadas por linhas
para uma delas ser escolhida aleatóriamente.

Exemplo de preenchimento caso queira personalizar o arquivo:

abacate
caju
banana

Não separe com vírgula, espaço ou qualquer outro modo.
'''
__author__ = 'funandmemes'
__version__ = '0.1.1'
__licence__ = 'unlicensed'

from os import system
from time import sleep
from random import choice

name = '''
 d888b  db    db d88888b .d8888. .d8888. .88b  d88. d88888b 
88' Y8b 88    88 88'     88'  YP 88'  YP 88'YbdP`88 88'     
88      88    88 88ooooo `8bo.   `8bo.   88  88  88 88ooooo 
88  ooo 88    88 88~~~~~   `Y8b.   `Y8b. 88  88  88 88~~~~~ 
88. ~8~ 88b  d88 88.     db   8D db   8D 88  88  88 88.     
 Y888P  ~Y8888P' Y88888P `8888Y' `8888Y' YP  YP  YP Y88888P 
'''

game_over = '''
 d888b   .d8b.  .88b  d88. d88888b    .d88b.  db    db d88888b d8888b. 
88' Y8b d8' `8b 88'YbdP`88 88'       .8P  Y8. 88    88 88'     88  `8D 
88      88ooo88 88  88  88 88ooooo   88    88 Y8    8P 88ooooo 88oobY' 
88  ooo 88~~~88 88  88  88 88~~~~~   88    88 `8b  d8' 88~~~~~ 88`8b   
88. ~8~ 88   88 88  88  88 88.       `8b  d8'  `8bd8'  88.     88 `88. 
 Y888P  YP   YP YP  YP  YP Y88888P    `Y88P'     YP    Y88888P 88   YD    
'''

win = '''
db    db d888888b  .o88b. d888888b  .d88b.  d8888b. db    db 
88    88   `88'   d8P  Y8 `~~88~~' .8P  Y8. 88  `8D `8b  d8' 
Y8    8P    88    8P         88    88    88 88oobY'  `8bd8'  
`8b  d8'    88    8b         88    88    88 88`8b      88    
 `8bd8'    .88.   Y8b  d8    88    `8b  d8' 88 `88.    88    
   YP    Y888888P  `Y88P'    YP     `Y88P'  88   YD    YP    
'''

def clear_screen():
    system('clear')
    
def guess_pos(l, arr):
    for letter in arr:
        if letter == l:
            ind = arr.index(letter)
            arr[ind] = '_'
            guess[ind] = l
    return guess
    
def interface():
    u_guess = ' '.join(guess)
    print(name)
    print(f'Vidas: {tries * heart}\n')
    print(f'Letras erradas: {wrong}\n')
    print(f'Palavra: {u_guess}')
    return ''
    
def popup(text):
    counter = 3
    while counter > 0:
        clear_screen()
        sleep(0.5)
        print(text)
        sleep(0.5)
        clear_screen()
        counter -= 1
    print(text)

while True:
    with open('words.txt', 'r') as file:
        lines = file.read().splitlines()
    word = choice(lines).upper()
    arr_word = list(word)
    guess = []
    wrong = []
    tries = 7
    heart = '💖'

    while len(guess) < len(word):
        guess.append('_')
    popup(name)
    input('Pressione enter para continuar...')
    clear_screen()
    print(interface())
    
    while '_' in guess:
        if tries == 0:
            break
        else:
            l = input('Escolha uma letra: ').upper()
            if l in arr_word:
                guess = guess_pos(l, arr_word)
                clear_screen()
                print(interface())
            elif l in wrong or l in guess:
                clear_screen()
                print(interface())
                print(f'A letra ´{l}´ já foi usada')
            else:
                if len(l) != 1 or l.isdigit():
                    clear_screen()
                    print(interface())
                    print(f'Entrada inválida, digite uma letra')
                else:
                    wrong.append(l)
                    tries -= 1
                    clear_screen()
                    print(interface())
    if not '_' in guess:
        clear_screen()
        popup(win)
        print(f'A palavra era {word}')
    elif '_' in guess:
        clear_screen()
        popup(game_over)
        print(f'A palavra era {word}')
    option = input('Você quer sair do jogo? (s/n): ')
    if option.lower() == 's':
        break
