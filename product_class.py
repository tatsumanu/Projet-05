from random import choice
import requests
from variables import sub, payload, data, web_page, bar


class Product:
    """ Create an instance of a food object. This object is defined
     by the elements given by the Database class. Methods can choose
      and print the result in terminal. """

    def __init__(self, cursor):

        self.product = [elt for elt in cursor]

    def print_product(self):
        """ Among the products returned by the Database class, choose
        ten food products of a given category and print them to the
        screen. """

        print(bar, "\nVoici une sélection de 10 \
produits correspondants à la catégorie choisie:\n")
        for i in range(10):
            result = choice(self.product)
            if result[0] == "":
                result = choice(self.product)
            result[0].replace(' ', '')
            print(" {}/ {} - Marque: {} - Nutri_grade:\
 {}".format(i+1, result[0], result[1], result[2]))
        print("\n")

    def print_substitute(self):
        """ Manages to split the result in attributes for the product
        object. Print the result to the screen. """

        try:
            result = choice(self.product)
            self.name = result[0]
            self.brand = result[1]
            self.nutri_grade = result[2]
            self.store = result[3]
            self.link = result[4]
            self.ingredients = result[5].replace('_', '')
            self.product = result

            a = sub.format(self.name, self.brand,
                           self.nutri_grade, self.store,
                           self.ingredients, self.link)
            for elt in a.split('+'):
                print("\t{}".format(elt))
        except IndexError:
            print("\n", bar)
            print("\nNous n'avons trouvé aucun substitut plus sain au\
 produit sélectionné!\n")

    def print_saved(self):
        """ Print to the screen the saved products returned by database. """

        if self.product:
            print("\n", " Voici les aliments que vous avez\
 sauvegardé: ".center(100, '-'), "\n")
            for elt in self.product:
                print(" {} - Marque: {} - Nutri_grade:\
 {}".format(elt[0], elt[1], elt[2]))
            print("\n", "--".center(100, '-'), "\n")
        else:
            print("\nVous n'avez sauvegardé aucun produit pour l'instant!\n")

    def search_internet(self, category):
        """ Allow the user to look for an other substitute directly on
         internet via an API request. """

        self.product = []
        payload['tag_0'] = category
        response = requests.get(web_page,
                                params=payload)
        for elt in response.json()['products']:
            for i in data:
                if not elt.get(i):
                    elt[i] = 'Non disponible'

            self.product.append((elt['product_name'], elt['brands'],
                                 elt['nutrition_grade_fr'],
                                 elt['stores'], elt['url'],
                                 elt['ingredients_text']))
