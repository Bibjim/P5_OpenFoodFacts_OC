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


main_app_loop = True

def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "Linux":
        os.system("clear")


while main_app_loop is True:
    choice = 0
    clear_prompt()
    
    print("\nBienvenue sur la base de données d'OpenFoodFacts.com (Version FR)\n")
    print("Menu principal de la base de données:")
    print("1 - Charger la base de données en local* ?")
    print("2 - Rechercher un produit de substitution dans la base ?")
    print("3 - Accéder de vos produits favoris ?")
    print("4 - Gestion de la base (suppression des données)")
    print("\n *Pour la première utilisation du programme, charger les données dans la base en local")
    
    while choice == 0:
        choice = input("\nVotre choix (Entrer Q pour quitter le programme): ")

        if choice.upper() == "Q":
            print("\n!!! A bientôt sur l'application OpenFoodFacts !!!")
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
                choice_dl = input("\nConfirmation du téléchargements en local des données d'OpnFoodFacts , O/n ")
                if choice_dl.upper() == "N":
                    print("\nRetour au menu principal")
                    break

                elif choice_dl.upper() == "O":
                    db_create = db_request()
                    db_create.create_db()
                    dfdownload = db_request()
                    dfdownload.create_db_cat()
                    dfdownload.create_db_prod()
                    break

        elif int(choice) == 2:
            search_prod = db_menu()
            search_prod.search_prod()
        elif int(choice) == 3:
            access_saved = db_menu()
            access_saved.search_substitute()
        elif int(choice) == 4:
            choice_del = 0
            while choice_del is 0:
                choice_del = input("\nVoulez vous supprimer les valeurs de la base de données ? O/n ")
                if choice_del.upper() == "N":
                    print("\nRetour au menu principal")
                    break
                elif choice_del.upper() == "O":
                    del_choice = 0

                    print("\nListe des table de la base de données:")
                    print("1 - Table Categories")
                    print("2 - Table Products")
                    print("3 - Table Substitute")
                    print("Q - Retour au menu principal")
                    print("\nAttention !!! vous ne pouvez pas supprimer la table Categories sans")
                    print("avoir préalablement supprimer les tables Products et Substitute !!!")
                    print("Toutes données supprimées sont définitives")

                    while del_choice == 0:
                        del_choice = input("\nSelectionner la table à supprimer: (Tapez A pour annuler)")

                        if del_choice.upper() == "A":
                            choice = False
                            break

                        elif del_choice.isdigit() == False or int(del_choice) >= 4 or int(del_choice) == 0:
                            print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 3\n")
                            time.sleep(2)
                            del_choice = 0
                        
                        elif int(del_choice) == 1:
                            clear_backup = db_request()
                            clear_backup.db_cleardata_cat()

                        elif int(del_choice) == 2:
                            clear_backup = db_request()
                            clear_backup.db_cleardata_prod()
                        
                        elif int(del_choice) == 3:
                            clear_backup = db_request()
                            clear_backup.db_cleardata_sub()