from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db 

# Create the Blueprint for registration-related routes
registration_bp = Blueprint('registration', __name__,)

@registration_bp.route('/registration', methods=['GET', 'POST'])
def register():
    if 'user' not in session:
        return redirect(url_for('login'))

    filter_event_id = None
    entity_id = session['entity_id']
    events = db.get_future_events()
    cattype = 'Event'
    catid = 1
    eventroles = db.get_transaction_code_data(cattype, catid)

    if request.method == 'POST':
        action = request.form.get('action')

        try:
            if action == 'create':
                event_id = request.form.get('event_id')
                member_ids_raw = request.form.get('member_id', '')
                registered = request.form.get('registered')
                eventrole = request.form.get('primary_role')

                # Handle multiple member IDs separated by comma or space
                member_ids = [mid.strip() for mid in member_ids_raw.replace(',', ' ').split() if mid.strip()]
                for member_id in member_ids:
                    db.create_registration(event_id, member_id, registered, eventrole)

            elif action == 'update':
                event_id = request.form.get('event_id')
                member_id = request.form.get('member_id')
                registered = request.form.get('registered')
                eventrole = request.form.get('primary_role')

                # Pass these roles to the update function
                db.update_registration(event_id, member_id, registered, eventrole)
                flash("Record updated successfully!", "success")

            elif action == 'filter':
                filter_event_id = request.form.get('filter_event_id')
                
        except Exception as e:
            flash(f"Error: {str(e)}", "error")

    if filter_event_id:
        registrations = db.get_att_reg_event(filter_event_id, entity_id)
    else:
        registrations = db.get_all_registrations()

    return render_template('registration.html', registrations=registrations, events=events, eventroles=eventroles, user=session['user'])
