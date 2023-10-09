import flask
from flask.json import jsonify
import uuid
from traffic import Street
import numpy as np

games = {}

app = flask.Flask(__name__)

def convert_to_json_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.int32):
        return int(obj)  # Convert int32 to regular Python int
    return obj

@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    model = games[id] = Street()

    lista = []
    for agent in model.schedule.agents:
        agente_info = {
            "id": agent.unique_id,
            "x": int(agent.pos[0]),
            "z": int(agent.pos[1])
        }

        if hasattr(agent, 'speed'):
            agente_info["dx"] = int(agent.speed[0])  # Convert int32 to int
            agente_info["dz"] = int(agent.speed[1])  # Convert int32 to int
        
        lista.append(agente_info)
    
    return jsonify(lista), 201, {'Location': f"/games/{id}"}

@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    lista = []
    for agent in model.schedule.agents:
        agente_info = {
            "id": agent.unique_id,
            "x": int(agent.pos[0]),
            "z": int(agent.pos[1])
        }

        if hasattr(agent, 'speed'):
            agente_info["dx"] = int(agent.speed[0])  # Convert int32 to int
            agente_info["dz"] = int(agent.speed[1])  # Convert int32 to int
        lista.append(agente_info)
        
    return jsonify(lista)

app.run(host="0.0.0.0")
