
from mysql import connector
from random import choice


class Datab:

    def __init__(self, cat=0, nutri='a', answer=[]):
        self.categories = ['gateau', 'soda', 'pizza', 'yaourt',
                           'pate a tartiner']
        self.cat = self.categories[cat-1]
        self.nutri = nutri
        self.answer = answer
        self.cnx = connector.connect(user='student', host='localhost',
                                     database='openfoodfacts')
        self.cursor = self.cnx.cursor(buffered=True)

    def print_products(self):
        query_cat = ("SELECT DISTINCT name, brand, nutri_grade FROM food "
                     "WHERE category = %s"
                     "LIMIT 100")
        self.cursor.execute(query_cat, (self.cat,))
        res = []
        for (name, brand, nutri_grade) in self.cursor:
            res.append((name, brand, nutri_grade))
        prod = []
        for j in range(10):
            prod.append((j+1, choice(res)))
        for elt in prod:
            print("\t{}/ {} - marque: {} -\
 nutri-score: {}".format(elt[0], elt[1][0], elt[1][1], elt[1][2]))

    def print_substituted(self):
        res = []
        query_sub = ("SELECT name, brand, nutri_grade, store, link,\
                     ingredients, product_id FROM food "
                     "WHERE category = %s AND nutri_grade = %s")
        while not res:
            self.cursor.execute(query_sub, (self.cat, self.nutri))
            for (name, brand, nutri_grade,
                 store, link, ingredients, product_id) in self.cursor:
                res.append((name, brand, nutri_grade,
                            store, link, ingredients, product_id))
            self.nutri = chr(ord(self.nutri)+1)
        self.answer = choice(res)
        self.answer = list(self.answer)
        print("\nNous vous proposons un substitut plus sain au produit\
 selectionné, il s'agit de l'article:\n\n\t{}, de la marque {} dont le\
 nutri-score est de: {}\n\n\tCe produit est distribué dans les\
 magasins: {}\n\n\tPour votre complète information, voici la liste\
 des ingrédients:\n\n\t{}\n\n\tVous pouvez retrouver toutes ces\
 informations sur la page internet: {}".format(self.answer[0], self.answer[1],
                                               self.answer[2], self.answer[3],
                                               self.answer[5], self.answer[4]))

    def save_substituted(self):
        query_save = ("UPDATE food SET substituted = 'YES' WHERE\
                      product_id = %s")
        self.cursor.execute(query_save, (self.answer[6],))
        self.cnx.commit()
        print("\n\tL'article a été enregistré avec succès!\n")

    def search_substituted(self):
        res = []
        query_search = ("SELECT name, brand, nutri_grade, store,\
                        product_id FROM food "
                        "WHERE substituted = %s")
        self.cursor.execute(query_search, ('YES',))
        for i, (name, brand, nutri_grade, store,
                product_id) in enumerate(self.cursor):
            res.append((i+1, name, brand, nutri_grade, store, product_id))
        if res:
            print("\nVoici les aliments substitués que vous avez\
 enregistré:\n\n")
            for elt in res:
                print("\t{}/ {} - marque: {} -\
 nutri-score: {} - magasin: {}\n".format(elt[0], elt[1], elt[2],
                                         elt[3], elt[4]))

    def close_cnx(self):
        self.cursor.close()
        self.cnx.close()
