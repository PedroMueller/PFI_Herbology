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




"""
# =============================
# CATEGORIAS
# =============================
def get_categorias():
    "Lista todas as categorias cadastradas."
    return db.list_categorias()


# =============================
# LOCAIS
# =============================
def get_locais():
    "Lista todos os locais cadastrados."
    return db._fetchall("SELECT * FROM locais ORDER BY regiao, bioma")


# =============================
# REFERÊNCIAS
# =============================
def get_referencias():
    "Lista todas as referências cadastradas."
    return db._fetchall("SELECT * FROM referencias ORDER BY nome")


# =============================
# PREPAROS
# =============================
def get_preparos():
    "Lista todos os tipos de preparo cadastrados."
    return db._fetchall("SELECT * FROM preparos")



"""
