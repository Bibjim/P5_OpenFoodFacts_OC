# ! /usr/bin/env python3
# coding: utf-8

'''
    mydb_gestion.py
    Author: Jimi Bourgeois
    Version: 2019-04-19
    Describe: Database connect
'''

import urllib.request as req
import json
import pymysql.cursors

from substitue_products import *

class db_request():

    def create_db_cat(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        url="https://fr.openfoodfacts.org/categories.json"
        u = req.urlopen(url)
        content = u.read()
        jsonstr = content.decode("UTF-8")
        dfAll = json.loads(jsonstr)

        for categories in dfAll['tags'][:30]:
            categories_name = categories['name']
            categories_name = categories_name.replace("'", " ")
            if len(categories_name) >= 30:
                continue
            dfAll = (categories_name, categories['url'])

            db.execute("INSERT IGNORE INTO `mydb`.`Categories` (category_name, category_url) VALUES ('{}', '{}')".format(
                categories_name, categories['url']))
            self.db_connect.commit()

                
        db.execute("SELECT COUNT(*) FROM `mydb`.`Categories`")
        sql_return = db.fetchone()
        print("\n*****************************************************************")
        print("* La base de données est chargée avec %s catégories de produits *" % (sql_return))
        print("*****************************************************************")

    def create_db_prod(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        db.execute("SELECT category_id, category_url FROM `mydb`.`Categories`")
        
        for ligne in db.fetchall():
            list_id_cat = ligne[0]
            list_url_cat = ligne[1]
            list_url_cat += '.json'
            
            url_prod = req.urlopen(list_url_cat)
            data = url_prod.read()
            dfAll = json.loads(data.decode("utf_8"))
                
            for products in dfAll['products']:
                product_name = products.get('product_name_fr', "")
                product_name = product_name.replace("'"," ")
                if product_name is "":
                    break
                
                product_nutri = products.get('nutrition_grades_tags', "")
                product_nutri = str(product_nutri)
                product_nutri = product_nutri.replace("[", "")
                product_nutri = product_nutri.replace("'", "")
                product_nutri = product_nutri.replace("]", "")

                if 'stores' in products:
                    product_shop = str(products['stores'])
                    product_shop = product_shop.replace(" ", "-")
                    product_shop = product_shop.replace("'", "")
                    product_shop = product_shop.replace(",", " ")
                    if product_shop is "":
                        product_shop = ("Shop inconnu")
               
                else:
                    product_shop = ("Shop inconnu")
                product_url = products['url']

                rec = "INSERT IGNORE INTO `mydb`.`Products`(product_name, product_shop, product_nutri, product_url, Categories_category_id) VALUES ('{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE product_name = '{}'".format(product_name, product_shop, product_nutri, product_url, list_id_cat, product_name)
                print(rec)
                db.execute(rec)
                self.db_connect.commit()
        
        #db.execute("SELECT COUNT(*) FROM `mydb`.`Products`")
        #sql_return = db.fetchone()
        #print("\n***************************************************")
        #print("* La base de données est chargée avec %s produits *" % (sql_return))
        #print("***************************************************")

    def show_list_cat(self):
        
        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        print("\n Liste des catégories:\n")
        db.execute("SELECT category_id, category_name FROM `mydb`.`Categories`")
        for ligne in db.fetchall():
            list_id_cat = ligne[0]
            list_name_cat = ligne[1]
            print(list_id_cat,'-', list_name_cat)

    def show_list_prod(self):
        
        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        print("\n Liste des produits par catégories:\n")
        db.execute("SELECT product_name, Categories_category_id FROM `mydb`.`Products`")
        for ligne in db.fetchall():
            list_name_prod = ligne[0]
            list_id_cat = ligne[1]
            print(list_id_cat,"-",list_name_prod)

    def db_cleardata_cat(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Categories`")
        db.execute("ALTER TABLE `mydb`.`Categories` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n*********************************************************************")
        print("* !!!La table de données 'Categories' a été supprimée de la base!!! *")
        print("*********************************************************************")

    def db_cleardata_prod(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Products`")
        db.execute("ALTER TABLE `mydb`.`Products` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n*******************************************************************")
        print("* !!!La table de données 'Products' a été supprimée de la base!!! *")
        print("*******************************************************************")

    def db_cleardata_sub(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Subtitute`")
        db.execute("ALTER TABLE `mydb`.`Subtitute` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n*********************************************************************")
        print("* !!!La table de données 'Substitute' a été supprimée de la base!!! *")
        print("*********************************************************************")
