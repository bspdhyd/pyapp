# Newmember.py
import db
import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash


nwmember_bp = Blueprint('nwmember', __name__)

@nwmember_bp.route('/nwmember', methods=['GET', 'POST'])
def memberlist():
    if 'user' not in session:
        return redirect(url_for('login'))

    members = db.get_lstmembers()
    gotras = db.get_gotras()
    member_data = None

    # FETCH MEMBER DETAILS
    if request.method == 'POST' and 'fetch_btn' in request.form:
        model_id = request.form.get('model_id')
        if model_id:
            member_data = db.get_member_data(model_id)
            if not member_data:
                flash("тЪая╕П Member ID not found.")
            else:
                print("тЬЕ DEBUG - Member Data Fetched:", member_data)
        else:
            flash("Please enter a Model ID to fetch.")

    return render_template('nwmember.html', members = members, gotras = gotras, member_data=member_data, user=session['user'])

@nwmember_bp.route('/create_nwmember', methods=['POST'])
def create_nwmember():
    if 'user' not in session:
        return redirect(url_for('login'))
# Surname, Name, Gender, Year_Of_Birth, Gotram_ID, Email_ID, Phone_Num, Referrer_ID, BloodGroup, Password, Address1, Address2, PIN_or_ZIP, City, State, Country, Created_By, Notes

    surname = request.form['last_name']
    name = request.form['first_name']
    gender = request.form['Gender']
    year_of_birth = request.form['YOB']
    gotram_id = request.form['GotramID']
    email = request.form['email']
    phone_num = request.form['Phone_Num']
    referrer = request.form['Referrer_Id']
    bloodgroup = request.form['Blood_Group']
    notes = request.form['Notes']
    addloc = request.form['Location']
    addline1 = request.form['Address_Line1']
    addline2 = request.form['Address_Line2']
    addcity = request.form['City']
    addstate = request.form['State']
    addpin = request.form['Zip_Code']
    addcntry = request.form['Country']
    
    # -------------------------------
    # EXTRA VALIDATION IN BACKEND
    # -------------------------------

    # Required field checks
    if not surname or not name or not email or not phone_num or not gender or not gotram_id:
        flash("⚠️ Please fill all mandatory fields.")
        return redirect(url_for('nwmember.memberlist'))

    # Phone number validation (8тАУ15 digits)
    if not re.fullmatch(r"[0-9]{8,15}", phone_num):
        flash("⚠️ Phone number must be 8 -15 digits.")
        return redirect(url_for('nwmember.memberlist'))

    # Email validation (simple format check)
    if "@" not in email or "." not in email:
        flash("⚠️ Invalid Email format.")
        return redirect(url_for('nwmember.memberlist'))

    # DUPLICATE CHECK
    alias = db.check_dup_member(surname, gender, year_of_birth, gotram_id, email, phone_num)
   
   
    if alias:
        flash("⚠️ Member already exists.")
    else:
        db.create_member(surname, name, gender, year_of_birth, gotram_id, email, phone_num, referrer, bloodgroup, notes, addloc, addline1, addline2, addcity, addstate, addpin, addcntry)
        flash("✅ Member created successfully!")
        
    return redirect(url_for('nwmember.memberlist'))
    
