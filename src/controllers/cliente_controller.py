import requests

BASE_URL = "http://localhost:8000"

def get_clients():
    print("No api_utils, metodo get_clients")
    try:
        request = requests.get(f"{BASE_URL}/clientes")
        if request.status_code == 200:
            print("Clientes buscados com sucesso!")
            return request.json()
        else:
            return []
    except Exception as e:
        print("Erro na requisição de clientes:", e)
        return []


def search_clients(query: str):
    print("No api_utils, metodo search_clients, variaveis: ", query)
    try:
        params = {"q": query} if query else {}
        response = requests.get(f"{BASE_URL}/clientes/search", params=params)
        response.raise_for_status()
        clients = response.json()
        print(f"Clientes buscados com sucesso via API! Total: {len(clients)}")
        return clients
    except requests.exceptions.RequestException as e:
        print("Erro ao buscar clientes via API:", e)
        return []


def post_client(client):
    print("No api_utils, metodo post_client, variaveis: ", client)
    try:
        novo_cliente = {
            "nome": client.get("nome", ""),
            "cpf": client.get("cpf", ""),
            "telefone": client.get("telefone", ""),
            "pontos": client.get("pontos", 0)
        }

        cliente = requests.post(f"{BASE_URL}/clientes", json=novo_cliente)
        if cliente.status_code == 201:
            print("Cliente cadastrado com sucesso via API!")
            return cliente.json()
        else:
            return None
    except Exception as e:
        print("Erro na requisição de cadastro de cliente via API:", e)
        return None


def put_client(client):
    print("No api_utils, metodo put_client, variaveis: ", client)
    try:
        id = client.get("id")
        print("ID do cliente a ser atualizado:", id)
        if not id:
            print("ID é obrigatório para atualizar.")
            return None
        
        update_data = {k: v for k, v in client.items() if k != 'id'}
        
        result = requests.put(f"{BASE_URL}/clientes/{id}", json=update_data)
        print("Resultado da atualização via API:", result.status_code)
        if result:
            print("Cliente atualizado com sucesso!")
        return client
    except Exception as e:
        print("Erro ao atualizar cliente:", e)
        return None


def delete_client(id):
    print("No api_utils, metodo delete_client, variaveis: ", id)
    try:
        result = requests.delete(f"{BASE_URL}/clientes/{id}")
        print("Resultado da deleção via API:", result.status_code)
        if result.status_code == 204:
            print("Cliente deletado com sucesso via API!")
            return True
        else:
            return False
    except Exception as e:
        print("Erro ao deletar cliente:", e)
        return 0
