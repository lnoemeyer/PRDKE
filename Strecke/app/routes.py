from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import LoginForm, TrainstationForm, UserForm, SegmentForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Segment
from urllib.parse import urlsplit
from app.models import Station, Address



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home',  posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/trainstation')
@login_required
def trainstation():
    stations = db.session.query(Station, Address).join(Address, Station.address_id == Address.id).all()
    return render_template('trainstation.html', title='Trainstation',stations = stations)

@app.route('/trainsstationNew', methods=['GET', 'POST'])
@login_required
def trainstationNew():
    form = TrainstationForm()
    if form.validate_on_submit():
        address = Address(street=form.street.data, no=form.no.data, zipcode=form.zipcode.data, city=form.city.data,
                          country=form.country.data)
        db.session.add(address)
        db.session.commit()
        trainstation = Station(name=form.name.data, address_id=address.id)
        db.session.add(trainstation)
        db.session.commit()
        flash('Bahnhof angelegt!')
        return redirect(url_for('trainstation'))

    return render_template('trainstationNew.html', title='New Trainstation', form = form)

@app.route('/trainsstationEdit/<station_id>', methods=['GET', 'POST'])
@login_required
def trainstationEdit(station_id):
    station = Station.query.get(station_id)
    address = Address.query.get(station.address_id)
    form = TrainstationForm()
    if form.validate_on_submit():
        address.street = form.street.data
        address.no = form.no.data
        address.zipcode = form.zipcode.data
        address.city = form.city.data
        address.country = form.country.data
        station.name = form.name.data
        db.session.merge(station)
        print(address.city)
        print(form.city.data)
        db.session.commit()  # Commit the changes
        flash('Änderungen gespeichert!')
        return redirect(url_for('trainstation'))
    form = TrainstationForm(obj=station)
    form.street.data = address.street
    form.no.data = address.no
    form.zipcode.data = address.zipcode
    form.city.data = address.city
    form.country.data = address.country
    return render_template('trainstationNew.html', title='Edit Trainstation', form=form)

@app.route('/trainsstationDelete/<station_id>', methods=['GET', 'POST'])
@login_required
def trainstationDelete(station_id):
    deletestation = Station.query.get_or_404(station_id)
    deleteaddress = Address.query.get(deletestation.address_id)
    # if request.method == 'POST':
    db.session.delete(deletestation)
    db.session.delete(deleteaddress)
    db.session.commit()
    return redirect(url_for('trainstation'))

@app.route('/Bahnhof/all')
def all_stations():
    stations = Station.query.all()
    stations_list = []

    for station in stations:
        station_dict = {
            'id': station.id,
            'name': station.name,
            'street': station.street,
            'no': station.no,
            'zipcode': station.zipcode,
            'city': station.city,
            'country': station.country
        }
        stations_list.append(station_dict)

    return jsonify(stations_list)


@app.route('/user')
@login_required
def user():
    users = User.query.all()
    return render_template('user.html', title='User', users=users)

@app.route('/userNew', methods=['GET', 'POST'])
@login_required
def userNew():
    form = UserForm()
    if form.validate_on_submit():
        address = Address(street=form.street.data, no=form.no.data, zipcode=form.zipcode.data, city=form.city.data,
                          country=form.country.data)
        db.session.add(address)
        db.session.commit()
        user = User(username=form.username.data, email=form.email.data, isAdmin=form.is_admin.data, address_id=address.id)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created!')
        return redirect(url_for('user'))
    return render_template('userNew.html', title='New User', form=form)

@app.route('/userEdit/<user_id>', methods=['GET', 'POST'])
@login_required
def userEdit(user_id):
    user = User.query.get(user_id)
    address = Address.query.get(user.address_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.isAdmin = form.is_admin.data
        address.street = form.street.data
        address.no = form.no.data
        address.zipcode = form.zipcode.data
        address.city = form.city.data
        address.country = form.country.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Changes saved!')
        return redirect(url_for('user'))
    form.street.data = address.street
    form.no.data = address.no
    form.zipcode.data = address.zipcode
    form.city.data = address.city
    form.country.data = address.country
    return render_template('userEdit.html', title='Edit User', form=form)
@app.route('/userDelete/<user_id>', methods=['GET', 'POST'])
@login_required
def userDelete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user'))

@app.route('/segment/new', methods=['GET', 'POST'])
@login_required
def segmentNew():
    form = SegmentForm()
    if form.validate_on_submit():
        segment = Segment(startStation=form.startStation.data, endStation=form.endStation.data, trackWidth=form.trackWidth.data, length=form.length.data, maxSpeed=form.maxSpeed.data, price=form.price.data)
        db.session.add(segment)
        db.session.commit()
        flash('New segment has been created!', 'success')
        return redirect(url_for('segments'))
    return render_template('segmentNew.html', title='New Segment', form=form)
@app.route('/segment/<int:segment_id>/edit', methods=['GET', 'POST'])
@login_required
def segmentEdit(segment_id):
    segment = Segment.query.get_or_404(segment_id)
    form = SegmentForm()
    if form.validate_on_submit():
        segment.startStation = form.startStation.data
        segment.endStation = form.endStation.data
        db.session.commit()
        flash('Segment has been updated!', 'success')
        return redirect(url_for('segments'))
    elif request.method == 'GET':
        form.startStation.data = segment.startStation
        form.endStation.data = segment.endStation
    return render_template('edit_segment.html', title='Edit Segment', form=form)

@app.route('/segment/<int:segment_id>/delete', methods=['POST'])
@login_required

def segmentDelete(segment_id):
    segment = Segment.query.get_or_404(segment_id)
    db.session.delete(segment)
    db.session.commit()
    flash('Segment has been deleted!', 'success')
    return redirect(url_for('segments'))

@app.route('/segments')
@login_required
def segments():
    segments = Segment.query.all()
    return render_template('segment.html', title='Segments', segments=segments)
