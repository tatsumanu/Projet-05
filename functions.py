from getpass import getpass
import hashlib


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


def choose_cat(choice, obj):

    lg = len(obj.categories)
    possibilities = [str(i) for i in range(1, lg+1)]
    print("Sélectionnez la catégorie de l'aliment:\n\n")
    for idx, elt in enumerate(obj.categories):
        print("\t{}/ {}".format(idx+1, elt))

    choice = input("\nVotre choix (1 à {})?".format(lg))

    while choice not in possibilities:
        print("Votre entrée n'est pas valide!")
        choice = input("Votre choix (1 à {})?".format(lg))

    obj.cat = obj.categories[int(choice)-1]
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


def who_r_u(profile):

    profile = input("\nAvec quel profil souhaitez vous vous connecter \
à l'application?\n\n\t1/ Administrateur\n\t2/ Utilisateur\n? ")

    while profile not in ['1', '2']:
        profile = input('\nVotre choix? ')

    return int(profile)


def authentication():

    print("\n--- Vérification du mot de passe ---\n")
    locked = True
    administrator = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'

    while locked:

        entry = getpass('Entrez votre mot de passe: ')
        entry = entry.encode()
        shuffled_entry = hashlib.sha1(entry).hexdigest()

        if shuffled_entry == administrator:

            locked = False
            print("\n\tBienvenue dans le module réservé à l'administrateur\n\
\t---------------------------------------------------")
        else:
            print("\nCe n'est pas le bon mot de passe!!\nIl fallait \
lire la documentation!\n")
