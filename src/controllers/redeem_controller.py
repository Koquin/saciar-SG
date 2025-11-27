import requests

BASE_URL = "http://localhost:8000"

def get_redeems():
    print("In redeem_controller, metodo get_redeems")
    try:
        url = f"{BASE_URL}/redeems"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar resgates via API: {response.status_code}")
            return []
    except Exception as e:
        print("Erro ao buscar resgates:", e)
        return []

def search_redeems(query):
    print("In redeem_controller, metodo search_redeems, variaveis: ", query)
    if not query:
        return get_redeems()
        
    try:
        params = {"q": query} if query else {}
        url = f"{BASE_URL}/redeems/search"
        print("URL:", url, "Params:", params)
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Erro ao buscar resgates:", e)
        return []

def post_redeem(redeem):
    print("In redeem_controller, metodo post_redeem, variaveis: ", redeem)
    telefone = redeem.get("telefone", "").strip()
    pontos = redeem.get("pontos", 0)

    payload = {
        "telefone": telefone,
        "pontos": pontos,
    }
    print("Requisição: payload =", payload, "url =", f"{BASE_URL}/redeems")
    try:
        url = f"{BASE_URL}/redeems"
        response = requests.post(url, json=payload)
        
        if response.status_code in (200, 201):
            return response.json()
        else:
            print(f"Falha ao criar resgate via API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("Erro na requisição para criar resgate via API:", e)
        return None

def delete_redeem(redeem_id):
    try:
        url = f"{BASE_URL}/redeems/{redeem_id}"
        response = requests.delete(url)
        
        if response.status_code in (200, 204):
            try:
                body = response.json()
                return int(body.get("deleted_count", 1))
            except Exception:
                return 1
        else:
            print(f"Falha ao deletar resgate via API: {response.status_code} - {response.text}")
            return 0
    except Exception as e:
        print("Erro ao deletar resgate:", e)
        return 0
