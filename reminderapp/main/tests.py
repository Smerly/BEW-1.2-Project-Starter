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
        response = self.app.get('/', follows_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertIn(
            '<a class="customlink nav-item" href="/login">Log In</a>', response_text)
        self.assertNotIn('Log Out', response_text)

    def test_homepage_logged_in(self):
        create_user()
        login(self.app, 'asd', 'asd')
        response = self.app.get('/', follows_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertNotIn(
            '<a class="customlink nav-item" href="/login">Log In</a>', response_text)
        self.assertIn('Log Out', response_text)

    def test_create_reminder_logged_out(self):
        response = self.app.get('/', follows_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertNotIn('Create A Reminder', response_text)

    def test_create_reminder_logged_in(self):
        create_user()
        create_reminders()
        login(self.app, 'asd', 'asd')
        new_reminder = {
            'name': 'new',
            'soft_deadline': '2022-03-04',
            'hard_deadline': '2022-03-04',
            'final_deadline': '2022-03-04'
        }
        self.app.post('/create_reminder', data=new_reminder)

        created_reminder = Reminder.query.filter_by(name='new').one()
        self.assertEqual(created_reminder.soft_deadline, '2022-03-04')

    def test_see_reminders_logged_in(self):
        create_user()
        create_reminders()
        login(self.app, 'asd', 'asd')
        new_reminder = {
            'name': 'new',
            'soft_deadline': '2022-03-04',
            'hard_deadline': '2022-03-04',
            'final_deadline': '2022-03-04'
        }
        self.app.post('/create_reminder', data=new_reminder)

        response = self.app.get('/', follows_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertIn('2022-03-04', response_text)

    def test_see_reminders_logged_out(self):
        create_user()
        create_reminders()

        new_reminder = {
            'name': 'new',
            'soft_deadline': '2022-03-04',
            'hard_deadline': '2022-03-04',
            'final_deadline': '2022-03-04'
        }
        self.app.post('/create_reminder', data=new_reminder)

        response = self.app.get('/', follows_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertNotIn('2022-03-04', response_text)
