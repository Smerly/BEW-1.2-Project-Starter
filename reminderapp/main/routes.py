import datetime
from reminderapp.extensions import db
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from reminderapp.main.forms import ReminderForm, FriendForm, CategoryForm
from reminderapp.models import User, Reminder, Category
from reminderapp.main.tasks import send_sms_reminder
main = Blueprint('main', __name__)

# Tasks


# Create your routes here.


@main.route('/')
def homepage():
    all_reminders = Reminder.query.all()
    all_users = User.query.all()
    all_categories = Category.query.all()
    return render_template('home.html', all_reminders=all_reminders, all_users=all_users, all_categories=all_categories)


@main.route('/create_reminder', methods=['GET', 'POST'])
@login_required
def create_reminder():
    form = ReminderForm()
    if form.validate_on_submit():
        new_reminder = Reminder(
            name=form.name.data,
            soft_deadline=form.soft_deadline.data,
            hard_deadline=form.hard_deadline.data,
            final_deadline=form.final_deadline.data,
            categories=form.categories.data,
        )
        db.session.add(new_reminder)
        db.session.commit()
        reminder_text = 'Its time'
        print('executing task')
        send_sms_reminder.apply_async(
            ('5108133250', reminder_text), eta=datetime.datetime.now())
        flash('Created new reminder.')
        return redirect(url_for('main.homepage', reminder_id=new_reminder.id))
    return render_template('create_reminder.html', form=form)


@main.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(
            name_of_category=form.name_of_category.data,
        )
        db.session.add(new_category)
        db.session.commit()

        flash('New category has been added')
        return redirect(url_for('main.homepage'))
    return render_template('create_category.html', form=form)
# name = db.Column(db.String(80), nullable=False)

# users = db.relationship('User', back_populates='current_reminders')


@main.route('/fulfill_reminder/<reminder_id>', methods=['POST'])
def fulfull(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    db.session.delete(reminder)
    db.session.commit()
    flash('Reminder has been fulfilled')
    return redirect(url_for('main.homepage'))


# @main.route('/alert_user/<reminder_id>', methods=['POST'])
# def alert_user(reminder_id):
#     reminder = Reminder.query.get(reminder_id)
#     datetime_object = str(datetime.date.today())
#     now = datetime_object[:10]
#     reminder_text = 'Its time'
#     reminder.status = True
#     db.session.commit()
#     flash('Reminder status changed')
#     return redirect(url_for('main.homepage'))


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)
