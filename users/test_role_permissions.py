from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core_auth.models import User

class RolePermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuarios con diferentes roles
        self.admin_user = User.objects.create_user(email='elta@kmkz.io', password='Kinteki.', role='admin')
        self.sysoper_user = User.objects.create_user(email='master@kmkz.io', password='Kinteki.', role='sysoper')
        self.opera_user = User.objects.create_user(email='useruno@kmkz.io', password='AlaVerga69', role='opera')

        # Crear un usuario objetivo para pruebas de modificación
        self.target_user = User.objects.create_user(email='usertres@kmkz.io', password='AlaVerga69', role='opera')

    def test_admin_can_register_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/apis/auth/register', {
            'email': 'usercuatro@kmkz.io',
            'password': 'AlaVerga69',
            'role': 'opera'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sysoper_cannot_register_user(self):
        self.client.force_authenticate(user=self.sysoper_user)
        response = self.client.post('/apis/auth/register', {
            'email': 'usercinco@kmkz.io',
            'password': 'AlaVerga69',
            'role': 'opera'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_other_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put('/apis/auth/mante', {
            'id': self.target_user.id,
            'role': 'sysoper'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_cannot_change_own_role(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put('/apis/auth/mante', {
            'id': self.admin_user.id,
            'role': 'opera'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sysoper_can_update_other_user_password(self):
        self.client.force_authenticate(user=self.sysoper_user)
        response = self.client.put('/apis/auth/mante', {
            'id': self.target_user.id,
            'password': 'QuePutas0ts'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_opera_cannot_update_any_user(self):
        self.client.force_authenticate(user=self.opera_user)
        response = self.client.put('/apis/auth/mante', {
            'id': self.target_user.id,
            'password': 'QuePutas0t'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
