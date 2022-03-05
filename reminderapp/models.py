# Create your models here.
from reminderapp.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

# category_reminder_table = db.Table('category_reminder',
#                                    db.Column('category_id', db.Integer,
#                                              db.ForeignKey('category.id')),
#                                    db.Column('reminder_id', db.Integer,
#                                              db.ForeignKey('reminder.id'))
#                                    )

category_reminder_table = db.Table('category_reminder',
                                   db.Column('category_id', db.Integer,
                                             db.ForeignKey('category.id')),
                                   db.Column('reminder_id', db.Integer,
                                             db.ForeignKey('reminder.id'))
                                   )


user_reminder_table = db.Table('user_reminder',
                               db.Column('user_id', db.Integer,
                                         db.ForeignKey('user.id')),
                               db.Column('reminder_id', db.Integer,
                                         db.ForeignKey('reminder.id'))
                               )


class Reminder(db.Model):

    # Reminder ID

    id = db.Column(db.Integer, primary_key=True)

    # Name

    name = db.Column(db.String(80), nullable=False)

    # Deadlines

    soft_deadline = db.Column(db.Date, nullable=False)
    hard_deadline = db.Column(db.Date, nullable=False)
    final_deadline = db.Column(db.Date, nullable=False)

    # category

    # categories = db.relationship(
    #     'Category', secondary='category_reminder', back_populates='reminders')

    categories = db.relationship(
        'Category', secondary='category_reminder', back_populates='reminders')
    users = db.relationship(
        'User', secondary=user_reminder_table, back_populates='current_reminders')
    # user = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)

    def __str__(self):
        return f'<Reminder: {self.name}>'

    def __repr__(self):
        return f'<Reminder: {self.name}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_category = db.Column(db.String(80), nullable=False, unique=True)
    # reminders = db.relationship(
    #     'Reminder', secondary='category_reminder', back_populates='categories')
    reminders = db.relationship(
        'Reminder', secondary='category_reminder', back_populates='categories')

    def __str__(self):
        return f'{self.name_of_category}'

    def __repr__(self):
        return f'{self.name_of_category}'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    current_reminders = db.relationship(
        'Reminder', secondary=user_reminder_table, back_populates='users')
    # friend_list = db.relationship('FriendList', backref='friends')

    def __repr__(self):
        return f'<User: {self.username}>'
