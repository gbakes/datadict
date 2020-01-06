# Database Creation

## from python3 terminal in project directory:

from app import db

db.create_all()

## site.db is created

from app import User, Events

## add user to user table
user_1 = User(username='gbakes', email='gbakes89@gmail.com', password='password')

## add change to session
db.session.add(user_1)

## commit changes to session
db.session.commit()

## Common quering commands

User.query.all()
User.query.first()
User.query.filter_by(username='gbakes').all()
User.query.filter_by(username='gbakes').first()

user = User.query.filter_by(username='gbakes').first()
user.id

user = User.query.get(1)


## creating Events
event_1 = Events(name='Sign In', description='This is a sign in event', user_id=user.id)
event_2 = Events(name='Sign Out', description='This is a sign out event', user_id=user.id)

db.session.add(event_1)
db.session.add(event_2)
db.session.commit()





