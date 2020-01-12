# -*-coding:'utf8'-*-

import requests
import argparse
import time
from tqdm import tqdm
from mysql import connector
from mysql.connector import errorcode

tables = {}
tables['category'] = (
    "CREATE TABLE category ("
    " category_id INT AUTO_INCREMENT,"
    " category VARCHAR(15),"
    " PRIMARY KEY (category_id)"
    ") ENGINE=INNODB"
)

tables['substituted'] = (
    "CREATE TABLE substituted ("
    " substituted_id INT AUTO_INCREMENT,"
    " name TEXT,"
    " brand TEXT,"
    " nutri_grade VARCHAR(5),"
    " store TEXT,"
    " link TEXT,"
    " ingredients TEXT,"
    " PRIMARY KEY (substituted_id)"
    ") ENGINE=INNODB"
)

tables['food'] = (
    "CREATE TABLE `openfoodfacts`.`food` ("
    " `product_id` INT NOT NULL AUTO_INCREMENT,"
    " `name` TEXT NULL,"
    " `brand` TEXT NULL,"
    " `nutri_grade` VARCHAR(5) NULL,"
    " `ingredients` TEXT NULL,"
    " `store` TEXT NULL,"
    " `link` TEXT NULL,"
    " `cat_id` INT NULL,"
    " PRIMARY KEY (`product_id`),"
    " INDEX `categories_fk_idx` (`cat_id`) VISIBLE,"
    " CONSTRAINT `categories_fk`"
    "     FOREIGN KEY (`cat_id`)"
    "     REFERENCES `openfoodfacts`.`category` (`category_id`)"
    "     ON DELETE CASCADE"
    "     ON UPDATE NO ACTION)"
    " ENGINE = InnoDB"
    " DEFAULT CHARACTER SET = utf8"
)


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


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET\
 'utf8'".format('openfoodfacts'))
    except connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def fill_db(nb_page, page_size, categories):

    # trying to connect to mysql database
    try:
        cnx = connector.connect(user='student', host='localhost')
        # creating cursor object
        cursor = cnx.cursor(buffered=True)
        print("Connexion established with database")
    except connector.Error as err:
        print(err)

    try:
        cursor.execute("USE {}".format('openfoodfacts'))
    except connector.Error as err:
        print("Database {} does not exists.".format('openfoodfacts'))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format('openfoodfacts'))
            cnx.database = 'openfoodfacts'
        else:
            print(err)
            exit(1)

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    # starting point
    t1 = time.time()

    # inserting categories in category table
    add_category = "INSERT INTO category (category) VALUES (%s)"
    for cat in categories:
        cursor.execute(add_category, (cat,))

    cnx.commit()

    # main loop iterating through the categories of food given to the script
    cpt = 1
    while cpt <= nb_page:
        print('Collecting products from {} categories \
    in page: {}/{}'.format(len(categories), cpt, nb_page))
        for cat in tqdm(categories):

            url = "https://fr.openfoodfacts.org/cgi/search.pl?"

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

            response = requests.get(url, params=payload)

            products = response.json()['products']

            p = (tuple(elt.get(i, None) for i in data) for elt in products)

            add_product = "INSERT INTO food (name, brand, nutri_grade, link,\
    store, ingredients, cat_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            for elt in p:
                elt += (categories.index(cat)+1),
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
