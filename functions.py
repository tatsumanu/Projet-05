
def welcome(choice):

    possibilities = ['1', '2', '3']

    print("\n\n\n--- Bienvenue dans l'application qui vous aide à \
mieux manger!! ---\n\n    Que souhaitez-vous faire?\n\
    1/ Choisir un aliment à remplacer\n\
    2/ Consulter mes aliments substitués\n\
    3/ Quitter\n")

    choice = input("Votre choix (1, 2 ou 3)?")

    while choice not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("Votre choix (1, 2 ou 3)?")

    return int(choice) if choice != '3' else 0


def choose_cat(choice):

    possibilities = ['1', '2', '3', '4', '5']

    print("Sélectionnez la catégorie de l'aliment:\n\n\
    1/ gateau   2/ soda   3/ pizza   4/ yaourt   5/ pate a tartiner")

    choice = input("Votre choix (1 à 5)?")

    while choice not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("Votre choix (1 à 5)?")

    return int(choice)


def choose_food(choice):

    possibilities = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    choice = input("\nSélectionnez l'aliment que vous voulez\
 remplacer (1 à 10): ")

    while choice not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("Votre choix (1 à 10) ?")

    return int(choice)


def save_food(choice):

    possibilities = ['1', '2', 'R']

    print("\nQue souhaitez-vous faire?\n\
        1/ Enregistrer ce substitut\n\
        2/ Trouver un autre substitut sur internet\n\
        (R)etourner au menu principal")

    choice = input("Votre choix (1, 2 ou R)?")

    while choice.upper() not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("Votre choix (1, 2 ou R) ?")

    return int(choice) if choice in ['1', '2'] else 'R'


def search_sub(choice):

    possibilities = ['1']

    print("\n1/ Retourner au menu principal")

    choice = input("?")

    while choice not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("?")

    return int(choice)
