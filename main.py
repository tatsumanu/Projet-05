# -*-coding:'utf8'-*-

import mysql.connector
from functions import welcome, choose_cat
from classes import Datab


choice = 1

while choice:

    choice = welcome(choice)
    print(choice)

    if choice == 1:
        choice = choose_cat(choice)

    print(choice)

    datab = Datab(choice)

    datab.print_to_screen()


print('Au revoir!')
