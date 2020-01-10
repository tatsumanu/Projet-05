# Projet 05
-----------

The main purpose of this project is to interact with the Openfoodfacts base to find healthier substitute for the user.

First of all, you will need a mysql database so, if not already done, download and install mysql from the official website. 
Once done, the program requires a database 'openfoodfacts' with three tables.

Next, follow the requirements.txt for your virtual environnement. We used Python 3.7.

Just launch the python script "fill_db_page.py": it will handle the creation of the database and of the 3 tables. It will also collect the data from the Openfoodfacts API and populate the database with it. You can play with arguments in command line with this script to add options: You can define the number of products by page for our API requests, Set the number of page in the API requests and also add food categories to default list (composed of: gateau, soda, pizza, yaourt, pate a tartiner)

For our program we used a simple user 'student' with no password checking. Feel free to adjust these variables as you want!

Also note that we developped 2 versions of the application: the first one simply working in terminal and the second one where we added the curses library for an improved user experience! You will find the first in the master's branch while the second is in the .. curses branch!

Once done, you're ready to play the program by running 'main.py' or alternate 'main_curses.py' for the curses version.

Enjoy!

Nota bene: Don't mention it before but note that inside the application, menu and all the stuff will be wrote in french...
