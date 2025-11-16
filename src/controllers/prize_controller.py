import requests

BASE_URL = "http://localhost:8000"

def get_prizes():
    """Busca todos os prêmios via API"""
    try:
        url = f"{BASE_URL}/prizes"
        print(f"[api_utils] GET {url}")
        response = requests.get(url)
        print(f"[api_utils] GET {url} -> status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[api_utils] GET {url} -> json (truncated): {str(data)[:1000]}")
            return data
        else:
            print(f"Erro ao buscar prêmios via API: {response.status_code} - {response.text}")
            return [
                {"pontos": 3, "premio": "Desconto de 10%"},
                {"pontos": 6, "premio": "Desconto de 30%"},
                {"pontos": 8, "premio": "Desconto de 50%"},
                {"pontos": 10, "premio": "Açaí gratis"}
            ]
    except Exception as e:
        print("Erro ao buscar prêmios:", e)
        return []

def update_prizes(prizes_list: list):
    """Atualiza a lista completa de prêmios via API"""
    print("[api_utils] Iniciando update_prizes")
    try:
        url = f"{BASE_URL}/prizes"
        print(f"[api_utils] PUT {url} payload={prizes_list}")
        
        response = requests.put(url, json=prizes_list)
        print(f"[api_utils] PUT {url} -> status: {response.status_code}")
        
        try:
            print(f"[api_utils] PUT {url} -> json (truncated): {str(response.json())[:1000]}")
        except Exception:
            print(f"[api_utils] PUT {url} -> text (truncated): {response.text[:1000]}")
        
        if response.status_code in (200, 201):
            print(f"[api_utils] Prêmios atualizados com sucesso! Total: {len(prizes_list)}")
            return True
        else:
            print(f"[api_utils] Falha ao atualizar prêmios via API: {response.status_code}")
            return False
    except Exception as e:
        print("Erro ao atualizar prêmios:", e)
        return False