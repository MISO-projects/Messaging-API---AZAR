from flask import Flask, request
from flask_restful import Api, Resource
from models.blacklist import db, BlacklistEntry

# Token estático para toda la aplicación
API_TOKEN = "token123456"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/blacklist_db'

db.init_app(app)
api = Api(app)

def validate_token():
    token = request.headers.get('Authorization')
    if not token or token != f"Bearer {API_TOKEN}":
        return False
    return True

class BlacklistResource(Resource):
    def post(self):
        if not validate_token():
            return {'message': 'Token inválido'}, 401

        data = request.get_json()
        email = data.get('email')
        app_uuid = data.get('app_uuid')
        blocked_reason = data.get('blocked_reason', '')

        if not email or not app_uuid:
            return {'message': 'Email y app_uuid son obligatorios'}, 400

        # Se captura la IP de origen
        ip_origen = request.remote_addr

        # Crear la entrada
        entry = BlacklistEntry(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason, ip_origen=ip_origen)
        db.session.add(entry)
        db.session.commit()

        return {'message': 'Email agregado a la lista negra'}, 201

    def get(self, email):
        if not validate_token():
            return {'message': 'Token inválido'}, 401

        # Consulta para verificar si el email está en la lista negra
        entry = BlacklistEntry.query.filter_by(email=email).first()
        if entry:
            return {'is_blacklisted': True, 'blocked_reason': entry.blocked_reason}, 200
        else:
            return {'is_blacklisted': False, 'blocked_reason': None}, 200

api.add_resource(BlacklistResource, '/blacklists', '/blacklists/<string:email>')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
