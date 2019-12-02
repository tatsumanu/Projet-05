
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

    possibilities = ['1', '2', '3', '4', '5', '6']

    print("Sélectionnez la catégorie de l'aliment:\n\
    1/ gateaux   2/ boisson   3/ pizzas   4/ yaourt\
   5/ fromage   6/ surgeles")

    choice = input("Votre choix (1 à 6)?")

    while choice not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("Votre choix (1 / 2)?")     

    return int(choice)

