from dd import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Login Manager needs to know how to get a user from your db


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# Database class for Users


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False,
                         default='default.jpg')
  password = db.Column(db.String(60), nullable=False)
  events = db.relationship('Events', backref='author', lazy=True)
  sources = db.relationship('Sources', backref='author', lazy=True)
  properties = db.relationship('Properties', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}','{self.image_file}')"


# Database Class for Events


sources_events = db.Table("sources_events",
                          db.Column("id", db.Integer, primary_key=True),
                          db.Column("source_id", db.Integer,
                                    db.ForeignKey("sources.id")),
                          db.Column("event_id", db.Integer,
                                    db.ForeignKey("events.id")),
                          db.Column("date_created", db.DateTime,
                                    nullable=False, default=datetime.utcnow),
                          db.Column("is_active", db.Boolean, default=True)
                          )

# Helper table for Sources and Events

events_properties = db.Table("events_properties",
                             db.Column("id", db.Integer, primary_key=True),
                             db.Column("event_id", db.Integer,
                                       db.ForeignKey("events.id")),
                             db.Column("property_id", db.Integer,
                                       db.ForeignKey("properties.id")),
                             db.Column("date_created", db.DateTime,
                                       nullable=False, default=datetime.utcnow),
                             db.Column("is_active", db.Boolean, default=True)
                             )


class Events(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text, nullable=False)
  date_created = db.Column(
      db.DateTime, nullable=False, default=datetime.utcnow)
  is_active = db.Column(db.Boolean, default=True, nullable=False)
  source = db.relationship(
      "Sources", secondary=sources_events, backref=db.backref("events", lazy="dynamic"))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


  def __repr__(self):
    return format(self.title)


class Sources(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  type = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text, nullable=False)
  is_active = db.Column(db.Boolean, default=True, nullable=False)
  date_created = db.Column(
      db.DateTime, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return format(self.title)


class Properties(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  type = db.Column(db.String(100), nullable=False)
  known_values = db.Column(db.String(100), nullable=True)
  min = db.Column(db.String(100), nullable=True)
  max = db.Column(db.String(100), nullable=True)
  description = db.Column(db.Text, nullable=False)
  is_active = db.Column(db.Boolean, default=True, nullable=False)
  date_created = db.Column(
      db.DateTime, nullable=False, default=datetime.utcnow)
  event = db.relationship(
      "Events", secondary=events_properties, backref=db.backref("properties", lazy="dynamic"))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return format(self.title)
