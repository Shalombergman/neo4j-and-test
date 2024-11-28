from flask import Flask
from phone_tracker.api.routes.phone_dispatcher import phone_blueprint
from phone_tracker.neo4j_service import Neo4jConnection
from phone_tracker.repositories.device_repository import DeviceRepository
from phone_tracker.config import NEO4J_CONFIG
app = Flask(__name__)


neo4j_connection = Neo4jConnection(**NEO4J_CONFIG)

device_repo = DeviceRepository(neo4j_connection) 


app.register_blueprint(phone_blueprint)


if __name__ == '__main__':
    app.run(debug=True,port=5004)