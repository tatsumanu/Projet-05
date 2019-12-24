
from mysql import connector
from random import choice
import requests
import json


class Datab:
    """ A class whose job is to handle the relation between the main
     program and the database. His methods manage to search the required
     data and print them to the screen. """

    def __init__(self, cat=0, nutri='a', answer=[]):
        self.nutri = nutri
        self.answer = answer
        self.cnx = connector.connect(user='student', host='localhost',
                                     database='openfoodfacts')
        self.cursor = self.cnx.cursor(buffered=True)
        self.sub = "\nNous vous proposons un substitut plus sain au produit\
 selectionné, il s'agit de l'article:\n\n\t{}, de la marque {} dont le\
 nutri-score est de: {}\n\n\tCe produit est distribué dans les\
 magasins: {}\n\n\tPour votre complète information, voici la liste\
 des ingrédients:\n\n\t{}\n\n\tVous pouvez retrouver toutes ces\
 informations sur la page internet: {}"
        search_cat = ("SELECT DISTINCT category FROM food")
        self.categories = []
        self.cursor.execute(search_cat,)
        for elt in self.cursor:
            self.categories += elt
        self.cat = self.categories[cat-1]

    def print_products(self):
        """ Query the DB and return 10 products of the selected category.
        Using the 'choice' function to randomize selection. """

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
        """ Query DB for a better product in the selected category. Print
         it with informations such as name, brand and ingredients. """

        res = []
        query_sub = ("SELECT name, brand, nutri_grade, store, link,\
                     ingredients, product_id FROM food "
                     "WHERE category = %s AND nutri_grade = %s")
        while len(res) < 5:
            self.cursor.execute(query_sub, (self.cat, self.nutri))
            for (name, brand, nutri_grade,
                 store, link, ingredients, product_id) in self.cursor:
                res.append((name, brand, nutri_grade,
                            store, link, ingredients, product_id))
            self.nutri = chr(ord(self.nutri)+1)
        self.answer = choice(res)
        self.answer = list(self.answer)
        print(self.sub.format(self.answer[0], self.answer[1],
                              self.answer[2], self.answer[3],
                              self.answer[5], self.answer[4]))

    def search_internet(self):
        """ Allow the user to look for an other substitute directly on
         internet via an API request. Then print it to the screen. """

        payload = {
            'tag_0': self.cat,
            'tag_contains_0': 'contains',
            'tagtype_0': 'categories',
            'tag_1': 'a',
            'tag_contains_1': 'contains',
            'tagtype_1': 'nutrition_grades',
            'tag_2': 'fr',
            'tag_contains_2': 'contains',
            'tagtype_2': 'lang',
            'sort_by': 'unique_scans_n',
            'page_size': 20,
            'action': 'process',
            'json': 1
        }
        data = ['product_name', 'brands', 'nutrition_grade_fr', 'url',
                'stores', 'ingredients_text']

        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                params=payload)
        for elt in response.json()['products']:
            for i in data:
                if not elt.get(i):
                    elt[i] = 'Non disponible'
            print(self.sub.format(elt['product_name'], elt['brands'],
                                  elt['nutrition_grade_fr'],
                                  elt['stores'], elt['ingredients_text'],
                                  elt['url']))
            self.answer = [elt['product_name'], elt['brands'],
                           elt['nutrition_grade_fr'], elt['stores'],
                           elt['url'], elt['ingredients_text']]

    def save_substituted(self):
        """ As the user chooses to save the substituted product, we save
        this information in the database by simply setting the corresponding
        'substituted' column to 'YES'. If the product comes from an API
        research, his informations are inserted into the database. """

        try:
            self.answer[6]
            query_save = ("UPDATE food SET substituted = 'YES' WHERE\
                        product_id = %s")
            self.cursor.execute(query_save, (self.answer[6],))
        except IndexError:
            query_save_web = ("INSERT INTO food (name, brand, nutri_grade,\
 store, link, ingredients, substituted, category) VALUES (%s, %s, %s, %s,\
 %s, %s, %s, %s)")
            self.cursor.execute(query_save_web,
                                (self.answer[0], self.answer[1],
                                 self.answer[2], self.answer[3],
                                 self.answer[4], self.answer[5],
                                 'YES', self.cat))
        print("\n\tL'article a été enregistré avec succès!\n")
        self.cnx.commit()

    def search_saved(self):
        """ Looks inside the database for previously saved products.
        An error message is printed if there isn't any. """

        res = []
        query_search = ("SELECT DISTINCT name, brand, nutri_grade, store,\
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
        else:
            print("\nVous n'avez aucun produit substitué enregistré\
 dans notre base de donnée!")

    def close_cnx(self):
        """ Closes mysql connector cursor and connexion with DB. """

        self.cursor.close()
        self.cnx.close()
