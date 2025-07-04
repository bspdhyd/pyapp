from flask import Blueprint, render_template, request, redirect, url_for, session
import db
import cfs

mbrsearch_bp = Blueprint('mbrsearch', __name__)

@mbrsearch_bp.route('/mbrsearch', methods=['GET', 'POST'])
def member_search():
    
    if 'user' not in session:
        return redirect(url_for('login'))
        
    results = []
    if request.method == 'POST':
        criteria = request.form.get('search_query')
        results = db.search_members(criteria)
        for member in results:
            member["Phone_Num"] = cfs.mask_num(member["Phone_Num"])
            member["Email_ID"] = cfs.mask_email(member["Email_ID"])

            
    return render_template('mbrsearch.html', results=results, user=session['user'])
