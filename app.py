from fastapi import FastAPI
import pymongo
from pymongo import MongoClient
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

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


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


if __name__=='__main__':
    uvicorn.run(app, host="10.38.24.35", port=5000, reload=True)