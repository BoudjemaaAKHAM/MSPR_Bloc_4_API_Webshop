import requests
import json
import webbrowser
import time
# import http.client

# import httpx

#----------------origine-------------------------------------------
# #version get
# def create(level, message, execution_id):
#     #url = "http://127.0.0.1:5000/create/milli/m@m.com/pwd" 
#     url = "http://127.0.0.1:5000/create/{0}/{1}/{2}".format(level, message, execution_id)
#     reponse = requests.get(url)
#     print(reponse)

# create("70info","failled",3)

#-----------------origine-------------------------------------------
# #version post
# def create(level, message, execution_id):#
#     data = {'level' : level, 'message' : message, 'execution_id' : execution_id} #, 'message' : message, 'execution_id' : execution_id
#     #url = "http://127.0.0.1:5000/create/milli/m@m.com/pwd" 
#     url = "http://127.0.0.1:5000/create"
#     reponse = requests.post(url, data)
#     print(reponse)

# create("70info","failled",3) #

#-----------------version 1 get-----------------------------------------
# # #version get
# def read(): 
#     url = "http://127.0.0.1:8082/read/"
#     reponse = requests.get(url)
#     print(reponse)
#     print(reponse.text)
#     #pour ouvrir l'url dans une page web
#     # webbrowser.open(url)

# read()

#-----------------version 1 post---------------------------------------------------------
# #version post qui fonctionne (qui n'est pas un post mais un get )

# def create(name, fullname, addresses):
#     data = {'name' : name, 'fullname' : fullname, 'addresses' : addresses}
#     url = "http://127.0.0.1:8082/createUserAcount/{0}/{1}/{2}".format(name, fullname, addresses)
#     reponse = requests.post(url, timeout=5) # timeout le temps que l'on accorde a la reponse 
#     #doit etre defini en python ici timeout est determiner a 5 seconde
#     print(reponse)
#     # print(reponse.content) # "content"pour avoir la reponses envoyer par le return de l'API
    
#     # if reponse.status_code == 200:
#     #     print('Success!') # retourne un succes si le status est 200

#     # print(reponse.text) # transphorme en texte

#     # print(reponse.headers) # affiche le contenu du retour https header

#     # print(reponse.json()) # j'ai ma reponse en json
#     dico = reponse.json() # je le determine en dictionnaire
#     print(dico['name']) # je peut recuperer les éléments de mon dictionnaire
#     print(dico['addresses'])
#     print(dico['fullname'])

# create("fillolli", "dolle", "fil@dolle.com")

#-----------------------------------------------------------
#version post qui fonctionne pas

# def create(name, fullname, addresses): #name, fullname, addresses
#     payload = {'name' : name, 'fullname' : fullname, 'addresses' : addresses}
#     url = "http://127.0.0.1:8082/createUserAcount/"
#     reponse = requests.post(url, data=payload, timeout=5) # timeout le temps que l'on accorde a la reponse # data=json.dumps(data)
#     print(reponse)
#     print(reponse.text)
#     print(payload)

# create("fillo", "dole", "fil@dole.com")
# # create()


#-------------------------------------------------------------------
# conn = http.client.HTTPSConnection('http://127.0.0.1:8082')

# headers = {'Content-type': 'application/json'}

# foo = {'name' : 'name', 'fullname' : 'fullname', 'addresses' : 'addresses'}
# json_data = json.dumps(foo)

# conn.request('POST', '/createUserAcount/', json_data, headers)

# response = conn.getresponse()
# print(response.read().decode())

#-----------------HTTPX----------------------
# def create(name, fullname, addresses):
#     data = {'name' : name, 'fullname' : fullname, 'addresses' : addresses}
#     r = httpx.post('http://127.0.0.1:8082/createUserAcount/{0}/{1}/{2}'.format(name, fullname, addresses))
#     print(r)
#     print(r.text)

# create("fillillo", "dole", "filo@dole.com")

#-----------------------------------------------------------
# version post qui fonctionne !!!

# def create(name, fullname, addresses): #name, fullname, addresses
#     data = {'name' : name, 'fullname' : fullname, 'addresses' : addresses}
#     url = "http://127.0.0.1:8082/createUserAcount/"
#     # reponse = requests.post(url, data=payload, timeout=5)
#     # reponse = requests.post(url, data={'input': data}, timeout=5) # timeout le temps que l'on accorde a la reponse # data=json.dumps(data)
#     # reponse = requests.post(url, json=data, timeout=5)
#     # reponse = requests.post(url, data=json.dumps(data), timeout=5)
#     reponse = requests.post(url, params=data, timeout=5)
#     print(reponse)
#     print(reponse.text)
#     print(reponse.content)
#     print(data)
#     print(reponse.json()) # j'ai ma reponse en json
#     dico = reponse.json() # je le determine en dictionnaire
#     print(dico['name']) # je peut recuperer les éléments de mon dictionnaire
#     print(dico['addresses'])
#     print(dico['fullname'])

