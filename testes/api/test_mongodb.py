
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
        documento_esperado = {"message": "Pokemon cadastrado com sucesso", "data": {'id':16, 'name': 'gengar', 'type': 'fantasma'}}
        documento_criado = response.json()
        self.assertEqual(documento_esperado, documento_criado)
        
    def test_patch_modificando_tipo(self):     
        response = requests.patch("http://localhost:5000/pokemon/{id}?pokemon_id=3", json={'name': 'blablabla'})
        self.assertEqual(response.status_code, 200)
        documento_esperado = {
        "message": "Pokemon atualizado com sucesso",
        "data": {"id": 3},
        "pokemon_atualizado": {"id": 3, "name": "blablabla", "type": "água"}}   
        documento_criado = response.json()
        self.assertEqual(documento_esperado, documento_criado)
        request.patch("http://localhost:5000/pokemon/{id}?pokemon_id=3", json={'name': 'squirtle'})
        
        
        
        
        
    # def test_delete_apagando_documento_3(self):
        
    #     self.assertEqual(1,1)

    
if __name__ == '__main__':
    unittest.main()
