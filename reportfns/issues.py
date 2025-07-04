# issues.py
from flask import Blueprint, render_template, request
import db

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/issues', methods=['GET', 'POST'])
def view_issues():
    selected_filter = None
    issues = []

    if request.method == 'POST':
        selected_filter = request.form.get('issue_type')

        if selected_filter == 'status':
            issues = db.get_members_with_status_issues()
        elif selected_filter == 'referrer':
            issues = db.get_members_with_referrer_issues()
        elif selected_filter == 'birthyear':
            issues = db.get_members_with_birthyear_issues()
        elif selected_filter == 'surname':
            issues = db.get_members_with_surname_issues()
        elif selected_filter == 'nocontrib':
            issues = db.get_members_with_no_contributions()

    return render_template('issues.html', issues=issues, selected_filter=selected_filter)
