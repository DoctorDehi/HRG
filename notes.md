TODO:
- přidat mongo pro uživatele
- implementovat login system https://flask-login.readthedocs.io/en/latest/

Vytahování holubů uživatele:
- z mongo db vytáhnout ID uživatele
- z neo4j vytáhnout všechny holuby co mají odpovídající ID uživatele


Vizualizace rodokmenu:
- https://github.com/neo4j-contrib/neovis.js



### Hladání předků:
    MATCH path=((p:Pigeon)-[r*0..4]->(:Pigeon {id : '1-TE254-21'})) return path
    
    MATCH path=((:Pigeon {id : '1-TE254-21'})<-[r*0..4]-(p:Pigeon)) return path

    MATCH path=((:Pigeon {id : '1-TE254-21'})<-[r*0..4]-(p:Pigeon)) returequirementsrn p, r


pip install flask, neo4j,flask-mongoengine, redis, PyPDF2, reportlab, requests