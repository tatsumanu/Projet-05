""" file with all the constants for the main program and classes """

header = '### OPENFOODFACTS & OPENCLASSROOM, ensembles pour une\
 application qui vous veut du bien !! ###'

sub = "Voici un substitut plus sain au produit\
 selectionné:+ {}, de la marque {}, nutri-score: {}.+ Disponible dans\
 les magasins: {}.+ Liste des ingrédients:+ {} +Vous pouvez retrouver\
 toutes ces informations sur la page internet:+{}"

end = "Press 'q' to exit | Parcours Python - projet 05\
 - Conçu par Emmanuel Nocquet (Openclassroom student)"

welcome = ["Que souhaitez-vous faire?",
           "1/ Choisir un aliment à remplacer",
           "2/ Consulter mes aliments substitués"]

food = "Sélectionnez l'aliment que vous voulez remplacer (1 à 10)"

comments = ["Bienvenue dans l'application OpenFoodFacts !!!",
            "(1) Sauvegarder, (2) Rechercher sur internet,\
 (3) Menu principal ",
            " (1) pour Retourner au menu principal",
            "Choisissez la categorie de l'aliment à remplacer",
            "### L'article a été enregistré avec succès!"]

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
