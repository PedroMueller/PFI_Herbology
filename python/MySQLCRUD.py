# =============================================================
# Projeto Herbology - CRUD com MySQL
# =============================================================
# Este script implementa todas as operações básicas (CRUD)
# para o banco de dados Herbology, que armazena informações
# sobre plantas medicinais brasileiras.
#
# O código usa o conector oficial do MySQL para Python
# (mysql-connector-python). Se não tiver instalado, use:
#    pip install mysql-connector-python
#
# =============================================================

import mysql.connector
from mysql.connector import errorcode
from typing import Optional, Dict, Any, List, Tuple


# =============================================================
# SCRIPT DE CRIAÇÃO DAS TABELAS
# =============================================================
# Aqui criamos as tabelas de acordo com o Modelo Conceitual:
# - Plantas
# - Categorias
# - Locais
# - Referencias
# - Preparos
# E também as tabelas de RELAÇÃO (N:N), pois uma planta pode:
# - Pertencer a várias categorias
# - Ser encontrada em vários locais
# - Ter várias referências
# - Ser usada em vários preparos
#
# O CHARSET utf8mb4 permite salvar acentos e emojis sem erro.
# =============================================================
SCHEMA_SQL = [
    # -------- Tabela principal: Plantas --------
    """
    CREATE TABLE IF NOT EXISTS plantas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome_popular      VARCHAR(120) NOT NULL,
        nome_cientifico   VARCHAR(160) NOT NULL UNIQUE,
        descricao         TEXT,
        imagem_url        VARCHAR(255)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # -------- Tabela de Categorias (ex: Medicinal, Culinária) --------
    """
    CREATE TABLE IF NOT EXISTS categorias (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # -------- Tabela de Locais (ex: Região Sul, Bioma Mata Atlântica) --------
    """
    CREATE TABLE IF NOT EXISTS locais (
        id INT AUTO_INCREMENT PRIMARY KEY,
        regiao VARCHAR(80) NOT NULL,
        bioma  VARCHAR(80) NOT NULL,
        UNIQUE KEY unq_local (regiao, bioma)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # -------- Tabela de Referências (livros, sites, artigos científicos) --------
    """
    CREATE TABLE IF NOT EXISTS referencias (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(160) NOT NULL,
        url  VARCHAR(255) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # -------- Tabela de Preparos (ex: chá, infusão, pomada) --------
    """
    CREATE TABLE IF NOT EXISTS preparos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        descricao TEXT NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # =============================================================
    # Tabelas de RELAÇÃO (N:N)
    # =============================================================
    # Cada relação garante integridade com FOREIGN KEY e
    # remove vínculos automaticamente com ON DELETE CASCADE.
    # =============================================================

    # -------- Planta ↔ Categoria --------
    """
    CREATE TABLE IF NOT EXISTS planta_categoria (
        planta_id   INT NOT NULL,
        categoria_id INT NOT NULL,
        PRIMARY KEY (planta_id, categoria_id),
        CONSTRAINT fk_pc_planta  FOREIGN KEY (planta_id)   REFERENCES plantas(id)     ON DELETE CASCADE,
        CONSTRAINT fk_pc_categ   FOREIGN KEY (categoria_id) REFERENCES categorias(id)  ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # -------- Planta ↔ Local --------
    """
    CREATE TABLE IF NOT EXISTS planta_local (
        planta_id INT NOT NULL,
        local_id  INT NOT NULL,
        PRIMARY KEY (planta_id, local_id),
        CONSTRAINT fk_pl_planta FOREIGN KEY (planta_id) REFERENCES plantas(id) ON DELETE CASCADE,
        CONSTRAINT fk_pl_local  FOREIGN KEY (local_id)  REFERENCES locais(id)   ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # -------- Planta ↔ Referencia --------
    """
    CREATE TABLE IF NOT EXISTS planta_referencia (
        planta_id INT NOT NULL,
        referencia_id INT NOT NULL,
        PRIMARY KEY (planta_id, referencia_id),
        CONSTRAINT fk_pr_planta     FOREIGN KEY (planta_id)     REFERENCES plantas(id)     ON DELETE CASCADE,
        CONSTRAINT fk_pr_referencia FOREIGN KEY (referencia_id) REFERENCES referencias(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,

    # -------- Planta ↔ Preparo --------
    """
    CREATE TABLE IF NOT EXISTS planta_preparo (
        planta_id INT NOT NULL,
        preparo_id INT NOT NULL,
        PRIMARY KEY (planta_id, preparo_id),
        CONSTRAINT fk_pp_planta  FOREIGN KEY (planta_id)  REFERENCES plantas(id)  ON DELETE CASCADE,
        CONSTRAINT fk_pp_preparo FOREIGN KEY (preparo_id) REFERENCES preparos(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
]


# =============================================================
# CLASSE PRINCIPAL DO CRUD
# =============================================================
# Essa classe gerencia a conexão com o banco de dados e
# fornece métodos para manipular cada tabela.
# =============================================================
class HerbologyDB:
    """
    Classe DAO (Data Access Object) para o banco Herbology.
    - Conecta ao MySQL
    - Cria o banco de dados se não existir
    - Cria as tabelas do modelo
    - Implementa CRUD completo para Plantas e auxiliares
    """

    def __init__(
        self,
        host: str = "localhost",
        user: str = "root",
        password: str = "ifprquedas",
        database: str = "herbology",
        port: int = 3306,
    ):
        # 1ª conexão sem database → garante que o banco exista
        self.cnx = mysql.connector.connect(host=host, user=user, password=password, port=port)
        self.cnx.autocommit = True  # executa CREATE DATABASE fora de transação
        cur = self.cnx.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` DEFAULT CHARACTER SET utf8mb4")
        cur.close()

        # 2ª conexão já apontando para o banco criado
        self.cnx.close()
        self.cnx = mysql.connector.connect(
            host=host, user=user, password=password, database=database, port=port
        )
        self.cnx.autocommit = False  # agora usamos transações
        self._create_schema()  # cria as tabelas

    # =============================================================
    # MÉTODOS INTERNOS (apoio)
    # =============================================================
    def _create_schema(self) -> None:
        """Executa o script SCHEMA_SQL e cria as tabelas."""
        cur = self.cnx.cursor()
        try:
            for sql in SCHEMA_SQL:
                cur.execute(sql)
            self.cnx.commit()
        finally:
            cur.close()

    def _fetchone(self, sql: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Executa SELECT e retorna apenas 1 registro (dict)."""
        cur = self.cnx.cursor(dictionary=True)
        try:
            cur.execute(sql, params)
            return cur.fetchone()
        finally:
            cur.close()

    def _fetchall(self, sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Executa SELECT e retorna todos os registros (lista de dicts)."""
        cur = self.cnx.cursor(dictionary=True)
        try:
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            cur.close()

    def _execute(self, sql: str, params: Tuple = ()) -> int:
        """
        Executa INSERT/UPDATE/DELETE.
        Retorna o ID gerado no caso de INSERT.
        """
        cur = self.cnx.cursor()
        try:
            cur.execute(sql, params)
            last_id = cur.lastrowid or 0
            self.cnx.commit()
            return last_id
        except Exception:
            self.cnx.rollback()  # se der erro, desfaz a transação
            raise
        finally:
            cur.close()

    def close(self) -> None:
        """Fecha a conexão com o banco."""
        self.cnx.close()

    # =============================================================
    # CRUD: PLANTAS
    # =============================================================
    def add_planta(self, nome_popular: str, nome_cientifico: str,
                   descricao: Optional[str] = None, imagem_url: Optional[str] = None) -> int:
        """Insere nova planta no banco."""
        sql = """
            INSERT INTO plantas (nome_popular, nome_cientifico, descricao, imagem_url)
            VALUES (%s, %s, %s, %s)
        """
        return self._execute(sql, (nome_popular, nome_cientifico, descricao, imagem_url))

    def get_planta(self, planta_id: int) -> Optional[Dict[str, Any]]:
        """Busca planta pelo ID."""
        return self._fetchone("SELECT * FROM plantas WHERE id=%s", (planta_id,))
    
    #!Olhar com o anderson sobre essa função

    #def list_plantas(self, termo: Optional[str] = None) -> List[Dict[str, Any]]:
    #    """Lista todas as plantas, podendo filtrar por nome."""
    #    if termo:
    #        like = f"%{termo}%"
    #        return self._fetchall(
    #            """SELECT * FROM plantas
    #               WHERE nome_popular LIKE '%f%' OR nome_cientifico LIKE '%f%' OR decricao LIKE '%f%'
    #               ORDER BY nome_popular""",
    #            (like, like),
    #        )
    #    return self._fetchall("SELECT * FROM plantas ORDER BY nome_popular")
    

    def list_plantas(self, termo: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todas as plantas, podendo filtrar por nome."""
        if termo:
            like = f"%{termo}%"
            print("Termo recebido:", termo)
            print("Filtro usado no LIKE:", like)

            return self._fetchall(
                """
                SELECT * FROM plantas
                WHERE nome_popular LIKE %s
                OR nome_cientifico LIKE %s
                OR descricao LIKE %s
                ORDER BY nome_popular
                """,
                (like, like, like),
            )
        else:
            # se nenhum termo for informado, retorna tudo
            return self._fetchall(
                "SELECT * FROM plantas ORDER BY nome_popular"
            )


    def get_plantas(self) -> List[Dict[str, Any]]:
        """Lista todas as plantas"""
        return self._fetchall("SELECT * FROM plantas ORDER BY id")


    def update_planta(self, planta_id: int, campos: Dict[str, Any]) -> bool:
        """Atualiza atributos de uma planta (parcial)."""
        if not campos:
            return False
        #* Monta dinamicamente as colunas para o comando SQL "nome_popular=%s, descricao=%s"
        cols = ", ".join(f"{k}=%s" for k in campos.keys())
        params = tuple(campos.values()) + (planta_id,)
        sql = f"UPDATE plantas SET {cols} WHERE id=%s"
        self._execute(sql, params)
        return True

    def delete_planta(self, planta_id: int) -> bool:
        """Remove planta e suas relações (ON DELETE CASCADE)."""
        self._execute("DELETE FROM plantas WHERE id=%s", (planta_id,))
        return True

    # =============================================================
    # CRUD: CATEGORIAS
    # =============================================================
    def add_categoria(self, nome: str) -> int:
        """Adiciona uma categoria (ou retorna existente)."""
        return self._execute(
            "INSERT INTO categorias (nome) VALUES (%s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)",
            (nome,),
        )

    def list_categorias(self) -> List[Dict[str, Any]]:
        """Lista todas as categorias."""
        return self._fetchall("SELECT * FROM categorias ORDER BY nome")

    def link_planta_categoria(self, planta_id: int, categoria_id: int) -> None:
        """Relaciona planta a uma categoria."""
        self._execute(
            "INSERT IGNORE INTO planta_categoria (planta_id, categoria_id) VALUES (%s,%s)",
            (planta_id, categoria_id),
        )

    # =============================================================
    # CRUD: LOCAIS
    # =============================================================
    def add_local(self, regiao: str, bioma: str) -> int:
        """Adiciona um local único (região+bioma)."""
        return self._execute(
            """INSERT INTO locais (regiao, bioma)
               VALUES (%s,%s)
               ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)""",
            (regiao, bioma),
        )

    def link_planta_local(self, planta_id: int, local_id: int) -> None:
        """Relaciona planta a um local."""
        self._execute(
            "INSERT IGNORE INTO planta_local (planta_id, local_id) VALUES (%s,%s)",
            (planta_id, local_id),
        )

    # =============================================================
    # CRUD: REFERÊNCIAS
    # =============================================================
    def add_referencia(self, nome: str, url: str) -> int:
        """Adiciona uma referência bibliográfica/site."""
        return self._execute(
            "INSERT INTO referencias (nome, url) VALUES (%s,%s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)",
            (nome, url),
        )

    def link_planta_referencia(self, planta_id: int, referencia_id: int) -> None:
        """Relaciona planta a uma referência."""
        self._execute(
            "INSERT IGNORE INTO planta_referencia (planta_id, referencia_id) VALUES (%s,%s)",
            (planta_id, referencia_id),
        )

    # =============================================================
    # CRUD: PREPAROS
    # =============================================================
    def add_preparo(self, descricao: str) -> int:
        """Adiciona um tipo de preparo (ex: infusão)."""
        return self._execute("INSERT INTO preparos (descricao) VALUES (%s)", (descricao,))

    def link_planta_preparo(self, planta_id: int, preparo_id: int) -> None:
        """Relaciona planta a um preparo."""
        self._execute(
            "INSERT IGNORE INTO planta_preparo (planta_id, preparo_id) VALUES (%s,%s)",
            (planta_id, preparo_id),
        )

    # =============================================================
    # CONSULTA COMPOSTA
    # =============================================================
    def get_planta_completa(self, planta_id: int) -> Optional[Dict[str, Any]]:
        """
        Retorna a planta + todas as suas relações:
        categorias, locais, referências e preparos.
        """
        planta = self.get_planta(planta_id)
        if not planta:
            return None
        planta["categorias"] = self._fetchall(
            """SELECT c.* FROM categorias c
               JOIN planta_categoria pc ON pc.categoria_id=c.id
               WHERE pc.planta_id=%s ORDER BY c.nome""",
            (planta_id,),
        )   
        planta["locais"] = self._fetchall(
            """SELECT l.* FROM locais l
               JOIN planta_local pl ON pl.local_id=l.id
               WHERE pl.planta_id=%s ORDER BY l.regiao, l.bioma""",
            (planta_id,),
        )
        planta["referencias"] = self._fetchall(
            """SELECT r.* FROM referencias r
               JOIN planta_referencia pr ON pr.referencia_id=r.id
               WHERE pr.planta_id=%s ORDER BY r.nome""",
            (planta_id,),
        )
        planta["preparos"] = self._fetchall(
            """SELECT p.* FROM preparos p
               JOIN planta_preparo pp ON pp.preparo_id=p.id
               WHERE pp.planta_id=%s""",
            (planta_id,),
        )
        return planta


# =============================================================
# EXEMPLO DE USO
# =============================================================
if __name__ == "__main__":
    db = HerbologyDB(user="root", password="ifprquedas", database="herbology")

    # 1. Criar planta
    cidreira_id = db.add_planta(
        nome_popular="Erva-cidreira",
        nome_cientifico="Melissa officinalis",
        descricao="Calmante leve; folhas aromáticas.",
        imagem_url="https://exemplo.com/imagens/melissa.jpg",
    )

    # 2. Adicionar categoria
    cat_medicinal = db.add_categoria("Medicinal")
    db.link_planta_categoria(cidreira_id, cat_medicinal)

    # 3. Adicionar local
    local_sul_mata = db.add_local(regiao="Sul", bioma="Mata Atlântica")
    db.link_planta_local(cidreira_id, local_sul_mata)

    # 4. Adicionar referência
    ref_id = db.add_referencia("Manual de Fitoterapia", "https://exemplo.com/manual-fitoterapia")
    db.link_planta_referencia(cidreira_id, ref_id)

    # 5. Adicionar preparo
    prep_id = db.add_preparo("Infusão de 5–10 min, 1 colher de folhas por xícara.")
    db.link_planta_preparo(cidreira_id, prep_id)

    # 6. Consultar planta completa
    print(db.get_planta_completa(cidreira_id))

    db.close()
