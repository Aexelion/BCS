<Auteur : DUMANGET Dorian>



# [BCS] Projet d'authentification



## Introduction

Le but de ce TP est d'effectué un chiffrement authentifié qui utilisera une méthode de chiffrement par bloc avec un mode opératoire. Il faudra également implémenté un MAC afin de pouvoir vérifié notre message après transmission.

## Méthode de chiffrement

On utilise comme fonction de chiffrement par bloc, la fonction Midori qui prend en entrée un bloc de taille 64 bits ainsi qu'une clé de taille 128 bits. On doit alors choisir un mode opératoire qui permettra de chiffrer un message de taille quelconque. On choisi comme mode opératoire **CTR** qui est un mode permettant de paralleliser facilement le calcul.

## Authentification du message

Afin d'authentifier un message on utilise une méthode de MAC. On décide ici d'utiliser la méthode d'authentifcation **OMAC** très proche du CBC-MAC, avec une modification du dernier bloc. De plus le MAC générer suite à la partie CBC est surchiffrée afin d'éviter les attaques par pré-calcul du MAC. L'avantage de l'utilisation de OMAC est l'utilisation d'une clé unique au lieu de fournir deux clés différentes.

## Les différents fichiers

Cette partie liste et fournis une bref explication de l'ensemble des fichiers utilisés lors de l'authentification.

Les différents fichiers ont été développés pour fonctionner sous *python3*. Chaque fichier peut être executé afin d'effectué une première vérification des différentes fonctions internes.

- Midori64_perso.py : Fichier contenant le chiffrement par bloc Midori.
- Sha3_perso.py : Fichier contenant la fonction de hash Keccak. Cette implémentation n'est pas conforme avec l'implémentation officiel de Keccak. L'erreur viens sans doute de l'introduction des données dans l'état interne.
- trad.py : Fichier servant à effectuer les différentes traductions String <-> Hexadécimal <-> Binaire.
- ModeOp.py : Fichier définissant le mode opératoire utilisé lors du chiffrement.
- MAC_perso.py : Fichier contenant la définition du MAC utilisé.
- Authentifie.py : Fichier final. Celui-ci permet de chiffrer et déchiffrer des messages. Les caractères du message doivent être des caractères ASCII (sur 8 bits).  Le programme peut aussi prendre en paramètres des fichiers (pour le message d'entrée, le message de sortie, ou la clé à utiliser). Pour plus de renseignement sur la façon d'utiliser le programme, utilisez la commande -h (ou --help).

## Temps d'execution

J'utilise la commande *time* de Linux afin de déterminer le temps de chiffrement et déchiffrement. J'utilise également un mot de passe de taille inférieur à 512 bits.

Pour un fichier de 1 Ko :

- Pour chiffrer le fichier :
    - 0m0.408s
- Pour déchiffrer le fichier :
    - 0m0.332s

Pour un fichier de 10 Ko :

- Pour chiffrer le fichier :
    - 0m1.184s
- Pour déchiffrer le fichier :
    - 0m0.748s

Pour un fichier de 100 Ko :

- Pour chiffrer le fichier :
    - 0m7.444s
- Pour déchiffrer le fichier :
    - 0m3.852s

Pour un fichier de 1 Mo :

- Pour chiffrer le fichier :
    - 1m54.368s
- Pour déchiffrer le fichier :
    - 0m57.808s

Pour un fichier de 10 Mo le temps de chiffrement étant déjà supérieur à 15m, je n'ai pas tenter d'effectuer un chiffrement sur un fichier de taille supérieur.

​	
