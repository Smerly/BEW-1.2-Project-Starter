from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError

# Category import

from reminderapp.models import Category, Reminder

# Create your forms here.


class ReminderForm(FlaskForm):
    """ Form to make a new reminder """
    name = StringField('Reminder Name', validators=[
                       DataRequired(), Length(min=1, max=80)])
    # soft_deadline = DateField('Soft Reminder', validators=[
    #     DataRequired()])
    # hard_deadline = DateField('Hoft Reminder', validators=[
    #     DataRequired()])
    # final_deadline = DateField('Final Reminder', validators=[
    #     DataRequired()])

    soft_deadline = DateField('Soft Reminder')
    hard_deadline = DateField('Hard Reminder')
    final_deadline = DateField('Final Reminder')
    categories = QuerySelectMultipleField('Categories',
                                          query_factory=lambda: Category.query)
    submit = SubmitField('Submit')


class FriendForm(FlaskForm):
    code = StringField('Friend Code', validator=[
                       DataRequired(), Length(min=20, max=60)])
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name_of_category = StringField('Name of Category', validators=[
                                   DataRequired(), Length(min=1, max=80)])
    submit = SubmitField('Submit')
