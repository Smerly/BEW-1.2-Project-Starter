# Create your tests here.
# Imports
import os
import unittest
import app

from datetime import date
from reminderapp.extensions import app, db, bcrypt
from reminderapp.models import Reminder, User, Category
#################################################
# Setup
#################################################


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def create_reminders():
    new_reminder = Reminder(
        name='reminder1',
        soft_deadline='2022-03-04',
        hard_deadline='2022-03-04',
        final_deadline='2022-03-04',
    )
    db.session.add(new_reminder)

    new_reminder2 = Reminder(
        name='reminder2',
        soft_deadline='2022-03-03',
        hard_deadline='2022-03-03',
        final_deadline='2022-03-03',
    )

    db.session.add(new_reminder2)
    db.session.commit()


def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('asd').decode('utf-8')
    user = User(username='asd', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################


class MainTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        create_reminders()
        create_user()

        response = self.app.get('/', follows_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertIn('')
        self.assertNotIn('')
