# ! /usr/bin/env python3
# coding: utf-8


"""
!!!! OpenFoodFacts App !!!!
Author: Jimi Bourgeois
Version: 20190419
Project: Project 5 OpenClassrooms
Code language: Python3
Coding: Utf-8
"""

import urllib.request
import json
import time
import os
import sys

from mydb_gestion import *


main_app_loop = True

def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "Linux":
        os.system("clear")


while main_app_loop is True:
    choice = 0
    clear_prompt()
    
    print("\nBienvenue sur la base de données d'OpenFoodFacts.com (Version FR)\n")
    print("Menu principale de la base de données:")
    print("1 - Charger la base de données en local* ?")
    print("2 - Rechercher un produit de substitution dans la base ?")
    print("3 - Accéder de vos produits préféres ?")
    print("4 - Supprimer vos produits préféres ?")
    print("\n *Pour la premère utilisation du programme, oublier pas de charger les données dans la base")
    
    while choice == 0:
        choice = input("\nVotre choix (Entrer Q pour quitter le programme): ")

        if choice.upper() == "Q":
            main_app_loop = False
            break

        elif choice.isdigit() == False or int(choice) >= 5 or int(choice) == 0:
            print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 4\n")
            time.sleep(2)
            break
        
        elif int(choice) == 1:
            dfcat = db_request()
            dfcat.create_db_cat()
        elif int(choice) == 2:
            search_prod = db_request()
            search_prod.show_list_cat()
        elif int(choice) == 3:
            access_saved = db_request()
            access_saved.create_db_prod()
        elif int(choice) == 4:
            clear_backup = db_request()
            clear_backup.db_cleardata_cat()
            clear_backup.db_cleardata_prod()
            clear_backup.db_cleardata_sub()