
def welcome(choice):

    possibilities = ['1', '2']

    print("\nBienvenue dans l'application qui vous aide à mieux manger!!\
        \nQue souhaitez-vous faire?\n\
        1/ Choisir un aliment à remplacer\n\
        2/ Consulter mes aliments substitués")

    choice = input("Votre choix (1 / 2)?")

    while choice not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("Votre choix (1 / 2)?")

    return int(choice)


def choose_cat(choice):

    possibilities = ['1', '2', '3', '4', '5']

    print("Sélectionnez la catégorie de l'aliment:\n\
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
        choice = input("Votre choix (1 à 10)?")     

    return int(choice)
