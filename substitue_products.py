# ! /usr/bin/env python3
# coding: utf-8

'''
    substitute_products.py
    Author: Jimi Bourgeois
    Version: 2019-05-16
    Describe: ...
'''

import urllib.request as req
import json
import pymysql.cursors
import time
import random

class db_menu():

    def search_prod(self):
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous afficher la liste de catégories ? O/n ")
            if choice.upper() == "N":
                print("\nRetour au menu principal")
                break
            elif choice.upper() == "O":
                choice_cat = 0

                print("\n Liste des catégories:\n")
                self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
                db = self.db_connect.cursor()
                db.execute("SELECT category_id, category_name FROM `mydb`.`Categories`")
                for ligne in db.fetchall():
                    list_id_cat = ligne[0]
                    list_name_cat = ligne[1]
                    print(list_id_cat,'-', list_name_cat)

                while choice_cat == 0:
                    choice_cat = input("\nSelectionner une catégorie de produit: ")

                    if choice.upper() == "Q":
                        choice = False
                        break

                    elif choice_cat.isdigit() == False or int(choice_cat) >= 29 or int(choice_cat) == 0:
                        print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 28\n")
                        time.sleep(2)
                        choice_cat = 0
                    
                    
                    elif int(choice_cat) == 1:
                        
                        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
                        db = self.db_connect.cursor()

                        print("\nListe des produits de la catégorie - Aliments d origine végétale -\n")
                        db.execute("SELECT product_name, Categories_category_id, product_nutri FROM `mydb`.`Products` WHERE `product_nutri`= 'a'")
                        for ligne in db.fetchall():
                            list_name_prod = ligne[0]
                            list_id_cat = ligne[1]
                            nutriscore_prod = ligne[2]
                            if list_id_cat == 1:
                                print(list_name_prod,"- Nutriscore:",nutriscore_prod)
                                choice_cat = 0


    def search_substitute(self):
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous afficher les produits sauvegardés ? O/n ")
            if choice.upper() == "N":
                print("\nRetour au menu principal")
                break
            elif choice.upper() == "O":
                user_choice = 0

    