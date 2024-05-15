from fastapi import FastAPI, HTTPException
import pymongo
from pymongo import MongoClient
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware 
from cassandra.cluster import Cluster
from pydantic import BaseModel
import json
import time
from cassandra.cluster import NoHostAvailable

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    client = MongoClient(host='test_mongodb', 
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin") 
    db = client["pokedex_db"] 
    return db



def wait_for_cassandra():
    while True:
        try:
            cluster = Cluster(contact_points=['cassandra'], port=9042)
            session = cluster.connect()
            print("Cassandra is available.")
            return session
        except NoHostAvailable:
            print("Cassandra is not available yet. Retrying in 5 seconds...")
            time.sleep(5)

def get_session():
    session = wait_for_cassandra()
    
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS pokedex_db 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """)
    session.set_keyspace("pokedex_db")
    
    session.execute("USE pokedex_db")  
    session.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_tb ( 
            id int PRIMARY KEY,
            name text,
            type text     
        )
    """)
    
    existing_records = session.execute("SELECT COUNT(*) FROM pokemon_tb").one()[0]
    
    if existing_records == 0:
        with open('pokemons_cassandra.json') as f:
            data = json.load(f)
            # Ordenar os registros pelo campo 'ordem'for pokemon in data:
            sorted_data = sorted(data, key=lambda x: x['id'])
            for pokemon in sorted_data:
                name = pokemon['name']
                type = pokemon['type']
                id = pokemon['id']
                session.execute(f"""
                INSERT INTO pokemon_tb (name, type, id)
                VALUES (%s, %s, %s)
                """, (name, type, id))
          
    return session

session = get_session() 

class Pokemon(BaseModel):
    id: int
    name: str
    type: str 
         
class Pokemon_patch(BaseModel):
    type: str    
    
class Pokemon_cassandra(BaseModel):
    name: str
    type: str     
        
@app.get('/pokemons-mongodb', tags=["Pokemons Mongo"])
def get_stored_pokemon():
    db = get_db()
    _pokemons = db.pokemon_tb.find()
    pokemons = [{"id": pokemon["id"], "name": pokemon["name"], "type": pokemon["type"]} for pokemon in _pokemons]
    return JSONResponse(content={"pokemons": pokemons})

@app.get("/pokemon/{pokemon_id}", tags=["Pokemons Mongo"])
def get_pokemon_by_id(pokemon_id: int):
    db = get_db()
    collection = db["pokemon_tb"]
    pokemon = collection.find_one({"id":pokemon_id})
    if pokemon:
        pokemon.pop('_id', None)
        return JSONResponse(pokemon)
    else:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")   
    
@app.put("/pokemon/{id}", tags=["Pokemons Mongo"])
def add_pokemon_by_id(pokemon_id: int, update_pokemon: Pokemon):
    db = get_db()
    collection = db["pokemon_tb"]
    pokemon = collection.find_one({"id": pokemon_id})
    if pokemon is None:
       raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    else:
        print("Pokemon encontrado: ", pokemon)
        
    resultado = collection.update_one({"id": pokemon_id}, {"$set": update_pokemon.dict()}) 
        
    if resultado.modified_count == 1:
        return {"message": "Pokemon atualizado com sucesso", "data": {"id": pokemon_id}, "pokemon_atualizado": update_pokemon.dict()}
    else:
        raise HTTPException(status_code=500, detail="Falha ao atualizar o Pokémon") 

@app.post("/mongodbpost/", tags=["Pokemons Mongo"])
def cadastrar_pokemon(pokemon: Pokemon):
    db = get_db()
    collection = db["pokemon_tb"]
    dicionario_novo_pokemon = {"id": pokemon.id, "name": pokemon.name, "type": pokemon.type}
    result = collection.insert_one(dicionario_novo_pokemon)
    if result.inserted_id:
        return {"message": "Pokemon cadastrado com sucesso"}
    else:
        return {"error": "Erro ao cadastrar o Pokemon"}

       
@app.patch("/pokemon/{pokemon_id}", tags=["Pokemons Mongo"])
def update_pokemon(pokemon_id: int, pokemon: Pokemon_patch):
    db = get_db()
    collection = db["pokemon_tb"]
    
    existing_pokemon = collection.find_one({"id": pokemon_id})
    if existing_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    
    resultado = collection.update_one({"id": pokemon_id}, {"$set": {"type": pokemon.type}})
    
    if resultado.modified_count == 1:
        updated_pokemon = collection.find_one({"id": pokemon_id})
        updated_pokemon.pop('_id', None)
        return updated_pokemon
    else:
        raise HTTPException(status_code=500, detail="Falha ao atualizar o Pokémon")

  
@app.delete("/pokemon/{pokemon_id}", tags=["Pokemons Mongo"]) 
def delete_pokemon(pokemon_id: int):    
    db = get_db()
    collection = db["pokemon_tb"]
    pokemon_existente = collection.find_one({"id": pokemon_id})
    if pokemon_existente:
        result = collection.delete_one({"id": pokemon_id})
        if result.deleted_count > 0:
            return {"message": "Pokemon deletado com sucesso"}
        else:
            return {"error": "Erro ao deletar o Pokemon"}
    else:
        return {"error": "Pokemon não encontrado"}
    

@app.get('/pokemons-cassandra', tags=["Pokemons Cassandra"], response_model=list[Pokemon])
def get_stored_pokemon_from_cassandra():
    try:
        session = get_session()
        session.set_keyspace("pokedex_db")  
        query = "SELECT * FROM pokemon_tb"
        rows = session.execute(query) 
        
        pokemons_data = []
        for row in rows:
            pokemon_data = Pokemon(id=row.id, name=row.name, type=row.type) 
            pokemons_data.append(pokemon_data)
        return pokemons_data
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"Erro ao buscar os pokemons do Cassandra: {str(e)}")
    

@app.put("/pokemons-cassandra/{id}", tags=["Pokemons Cassandra"])
def put_pokemon(id: int, pokemon_update: Pokemon_cassandra):
    session = wait_for_cassandra()
    session.set_keyspace("pokedex_db")
    
    query = "SELECT name, type FROM pokemon_tb WHERE id = %s"
    result = session.execute(query, (id,))
    
    selected_pokemon = None
    for row in result:
        selected_pokemon = Pokemon_cassandra(name=row.name, type=row.type)
    
    if selected_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado.")
    
    if pokemon_update.name:
        selected_pokemon.name = pokemon_update.name
    if pokemon_update.type:
        selected_pokemon.type = pokemon_update.type
    
    query = "UPDATE pokemon_tb SET name = %s, type = %s WHERE id = %s" 
    session.execute(query, (selected_pokemon.name, selected_pokemon.type, id)) 
    
    return selected_pokemon
         
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Pokemon",
        version="1.0.0",
        description="Pokemons",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

 


    




