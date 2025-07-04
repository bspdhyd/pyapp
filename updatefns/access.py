from flask import Blueprint, render_template, request, flash, session
import db

access_bp = Blueprint('access', __name__)

@access_bp.route('/access', methods=['GET', 'POST'])
def access():
    results = []
    search_member_id = session['user']['MEMBER_ID']
    results = session['access']

    memdata = db.get_member_data(search_member_id)
    alias = memdata['Alias']

    if request.method == 'POST':
        search_member_id = request.form.get('member_id', '').strip()
        action = request.form.get('action')
        results = []
        if not search_member_id:
            flash("Please enter a Member ID.", "warning")
        else:
            try:
                if action == "search":
                    results = db.get_access_by_member(search_member_id)
                    if not results:
                        flash("No access records found for this Member ID.", "info")
                        results = {
                            'Member_ID': search_member_id,
                            'Event': 'N',
                            'Member_CU': 'N'}

                elif action == "update":
                    membercu_value = request.form.get('membercu_access', '').strip().upper()
                    event_value = request.form.get('event_access', '').strip().upper()
                    db.update_member_access(search_member_id, event_value, membercu_value)
                    flash("Access updated successfully.", "success")
                    results = db.get_access_by_member(search_member_id)
            except Exception as e:
                flash(f"Error occurred: {e}", "danger")

            memdata = db.get_member_data(search_member_id)
            alias = memdata['Alias']

    try:
        return render_template('access.html', results=results or [], alias=alias, member_id=search_member_id)
    except Exception as e:
        return f"Error rendering page: {e}"

#    return render_template('access.html', row=results or [], alias=alias, member_id=search_member_id)
