#-*- coding: utf-8 -*-
"""
    tests.apps.portal.test_user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test some user model functions

    :copyright: (c) 2007-2015 by the Inyoka Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from django.http import Http404
from django.test import TestCase

from inyoka.portal.user import User, Group, deactivate_user
from inyoka.portal.views import get_user
from posix import rename


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.register_user('testing', 'example@example.com',
                                               'pwd', False)

    def test_deactivation(self):
        """Test if the user status is correctly changed after deactivating a
        user.
        """
        deactivate_user(self.user)
        self.user = User.objects.get(pk=self.user.id)
        self.assertEqual(self.user.status, 3)

    def test_get_user_by_username(self):
        user = get_user('testing')
        self.assertEqual(user, self.user)

    def test_get_user_by_email(self):
        user = get_user('example@example.com')
        self.assertEqual(user, self.user)

    def test_get_user_fallback_to_username(self):
        created_user = User.objects.register_user('foo@bar.d', 'foo@bar.de', 'pwd', False)
        user = get_user('foo@bar.d')
        self.assertEqual(user, created_user)

    def test_get_user_fallback_fails(self):
        User.objects.register_user('foo@bar.d', 'foo@bar.de', 'pwd', False)
        with self.assertRaises(Http404):
            get_user('foo@bar')
    
    def test_rename_user(self):
        created_user = User.objects.register_user('testuser', 'test@user.de', 'pwd', False)        
        self.assertEqual(True, created_user.rename('testuser2', False))
        self.assertEqual(created_user.__unicode__(), 'testuser2')
    
    def test_rename_user_collision(self):
        User.objects.register_user('testuser', 'test@user.de', 'pwd', False)
        created_user = User.objects.register_user('testuser2', 'test2@user.de', 'pwd', False)
        self.assertEqual(False, created_user.rename('testuser', False))
            
    def test_rename_user_invalid(self):
        created_user = User.objects.register_user('testuser', 'test@user.de', 'pwd', False)
        with self.assertRaises(ValueError):
            created_user.rename('**testuser**', False)
        

class TestGroupModel(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testing', is_public=True)

    def test_icon(self):
        # TODO? What should be tested here?
        self.assertEqual(self.group.icon_url, None)
