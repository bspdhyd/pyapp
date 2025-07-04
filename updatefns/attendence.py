from flask import Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
import db

attendence_bp = Blueprint('attendence', __name__)

@attendence_bp.route('/attendence', methods=['GET', 'POST'])
def attend():
    if 'user' not in session:
        return redirect(url_for('login'))

    total_attended = 0
    event_id = None
    entity_id = session['entity_id']
    events = db.get_future_events()
    
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        member_id = request.form.get('member_id')
        entity_id = request.form.get('entity_id')
        attended = 'Y'
        registered = 'N'

        if member_id:
            verify_member = db.get_member_data(member_id)
            if verify_member:
                db.create_attendence(event_id, entity_id, member_id, registered, attended)
            else:
                flash(f'Invalid member id {member_id}', 'danger')

        result = db.get_attendcount_event(event_id)
        total_attended = result['total_attended'] if result else 0

    if event_id:
        records = db.get_att_reg_event(event_id, entity_id)
    else:
        records = []

    return render_template('attendence.html', total_attended=total_attended, events=events, event_id=event_id, records=records)


# API endpoint for AJAX to fetch Event Description
@attendence_bp.route('/get_member_name', methods=['POST'])
def get_member_name():
    member_id = request.form.get('member_id')
    member = db.get_member_data(member_id)
    if member:
        return jsonify({'description': member['Alias']})
    return jsonify({'description': ''})
