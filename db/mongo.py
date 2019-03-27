# -*- coding: UTF-8 -*-

from environment import db_uri
from pymongo import MongoClient


client = MongoClient(db_uri)
