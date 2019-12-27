
from mysql import connector
from random import choice
from texts import welcome, comments, food
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
        self.sub = "Voici un substitut plus sain au produit\
 selectionné: {}, de la marque {}, nutri-score: {}. Disponible dans\
 les magasins: {}. Liste des ingrédients: {} Vous pouvez retrouver toutes ces\
 informations sur la page internet:{}"
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
        solution = []
        for elt in prod:
            solution.append("\t{}/ {} - marque: {} -\
 nutri-score: {}".format(elt[0], elt[1][0], elt[1][1], elt[1][2]))
        return solution

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
        solution = ""
        solution = self.sub.format(self.answer[0], self.answer[1],
                                   self.answer[2], self.answer[3],
                                   self.answer[5], self.answer[4])
        return solution

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
        res = ""
        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                params=payload)
        for elt in response.json()['products']:
            for i in data:
                if not elt.get(i):
                    elt[i] = 'Non disponible'
            res = self.sub.format(elt['product_name'], elt['brands'],
                                  elt['nutrition_grade_fr'],
                                  elt['stores'], elt['ingredients_text'],
                                  elt['url'])
            self.answer = [elt['product_name'], elt['brands'],
                           elt['nutrition_grade_fr'], elt['stores'],
                           elt['url'], elt['ingredients_text']]
        return res

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
        self.cnx.commit()
        return "### L'article a été enregistré avec succès!"

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
            solution = ["Voici les aliments substitués que vous avez\
 enregistré:"]
            for elt in res:
                solution.append("\t{}/ {} - marque: {} -\
 nutri-score: {} - magasin: {}\n".format(elt[0], elt[1], elt[2],
                                         elt[3], elt[4]))
            print(solution)
            return solution
        else:
            return ["Vous n'avez aucun produit substitué enregistré!"]

    def close_cnx(self):
        """ Closes mysql connector cursor and connexion with DB. """

        self.cursor.close()
        self.cnx.close()


class Menu(Datab):
    """ Create a Menu object that will handle relations between the
    database and the user of the application. The app_menu method
    is called in every loop of the main function after checking if
    a key has been pressed, changing his parameters as the user
    makes his choices """

    def __init__(self, text="", choice=""):
        Datab.__init__(self)
        self.text = welcome
        self.choice = choice
        self.possibilities = ['1', '2']
        self.step = 1
        self.comments = comments[0]

    def app_menu(self):
        if self.step == 1:
            # welcome menu
            if self.choice == '1':
                # choosing products's category
                self.step = 2
                self.text = []
                self.comments = comments[3]
                self.possibilities = [str(i) for i in range(1, len(self.categories)+1)]
                for elt in list(zip(self.possibilities, self.categories)):
                    i, j = elt
                    self.text.append(("{}/ {}".format(i, j)))
            elif self.choice == '2':
                # going to already saved products
                self.step = 9
                self.text = self.search_saved()
                self.comments = comments[2]
                self.possibilities = ['1']
        elif self.step == 2:
            # now printing random products from the choosen category
            if self.choice in self.possibilities:
                self.step = 3
                self.comments = food
                self.cat = self.categories[int(self.choice)-1]
                self.text = self.print_products()
                self.possibilities = [str(i) for i in range(10)]
        elif self.step == 3:
            # now heading to a healthier product
            self.step = 4
            self.text = self.print_substituted()
            self.possibilities = [str(i) for i in range(1, 4)]
            self.comments = comments[1]
        elif self.step == 4:
            # choose between saving, API live search, and back to main menu
            if self.choice == '1':
                # saving result in database
                self.comments += self.save_substituted()
            elif self.choice == '2':
                # looking for an alternative from internet
                self.text = self.search_internet()
                self.comments = comments[1]
            elif self.choice == '3':
                # back to main menu
                self.text = welcome
                self.comments = comments[0]
                self.step = 1
        elif self.step == 9:
            # back to main menu
            if self.choice in self.possibilities:
                self.text = welcome
                self.comments = comments[0]
                self.step = 1
