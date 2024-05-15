import unittest
import requests
import json


class Cassandradb_teste(unittest.TestCase): 
    
    def test_get_capturando_primeiro_documento(self):
        response = requests.get("http://localhost:5000/pokemons-cassandra")
        self.assertEqual(response.status_code, 200)
        documento_esperado = response.json()
        self.assertTrue(documento_esperado)

    def test_put_modificando_nome_tipo(self):
        response = requests.put("http://localhost:5000/pokemons-cassandra/2", json={'name': 'pikachu', 'type': 'elétrico'})
        self.assertEqual(response.status_code, 200)
        documento_esperado = {"name": "pikachu", "type": "elétrico"}
        documento_criado = response.json()
        self.assertEqual(documento_esperado, documento_criado)
        response = requests.put("http://localhost:5000/pokemons-cassandra/2", json={'name': 'charizard', 'type': 'fogo'})
   

if __name__ == '__main__':
    unittest.main()    
   