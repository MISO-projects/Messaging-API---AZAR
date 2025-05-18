from flask import Flask, request
from flask_restful import Api, Resource
from models.blacklist import db, BlacklistEntry
import os
from sqlalchemy.sql import text
import newrelic.agent
newrelic.agent.initialize()

# Token estático para toda la aplicación
API_TOKEN = "token123456"
DB_USER = os.getenv('RDS_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('RDS_PASSWORD', 'postgres')
DB_HOST = os.getenv('RDS_HOSTNAME', 'localhost')
DB_PORT = os.getenv('RDS_PORT', '5432')
DB_NAME = os.getenv('RDS_DB_NAME', 'postgres')

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

db.init_app(application)

with application.app_context():
    db.create_all()
    print("Base de datos inicializada correctamente.") 

api = Api(application)

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
        entry = BlacklistEntry(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip_origen=ip_origen,
        )
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


class HealthCkResource(Resource):
    def get(self):
        try:
            # Verificar conexión a la base de datos
            db.session.execute(text('SELECT 1'))
            return {
                'status': 'healthy',
                'database': 'connected'
            }, 200
        except Exception as e:
            return {
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }, 500

api.add_resource(BlacklistResource, '/blacklists', '/blacklists/<string:email>')
api.add_resource(HealthCkResource, '/health')


if __name__ == '__main__':
    application.run(debug=True, port=8000)
