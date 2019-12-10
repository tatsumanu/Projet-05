# Projet 05
-----------

-> Il s'agit de créer un programme qui interagit avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

Le projet comprend:

 - Une base de données mysql 'openfoodfacts' avec une table 'food'
 
 - Un script python d'alimentation de la base de données: 
 
       * le programme adresse des requêtes à l'API du site internet d'Openfoodfacts
       
       * le programme effectue un tri dans les réponses obtenues (au format JSON) et gère les erreurs dans les réponses
       
       * il alimente la table 'food' de la base de données 'openfoodfacts'
       
 - Le programme principal, destiné à l'utilisateur final: 
 
       * un menu accueille l'utilisateur et lui laisse le choix entre choisir un aliment à remplacer et consulter les aliments substitués déjà enregistrés
       
       * le premier choix le conduit ensuite à définir une catégorie d'aliment à rechercher
       
       * le programme affiche un échantillon aléatoire de 10 produits de cette catégorie. L'utilisateur doit saisir le chiffre correspondant au produit qu'il désire substituer
       
       * le programme effectue une recherche dans la base de données et renvoie un produit de la même catégorie mais présentant un score nutritionnel plus avantageux que celui choisi par l'utilisateur. Il donne la description complète de celui-ci avec un lien vers le site internet d'openfoodfacts
       
       * l'utilisateur a la possibilité d'enregistrer ce produit proposé par le programme dans ses produits substitués
       
       * l'utilisateur revient ensuite au menu principal. Il peut à nouveau rechercher un aliment à substituer, consulter ses produits déjà substitués ou quitter le programme
 
 
