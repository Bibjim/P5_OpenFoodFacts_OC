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
        print("\n*********************************************************")
        print("* The database is loaded with %s categories of products *" % (sql_return))
        print("*********************************************************")

    def show_list_cat(self):
        
        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        print("\n List of categories:\n")
        db.execute("SELECT category_id, category_name FROM `mydb`.`Categories`")
        for ligne in db.fetchall():
            print(ligne)

    def db_cleardata_cat(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Categories`")
        db.execute("ALTER TABLE `mydb`.`Categories` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n***********************************************************")
        print("* !!!The data in the database 'Categories' are deleted!!! *")
        print("***********************************************************")

    def db_cleardata_prod(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Products`")
        db.execute("ALTER TABLE `mydb`.`Products` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n*********************************************************")
        print("* !!!The data in the database 'Products' are deleted!!! *")
        print("*********************************************************")

    def db_cleardata_sub(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Subtitute`")
        db.execute("ALTER TABLE `mydb`.`Subtitute` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n***********************************************************")
        print("* !!!The data in the database 'Substitute' are deleted!!! *")
        print("***********************************************************")
