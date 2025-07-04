# events.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import db

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET', 'POST'])
def events():
    if 'user' not in session:
        return redirect(url_for('login'))

    events = db.get_events()

    selected_event = None
    if request.method == 'POST':
        selected_event_id = request.form.get('selected_event_id')
        if selected_event_id:
            selected_event = db.get_event_by_id(selected_event_id)

    return render_template('events.html', events=events, selected_event=selected_event, user=session['user'])

@events_bp.route('/create_event', methods=['POST'])
def create_event():
    if 'user' not in session:
        return redirect(url_for('login'))

    event_id = request.form['event_id']
    entity_id = request.form['entity_id']
    event_date = request.form['event_date']
    event_description = request.form['event_description']
    event_loc = request.form['event_loc']
    event_notes = request.form['event_notes']

    db.create_event(event_id, entity_id, event_date, event_description, event_loc, event_notes)
    return redirect(url_for('events.events'))

@events_bp.route('/update_event', methods=['POST'])
def update_event():
    if 'user' not in session:
        return redirect(url_for('login'))

    event_id = request.form['event_id']
    entity_id = request.form['entity_id']
    action = request.form['action']

    if action == 'modify':
        event_date = request.form['event_date']
        event_description = request.form['event_description']
        event_loc = request.form['event_loc']
        event_notes = request.form['event_notes']
        event_status = request.form['event_status']
        
        db.update_event(event_id, entity_id, event_date, event_description, event_loc, event_notes, event_status)

    elif action == 'delete':
        db.delete_event(event_id, entity_id)

    return redirect(url_for('events.events'))
