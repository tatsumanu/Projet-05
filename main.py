# -*-coding:'utf8'-*-

from database_class import Database
from product_class import Product
from variables import welcome, categorie, bar, sub_menu


db = Database()

while True:

    for elt in welcome:
        print(elt)
    choose = input('Votre choix: ')
    if choose == '1':
        cursor = db.search_category()
        res = []
        for elt in cursor:
            res += elt
        print("\n", categorie, "\n")
        for idx, elt in enumerate(res):
            print(" {}/ {}".format(idx+1, elt))
        print("\n", bar, "\n")
        choose = input(" Votre choix: ")
        while choose not in res:
            choose = input(" Votre choix: ")
        cursor = db.ten_random_prod(choose)
        prod = Product(cursor)
        prod.print_product()
        food = 0
        while int(food) not in range(1, 11):
            food = input('Votre choix: ')
        cursor = db.search_a_substitute(choose)
        prod = Product(cursor)
        prod.print_substitute()
        substitute = ""
        while substitute.lower() != 'q':
            print("\n", sub_menu)
            substitute = input("\nVotre choix: ")
            if substitute == '1':
                db.save_a_product(prod.product)
            elif substitute == '2':
                prod.search_internet(choose)
                prod.print_substitute()
    elif choose == '2':
        cursor = db.search_already_saved()
        prod = Product(cursor)
        prod.print_saved()
        print("\n\n")
        input("Appuyez sur une touche pour revenir au menu principal..")
    elif choose == '3':
        break

db.close_cnx()
