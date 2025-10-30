# utils/api_utils.py
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

# Conexão com o MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["gerenciamento_clientes"]
collection_clients = db["clientes"]
collection_purchases = db["compras"] 

# ----------------- Funções CRUD - CLIENTES (MongoDB) -----------------

def get_clients():
    """Busca todos os clientes"""
    try:
        # Busca, projeta e converte ObjectId para str para evitar erros
        clients = list(collection_clients.find({}, {"_id": 0})) 
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

        # Verifica se CPF já existe
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
        
        # Remove o CPF dos dados a serem atualizados para garantir que ele não seja alterado
        update_data = {k: v for k, v in client.items() if k != 'cpf'}
        
        result = collection_clients.update_one({"cpf": cpf}, {"$set": update_data})
        if result.modified_count > 0:
            print("Cliente atualizado com sucesso!")
        
        # Retorna o cliente com os dados atualizados (incluindo o CPF)
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
        # Busca, projeta e converte ObjectId para str
        purchases = list(collection_purchases.find({}, {"_id": 0}))
        return purchases
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return []

def post_purchase(purchase):
    """
    Cadastra uma nova compra.
    1. Busca o cliente para obter o nome.
    2. Calcula os pontos ganhos.
    3. Atualiza a pontuação total do cliente.
    4. Insere o registro da compra.
    """
    cpf = purchase.get("cpf", "")
    valor = purchase.get("valor", 0.0)
    is_delivery = purchase.get("is_delivery", False)
    
    # 1. Busca o cliente
    cliente_encontrado = collection_clients.find_one({"cpf": cpf})
    if not cliente_encontrado:
        print(f"Cliente com CPF {cpf} não encontrado.")
        return None

    cliente_nome = cliente_encontrado.get("nome", "Desconhecido")
    
    # 2. Calcula os pontos (Exemplo: 1 ponto a cada R$10,00)
    calculated_points = int(valor // 15)
    pontos_ganhos = min(10, calculated_points)
    # 3. Atualiza a pontuação total do cliente
    pontos_atuais = cliente_encontrado.get("pontos", 0)
    novo_total_pontos = pontos_atuais + pontos_ganhos
    
    try:
        collection_clients.update_one(
            {"cpf": cpf},
            {"$set": {"pontos": novo_total_pontos}}
        )
    except Exception as e:
        print("Erro ao atualizar pontos do cliente:", e)
        return None

    # 4. Prepara e insere o registro da compra
    nova_compra = {
        "cliente": cliente_nome,
        "cpf": cpf,
        "valor": valor,
        "is_delivery": is_delivery,
        "pontos_ganhos": pontos_ganhos,
        "data": datetime.date.today().strftime("%Y-%m-%d")
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