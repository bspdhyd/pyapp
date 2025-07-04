from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import db

requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/requests', methods=['GET', 'POST'])
def view_requests():
    if request.method == 'POST':
        try:
            category = request.form['category']
            description = request.form['description']
            status = request.form.get('status', 'Open')

            db.insert_request(category, description, status)
            flash("Request created successfully", "success")
        except Exception as e:
            flash("Error creating request: " + str(e), "danger")

    # Handle search filters
    req_member_id = request.args.get('search_member_id', '').strip()
    request_num = request.args.get('search_request_num', '').strip()
    category = request.args.get('search_category', '').strip()
    status = request.args.get('search_status', '').strip()

    requests = db.get_all_requests_filtered(req_member_id, category, status)
    return render_template('requests.html', requests=requests)


@requests_bp.route('/requests/update', methods=['POST'])
def update_request():
    try:
        request_num = request.form['request_num']
        status = request.form['status']
        resolution = request.form['resolution']
        resolver_id = request.form.get('resolver_id') or None
        updated_by = session['user']['MEMBER_ID']  # From session
        now = datetime.now()

        db.update_request(request_num, status, resolution, resolver_id)
        flash("Request updated successfully", "success")
    except Exception as e:
        flash("Error updating request: " + str(e), "danger")

    return redirect(url_for('requests.view_requests'))
