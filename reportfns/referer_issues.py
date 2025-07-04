from flask import Blueprint, render_template, request, session
import db

referer_issues_bp = Blueprint('referer_issues', __name__)

@referer_issues_bp.route('/referer_issues', methods=['GET', 'POST'])
def referer_issues():
    data = []
    error_type = ""
    name = ""

    if request.method == 'POST':
        member_id = request.form.get('Member_id')
        error_type = request.form.get('Search')

        try:
            member = db.get_member_data(member_id)
            if member:
                name = member['Alias']
                if error_type == 'YrBirth':
                    data = db.get_yob_issues(member_id)
                elif error_type == 'Surname':
                    data = db.get_surname_issues(member_id)
                elif error_type == 'AddrIssue':
                    data = db.get_address_issues(member_id)
                elif error_type == 'ParentData':
                    data = db.get_parent_issues(member_id)
                elif error_type == 'DupIssue':
                    data = db.get_duplicate_issues(member_id)
            else:
                name = "Invalid Member"
        except Exception as e:
            name = f"Error occurred: {str(e)}"

    return render_template('referer_issues.html', data=data, error_type=error_type, name=name)

