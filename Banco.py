from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB('db.json', indent=4)
db_dados = db.table("dados")
q = Query()

db2_table2 = db.table("tree")

db_config = db.table("config")
#db_config.truncate()
""" db2_table2.truncate()


myDoc = {"Cod": "1","Departamento": "Gerente Financeiro","cod_Pai": "Raiz"}
db2_table2.insert(myDoc)
myDoc = {"Cod": "2","Departamento": "Gerente Vendas","cod_Pai": "Raiz"}
db2_table2.insert(myDoc)
myDoc = {"Cod": "3","Departamento": "Gerente RH","cod_Pai": "Raiz"}
db2_table2.insert(myDoc)

myDoc = {"Cod": "4","Departamento": "Peao 1","cod_Pai": "1"}
db2_table2.insert(myDoc)
myDoc = {"Cod": "5","Departamento": "Peao 2","cod_Pai": "1"}
db2_table2.insert(myDoc)
myDoc = {"Cod": "6","Departamento": "Peao 3","cod_Pai": "1"}
db2_table2.insert(myDoc)
myDoc = {"Cod": "7","Departamento": "Peao 4","cod_Pai": "2"}
db2_table2.insert(myDoc)
myDoc = {"Cod": "8","Departamento": "Peao 5","cod_Pai": "2"}
db2_table2.insert(myDoc)
myDoc = {"Cod": "9","Departamento": "Peao 6","cod_Pai": "3"}
db2_table2.insert(myDoc) """

def configInicio():
    #password = db_config.search(q.senhaInicial)
    password = db_config.get(doc_id=1)
    if password is None:
        password = []    
    return password

def configSenhaInicial(password):
    db_config.insert({"senhaInicial": password})
    #db_config.update({"senhaInicial": password})
    
    

def selectAll(): #select All
    dados = db_dados.all()
    #for x in dados:
        #print(x)
    return dados

def selectAllGrupo(): #select All
    dados2 = db2_table2.all()
    #for x in dados2:
        #print(x)
    return dados2

def selectOne(query): #select one
    pesquisa = db_dados.search(q.id == query)
    return pesquisa

def alterar(id,titulo,username,password,url,tags,notes):
    db_dados.update({"titulo": titulo, "username": username, "password": password, "url": url, "tags": tags, "notes": notes}, q.id == id)
    
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
    db_dados.insert(myDoc)

def deleteOne(query):
    #db_dados.remove(q.id == query)
    #print("Deletando..: " + str(query))
    db_dados.remove(q.titulo == query)

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
    db_dados.insert(myDoc)
    print(myDoc)

def teste(titulo):
    dataHora = datetime.now().strftime('%Y%m%d-%H-%M-%S')
    db_dados.update({"id": dataHora}, db.titulo == titulo)
