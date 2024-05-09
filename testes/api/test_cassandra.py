import unittest
import requests
import json


class Cassandradb_teste(unittest.TestCase): 
    
    def test_get_capturando_primeiro_documento(self):
        response = requests.get("http://localhost:5000/pokemons-cassandra")
        self.assertEqual(response.status_code, 200)
        documento_esperado = [
            {
                "name": "pikachu",
                "type": "elétrico"
            },
            {
                "name": "charizard",
                "type": "fogo"
            },
            {
                "name": "dug",
                "type": "terra"
            },
            {
                "name": "squirtle",
                "type": "água"
            }
        ]
        self.assertEqual(response.json(), documento_esperado)
   

if __name__ == '__main__':
    unittest.main()    
   