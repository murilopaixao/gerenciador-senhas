from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB('db.json')
q = Query()



def selectAll(): #select All
    dados = db.all()
    #for x in dados:
        #print(x)

    return dados

def selectOne(query): #select one
    pesquisa = db.search(q.id == query)
    return pesquisa

def alterar(id,titulo,username,password,url,tags,notes):
    db.update({"titulo": titulo, "username": username, "password": password, "url": url, "tags": tags, "notes": notes}, q.id == id)
    
def insertOne(titulo,username,password,url,tags,notes):
    dataHora = datetime.now().strftime('%Y%m%d-%H-%M-%S')
    myDoc = {
        "id": dataHora,
        "titulo": titulo,
        "username": username,
        "password": password,
        "url" : url,
        "tags": tags,
        "notes": notes
    }
    db.insert(myDoc)

def deleteOne(query):
    #db.remove(q.id == query)
    #print("Deletando..: " + str(query))
    db.remove(q.titulo == query)

def popular():
    dataHora = datetime.now().strftime('%Y%m%d-%H-%M-%S')
    myDoc = {
        "id": dataHora,
        "titulo": "Site5",
        "username": "st5",
        "password": "m5",
        "url" : "url5",
        "tags": "tags5",
        "notes": "notes5"
    }    
    db.insert(myDoc)
    print(myDoc)

def teste(titulo):
    dataHora = datetime.now().strftime('%Y%m%d-%H-%M-%S')
    db.update({"id": dataHora}, db.titulo == titulo)