# create("fillola", "dolela", "fil@dolllle.com")
# # create()
# #-------------------------------------------------------------
# # ce client doit etre chez rim-nat # il envoie des données dans la bdd request
# def createFromRimnat(userid, service, input, statuts, step): #name, fullname, addresses
#     data = {'userid' : userid, 'service' : service, 'input' : input, 'statuts' : statuts, 'step' : step}
#     url = "http://127.0.0.1:8082/api/v1.0/queue/"
#     reponse = requests.post(url, params=data) # , timeout=5
#     print(reponse)
#     dico = reponse.json() # je le determine en dictionnaire 
#     # print(dico['statuts'])
#     # print("recup de l'id",dico['id'])
#     # print("recup de l'userid",dico['userid'])
#     print(dico)
    

# createFromRimnat(228, "mnt-diff", "adresse/a/adresse/b", "succes", 0)

# time.sleep(5)

#-------------------------------------------------------------
# # ce client doit etre chez mnt-diff
# def read(): #service
# #     data = {'service' : 'mnt-diff'} # service #parce que le micro service est mnt-diff
#     url = "http://127.0.0.1:8082/api/v1.0/queue/mnt-diff"     #{0}".format(service)
#     reponse = requests.get(url) #, params=data, timeout=5
#     print(reponse)
#     # print(reponse.content)
#     # liste = []
#     # liste.append(reponse.content)
#     # print(liste)

#     # recup = reponse.text
#     # print(recup) 


#     dico = reponse.json() # je le determine en dictionnaire
#     print(dico)
#     dico1 = dico[1] # pour le sortir du tableau
#     print(dico1)
#     # # print("l'etape est a :",dico[0]) # fonctionne
#     # print("l'etape est a :",dico1["service"])
#     # print(dico1['step'])
#     # print("recup de l'id",dico1['id'])
#     # print("recup de l'userid",dico1['userid'])
#     # print("recup de la date",dico1['date'])

#     # for elem in dico1  
    
    
#     # liste1 = []
#     # liste1.append(dico)
#     # print(liste1)

# read() #'mnt-diff'
#-------------------------------------------------------------

# # ce client doit etre chez mnt-diff # il envoie des données dans la bdd output
# def createFromMntdiff(producer, types, path, size): #name, fullname, addresses
#     data = {'producer' : producer, 'types' : types, 'path' : path, 'size' : size}
#     url = "http://127.0.0.1:8082/api/v1.0/queue/mnt-diff"
#     reponse = requests.post(url, params=data) # , timeout=5
#     print(reponse)
#     dico = reponse.json() # je le determine en dictionnaire 
#     print(reponse.content)
#     # print(dico['id'])
#     # print(dico['producer'])
#     # print(dico['types'])
#     # print(dico['path'])
#     # print(dico['size'])
    

# createFromMntdiff("mnt-diff", "txt", "adresse/a/adresse/C", 17)


# #-------------------------test pour table association------------------------------------
# # ce client doit etre chez mnt-diff # il envoie des données dans la bdd output
# def createFromMntdiff(producer, types, path, size, requestId): #name, fullname, addresses
#     data = {'producer' : producer, 'types' : types, 'path' : path, 'size' : size, 'requestId' : requestId}
#     url = "http://127.0.0.1:8082/api/v1.0/queue/mnt-diff"
#     reponse = requests.post(url, params=data) # , timeout=5 , verify=False
#     print(reponse)
#     # print(reponse.text)
#     # # dico = reponse.json() # je le determine en dictionnaire 
#     print(reponse.content)
#     # data = json.loads(reponse.text)
#     # print(data)

#     # print(dico['id'])
#     # print(dico['producer'])
#     # print(dico['types'])
#     # print(dico['path'])
#     # print(dico['size'])
    

# createFromMntdiff("mnt-diff", "txt", "adresse/a/adresse/C", 15, 226)

#-----------------version 1 get-----------------------------------------
# #version get
def read(): 
    # url = "http://127.0.0.1:9001/read"
    url = "http://127.0.0.1:9001/customers/7" #customers/7
    # url = "http://192.168.65.4:9001/read"
    reponse = requests.get(url)
    print(reponse)
    print(reponse.text)
    text = reponse.text
    data = json.loads(text)
    # customers = data[1]
    # print(customers['name'])
    # id = customers['id']
    # print(id)

    print(data['name'])
    id = data['id']
    print(id)


read()

# -------------------------
# test request base en get:
# -------------------------

# url = requests.get("https://jsonplaceholder.typicode.com/posts")
# text = url.text
# print(type(text))

# data = json.loads(text)
# print(type(data))

# user = data[1] # position sur les donnée du json
# print(user['userId'])

# id = user['id']
# print(id)

# title = user['title']
# print(title)

# body = user['body']
# print(body)

