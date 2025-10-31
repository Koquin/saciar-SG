# utils/api_utils.py
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import hashlib 

# Conexão com o MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["gerenciamento_clientes"]
collection_clients = db["clientes"]
collection_purchases = db["compras"] 
collection_prizes = db["premios"]
collection_auth = db["auth_users"] # COLLECTION PARA AUTENTICAÇÃO

# --- FUNÇÃO DE AJUDA PARA HASH (usada internamente) ---
def hash_password(password):
    """Gera o hash MD5 da senha."""
    return hashlib.md5(password.encode()).hexdigest()

# ----------------- CONFIGURAÇÃO INICIAL DE AUTENTICAÇÃO -----------------
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "123" 

if collection_auth.count_documents({}) == 0:
    try:
        hashed_password = hash_password(DEFAULT_PASSWORD)
        collection_auth.insert_one({
            "username": DEFAULT_USERNAME,
            "password_hash": hashed_password
        })
        print("---------------------------------------------------------")
        print(f"USUÁRIO PADRÃO CRIADO: {DEFAULT_USERNAME} / {DEFAULT_PASSWORD}")
        print("---------------------------------------------------------")
    except Exception as e:
        print(f"Erro ao criar usuário padrão no MongoDB: {e}")

# ----------------- Funções de AUTENTICAÇÃO (MongoDB) -----------------

def authenticate_user(username, password):
    """
    Verifica se o usuário e a senha correspondem ao registro no banco de dados.
    Retorna True se autenticado, False caso contrário.
    """
    try:
        password_hash = hash_password(password)
        
        user = collection_auth.find_one({
            "username": username,
            "password_hash": password_hash
        })
        
        return user is not None
        
    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return False

# ----------------- Funções CRUD - CLIENTES (MongoDB) -----------------

def get_clients():
    """Busca todos os clientes"""
    try:
        clients = list(collection_clients.find({}, {"_id": 0})) 
        return clients
    except Exception as e:
        print("Erro ao buscar clientes:", e)
        return []

# --- NOVA FUNÇÃO DE BUSCA PARA CLIENTES ---
def search_clients(query):
    """Busca clientes por nome, CPF ou telefone usando regex (insensível a caixa)."""
    if not query:
        return get_clients() # Retorna todos se a consulta estiver vazia
        
    try:
        # Cria um padrão de regex insensível a caixa para a consulta
        regex_pattern = {"$regex": query, "$options": "i"}
        
        filter_query = {
            "$or": [
                {"nome": regex_pattern},
                {"cpf": regex_pattern},
                {"telefone": regex_pattern}
            ]
        }
        
        clients = list(collection_clients.find(filter_query, {"_id": 0}))
        return clients
    except Exception as e:
        print("Erro ao buscar clientes:", e)
        return []


def post_client(client):
    """Cadastra um novo cliente"""
    try:
        novo_cliente = {
            "nome": client.get("nome", ""),
            "cpf": client.get("cpf", ""),
            "telefone": client.get("telefone", ""),
            "pontos": client.get("pontos", 0)
        }

        if collection_clients.find_one({"cpf": novo_cliente["cpf"]}):
            print("Cliente com esse CPF já existe.")
            return None

        collection_clients.insert_one(novo_cliente)
        return novo_cliente
    except Exception as e:
        print("Erro ao cadastrar cliente:", e)
        return None


def put_client(client):
    """Atualiza dados de um cliente pelo CPF"""
    try:
        cpf = client.get("cpf")
        if not cpf:
            print("CPF é obrigatório para atualizar.")
            return None
        
        update_data = {k: v for k, v in client.items() if k != 'cpf'}
        
        result = collection_clients.update_one({"cpf": cpf}, {"$set": update_data})
        if result.modified_count > 0:
            print("Cliente atualizado com sucesso!")
        
        return client
    except Exception as e:
        print("Erro ao atualizar cliente:", e)
        return None


def delete_client(cpf):
    """Remove cliente pelo CPF"""
    try:
        result = collection_clients.delete_one({"cpf": cpf})
        return result.deleted_count
    except Exception as e:
        print("Erro ao deletar cliente:", e)
        return 0

# ----------------- Funções CRUD - COMPRAS (MongoDB) -----------------

def get_purchases():
    """Busca todos os históricos de compras"""
    try:
        purchases = list(collection_purchases.find({}, {"_id": 0}))
        return purchases
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return []

