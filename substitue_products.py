# ! /usr/bin/env python3
# coding: utf-8

'''
    substitute_products.py
    Author: Jimi Bourgeois
    Version: 20190516
    Describe: ...
'''

import urllib.request as req
import json
import pymysql.cursors
import time
import random

from mydb_gestion import *

class db_menu():

    def search_prod(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous afficher la liste de catégories ? O/n ")
            if choice.upper() == "N":
                print("\nRetour au menu principal")
                break
            elif choice.upper() == "O":
                choice_cat = True

                print("\n Liste des catégories:\n")
                
                db.execute("SELECT category_id, category_name FROM `mydb`.`Categories`")
                for ligne in db.fetchall():
                    list_id_cat = ligne[0]
                    list_name_cat = ligne[1]
                    print(list_id_cat,'-', list_name_cat)
                
                choice_cat = 0
                while choice_cat == 0:
                    choice_cat = input("\nSélectionner une catégorie de produit: ")

                    if choice_cat.upper() == "Q":
                        choice = False
                        break

                    elif choice_cat.isdigit() == False or int(choice_cat) >= 29 or int(choice_cat) == 0:
                        print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 28\n")
                        time.sleep(2)
                        choice_cat = 0

                    show_list_prod_select = f"SELECT product_id, product_name, product_nutri FROM `mydb`.`Products` WHERE Categories_category_id = {choice_cat}"
                    db.execute(show_list_prod_select)
                    for ligne in db.fetchall():
                        list_id_prod = ligne[0]
                        list_name_prod = ligne[1]
                        nutriscore_prod = ligne[2]
                        print(list_id_prod,"-", list_name_prod, "- Nutriscore:",nutriscore_prod)
                        continue
                        
                    choice_sub = 0
                    while choice_sub == 0:
                        choice_sub = input("\nSélectionner un produit à substituer: ")

                        if choice_sub.upper() == "Q":
                            choice = 0
                            break
                        
                        show_list_sub_select = f"SELECT * FROM `mydb`.`Products` WHERE product_id = {choice_sub}"
                        db.execute(show_list_sub_select)
                        for ligne_sub in db.fetchall():
                            sub_id = ligne_sub[0]
                            sub_name = ligne_sub[1]
                            sub_nutri = ligne_sub[3]
                            
                            list_best_nutri = f"SELECT * FROM `mydb`.`Products` WHERE Categories_category_id = {choice_cat} AND product_nutri <= '{sub_nutri}' ORDER BY product_nutri ASC"

                            db.execute(list_best_nutri)
                            result = db.fetchall()
                            best = (result)[0]
                            product_select = "Pas de produit à substituer"
                            if sub_nutri == (best)[3]:
                                print("\nLe produit sélectionné a le meilleur nutriscore de cette catégorie")
                                save_choice2 = 0
                                while save_choice2 is 0:
                                    choice = input("Souhaitez-vous quand même sauvegarder le produit dans les favoris ? O/n ")
                                    if choice.upper() == "N":
                                        print("\nRetour au menu principal")
                                        time.sleep(3)
                                        break
                                    elif choice.upper() == "O":
                                        db.execute("INSERT IGNORE INTO `mydb`.`Substitute` (save_product_id, save_product_sub_name) VALUES ('{}','{}')".format(sub_id, product_select))
                                        self.db_connect.commit()
                                        print("\nLe produit a bien été sauvegardé dans vos favoris")
                                        print("Retour au menu principal")
                                        time.sleep(3)
                                        break
                                
                            else:
                                best_id = (best)[0]
                                best_name = (best)[1]
                                best_nutriscore = (best)[3]
                                best_shop = (best)[2]
                                best_url = (best)[4]
                                print("\nProduit sélectionné:",sub_name,". Nutriscore:",sub_nutri)
                                print("Substitue:",best_name,". Nutriscore:",best_nutriscore)
                                print("Magasin(s):",best_shop)
                                print("Infos produit:",best_url)
                                save_choice1 = 0
                                while save_choice1 is 0:
                                    save_choice1 = input("\nSouhaitez-vous sauvegarder le produit dans la base ? O/n ")
                                    if save_choice1.upper() == "N":
                                        print("\nRetour au menu principal")
                                        time.sleep(3)
                                        break
                                    elif save_choice1.upper() == "O":
                                        db.execute("INSERT IGNORE INTO `mydb`.`Substitute` (save_product_id, save_product_sub_name) VALUES ('{}','{}')".format(best_id, sub_name))
                                        self.db_connect.commit()
                                        print("\nLe produit a bien été sauvegardé dans vos favoris")
                                        print("Retour au menu principal")
                                        time.sleep(3)
                                        break
                                


    def search_substitute(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous afficher vos produits favoris ? O/n ")
            if choice.upper() == "N":
                print("\nRetour au menu principal")
                time.sleep(2)
                break
            elif choice.upper() == "O":
                save_show = "SELECT * FROM PRODUCTS INNER JOIN SUBSTITUTE ON PRODUCTS.product_id = SUBSTITUTE.save_product_id INNER JOIN CATEGORIES ON PRODUCTS.Categories_category_id = CATEGORIES.category_id WHERE SUBSTITUTE.save_product_id"
                db.execute(save_show)
                #print(save_show)
                for results in db.fetchall():
                    #print(results)
                    name_sub = results[8]
                    name_save = results[1]
                    nutri_save = results[3]
                    shop_save = results[2]
                    url_save = results[4]
                    cat_save = results[10]
                    print("\nProduit substitué:",name_sub)
                    print("Substitue:",name_save,". Nutriscore:",nutri_save)
                    print("Catégorie:",cat_save)
                    print("Magasin(s):",shop_save)
                    print("Infos produit:",url_save)
                print("\nRetour au menu principal")
                time.sleep(3)
                break
