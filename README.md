# Projet 05
-----------

The main purpose of this project is to interact with the Openfoodfacts base to find healthier substitute for the user.

First of all, you will need a mysql database so, if not already done, download and install mysql from the official website. 
Once done, the program requires a database 'openfoodfacts' with a unique table we called 'food'. Take it easy as we have already wrote the database's creation script for you: you can find it in the repository. For our program we used a simple user 'student' with no password checking. Feel free to adjust these variables as you want!

Next, follow the requirements.txt for your virtual environnement. We used Python 3.7.

Also note that we developped 2 versions of the application: the first one simply working in terminal and the second one where we added the curses library for an improved user experience! You will find the first in the master's branch while the second is in the .. curses branch!

Once you have chosen your version, you will need the database to be populated so, simply run the 'fill_db_page.py' script.

Once done, you're ready to play the program by running 'main.py' or alternate 'main_curses.py' for the curses version.

Enjoy!

Nota bene: Don't mention it before but note that inside the application, menu and all the stuff will be wrote in french...
