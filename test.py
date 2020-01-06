from dd import *
from dd.models import Sources, Events, Properties, sources_events, events_properties
from prettytable import PrettyTable
from dd.data import EventsTable

"""
x = db.session.query(Sources).join(sources_events).filter_by(event_id=1)
y = Sources.query.filter(Sources.events).all()

for i in y:
    if i not in x:
        print(i)

"""
events = Events.query.all()
events2= Events.query.outerjoin(events_properties).outerjoin(Properties)

#userList = users.query.join(friendships, users.id == friendships.user_id).add_columns(users.userId, users.name, users.email, friends.userId, friendId)

#prop = Properties.query.join(Events,  Properties.event == Events.id).add_columns(Properties.id,Properties.title,Properties.event,Events.id,Events.title)
"""
events = "SELECT e.title,  GROUP_CONCAT(DISTINCT s.title) as source, e.description,GROUP_CONCAT(DISTINCT p.title) as property FROM events e LEFT JOIN events_properties ep ON(ep.event_id=e.id) LEFT JOIN properties p ON(p.id=ep.property_id) LEFT JOIN sources_events se ON(se.event_id=e.id) LEFT JOIN sources s ON(s.id=se.source_id) GROUP BY e.id"
ev = db.engine.execute(events)
type(ev)
print(ev)
"""

#et = EventsTable(ev)

"""
#x = db.session.execute(sql)

t = PrettyTable(x)
print(t)

"""
src = Properties.query.all()

for i in  src:
    print(i.event)
