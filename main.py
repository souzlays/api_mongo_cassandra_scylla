from fastapi import FastAPI, HTTPException
import pymongo
from pymongo import MongoClient
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel

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

class Pokemon(BaseModel):
    id: int
    name: str
    type: str
    
class Pokemon_patch(BaseModel):
    name: str
    type: str    

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
        return {"message": "Pokemon atualizado com sucesso", "data": {"id": pokemon_id}, "pokemon_atualizado": update_pokemon}
    else:
        raise HTTPException(status_code=500, detail="Falha ao atualizar o Pokémon") 

@app.post("/mongodbpost/")
async def cadastrar_pokemon(pokemon: Pokemon):
    db = get_db()
    collection = db["pokemon_tb"]
    novo_pokemon = {"id": pokemon.id, "name": pokemon.name, "type": pokemon.type}
    result = collection.insert_one(novo_pokemon)
    if result.inserted_id:
        return {"message": "Pokemon cadastrado com sucesso"}
    else:
        return {"error": "Erro ao cadastrar o Pokemon"}
    
       
@app.patch("/pokemon/{pokemon_id}")
async def update_pokemon(pokemon_id: int, pokemon: Pokemon_patch):
    db = get_db()
    collection = db["pokemon_tb"]
    existing_pokemon = collection.find_one({"id": pokemon_id})
    if existing_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    
    pokemon_data = pokemon.dict(exclude_unset=True)
    if not pokemon_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    resultado = collection.update_one({"id": pokemon_id}, {"$set": pokemon_data})
    
    if resultado.modified_count == 1:
        updated_pokemon = collection.find_one({"id": pokemon_id})
        updated_pokemon.pop('_id', None)
        return {
            "message": "Pokemon atualizado com sucesso",
            "data": {"id": pokemon_id},
            "pokemon_atualizado": updated_pokemon
        } 
    else:
        raise HTTPException(status_code=500, detail="Falha ao atualizar o Pokémon")
    
@app.delete("/pokemon/{pokemon_id}")
async def delete_pokemon(pokemon_id: int):    
    db = get_db()
    collection = db["pokemon_tb"]
    pokemon_existente = collection.find_one({"id": pokemon_id})
    if pokemon_existente:
        # Remove o Pokémon
        result = collection.delete_one({"id": pokemon_id})
        if result.deleted_count > 0:
            return {"message": "Pokemon deletado com sucesso"}
        else:
            return {"error": "Erro ao deletar o Pokemon"}
    else:
        return {"error": "Pokemon não encontrado"}
                
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


