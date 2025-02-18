"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import app, db
from models import User, Message, Follows

with app.app_context():
  
    db.drop_all()
    db.create_all()

   
    with open('generator/users.csv', 'r') as users_file:
        db.session.bulk_insert_mappings(User, DictReader(users_file))

    
    with open('generator/messages.csv', 'r') as messages_file:
        db.session.bulk_insert_mappings(Message, DictReader(messages_file))

   
    with open('generator/follows.csv', 'r') as follows_file:
        db.session.bulk_insert_mappings(Follows, DictReader(follows_file))

    
    db.session.commit()
