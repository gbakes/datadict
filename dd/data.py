from flask_table import Table, Col


class PropertyTable(Table):
    classes = ['table table-striped table-hover']
    title = Col('Name')
    type = Col('Type')
    description = Col('Description')
    #expected = Col('Expected')
    date_created = Col('Date Created')
    #update_date = Col('Update_Date')


# Should probably create a dynamically generated table here to handle all of the tables to be made
class EventsTable(Table):
    classes = ['table table-striped table-hover']
    title = Col('Name')
    source = Col('Sources')
    description = Col('Description')
    properties = Col('Properties')
    date_created = Col('Date Created')


class SourcesTable(Table):
    classes = ['table table-striped table-hover']
    title = Col('Name')
    type = Col('Type')
    #event = Col('Events')
    description = Col('Description')
    date_created = Col('Date Created')
    #update_date = Col('Update_Date')


# Or, more likely, load items from your database with something like
#items = ItemModel.query.all()

# Populate the table
#st = SourcesTable(srcs)
