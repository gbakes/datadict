import os
import secrets
from PIL import Image
from datadictionary import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from datadictionary.data import pt, st, et
from datadictionary.models import User, Events, Sources, Properties, sources_events
from datadictionary.forms import RegistrationForm, LoginForm, EventForm, UpdateAccountForm, SourceForm, PropertyForm, available_sources
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.datastructures import MultiDict

# Home Page


@app.route("/")
def home():
    events = Events.query.all()
    sources = Sources.query.all()
    properties = Properties.query.all()
    return render_template('home.html', title="Home", events=events, sources=sources, properties=properties)

# Sources Page


@app.route("/sources")
def sources():
    return render_template('sources.html', title="Sources", st=st)


# Events Page

@app.route("/events")
def events():
    return render_template('events.html', title="Events",  et=et)

# Properties Page


@app.route("/properties")
def prop():
    return render_template('properties.html', title="Properties", pt=pt)


# About Page


@app.route("/about")
def about():
    return render_template('About.html', title="About")

# Register Page


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your Account has been created and you can now Login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

# Login Page


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

# Create a new event


@app.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Events(title=form.title.data,
                       description=form.description.data, author=current_user)
        db.session.add(event)
        db.session.commit()
        flash('Event has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_event.html', title="New Event", form=form, legend='New Event')

# Create a new Source


@app.route("/source/new", methods=['GET', 'POST'])
@login_required
def new_source():
    form = SourceForm()
    if form.validate_on_submit():
        source = Sources(title=form.title.data,
                         description=form.description.data, type=form.type.data, author=current_user)
        db.session.add(source)
        db.session.commit()
        flash('Source has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_source.html', title="New Source", form=form, legend='New Source')


# New property
@app.route("/property/new", methods=['GET', 'POST'])
@login_required
def new_property():
    form = PropertyForm()
    if form.validate_on_submit():
        property = Properties(title=form.title.data,
                              description=form.description.data, type=form.type.data, author=current_user)
        db.session.add(property)
        db.session.commit()
        flash('Property has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_property.html', title="New Property", form=form, legend='New Property')

# Single Event Page


@app.route("/events/<int:event_id>")
def event(event_id):
    event = Events.query.get_or_404(event_id)
    return render_template('event.html', title=event.title, event=event)

# Single Source Page


@app.route("/sources/<int:source_id>")
def source(source_id):
    source = Sources.query.get_or_404(source_id)
    return render_template('source.html', title=source.title, source=source)

# Single Property Page


@app.route("/properties/<int:property_id>")
def property(property_id):
    property = Properties.query.get_or_404(property_id)
    return render_template('property.html', title=property.title, property=property)


@app.route("/events/<int:event_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Events.query.get_or_404(event_id)
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        for i in form.source.data:
            event.source.append(i)
        db.session.commit()
        flash('Your event has been updated', 'success')
        return redirect(url_for('event', event_id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
    return render_template('create_event.html', title="Update ", event=event,  form=form, legend="Update Event")


@app.route("/events/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Events.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Your Event has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/sources/<int:source_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_source(source_id):
    source = Sources.query.get_or_404(source_id)
    form = SourceForm()
    if form.validate_on_submit():
        source.title = form.title.data
        source.description = form.description.data
        source.type = form.type.data
        db.session.commit()
        flash('Your source has been updated', 'success')
        return redirect(url_for('source', source_id=source.id))
    elif request.method == 'GET':
        form.title.data = source.title
        form.type.data = source.type
        form.description.data = source.description
    return render_template('create_source.html', title="Update ", source=source,  form=form, legend="Update Source")


@app.route("/sources/<int:source_id>/delete", methods=['POST'])
@login_required
def delete_source(source_id):
    source = Sources.query.get_or_404(source_id)
    db.session.delete(source)
    db.session.commit()
    flash('Your Source has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/properties/<int:property_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    property = Properties.query.get_or_404(property_id)
    form = PropertyForm()
    if form.validate_on_submit():
        property.title = form.title.data
        property.description = form.description.data
        property.type = form.type.data
        db.session.commit()
        flash('Your source has been updated', 'success')
        return redirect(url_for('property', property_id=property.id))
    elif request.method == 'GET':
        form.title.data = property.title
        form.type.data = property.type
        form.description.data = property.description
    return render_template('create_property.html', title="Update ", property=property,  form=form, legend="Update Property")


@app.route("/properties/<int:property_id>/delete", methods=['POST'])
@login_required
def delete_property(property_id):
    property = Properties.query.get_or_404(property_id)
    db.session.delete(property)
    db.session.commit()
    flash('Your Property has been deleted!', 'success')
    return redirect(url_for('home'))
