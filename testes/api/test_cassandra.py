import unittest
import requests
import json


class Cassandradb_teste(unittest.TestCase): 

    def test_get_all_pokemon(self):
        with open("pokemons_cassandra.json", "r", encoding="utf-8") as file:
            expected_data = json.load(file)

        response = requests.get("http://localhost:5000/pokemons-cassandra")
        self.assertEqual(response.status_code, 200)
        pokemon_data = response.json()

        self.assertEqual(len(pokemon_data), len(expected_data))

        for i, pokemon in enumerate(pokemon_data):
            self.assertEqual(pokemon["name"], expected_data[i]["name"])
            self.assertEqual(pokemon["type"], expected_data[i]["type"])
            

if __name__ == '__main__':
    unittest.main()    
   