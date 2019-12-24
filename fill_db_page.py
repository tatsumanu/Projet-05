# -*-coding:'utf8'-*-

import requests
import json
import argparse
import time
from tqdm import tqdm
from mysql import connector


def main():

    # command line functionnalities
    parser = argparse.ArgumentParser(description="\nLet's find some \
    food for our database...")
    parser.add_argument('--page_size', type=int, default=20, help='Set \
    the number of products by page for our API requests')
    parser.add_argument('--nb_page', type=int, default=10, help='Set the \
    number of page in the API requests')
    parser.add_argument('--categories', type=str, default=['gateau',
                                                           'soda', 'pizza',
                                                           'yaourt',
                                                           'pate a tartiner'],
                        action='append', help='Add food categories to default\
    (default: gateau, soda, pizza, yaourt, pate a tartiner)')
    args = parser.parse_args()

    nb_page = args.nb_page
    page_size = args.page_size
    categories = args.categories

    fill_db(nb_page, page_size, categories)


def fill_db(nb_page, page_size, categories):

    # starting point
    t1 = time.time()

    # trying to connect to mysql database
    try:
        cnx = connector.connect(user='student', host='localhost',
                                database='openfoodfacts')
        print("Connexion established with database")
    except connector.Error as err:
        print(err)

    # creating cursor object
    cursor = cnx.cursor(buffered=True)

    # main loop iterating through the categories of food given to the script
    cpt = 1
    while cpt <= nb_page:
        print('Collecting products from {} categories \
    in page: {}/{}'.format(len(categories), cpt, nb_page))
        for cat in tqdm(categories):

            data = ['product_name', 'brands', 'nutrition_grade_fr', 'url',
                    'stores', 'ingredients_text']

            payload = {
                'tag_0': cat,
                'tag_contains_0': 'contains',
                'tagtype_0': 'categories',
                'tag_1': 'fr',
                'tag_contains_1': 'contains',
                'tagtype_1': 'lang',
                'sort_by': 'unique_scans_n',
                'page_size': page_size,
                'page': cpt,
                'action': 'process',
                'json': 1
            }

            response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                    params=payload)

            products = response.json()['products']

            p = (tuple(elt.get(i, None) for i in data) for elt in products)

            add_product = "INSERT INTO food (name, brand, nutri_grade, link,\
    store, ingredients, category) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            for elt in p:
                elt += cat,
                cursor.execute(add_product, elt)
        cpt += 1

    # clearing the results in database for name and brand
    var = None
    cursor.execute("DELETE FROM FOOD WHERE name IS %s OR brand IS %s",
                   (var, var))

    print("Operations completed successfully in {:02f}\
    seconds!".format((time.time() - t1)))

    # commit informations stored in database
    cnx.commit()

    # closing cursor and connexion to database
    cursor.close()
    cnx.close()


if __name__ == "__main__":

    main()
