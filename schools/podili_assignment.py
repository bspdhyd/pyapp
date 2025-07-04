from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
import db  # your db.py with DB helper functions
import cfs

podili_assignment_bp = Blueprint('podili_assignment', __name__, template_folder='templates')

@podili_assignment_bp.route('/podili_assignment')
def show_podili_assignment():
    year_of_birth = request.args.get('year_of_birth', default=None, type=int)
    alias = request.args.get('alias', default=None, type=str)
    assigned_status = request.args.get('assigned_status', default='all', type=str)
    action = request.args.get('action')

    members = db.get_podili_assignment(year_of_birth=year_of_birth, alias=alias, assigned_status=assigned_status)
    
    if action == 'download':
        if members:
            output = cfs.xls_download (members)

            filename = f"{assigned_status}_Podili_assignmentreport.xlsx"

            return send_file(
                output,
                download_name=filename,
                as_attachment=True,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            error = f"No data available to download for Podili data."
    

    return render_template('podili_assignment.html', members=members)

@podili_assignment_bp.route('/podili_assignment/update', methods=['POST'])
def update():
    member_id = request.form.get('member_id')
    notes = request.form.get('notes')
    assigned_memid = request.form.get('assigned_memid')

    if member_id and notes is not None and assigned_memid is not None:
        try:
            db.update_notes_and_assigned(member_id, notes, assigned_memid)
            flash('Notes and Assigned Member ID updated successfully.', 'success')
        except Exception as e:
            flash(f"Error updating: {e}", 'danger')
    else:
        flash('Missing data for update.', 'danger')

    return redirect(url_for('podili_assignment.show_podili_assignment'))
