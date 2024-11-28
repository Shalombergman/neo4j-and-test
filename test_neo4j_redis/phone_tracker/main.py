from flask import Flask
from phone_tracker.api.routes.phone_dispatcher import phone_blueprint
app = Flask(__name__)

app.register_blueprint(phone_blueprint)


if __name__ == '__main__':
    app.run(debug=True,port=5004)