from flask import Blueprint, render_template, request, session, flash
import db

podili_admission_bp = Blueprint('podili_admission', __name__, template_folder='templates')

@podili_admission_bp.route('/podili_admission', methods=['GET', 'POST'])
def podili_admission_list():
    current_user_id = None
    if 'user' in session:
        current_user_id = session['user'].get('MEMBER_ID')
    elif 'MEMBER_ID' in session:
        current_user_id = session.get('MEMBER_ID')

    alias = request.args.get('alias', '').strip()
    year_of_birth = request.args.get('year_of_birth', '').strip()
    status = request.args.get('status', '').strip()

    try:
        year_of_birth = int(year_of_birth) if year_of_birth else None
    except ValueError:
        year_of_birth = None

    def filter_by_assigned_memid(admissions):
        if current_user_id is None:
            return []
        return [a for a in admissions if str(a.get('Assigned_MemID')) == str(current_user_id)]

    if request.method == 'POST':
        selected_memid = request.form.get('selected_memid')
        if selected_memid:
            admissions = db.search_college_admissions(alias, year_of_birth, status)
            admissions = filter_by_assigned_memid(admissions)
            selected_admission = next((a for a in admissions if str(a['Student_MemID']) == str(selected_memid)), None)
            return render_template('podili_admission.html', admissions=admissions, selected_admission=selected_admission)

        student_memid = request.form.get('student_memid')
        if student_memid:
            admission_dt = request.form.get('admission_dt') or None
            assignee_notes = request.form.get('assignee_notes', '')
            onboard_status = request.form.get('onboard_status', 'Pending')
            admission_num = request.form.get('admission_num', '')
            updated_by = current_user_id or 'system'

            try:
                db.update_college_admission(student_memid, admission_dt, assignee_notes, onboard_status, admission_num, updated_by)
                flash('Admission updated successfully.', 'success')
            except Exception as e:
                flash(f'Error updating admission: {e}', 'danger')

            admissions = db.search_college_admissions(alias, year_of_birth, status)
            admissions = filter_by_assigned_memid(admissions)
            return render_template('podili_admission.html', admissions=admissions, selected_admission=None)

    # GET request
    admissions = db.search_college_admissions(alias, year_of_birth, status)
    admissions = filter_by_assigned_memid(admissions)
    return render_template('podili_admission.html', admissions=admissions, selected_admission=None)
