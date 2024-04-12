
import unittest
import requests 

class Mongodb_test(unittest.TestCase):
    
    
    def test_get_capturando_primeiro_documento(self):
        response = requests.get("http://localhost:5000/pokemon/1")
        self.assertEqual(response.status_code, 200)
        documento_esperado = {'id': 1, 'name': 'pikachu', 'type': 'elétrico'}
        self.assertEqual(response.json(), documento_esperado)
            
    def test_put_modificando_nome_tipo(self):
        response = requests.put("http://localhost:5000/pokemon/2?pokemon_id=2", json={'id':7, 'name': 'pikachu', 'type': 'elétrico'})
        self.assertEqual(response.status_code, 200)
        documento_atualizado = response.json()
        self.assertEqual(documento_atualizado, ["message:Pokemon atualizado com sucesso"])
        
     
    def test_post_criando_registro(self):
        response = requests.post("http://localhost:5000/pokemon/", json={'id':5, 'name': 'gengar', 'type': 'fantasma'})
        self.assertEqual(response.status_code, 201)
        documento_criado = response.json()
        self.assertEqual(documento_criado, {"message:Pokemon atualizado com sucesso"})    
        
    
    
    '''def test_patch_modificando_tipo(self):
        
        self.assertEqual(1,1)
        
    def test_delete_apagando_documento_3(self):
        
        self.assertEqual(1,1)'''              

    
if __name__ == '__main__':
    unittest.main()
