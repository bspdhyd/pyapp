from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db
import cfs

password_bp = Blueprint('password', __name__)

@password_bp.route('/password_modify', methods=['GET', 'POST'])
def password_modify():
    if 'user' not in session:
        return redirect(url_for('login'))

    member_id = session['user']['MEMBER_ID']

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        re_password = request.form.get('re_password')

        # Check if passwords match
        if new_password != re_password:
            flash("New passwords do not match.", "danger")
            return render_template('password_modify.html')

        # Check if old password is correct
        if not db.get_user_by_credentials(member_id, old_password):
            flash("Old password is incorrect.", "danger")
            return render_template('password_modify.html')

        # Update password
        try:
            db.update_user_password(member_id, new_password)
            flash('Password updated successfully.', 'success')
        except Exception as e:
            flash(f'Error updating Password: Please try again: {e}', 'danger')
        
    return render_template('password_modify.html')

@password_bp.route('/password_reset', methods=['POST'])
def password_reset():
    if 'user' not in session:
        return redirect(url_for('login'))

    member_id = request.form['memberid']
    member = db.get_member_data(member_id)
    otp = cfs.generate_complex_otp(8)
    
    name = member['Alias']
    tomail = member['Email_ID']
    subject = 'Password Reset'
    message = f""" Hello {name}, Your new password is     {otp}       Thank you - BSPD """
            
    cfs.send_email(tomail, subject, message)
    
    try:
        db.update_user_password(member_id, otp)
        flash('New Password sent to email', 'success')
    except Exception as e:
        flash(f'Error resetting Password: Please try again: {e}', 'danger')

    return render_template('password_modify.html')