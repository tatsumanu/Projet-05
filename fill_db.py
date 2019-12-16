# -*-coding:'utf8'-*-

import requests
import json
from mysql import connector
import time
from tqdm import tqdm

t1 = time.time()

try:
    cnx = connector.connect(user='student', host='localhost',
                            database='openfoodfacts')
except connector.Error as err:
    print(err)

cursor = cnx.cursor(buffered=True)

categories = ['gateau', 'soda', 'pizza', 'yaourt',
              'pate a tartiner']


for cat in tqdm(categories):

    res = []

    data = ['product_name', 'brands', 'nutrition_grade_fr', 'url', 'stores',
            'ingredients_text']

    payload = {
        'tag_0': cat,
        'tag_contains_0': 'contains',
        'tagtype_0': 'categories',
        'tag_1': 'fr',
        'tag_contains_1': 'contains',
        'tagtype_1': 'lang',
        'sort_by': 'unique_scans_n',
        'page_size': 1000,
        'action': 'process',
        'json': 1
    }

    response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                            params=payload)

    for elt in response.json()['products']:
        for i in data:
            if not elt.get(i):
                elt[i] = 'non disponible'
        res.append((elt['product_name'], elt['brands'],
                    elt['nutrition_grade_fr'], elt['url'],
                    elt['stores'], elt['ingredients_text'],
                    payload['tag_0']))

    add_product = ("INSERT INTO food (name, brand, nutri_grade, link, store,\
        ingredients, category) VALUES (%s, %s, %s, %s, %s, %s, %s)")

    for elt in res:
        cursor.execute(add_product, elt)

cursor.execute("DELETE FROM FOOD WHERE name = %s OR brand = %s",
               ('non disponible', 'non disponible'))

print("Operations completed successfully in {:02f}\
 seconds!".format((time.time() - t1)))

cnx.commit()

cursor.close()
cnx.close()
