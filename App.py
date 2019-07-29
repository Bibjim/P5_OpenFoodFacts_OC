# ! /usr/bin/env python3
# coding: utf-8


"""
!!!! OpenFoodFacts App !!!!
Author: Jimi Bourgeois
Version: 2019-07-22
Project: Project 5 OpenClassrooms
Code language: Python3
Coding: utf-8
"""
# Specific import modules
import pymysql.cursors

# Standard import modules
import urllib.request
import json
import time
import os
import sys

# Import modules for app operation
from mydb_gestion import *
from substitue_products import *


main_app_loop = True

# Main loop
while main_app_loop is True:
    choice = 0
    
    # Main menu display
    print("\nBienvenue sur la base de données d'OpenFoodFacts.com (Version FR)\n")
    print("Menu principal de la base de données:")
    print("1 - Charger la base de données en local* ?")
    print("2 - Rechercher un produit de substitution dans la base ?")
    print("3 - Accéder à vos produits favoris ?")
    print("4 - Gestion de la base (suppression des données)")
    print("\n *Pour la première utilisation du programme, charger les données dans la base en local")
    
    while choice == 0:
        choice = input("\nVotre choix (Entrer Q pour quitter le programme): ")

        if choice.upper() == "Q":
            print("\n!!! A bientôt sur l'application OpenFoodFacts !!!")
            time.sleep(2)
            main_app_loop = False
            break
        # Bound the choice of the main menu
        elif choice.isdigit() == False or int(choice) >= 5 or int(choice) == 0:
            print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 4\n")
            time.sleep(2)
            break
        # Choice of menu 1 "creation of the database and local loading of the data"
        elif int(choice) == 1:
            choice_dl = 0
            while choice_dl is 0:
                choice_dl = input("\nConfirmation du téléchargements en local des données d'OpnFoodFacts , O/n ")
                if choice_dl.upper() == "N":
                    print("\nRetour au menu principal")
                    break

                elif choice_dl.upper() == "O":
                    # Create the database ans tables
                    db_create = db_request() # class of "mydb_gestion.py"
                    db_create.create_db() # def of "mydb_gestion.py"
                    db_create.create_tables() # def of "mydb_gestion.py"

                    # Loading API data
                    dfdownload = db_request() # class of "mydb_gestion.py"
                    dfdownload.create_db_cat() # def of "mydb_gestion.py"
                    dfdownload.create_db_prod() # def of "mydb_gestion.py"
                    break
        
        # Choice of menu 2 "search for a substitute product"
        elif int(choice) == 2:
            search_prod = db_menu() # class of "substitute_products.py"
            search_prod.search_prod() # def of "substitute_products.py"

        # Choice of menu 3 "show substitute product"
        elif int(choice) == 3:
            access_saved = db_menu() # class of "substitute_products.py"
            access_saved.search_substitute() # def of "substitute_products.py"
        
        # Choice of menu 4 "Delete menu"
        elif int(choice) == 4:
            choice_del = 0
            while choice_del is 0:
                choice_del = input("\nVoulez vous supprimer les valeurs de la base de données ? O/n ")
                if choice_del.upper() == "N":
                    print("\nRetour au menu principal")
                    break
                elif choice_del.upper() == "O":
                    del_choice = 0
                    
                    # Display of the delete menu
                    print("\nListe des table de la base de données:")
                    print("1 - Table Categories")
                    print("2 - Table Products")
                    print("3 - Table Substitute")
                    print("Q - Retour au menu principal")
                    print("\nAttention !!! vous ne pouvez pas supprimer la table Categories sans")
                    print("avoir préalablement supprimer les tables Products et Substitute !!!")
                    print("Toutes données supprimées sont définitives")

                    while del_choice == 0:
                        del_choice = input("\nSelectionner la table à supprimer (Q pour annuler): ")

                        if del_choice.upper() == "Q":
                            choice = False
                            break
                        
                        # Bound the choice of the menu
                        elif del_choice.isdigit() == False or int(del_choice) >= 3 or int(del_choice) == 0:
                            print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 3\n")
                            time.sleep(2)
                            del_choice = 0
                        
                        elif int(del_choice) == 1:
                            clear_backup = db_request() # class of "mydb_gestion.py"
                            clear_backup.db_cleardata_cat() # def of "mydb_gestion.py"

                        elif int(del_choice) == 2:
                            clear_backup = db_request() # class of "mydb_gestion.py"
                            clear_backup.db_cleardata_prod() # def of "mydb_gestion.py"
                        
                        elif int(del_choice) == 3:
                            clear_backup = db_request() # class of "mydb_gestion.py"
                            clear_backup.db_cleardata_sub() # def of "mydb_gestion.py"