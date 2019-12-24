# -*-coding:'utf8'-*-

import mysql.connector
import curses
from functions import welcome, choose_cat, choose_food, save_food
from functions import search_sub
from classes import Datab

choice = 1


while choice:

    choice = welcome(choice)

    if choice == 1:
        datab = Datab(choice)
        choice = choose_cat(choice, datab)
        datab.print_products()
        choice == choose_food(choice)
        datab.print_substituted()
        while choice != 'R':
            choice = save_food(choice)
            if choice == 1:
                datab.save_substituted()
            elif choice == 2:
                datab.search_internet()

    elif choice == 2:
        datab = Datab()
        datab.search_saved()
        choice = search_sub(choice)

datab = Datab(choice)
datab.close_cnx()
print('Au revoir!')
