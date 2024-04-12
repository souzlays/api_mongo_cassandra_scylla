from fastapi import FastAPI, HTTPException
import pymongo
from pymongo import MongoClient
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware 

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

@app.get("/", tags=["Saudação"])
async def read_root():
    return "Bem-vindo a pokedex NOSQL!"

@app.get('/pokemons-mongodb', tags=["Pokemons"])
async def get_stored_pokemon():
    db = get_db()
    _pokemons = db.pokemon_tb.find()
    pokemons = [{"id": pokemon["id"], "name": pokemon["name"], "type": pokemon["type"]} for pokemon in _pokemons]
    return JSONResponse(content={"pokemons": pokemons})

@app.get("/pokemon/{pokemon_id}")
async def get_pokemon_by_id(pokemon_id: int):
    db = get_db()
    collection = db["pokemon_tb"]
    pokemon = collection.find_one({"id":pokemon_id})
    if pokemon:
        # Remover o campo _id do MongoDB (ObjectId) para evitar erro de serialização JSON
        pokemon.pop('_id', None)
        return JSONResponse(pokemon)
    else:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")   
    
@app.put("/pokemon/{id}")
async def add_pokemon_by_id(pokemon_id: int, update_pokemon: dict):
    db = get_db()
    collection = db["pokemon_tb"]
    
    pokemon = collection.find_one({"id": pokemon_id})
    
    if pokemon is None:
       raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    else:
        print("Pokemon encontrado: ", pokemon)
   
    resultado = collection.update_one({"id": pokemon_id}, {"$set": update_pokemon})     
    
    if resultado.modified_count == 1:
        return {"message:" "Pokemon atualizado com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Falha ao atualizar o Pokémon") 

@app.post("/pokemon/")
async def create_pokemon(pokemon_id: int, name:str, type:str):
    db = get_db()
    collection = db["pokemon_tb"]     
    result = collection.insert_one({"id": pokemon_id, "name": name, "type": type})
    if result.inserted_id:
        return {"message": "Pokémon criado com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Falha ao criar o Pokémon")
    
    
        
        
        
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


