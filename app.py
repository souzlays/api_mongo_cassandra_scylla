from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

app.debug = True

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["pokedex_db"]
    return db

@app.route('/')
def ping_server():
    return "Bem-vindo a pokedex NOSQL!"

@app.route('/pokemons-mongodb')
def get_stored_pokemon():
    db = get_db()
    _pokemons = db.pokemon_tb.find()
    pokemons = [{"id": pokemon["id"], "name": pokemon["name"], "type": pokemon["type"]} for pokemon in _pokemons]
    return jsonify({"pokemons": pokemons})

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)