
import unittest
import requests 

class Mongodb_test(unittest.TestCase):
    
    
    def test_get_capturando_primeiro_documento(self):
        response = requests.get("http://localhost:5000/pokemon/1")
        self.assertEqual(response.status_code, 200)
        documento_esperado = {'id': 1, 'name': 'pikachu', 'type': 'elétrico'}
        self.assertEqual(response.json(), documento_esperado)
            
    def test_put_modificando_nome_tipo(self):
        response = requests.put("http://localhost:5000/pokemon/{id}?pokemon_id=2", json={'id':2, 'name': 'pikachu', 'type': 'elétrico'})
        self.assertEqual(response.status_code, 200)
        documento_esperado = {
        "message": "Pokemon atualizado com sucesso",
        "data": {"id": 2},
        "pokemon_atualizado": {"id": 2, "name": "pikachu", "type": "elétrico"}}   
        documento_criado = response.json()
        self.assertEqual(documento_esperado, documento_criado)
        requests.put("http://localhost:5000/pokemon/{id}?pokemon_id=2", json={'id':2, 'name': 'charizard', 'type': 'fogo'})
    
            
    def test_post_criando_registro(self):
        response = requests.post("http://localhost:5000/mongodbpost/", json={'id':16, 'name': 'gengar', 'type': 'fantasma'})
        self.assertEqual(response.status_code, 200)
        documento_esperado = {"message": "Pokemon cadastrado com sucesso"}
        documento_criado = response.json()
        self.assertEqual(documento_esperado, documento_criado)
        
    def test_patch_modificando_tipo(self):     
        response = requests.patch("http://localhost:5000/pokemon/3", json={'type': 'elétrico'})
        self.assertEqual(response.status_code, 200)
        documento_esperado = {"id": 3, "name": "squirtle", "type": "elétrico"}
        documento_criado = response.json()
        self.assertEqual(documento_esperado, documento_criado)
        response = requests.patch("http://localhost:5000/pokemon/3", json={"type": "água"})
        self.assertEqual(response.status_code, 200)

        
    def test_delete_excluindo(self):     
        response = requests.delete("http://localhost:5000/pokemon/4?pokemon_id=4")
        self.assertEqual(response.status_code, 200)
        documento_esperado = {"message": "Pokemon deletado com sucesso"}  
        self.assertEqual(response.json(), documento_esperado)
        requests.post("http://localhost:5000/mongodbpost/", json={"id": 4, "name": "dug", "type": "terra"})    
        
if __name__ == '__main__':
    unittest.main()
