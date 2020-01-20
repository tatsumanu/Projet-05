""" file with all the constants for the main program and classes """

header = '#      OPENFOODFACTS & OPENCLASSROOM, ensembles pour une\
 application qui vous veut du bien !!      #'

escape = "\n\n\n"

bar = "--".center(100, '-')

welcome = [escape, "##".center(100, '#'), "\n", header, "\n",
           "##".center(100, '#'), "\n",
           " Menu principal ".center(100, '-'), "\n",
           "Que souhaitez-vous faire?".center(100),
           "1/ Choisir un aliment à remplacer".center(100),
           "2/ Consulter mes aliments substitués".center(100),
           "3/ Quitter le programme".center(100),
           "\n\n", bar, escape]

categorie = " Faites votre choix parmi les catégories\
 suivantes: ".center(100, '-')

sub_menu = " (1) Sauvegarder l'aliment - (2)\
 Rechercher une alternative sur internet - (q) Menu\
 principal ".center(100, '-')

sub = "\nVoici un substitut plus sain au produit\
 selectionné:+\n+{}, de la marque {}, nutri-score: {}.+Disponible dans\
 les magasins: {}+\n+Liste des ingrédients:+{}+\n+Vous pouvez retrouver\
 toutes ces informations sur la page internet:+{}\n"

back = "Appuyez sur 'Enter' pour revenir au menu principal.."

data = ['product_name', 'brands', 'nutrition_grade_fr', 'url',
        'stores', 'ingredients_text']

payload = {
    'tag_0': 'to be changed',
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

web_page = "https://fr.openfoodfacts.org/cgi/search.pl?"
