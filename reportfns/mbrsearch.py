# from flask import Blueprint, render_template, request, redirect, url_for, session
# import db
# import cfs

# mbrsearch_bp = Blueprint('mbrsearch', __name__)

# @mbrsearch_bp.route('/mbrsearch', methods=['GET', 'POST'])
# def member_search():
    
#     if 'user' not in session:
#         return redirect(url_for('login'))
        
#     results = []
#     if request.method == 'POST':
#         criteria = request.form.get('search_query')
#         results = db.search_members(criteria)
#         for member in results:
#             member["Phone_Num"] = cfs.mask_num(member["Phone_Num"])
#             member["Email_ID"] = cfs.mask_email(member["Email_ID"])

            
#     return render_template('mbrsearch.html', results=results, user=session['user'])

from flask import Blueprint, render_template, request, redirect, url_for, session
import db
import cfs

mbrsearch_bp = Blueprint('mbrsearch', __name__)

@mbrsearch_bp.route('/mbrsearch', methods=['GET', 'POST'])
def member_search():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    member_id = str(user.get('MEMBER_ID')).strip()
    results = []

    # ---------------------------------------------------
    # Check if user is admin
    # ---------------------------------------------------
    is_admin = False
    access = db.get_access_by_member(member_id)
    print(f"\n[DEBUG] Raw access for member_id={member_id}: {access}")

    # Handle both dict and tuple returns
    if access:
        if isinstance(access, dict):
            # Normalize key names
            for k, v in access.items():
                if str(v).strip().upper() == 'Y' and 'ADMIN' in k.upper():
                    is_admin = True
                    break

        elif isinstance(access, (tuple, list)):
            # Convert all values to uppercase strings and check for 'Y'
            for val in access:
                if str(val).strip().upper() == 'Y':
                    is_admin = True
                    break

    print(f"[DEBUG] is_admin for {member_id} = {is_admin}")

    # ---------------------------------------------------
    # Search members
    # ---------------------------------------------------
    if request.method == 'POST':
        criteria = request.form.get('search_query', '').strip()
        if criteria:
            results = db.search_members(criteria)

            # Mask only for non-admins
            if not is_admin:
                for member in results:
                    member["Phone_Num"] = cfs.mask_num(member.get("Phone_Num", "") or "")
                    member["Email_ID"] = cfs.mask_email(member.get("Email_ID", "") or "")

    return render_template('mbrsearch.html', results=results, user=user)
