# member_reports.py
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, send_file
import db
import cfs

member_reports_bp = Blueprint('member_reports', __name__,)

@member_reports_bp.route('/member_reports', methods=['GET'])
def member_reports_home():
    member_id = request.args.get('member_id', '').strip()
    category = request.args.get('category', '').strip()
    action = request.args.get('action')
    results = []
    error = None

    try:
        if member_id:
            if category == 'contribution':
                results = db.get_contribution_report(member_id, None)
            elif category == 'expenses':
                results = db.get_expenses_report(member_id, None)
            elif category == 'attendance':
                results = db.get_attendance_report(member_id, None)
            elif category == 'recognition':
                results = db.get_recognition_report(member_id, None)
            elif category == 'references':
                results = db.get_references_report(member_id)
            else:
                error = "Select a valid report category."
        elif category:
            error = "Please enter a Member ID to view this report."
    except Exception as e:
        error = str(e)

    if action == 'download':
        if results:
            output = cfs.xls_download (results)

            filename = f"{category}_report_{member_id}.xlsx"

            return send_file(
                output,
                download_name=filename,
                as_attachment=True,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            error = f"No data available to download for Member ID {member_id}."

    return render_template('member_reports.html', member_id=member_id, category=category, results=results, error=error)
