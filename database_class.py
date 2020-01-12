from mysql import connector


class Database:
    """ A class whose job is to handle the relation between the main
     program and the database. His methods manage to search the required
     data and return them. """

    def __init__(self):

        try:
            self.cnx = connector.connect(user='student', host='localhost',
                                         database='openfoodfacts')
            print("Connexion established with database")
        except connector.Error as err:
            print(err)
        self.cursor = self.cnx.cursor(buffered=True)

    def search_category(self):

        search_cat = ("SELECT DISTINCT category FROM category")
        self.cursor.execute(search_cat,)
        return self.cursor

    def ten_random_prod(self, category):
        """ Query the DB and return 100 products of the selected category
        to introduce some sort of random selection between products in
        base. """

        query_cat = ("SELECT name, brand, nutri_grade FROM food "
                     "JOIN category "
                     "ON food.cat_id = category.category_id "
                     "WHERE category.category = %s AND nutri_grade > %s"
                     "LIMIT 100")
        self.cursor.execute(query_cat, (category, "c"))
        return self.cursor

    def search_a_substitute(self, category):
        """ Query for a better product in the selected category. """

        query_sub = ("SELECT name, brand, nutri_grade, store, link,\
                     ingredients FROM food "
                     "JOIN category "
                     "ON food.cat_id = category.category_id "
                     "WHERE category.category = %s AND food.nutri_grade <= %s")
        self.cursor.execute(query_sub, (category, 'b'))
        return self.cursor

    def save_a_product(self, substitute):
        """ As the user chooses to save the substituted product, we save
        this information in the database by simply setting the corresponding
        'substituted' column to 'YES'. If the product comes from an API
        research, his informations are inserted into the database. """

        query_save = ("INSERT INTO substituted (name, brand, nutri_grade,\
 store, link, ingredients) VALUES (%s, %s, %s, %s, %s, %s)")

        try:
            self.cursor.execute(query_save, (substitute))
            self.cnx.commit()
            print("\n L'article a été enregistré avec succès!\n")
        except connector.Error:
            print("\n Il n'y a aucun produit à enregistrer!\n")

    def search_already_saved(self):
        """ Looks inside the database for previously saved products. """

        query_search = ("SELECT DISTINCT name, brand, nutri_grade, store\
 FROM substituted ")
        self.cursor.execute(query_search,)
        return self.cursor

    def close_cnx(self):
        """ Closes mysql connector cursor and connexion with DB. """
        print("Closing the connection...\nGood bye!")
        self.cursor.close()
        self.cnx.close()
