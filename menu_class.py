from constants import welcome, comments, food, sub, payload, data
from random import choice
import requests


class Menu:
    """ Create a Menu object that will handle relations between the
    database and the user of the application. The app_menu method
    is called in every loop of the main function after checking if
    a key has been pressed, changing his parameters as the user
    makes his choices. """

    def __init__(self, obj, choice=""):
        self.obj = obj
        self.text = welcome
        self.choice = choice
        self.possibilities = ['1', '2']
        self.step = 1
        self.comments = comments[0]
        self.categories = []
        self.category = ""
        self.substituted = []

    def app_menu(self):
        # dispatching function
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
        # printing random products from the choosen category
        if self.choice in self.possibilities:
            self.step = 3
            self.comments = food
            self.category = self.categories[int(self.choice)-1]
            cursor = self.obj.ten_random_prod(self.category)
            res = [elt for elt in cursor]
            result = [((j,) + choice(res)) for j in range(10)]
            self.text = []
            for elt in result:
                self.text.append("\t{}/ {} - marque: {} -\
 nutri-score: {}".format(elt[0], elt[1], elt[2], elt[3]))
            self.possibilities = [str(i) for i in range(10)]

    def menu_step_3(self):
        # print a healthier product
        self.step = 4
        cursor = self.obj.search_a_substitute(self.category)
        res = [elt for elt in cursor]
        self.substituted = list(choice(res))

        self.text = sub.format(self.substituted[0], self.substituted[1],
                               self.substituted[2], self.substituted[3],
                               self.substituted[5], self.substituted[4])

        self.possibilities = [str(i) for i in range(1, 4)]
        self.comments = comments[1]

    def menu_step_4(self):
        # choose between saving, API live search, and back to main menu
        if self.choice == '1':
            # saving result in database
            self.obj.save_a_product(self.substituted)
            self.comments += comments[4]
        elif self.choice == '2':
            # looking for an alternative from internet
            self.search_internet()
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
        cursor = self.obj.search_category()
        self.categories = []
        for elt in cursor:
            self.categories += elt
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
        res = []
        self.step = 5
        cursor = self.obj.search_already_saved()
        for i, (name, brand, nutri_grade, store) in enumerate(cursor):
            res.append((i+1, name, brand, nutri_grade, store))
        if res:
            self.text = ["Voici les aliments substitués que vous avez\
 enregistré:"]
            for elt in res:
                self.text.append("{}/ {} - marque: {} -\
 nutri-score: {}".format(elt[0], elt[1], elt[2], elt[3]))
        else:
            self.text = ["Vous n'avez aucun produit substitué enregistré!"]
        self.comments = comments[2]
        self.possibilities = ['1']

    def search_internet(self):
        """ Allow the user to look for an other substitute directly on
         internet via an API request. """

        self.text = []
        payload['tag_0'] = self.category
        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                params=payload)
        for elt in response.json()['products']:
            for i in data:
                if not elt.get(i):
                    elt[i] = 'Non disponible'
            self.text = sub.format(elt['product_name'], elt['brands'],
                                   elt['nutrition_grade_fr'],
                                   elt['stores'], elt['ingredients_text'],
                                   elt['url'])
            self.substituted.append((elt['product_name'], elt['brands'],
                                     elt['nutrition_grade_fr'],
                                     elt['stores'], elt['ingredients_text'],
                                     elt['url']))
        if self.text == []:
            return "Nous n'avons trouvé aucun substitut plus sain au\
 produit sélectionné!"
