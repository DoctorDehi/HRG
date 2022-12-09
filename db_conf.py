from neo4j import GraphDatabase, basic_auth
from flask_mongoengine import MongoEngine
from mongoengine import StringField, SequenceField


driver = GraphDatabase.driver("bolt://127.0.0.1:7689", auth=basic_auth("neo4j", "knock-cape-reserve"))
mongo_engine = MongoEngine()


class User(mongo_engine.Document):
    id = SequenceField(primary_key=True)
    email = StringField(required=True)
    password = StringField(required=True)
