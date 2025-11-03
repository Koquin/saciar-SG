import requests

BASE_URL = "http://localhost:8000"

def authenticate_user(username, password):
    print("No api_utils, metodo authenticate_user")
    try:
        request = requests.post(f"{BASE_URL}/auth/login", json={
            "username": username, "password": password})
        if request.status_code == 200:
            print("Autenticação bem sucedida!")
            return True
        else:
            return None
    except Exception as e:
        print("Erro na requisição de autenticação:", e)
        return None
    
