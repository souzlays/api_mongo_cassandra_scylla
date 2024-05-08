import unittest
import requests

class Cassandradb_teste(unittest.TestCase): 

    def test_get_all_pokemon(self):
        response = requests.get("http://localhost:5000/pokemons-cassandra")
        self.assertEqual(response.status_code, 200)
        pokemon_data = response.json()

        self.assertEqual(len(pokemon_data), 4)  

        expected_data = [
            {"name": "pikachu", "type": "elétrico"},
            {"name": "charizard", "type": "fogo"},
            {"name": "dug", "type": "terra"},
            {"name": "squirtle", "type": "água"}
            
            
        ]

        for i, pokemon in enumerate(pokemon_data):
            self.assertEqual(pokemon["name"], expected_data[i]["name"])
            self.assertEqual(pokemon["type"], expected_data[i]["type"])
            
            


if __name__ == '__main__':
    unittest.main()    
   