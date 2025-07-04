from flask import Blueprint, render_template, request, session
import db
import cfs
import pandas as pd

event_reports_bp = Blueprint('event_reports', __name__)

@event_reports_bp.route('/event_reports')
def event_reports_home():
    event_id = request.args.get('event_id', '').strip()
    category = request.args.get('category', '').strip()
    results = error = None
    expense_img = contribution_img = registration_img = None
    total_expense_amount = total_contribution_amount = total_registration_count = 0

    try:
        if not event_id and category:
            error = "Please enter an Event ID."
        elif event_id:
            if category in ['contribution', 'expenses', 'attendance', 'recognition']:
                func_map = {
                    'contribution': db.get_contribution_report,
                    'expenses': db.get_expenses_report,
                    'attendance': db.get_attendance_report,
                    'recognition': db.get_recognition_report,
                }
                results = func_map[category](None, event_id)
            elif category == 'graphs':
                exp = pd.DataFrame(db.get_expenses_by_event(event_id), columns=['Category_ID', 'TotalAmount'])
                con = pd.DataFrame(db.get_contributions_by_event(event_id), columns=['Contribution_Type', 'TotalAmount'])
                reg = pd.DataFrame(db.get_registrations_by_event(event_id), columns=['Role', 'TotalRgns'])
                exp = exp.groupby('Category_ID')['TotalAmount'].sum().reset_index()
                con = con.groupby('Contribution_Type')['TotalAmount'].sum().reset_index()
                reg = reg.groupby('Role')['TotalRgns'].sum().reset_index()

                total_expense_amount = exp['TotalAmount'].sum()
                total_contribution_amount = con['TotalAmount'].sum()
                total_registration_count = reg['TotalRgns'].sum()

                expense_img = cfs.plot_graph(exp['Category_ID'], exp['TotalAmount'], 'Category ID', 'Amount', f'Expenses for Event {event_id}')
                contribution_img = cfs.plot_graph(con['Contribution_Type'], con['TotalAmount'], 'Contribution Type', 'Amount', f'Contributions for Event {event_id}')
                registration_img = cfs.plot_graph(reg['Role'], reg['TotalRgns'], 'Role', 'Rgns', f'Registrations for Event {event_id}')
            else:
                error = "Select a valid report category."
    except Exception as e:
        error = str(e)

    return render_template('event_reports.html',
                           event_id=event_id,
                           category=category,
                           results=results or [],
                           error=error,
                           user=session.get('user'),
                           expense_img=expense_img,
                           contribution_img=contribution_img,
                           registration_img=registration_img,
                           total_expense_amount=total_expense_amount,
                           total_contribution_amount=total_contribution_amount,
                           total_registration_count=total_registration_count)
