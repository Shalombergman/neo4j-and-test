from neo4j import GraphDatabase
from typing import Any, Dict

class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def execute_write(self, query: str, params: Dict[str, Any] = None) -> Any:
        with self.driver.session() as session:
            def transaction(tx):
                result = tx.run(query, params)
                return list(result)
            return session.execute_write(transaction)

    def execute_read(self, query: str, params: Dict[str, Any] = None) -> Any:
        with self.driver.session() as session:
            def transaction(tx):
                result = tx.run(query, params)
                return list(result)
            return session.execute_read(transaction)

    def close(self):
        if self.driver:
            self.driver.close()

    def __del__(self):
        self.close()