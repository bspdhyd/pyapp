from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db

contribution_bp = Blueprint('contribution', __name__, url_prefix='/contributions')

@contribution_bp.route('/', methods=['GET', 'POST'])
def manage_contributions():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':
            data = (
                request.form['member_id'],
                request.form['event_id'],
                request.form['amount'],
                request.form['contribution_type'],
                request.form['contribution_date'],
                request.form['reference_details'],
                request.form['receipt_pdf_url']
            )
            db.create_contribution(*data)
            flash("Contribution created successfully", "success")

        elif action == 'update':
            data = (
                request.form['amount'],
                request.form['contribution_type'],
                request.form['reference_details'],
                request.form['approved'],
                request.form['receipt_pdf_url'],
                request.form['member_id'],
                request.form['event_id']
            )
            db.update_contribution(*data)
            flash("Contribution updated successfully", "success")

        elif action == 'delete':
            member_id = request.form['member_id']
            event_id = request.form['event_id']
            db.delete_contribution(member_id, event_id)
            flash("Contribution deleted successfully", "danger")

    search_value = request.form.get('filter_value')
    contributions = db.get_contributions_by_member_or_event(search_value) if search_value else db.get_all_contributions()

    return render_template('contribution.html', contributions=contributions, user=session['user'])
