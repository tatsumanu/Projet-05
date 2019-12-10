# -*-coding:'utf8'-*-

import mysql.connector
from functions import welcome, choose_cat, choose_food, save_food, search_sub
from classes import Datab


choice = 1


while choice:

    choice = welcome(choice)

    if choice == 1:
        choice = choose_cat(choice)
        datab = Datab(choice)
        datab.print_products()
        choice == choose_food(choice)
        datab.print_substituted()
        choice = save_food(choice)
        if choice == 1:
            datab.save_substituted()

    elif choice == 2:
        datab = Datab()
        datab.search_substituted()
        choice = search_sub(choice)

print('Au revoir!')
