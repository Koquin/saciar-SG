import requests

BASE_URL = "http://localhost:8000"

def get_purchases():
    try:
        url = f"{BASE_URL}/purchase"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar compras via API: {response.status_code}")
            return []
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return []

def search_purchases(query):
    if not query:
        return get_purchases()
        
    try:
        params = {"q": query} if query else {}
        url = f"{BASE_URL}/purchase/search"
        print(f"[purchase_controller] GET {url} params={params}")
        response = requests.get(url, params=params)
        print(f"[purchase_controller] GET {url} -> status: {response.status_code}")
        try:
            print(f"[purchase_controller] GET {url} -> json (truncated): {str(response.json())[:1000]}")
        except Exception:
            print(f"[purchase_controller] GET {url} -> text (truncated): {response.text[:1000]}")

        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return []

def post_purchase(purchase):
    cpf = purchase.get("cpf", "").strip() 
    valor = purchase.get("valor", 0.0)
    is_delivery = purchase.get("is_delivery", False)
    
    payload = {
        "cpf": cpf or "AVULSO",
        "valor": valor,
        "is_delivery": is_delivery,
        'isFromClient': False,
    }
    try:
        url = f"{BASE_URL}/purchase"
        print(f"[purchase_controller] POST {url} payload={payload}")
        response = requests.post(url, json=payload)
        print(f"[purchase_controller] POST {url} -> status: {response.status_code}")
        try:
            print(f"[purchase_controller] POST {url} -> json (truncated): {str(response.json())[:1000]}")
        except Exception:
            print(f"[purchase_controller] POST {url} -> text (truncated): {response.text[:1000]}")

        if response.status_code in (200, 201):
            return response.json()
        else:
            print(f"Falha ao cadastrar compra via API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("Erro na requisição para cadastrar compra via API:", e)
        return None

def delete_purchase(purchase_id):
    """Remove uma compra específica pelo ID"""
    try:
        url = f"{BASE_URL}/purchase/{purchase_id}"
        print(f"[purchase_controller] DELETE {url}")
        response = requests.delete(url)
        print(f"[purchase_controller] DELETE {url} -> status: {response.status_code}")
        try:
            print(f"[purchase_controller] DELETE {url} -> json (truncated): {str(response.json())[:1000]}")
        except Exception:
            print(f"[purchase_controller] DELETE {url} -> text (truncated): {response.text[:1000]}")

        if response.status_code in (200, 204):
            try:
                body = response.json()
                return int(body.get("deleted_count", 1))
            except Exception:
                return 1
        else:
            print(f"Falha ao deletar compra via API: {response.status_code} - {response.text}")
            return 0
    except Exception as e:
        print("Erro ao deletar compra:", e)
        return 0
