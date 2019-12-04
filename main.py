# -*-coding:'utf8'-*-

import mysql.connector
from functions import welcome, choose_cat, choose_food
from classes import Datab


choice = 1

while choice:

    choice = welcome(choice)
    print(choice)

    if choice == 1:
        choice = choose_cat(choice)

        datab = Datab(choice)

        datab.print_products()
        choice == choose_food(choice)
        datab.print_substituted()


print('Au revoir!')
