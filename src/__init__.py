from flask import Flask, request, json, Response, jsonify
from functools import wraps
from datetime import datetime


def required_params(required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _json = request.get_json()
            missing = [r for r in required.keys()
                       if r not in _json]
            if missing:
                response = {
                    "code": "BSERR-001",
                    "data": {
                        "error": "inconsistency on JSON structure",
                        "message": "Missing required JSON field",
                        "aux": missing,
                    },
                    "date": str(datetime.now().timestamp()), 
                }
                return jsonify(response), 400
            wrong_types = []    
            for item in required.keys():
                if isinstance(_json[item], dict):
                    for i in required[item].keys():
                        if type(_json[item][i]) != required[item][i]:
                            wrong_types.append(item)
                elif type(_json[item]) != required[item]:
                    wrong_types.append(item)
            if wrong_types:
                response = {
                    "code": "BSERR-002",
                    "data": {
                        "error": "inconsistency on JSON structure",
                        "message": "JSON field type is incorrect",
                        "aux": {k: str(v) for k, v in required.items()}
                    },
                    "date": str(datetime.now().timestamp()),
                   
                }
                return jsonify(response), 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# TODO - Criar os logs dos eventos de sucesso e falha
# TODO - Utilizar try catch(tratamento de erro) nas etapas de comunicação externa
def create_app(): 
    app = Flask(__name__)
    return app    

app_ext = create_app()

schema =  {
    "idUser": str,
    "data": {
      "name": str,
      "message": str,
    },
    "date": str
}


@app_ext.route("/message", methods=['POST'])
@required_params(schema)
def message():
    message = get_client_message_response(request.json["data"])
    response = handle_message_request(message)
    return response


def get_client_message_response(clientData):
    message_response = search_message(clientData["message"])
    if not message_response:
        return "Não entendi, pergunta novamente " + clientData["name"]
    return message_response + " " + str(clientData["name"])


def handle_message_request(message):
    response_data = {
        "message": message,
        "date": str(datetime.now().timestamp())
    }
    json_string = json.dumps(response_data,ensure_ascii = False)
    return Response(json_string,content_type="application/json; charset=utf-8")


def search_message(clientMessage):
    messages_responses = [{"hello": "ola"}, {"Qual o seu nome?": "bot simplão"}]
    response = str()
    for value in messages_responses:
        if not clientMessage in value:
            continue
        response = value[clientMessage]
    return response





     