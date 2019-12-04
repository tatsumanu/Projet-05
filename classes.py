
from mysql import connector


class Datab:

    def __init__(self, cat, nutri='a'):
        self.categories = ['gateau', 'soda', 'pizza', 'yaourt',
                           'pate a tartiner']

        self.cat = self.categories[cat-1]
        self.nutri = nutri
        self.cnx = connector.connect(user='student', host='localhost',
                                     database='openfoodfacts')

        self.cursor = self.cnx.cursor(buffered=True)

        self.query_cat = ("SELECT DISTINCT name, brand, nutri_grade FROM food "
                          "WHERE category = %s"
                          "LIMIT 10")

        self.query_sub = ("SELECT name, brand, nutri_grade FROM food "
                          "WHERE category = %s AND nutri_grade = '%s'"
                          "LIMIT 1")

    def print_products(self):
        self.cursor.execute(self.query_cat, (self.cat,))

        for i, (name, brand, nutri_grade) in enumerate(self.cursor):
            print("{}/ {} - marque: {} - nutri-score: {}".format(i+1, name, brand, nutri_grade))

    def print_substituted(self):

        while not self.cursor:
            self.cursor.execute(self.query_sub, (self.cat, self.nutri))
            self.nutri = chr(ord(self.nutri)+1)

        for (name, brand, nutri_grade) in self.cursor:
            print('{} - {} - {}'.format(name, brand, nutri_grade))

