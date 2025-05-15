from flask import Flask
from flask_cors import CORS
from src.controllers.piloto_controller import piloto_bp
from src.controllers.circuito_controller import circuito_bp
from src.controllers.lenda_controller import lenda_bp

app = Flask(__name__)
CORS(app)

# Registrando os blueprints
app.register_blueprint(piloto_bp, url_prefix='/api')
app.register_blueprint(circuito_bp, url_prefix='/api')
app.register_blueprint(lenda_bp, url_prefix='/api')

@app.route('/')
def home():
    return {"message": "API do Sistema Fórmula 1"}

if __name__ == '__main__':
    app.run(debug=True) 