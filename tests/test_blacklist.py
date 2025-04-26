import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

from application import application, API_TOKEN
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestBlacklistAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = application
        self.client = self.app.test_client()
        self.headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
        
    @patch('application.db.session')
    def test_add_to_blacklist_success(self, mock_db_session):
        test_data = {
            'email': 'test@example.com',
            'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
            'blocked_reason': 'Prueba de bloqueo'
        }
        
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()
        
        response = self.client.post(
            '/blacklists', 
            data=json.dumps(test_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Email agregado a la lista negra')
        
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    def test_add_to_blacklist_invalid_token(self):
        test_data = {
            'email': 'test@example.com',
            'app_uuid': '123e4567-e89b-12d3-a456-426614174000'
        }
        
        invalid_headers = {'Authorization': 'Bearer token_invalido', 'Content-Type': 'application/json'}
        
        response = self.client.post(
            '/blacklists', 
            data=json.dumps(test_data),
            headers=invalid_headers
        )
        
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Token inválido')
    
    def test_add_to_blacklist_missing_data(self):
        test_data = {
            'email': 'test@example.com'
        }
        
        response = self.client.post(
            '/blacklists', 
            data=json.dumps(test_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Email y app_uuid son obligatorios')
    
    @patch('application.BlacklistResource.get')
    def test_check_email_in_blacklist(self, mock_get):
        mock_get.return_value = (
            {'is_blacklisted': True, 'blocked_reason': 'Razón de prueba'}, 
            200
        )
        
        response = self.client.get(
            '/blacklists/test@example.com',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['is_blacklisted'])
        self.assertEqual(response_data['blocked_reason'], 'Razón de prueba')
        
        mock_get.assert_called_once_with(email='test@example.com')
    
    @patch('application.BlacklistResource.get')
    def test_check_email_not_in_blacklist(self, mock_get):
        mock_get.return_value = (
            {'is_blacklisted': False, 'blocked_reason': None}, 
            200
        )
        
        response = self.client.get(
            '/blacklists/clean@example.com',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertFalse(response_data['is_blacklisted'])
        self.assertIsNone(response_data['blocked_reason'])
        
        mock_get.assert_called_once_with(email='clean@example.com')
    
    @patch('application.db.session')
    def test_health_check_success(self, mock_db_session):
        mock_db_session.execute = MagicMock()
        
        response = self.client.get('/health')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'healthy')
        self.assertEqual(response_data['database'], 'connected')
    
    @patch('application.db.session')
    def test_health_check_failure(self, mock_db_session):
        mock_db_session.execute.side_effect = Exception("Error de conexión")
        
        response = self.client.get('/health')
        
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'unhealthy')
        self.assertEqual(response_data['database'], 'disconnected')
        self.assertEqual(response_data['error'], 'Error de conexión')


if __name__ == '__main__':
    unittest.main()
