The main purpose of this project is to interact with the Openfoodfacts base to find healthier substitute for the user.

First of all, to run the application you will need a mysql database so, if not already done, download and install mysql from the official website.
Once done, the program requires a database 'openfoodfacts' with three tables.

Just launch the python script "fill_db_page.py": it will handle the creation of the database and of the 3 tables. It will also collect the data from the Openfoodfacts API and populate the database with it. You can play with arguments in command line with this script to add options: You can define the number of products by page for our API requests, Set the number of page in the API requests and also add food categories to default list (composed of: gateau, soda, pizza, yaourt, pate a tartiner)

For our program we used a simple user 'student' with no password checking. Feel free to adjust these variables as you want!

Also note that we added the possibility of directly requesting the Openfoodfacts API inside the main program for an improved user experience!

You're now ready to play the program by running 'main.py'. Here is an example of a typical use case:

    (1) The user connects to the application

    (2) The app prints a menu and waits for an input

    •  1/ Food to replace
       2/ Saved food products

    (3) The user's choice is (1). The system prints to the screen all the food categories availables with a one-digit number for each one
  
    (4) The user enters a number. The system prints ten random products of the selected category. Each of them is associated with a number
   
    (6) Again, the user selects a food product by entering the number associated to. The application prints an healthier alternative for the selected product

    (8) The user can choose to save this article among his saved products or try a live request to the OpenFoodFacts API database to find an other alternative for this category

    (9) The user can now go back to the main menu to begin a new research or search among his saved products

    (10) You can quit application when returning to the main menu and choosing '3'

Enjoy!

Nota bene: Don't mention it before but note that inside the application, menu and all the stuff will be wrote in french...
