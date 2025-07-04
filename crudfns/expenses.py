from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/', methods=['GET', 'POST'])
def manage_expenses():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')
        trn_id = request.form.get('trn_id')

        if action == 'create':
            data = (
                request.form.get('event_id'),
                request.form.get('voucher_num'),
                request.form.get('payee_id'),
                request.form.get('amount'),
                request.form.get('amount_details'),
                request.form.get('expense_type')
            )
            db.create_expense(*data)
            flash('Expense created successfully!', 'success')

        elif action == 'update':
            data = (
                request.form.get('amount'),
                request.form.get('amount_details'),
                request.form.get('expense_type'),
                request.form.get('voucher_num'),
                trn_id
            )
            db.update_expense(*data)
            flash('Expense updated successfully!', 'success')

        elif action == 'delete':
            db.delete_expense(trn_id)
            flash('Expense deleted successfully!', 'success')

    # Handling search functionality
    search_value = request.form.get('filter_event_member')  # Can be either Event ID or Member ID

    if search_value:
        expenses = db.get_expenses_by_event_or_member_id(search_value)
    else:
        expenses = db.get_all_expenses()

    return render_template('expenses.html', expenses=expenses, user=session['user'])
