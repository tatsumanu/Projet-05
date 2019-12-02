# -*-coding:'utf8'-*-

import requests
import json
from mysql import connector

# connecting to the database
cnx = connector.connect(user='student', host='localhost',
                        database='openfoodfacts')

# creating a cursor object
cursor = cnx.cursor(buffered=True)

categories = ['gateaux', 'boisson', 'pizzas', 'yaourt', 'fromage', 'surgeles']

res = []


def get_data(liste, cat):

    # sending request to openfoodfacts API and adding the result in a list
    liste = []
    data = ['product_name', 'nutrition_grade_fr', 'url', 'stores',
            'ingredients_text']

    response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?\
        search_terms={}&page_size=100&json=1".format(cat))

    for elt in response.json()['products']:
        for i in data:
            if not elt.get(i):
                elt[i] = 'non dispo'
        liste.append((elt['product_name'], elt['nutrition_grade_fr'],
                      elt['url'], elt['stores'], elt['ingredients_text'], cat))
    print(liste)
    return liste, cat


def insert_data(liste, cat):

    # inserting data in database
    liste, cat = get_data(liste, cat)

    add_product = ("INSERT INTO food (name, nutri_grade, link, store,\
        ingredients, category) VALUES (%s, %s, %s, %s, %s, %s)")

    for i in range(len(liste)-1):
        cursor.execute(add_product, liste[i])


# doing the stuff for all categories
for cat in categories:
    insert_data(res, cat)

# updating database
cnx.commit()

# leaving the database
cursor.close()
cnx.close()
