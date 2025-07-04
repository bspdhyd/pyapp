# Newmember.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import db

nwmember_bp = Blueprint('nwmember', __name__)

@nwmember_bp.route('/nwmember', methods=['GET', 'POST'])
def memberlist():
    if 'user' not in session:
        return redirect(url_for('login'))

    members = db.get_lstmembers()
    gotras = db.get_gotras()

    return render_template('nwmember.html', members = members, gotras = gotras, user=session['user'])

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
    
    alias = db.check_dup_member(surname, gender, year_of_birth, gotram_id, email, phone_num)
    if alias:
        error = "Member already exists"
    else:
        db.create_member(surname, name, gender, year_of_birth, gotram_id, email, phone_num, referrer, bloodgroup, notes, addloc, addline1, addline2, addcity, addstate, addpin, addcntry)
    
    return redirect(url_for('nwmember.memberlist'))
    
