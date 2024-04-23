db = db.getSiblingDB("pokedex_db");
db.pokemon_tb.drop();

db.pokemon_tb.insertMany([
    {
        "id": 1,
        "name": "pikachu",
        "type": "elétrico"
    },
    {
        "id": 2,
        "name": "charizard",
        "type": "fogo"
    },
    {
        "id": 3,
        "name": "squirtle",
        "type": "água"
    },
    {
        "id": 4,
        "name": "dug",
        "type": "terra"
    },
]);