import unittest
import requests
import json


class Cassandradb_teste(unittest.TestCase): 
    
    def test_get_capturando_primeiro_documento(self):
        response = requests.get("http://localhost:5000/pokemons-cassandra")
        self.assertEqual(response.status_code, 200)
        documento_esperado = [
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
                "id": 4,
                "name": "dug",
                "type": "terra"
            },
            {
                "id": 3,
                "name": "squirtle",
                "type": "água"
            }
        ]
        self.assertEqual(response.json(), documento_esperado)

    def test_put_modificando_nome_tipo(self):
        response = requests.put("http://localhost:5000/pokemon/{id}?pokemon_id=2", json={'id':2, 'name': 'pikachu', 'type': 'elétrico'})
        self.assertEqual(response.status_code, 200)
        documento_esperado = {
            "message": "Pokemon atualizado com sucesso",
            "data": {"id": 2},
            "pokemon_atualizado": {"id": 2, "name": "pikachu", "type": "elétrico"}
        }   
        documento_criado = response.json()
        self.assertEqual(documento_esperado, documento_criado)
        requests.put("http://localhost:5000/pokemon/{id}?pokemon_id=2", json={'id':2, 'name': 'charizard', 'type': 'fogo'})

   

if __name__ == '__main__':
    unittest.main()    
   