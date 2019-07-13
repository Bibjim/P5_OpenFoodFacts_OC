# ! /usr/bin/env python3
# coding: utf-8

'''
    create_database.py
    Author: Jimi Bourgeois
    Version: 2019-04-19
    Describe: Requets of create database structure
'''

import pymysql.cursors

from requets import *

class create_structure_db():
      
   def create_db(self):
      
      self.db_connect = pymysql.connect("localhost","root","","")
      db = self.db_connect.cursor()

      db.execute(db_test)
      self.db_connect.commit()

   def create_table_cat(self):

      self.db_connect = pymysql.connect("localhost","root","","test")
      db = self.db_connect.cursor()

      db.execute(table_categories)
      self.db_connect.commit()

