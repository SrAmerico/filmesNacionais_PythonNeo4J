# database.py
from neo4j import GraphDatabase


class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            # Garante que todos os resultados sejam consumidos
            return list(result)  # Consume todos os resultados


# Configuração de conexão com o Neo4j
db = Database("bolt://localhost:7687", "neo4j", "teste1234")
