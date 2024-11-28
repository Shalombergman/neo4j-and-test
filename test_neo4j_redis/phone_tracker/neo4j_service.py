from neo4j import GraphDatabase
from typing import Any, Dict


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def execute_write(self, query: str, params: Dict[str, Any] = None):
        with self.driver.session() as session:
            return session.execute_write(lambda tx: tx.run(query, params))

    def execute_read(self, query: str, params: Dict[str, Any] = None):
        with self.driver.session() as session:
            return session.execute_read(lambda tx: tx.run(query, params))
    def close(self):
        self.driver.close()