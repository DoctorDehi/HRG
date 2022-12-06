from neo4j import GraphDatabase, basic_auth


driver = GraphDatabase.driver("bolt://127.0.0.1:7689", auth=basic_auth("neo4j", "knock-cape-reserve"))
