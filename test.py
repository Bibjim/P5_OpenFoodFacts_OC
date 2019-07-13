# ! /usr/bin/env python3
# coding: utf-8


"""
!!!! OpenFoodFacts App !!!!
Author: Jimi Bourgeois
Version: 20190419
Project: Project 5 OpenClassrooms
Code language: Python3
Coding: utf-8
"""
# Import specifique modules
import pymysql.cursors

# Import standard modules
import urllib.request
import json
import time
import os
import sys

from mydb_gestion import *
from substitue_products import *
from create_database import *


main_app_loop = True

def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "Linux":
        os.system("clear")


while main_app_loop is True:
    choice = 0
    clear_prompt()
    
    print("\nBienvenue dans la partie test du programme\n")
    print("Menu principal:")
    print("1 - test de creation de la structure")
    print("2 - test de recherche de produit de substitution")
    print("3 - Accéder de vos produits favoris")
    print("4 - Gestion de la base")
    
    while choice == 0:
        choice = input("\nVotre choix (Entrer Q pour quitter le programme): ")

        if choice.upper() == "Q":
            print("\n!!! A bientôt !!!")
            time.sleep(3)
            main_app_loop = False
            break

        elif choice.isdigit() == False or int(choice) >= 7 or int(choice) == 0:
            print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 4\n")
            time.sleep(2)
            break
        
        elif int(choice) == 1:
            choice_dl = 0
            while choice_dl is 0:
                choice_dl = input("\ntest de creation de la base de données, O/n ")
                if choice_dl.upper() == "N":
                    print("\nRetour au menu principal")
                    break

                elif choice_dl.upper() == "O":
                    create = create_structure_db()
                    create.create_db()
                    create.create_table_cat()
                    #dfdownload = db_request()
                    #dfdownload.create_db_cat()
                    #dfdownload.create_db_prod()
                    break

        elif int(choice) == 2:
            search_prod = db_menu()
            search_prod.search_prod()
        elif int(choice) == 3:
            access_saved = db_menu()
            access_saved.search_substitute()


