from flask import request, jsonify
from flask_restful import Resource
from models.blacklist import BlacklistEntry, db
from flask_jwt_extended import jwt_required


class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        email = data.get('email')
        app_uuid = data.get('app_uuid')
        blocked_reason = data.get('blocked_reason', '')

        if not email or not app_uuid:
            return {'message': 'Email y app_uuid son obligatorios'}, 400

        ip_origen = request.remote_addr

        entry = BlacklistEntry(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason, ip_origen=ip_origen)
        db.session.add(entry)
        db.session.commit()

        return {'message': 'Email agregado a la lista negra'}, 201

    @jwt_required()
    def get(self, email):
        entry = BlacklistEntry.query.filter_by(email=email).first()
        if entry:
            return {'is_blacklisted': True, 'blocked_reason': entry.blocked_reason}, 200
        else:
            return {'is_blacklisted': False, 'blocked_reason': None}, 200
