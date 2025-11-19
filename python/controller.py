from MySQLCRUD import HerbologyDB

# Cria instância da conexão (pode ser ajustado via .env depois)
db = HerbologyDB(user="root", password="ifprquedas", database="herbology")

# =============================
# PLANTAS
# =============================
def get_plantas():
    """Retorna uma planta pelo ID."""
    print(db.get_plantas())
    return db.get_plantas()



def get_planta_completa(planta_id: int):
    """Obtém todas as informações detalhadas de uma planta."""
    return db.get_planta_completa(planta_id)


def buscar_planta(termo: str):
    """
    Busca plantas por nome popular ou científico.
    """
    if not termo:
        # Se o termo estiver vazio, retorna todas
        return db.list_plantas()
        
    return db.list_plantas(termo)

# =============================
# ADMIN - CRUD PLANTAS
# =============================

def add_planta(nome_popular: str, nome_cientifico: str, descricao: str, imagem_url: str):
    """
    Adiciona uma nova planta no banco.
    """
    return db.add_planta(nome_popular, nome_cientifico, descricao, imagem_url)


def update_planta(planta_id: int, campos: dict):
    """
    Atualiza parcialmente os dados de uma planta.
    Campos deve ser um dict com:
    {
        "nome_popular": "...",
        "nome_cientifico": "...",
        "descricao": "...",
        "imagem_url": "..."
    }
    """
    # Remove campos None (não enviados)
    campos_limpos = {k: v for k, v in campos.items() if v is not None}

    if not campos_limpos:
        raise ValueError("Nenhum campo para atualizar.")

    return db.update_planta(planta_id, campos_limpos)


def delete_planta(planta_id: int):
    """
    Remove uma planta pelo ID.
    """
    return db.delete_planta(planta_id)

