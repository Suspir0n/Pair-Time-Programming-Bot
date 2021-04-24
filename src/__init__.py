from flask import Flask, request
import datetime

def create_app(): 
    app = Flask(__name__)
    return app    

app_ext = create_app()

#1-Só recebe POST
    #1.1- Só responde POST com 
#2-Responde em json
@app_ext.route("/message", methods = ['POST'])
def message(): 
    print(request.json)
    # TODO - Buscar formas mais padronizadas de usar um json
    message = getClientMessageResponse(request.json["data"])
    return {
        "message": message,
        "date": str(datetime.datetime.now().timestamp())
    }

def getClientMessageResponse(clientData):
    #Pesquisa na lista de mensagens se tem resposta
    response = searchMessage(clientData["message"])
    if not response:
        return "Não entendi, pergunta novamente " + clientData["name"]
    return response + " " + clientData["name"]#olá

def searchMessage(clientMessage):
    # TODO - Resolver o UTF8
    test = [{"hello": "ola"}, {"Qual o seu nome?": "bot simplão"}]
    response = str()
    for value in test:
        if not clientMessage in value:
            continue
        response = value[clientMessage]
    return response