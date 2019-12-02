
from mysql import connector


class Datab:

    def __init__(self, cat):
        self.categories = ['gateaux', 'boisson', 'pizzas',
                           'yaourt', 'fromage', 'surgeles']

        self.cat = self.categories[cat-1]

        self.cnx = connector.connect(user='student', host='localhost',
                                     database='openfoodfacts')

        self.cursor = self.cnx.cursor(buffered=True)

        self.query_cat = ("SELECT name FROM food "
                          "WHERE category = %s"
                          "LIMIT 10")

        self.query_sub = ("SELECT * FROM food"
                          "WHERE category = %s"
                          "ORDER BY nutri_grade ASC"
                          "LIMIT 1")

    def print_to_screen(self):
        print(self.cat)
        self.cursor.execute(self.query_cat, (self.cat,))

        for name in self.cursor:
            print("{}".format(name))

        