# --- NOVA FUNÇÃO DE BUSCA PARA COMPRAS ---
def search_purchases(query):
    """Busca compras por nome do cliente, CPF ou data usando regex (insensível a caixa)."""
    if not query:
        return get_purchases() # Retorna todos se a consulta estiver vazia
        
    try:
        # Cria um padrão de regex insensível a caixa para a consulta
        regex_pattern = {"$regex": query, "$options": "i"}
        
        filter_query = {
            "$or": [
                {"cliente": regex_pattern},
                {"cpf": regex_pattern},
                {"data": regex_pattern}
            ]
        }
        
        purchases = list(collection_purchases.find(filter_query, {"_id": 0}))
        return purchases
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return []

def post_purchase(purchase):
    """
    Cadastra uma nova compra. Permite compra avulsa, implementa o limite de 10 pontos.
    """
    cpf = purchase.get("cpf", "").strip() 
    valor = purchase.get("valor", 0.0)
    is_delivery = purchase.get("is_delivery", False)
    
    cliente_encontrado = None
    cliente_nome = "Cliente Avulso"
    pontos_ganhos = 0
    MAX_PONTOS_ACUMULADOS = 10
    
    # 1. VERIFICAÇÃO CONDICIONAL DO CLIENTE
    if cpf:
        cliente_encontrado = collection_clients.find_one({"cpf": cpf})
        
        if cliente_encontrado:
            cliente_nome = cliente_encontrado.get("nome", "Desconhecido")
            pontos_atuais = cliente_encontrado.get("pontos", 0)
            
            # --- LÓGICA DE LIMITE DE PONTOS ---
            if pontos_atuais >= MAX_PONTOS_ACUMULADOS:
                pontos_ganhos = 0
                print(f"Cliente {cliente_nome} (CPF: {cpf}) já atingiu {MAX_PONTOS_ACUMULADOS} pontos. Sem novos pontos ganhos.")
            else:
                pontos_a_somar_raw = int(valor // 15)
                espaco_disponivel = MAX_PONTOS_ACUMULADOS - pontos_atuais
                pontos_ganhos = min(pontos_a_somar_raw, espaco_disponivel)
                
            
            # 3. ATUALIZA A PONTUAÇÃO DO CLIENTE NO DB (SOMENTE SE HOUVE GANHO)
            if pontos_ganhos > 0:
                novo_total_pontos = pontos_atuais + pontos_ganhos
                
                try:
                    collection_clients.update_one(
                        {"cpf": cpf},
                        {"$set": {"pontos": novo_total_pontos}}
                    )
                except Exception as e:
                    print("Erro ao atualizar pontos do cliente:", e)
            
        else:
            # CPF fornecido, mas não existe no cadastro.
            cliente_nome = f"CPF NÃO CADASTRADO ({cpf})"
            pontos_ganhos = 0
            
    data_hora_agora = datetime.datetime.now()

    # 4. Prepara e insere o registro da compra (SEMPRE SALVA AQUI)
    nova_compra = {
        "cliente": cliente_nome,
        "cpf": cpf or "AVULSO", 
        "valor": valor,
        "is_delivery": is_delivery,
        "pontos_ganhos": pontos_ganhos,
        "data": data_hora_agora.strftime("%Y-%m-%d %H:%M:%S")            
    }
    
    try:
        collection_purchases.insert_one(nova_compra)
        return nova_compra
    except Exception as e:
        print("Erro ao cadastrar compra:", e)
        return None

def put_purchase(purchase_id, new_data):
    """Atualiza dados de uma compra (não implementado, retorna None)"""
    return None 

def delete_purchase(cpf, data):
    """Remove uma compra específica pelo CPF e Data (para fins didáticos)"""
    try:
        result = collection_purchases.delete_one({"cpf": cpf, "data": data})
        return result.deleted_count
    except Exception as e:
        print("Erro ao deletar compra:", e)
        return 0

# ----------------- Funções CRUD - PRÊMIOS (MongoDB) -----------------

def get_prizes():
    try:
        prizes = list(collection_prizes.find({}, {"_id": 0}))
        
        if not prizes:
             return [
                 {"pontos": 3, "premio": "Desconto de 10%"},
                 {"pontos": 6, "premio": "Desconto de 30%"},
                 {"pontos": 8, "premio": "Desconto de 50%"},
                 {"pontos": 10, "premio": "Açái gratis"}
             ]
        
        return prizes
    except Exception as e:
        print("Erro ao buscar prêmios:", e)
        return []


def update_prizes(prizes_list: list):
    print("NO update_prizes, api_utils")
    try:
        collection_prizes.delete_many({})
        
        if prizes_list:
            print(f"Inserindo {len(prizes_list)} prêmios na coleção.")
            collection_prizes.insert_many(prizes_list)
        
        print(f"Prêmios atualizados com sucesso! Total de {len(prizes_list)} prêmios.")
        
        return True
    
    except Exception as e:
        print("Erro ao atualizar prêmios:", e)
        return False