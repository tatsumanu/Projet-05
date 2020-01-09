from mysql import connector
from random import choice
from texts import welcome, comments, food, sub, data, query_search
from texts import query_cat, query_sub, query_save, query_save_web
import requests


class Datab:
    """ A class whose job is to handle the relation between the main
     program and the database. His methods manage to search the required
     data and print them to the screen. """

    def __init__(self, cat=0, nutri='b', answer=[]):
        self.nutri = nutri
        self.answer = answer
        try:
            self.cnx = connector.connect(user='student', host='localhost',
                                         database='openfoodfacts')
            print("Connexion established with database")
        except connector.Error as err:
            print(err)
        self.cursor = self.cnx.cursor(buffered=True)
        search_cat = ("SELECT DISTINCT category FROM food")
        self.categories = []
        self.cursor.execute(search_cat,)
        for elt in self.cursor:
            self.categories += elt
        self.cat = self.categories[cat-1]

    def print_products(self):
        """ Query the DB and return 10 products of the selected category.
        Using the 'choice' function to randomize selection. """

        self.cursor.execute(query_cat, (self.cat,))
        res = [(name, brand, nutri_grade)
               for (name, brand, nutri_grade) in self.cursor
               ]
        result = [((j,) + choice(res)) for j in range(10)]
        solution = []
        for elt in result:
            solution.append("\t{}/ {} - marque: {} -\
 nutri-score: {}".format(elt[0], elt[1], elt[2], elt[3]))
        return solution

    def print_substituted(self):
        """ Query DB for a better product in the selected category. Print
         it with informations such as name, brand and ingredients. """

        res = []
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
        solution = sub.format(self.answer[0], self.answer[1],
                              self.answer[2], self.answer[3],
                              self.answer[5], self.answer[4])
        return solution

    def search_internet(self):
        """ Allow the user to look for an other substitute directly on
         internet via an API request. Then print it to the screen. """

        res = ""
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
        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                params=payload)
        for elt in response.json()['products']:
            for i in data:
                if not elt.get(i):
                    elt[i] = 'Non disponible'
            res = sub.format(elt['product_name'], elt['brands'],
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
            self.cursor.execute(query_save, (self.answer[6],))
        except IndexError:
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
            self.menu_step_1()
        elif self.step == 2:
            self.menu_step_2()
        elif self.step == 3:
            self.menu_step_3()
        elif self.step == 4:
            self.menu_step_4()
        elif self.step == 5:
            self.menu_step_5()

    def menu_step_1(self):
        # welcome menu
        if self.choice == '1':
            self.menu_categories()
        elif self.choice == '2':
            self.menu_saved_products()

    def menu_step_2(self):
        # now printing random products from the choosen category
        if self.choice in self.possibilities:
            self.step = 3
            self.comments = food
            self.cat = self.categories[int(self.choice)-1]
            self.text = self.print_products()
            self.possibilities = [str(i) for i in range(10)]

    def menu_step_3(self):
        # print a healthier product
        self.step = 4
        self.text = self.print_substituted()
        self.possibilities = [str(i) for i in range(1, 4)]
        self.comments = comments[1]

    def menu_step_4(self):
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

    def menu_step_5(self):
        # saved products menu
        if self.choice in self.possibilities:
            self.text = welcome
            self.comments = comments[0]
            self.step = 1

    def menu_categories(self):
        # choosing products's category
        self.step = 2
        self.text = []
        self.comments = comments[3]
        self.possibilities = [
            str(i)
            for i in range(1, len(self.categories)+1)
        ]
        for elt in list(zip(self.possibilities, self.categories)):
            i, j = elt
            self.text.append(("{}/ {}".format(i, j)))

    def menu_saved_products(self):
        # going to already saved products
        self.step = 5
        self.text = self.search_saved()
        self.comments = comments[2]
        self.possibilities = ['1']
