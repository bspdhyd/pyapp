from flask import Blueprint, render_template, request, session, send_file
import io
import db
import cfs
import pandas as pd

event_reports_bp = Blueprint('event_reports', __name__)

@event_reports_bp.route('/event_reports/download')
def download_report():
    event_id = request.args.get('event_id', '').strip()
    category = request.args.get('category', '').strip()

    if not event_id or not category:
        return "Event ID and category are required", 400

    try:
        func_map = {
            'contribution': db.get_contribution_report,
            'expenses': db.get_expenses_report,
            'attendance': db.get_attendance_report,
            'recognition': db.get_recognition_report,
            'registration': db.get_registration_report,
        }

        if category not in func_map:
            return "Invalid category", 400

        # Get data from DB
        results = func_map[category](member_id=None,event_id=event_id)

        if not results:
            return "No data found for this report", 404

        # Generate Excel file using cfs.xls_download
        output = cfs.xls_download(results)

        return send_file(
            output,
            as_attachment=True,
            download_name=f"{category}_report_event_{event_id}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        return str(e), 500


@event_reports_bp.route('/event_reports')
def event_reports_home():
    event_id = request.args.get('event_id', '').strip()
    category = request.args.get('category', '').strip()
    results = error = None
    expense_img = contribution_img = None
    total_expense_amount = total_contribution_amount = 0

    user = session.get('user')
    member_id = user['MEMBER_ID'] if user else None

    try:
        if not event_id and category:
            error = "Please enter an Event ID."
        elif event_id:
            if category in ['contribution', 'expenses', 'attendance', 'recognition', 'registration']:
                func_map = {
                    'contribution': db.get_contribution_report,
                    'expenses': db.get_expenses_report,
                    'attendance': db.get_attendance_report,
                    'recognition': db.get_recognition_report,
                    'registration': db.get_registration_report,
                }
                results = func_map[category](member_id=None,event_id=event_id)

            elif category == 'graphs':
                exp = pd.DataFrame(db.get_expenses_by_event(event_id), columns=['Category_ID', 'TotalAmount'])
                con = pd.DataFrame(db.get_contributions_by_event(event_id), columns=['Contribution_Type', 'TotalAmount'])
                exp = exp.groupby('Category_ID')['TotalAmount'].sum().reset_index()
                con = con.groupby('Contribution_Type')['TotalAmount'].sum().reset_index()

                total_expense_amount = exp['TotalAmount'].sum()
                total_contribution_amount = con['TotalAmount'].sum()

                expense_img = cfs.plot_graph(
                    exp['Category_ID'], exp['TotalAmount'],
                    'Category ID', 'Amount', f'Expenses for Event {event_id}'
                )
                contribution_img = cfs.plot_graph(
                    con['Contribution_Type'], con['TotalAmount'],
                    'Contribution Type', 'Amount', f'Contributions for Event {event_id}'
                )
            else:
                error = "Select a valid report category."
    except Exception as e:
        error = str(e)

    return render_template(
        'event_reports.html',
        event_id=event_id,
        category=category,
        results=results or [],
        error=error,
        user=user,
        expense_img=expense_img,
        contribution_img=contribution_img,
        total_expense_amount=total_expense_amount,
        total_contribution_amount=total_contribution_amount
    )
