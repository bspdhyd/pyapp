from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import db
import base64
from PIL import Image
from io import BytesIO


payee_bp = Blueprint('payee', __name__)

@payee_bp.route('/payee', methods=['GET', 'POST'])
def view_payees():
    if request.method == 'POST' and 'search_term' not in request.form:
        try:
            data = {key: request.form.get(key) for key in [
                'Name', 'Govt_ID', 'Govt_ID_Num', 'Purpose', 'Email_ID', 'Phone_Num',
                'Address1', 'Address2', 'City', 'State', 'Country', 'Aadhar_Img_URL', 'MEMBER_ID'
            ]}

            data['MEMBER_ID'] = data['MEMBER_ID'].strip() if data['MEMBER_ID'] else ''
            data['Created_By'] = session['user']['MEMBER_ID']

            # Handle Govt ID Image
            file = None
            if 'Govt_ID_Img' in request.files and request.files['Govt_ID_Img'].filename != '':
                uploaded_file = request.files['Govt_ID_Img']
                img = Image.open(uploaded_file.stream)
                img = img.convert('RGB')  # Ensure JPEG compatibility
                img = img.resize((100, 100))
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                img_io.seek(0)
                file = img_io.getvalue()

            db.insert_payee(data, file)
            flash('Payee created successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('payee.view_payees'))

    search_term = request.args.get('search')
    payees = db.search_payee(search_term) if search_term else db.get_all_payees()

    # Convert Govt_ID_Img BLOBs to base64 for display
    for p in payees:
        if p.get('Govt_ID_Img'):
            p['Govt_ID_Img'] = base64.b64encode(p['Govt_ID_Img']).decode('utf-8')

    return render_template('payee.html', payees=payees)


@payee_bp.route('/payee/update', methods=['POST'])
def update_payee():
    try:
        data = {key: request.form.get(key) for key in [
            'Payee_ID', 'Name', 'Govt_ID', 'Govt_ID_Num', 'Purpose', 'Email_ID',
            'Phone_Num', 'Address1', 'Address2', 'City', 'State', 'Country', 'Aadhar_Img_URL', 'MEMBER_ID'
        ]}

        data['MEMBER_ID'] = data['MEMBER_ID'].strip() if data['MEMBER_ID'] else None
        data['Updated_By'] = session['user']['MEMBER_ID']

        # Handle Govt ID Image update
        file = None
        if 'Govt_ID_Img' in request.files and request.files['Govt_ID_Img'].filename != '':
#            file = request.files['Govt_ID_Img'].read()
                uploaded_file = request.files['Govt_ID_Img']
                img = Image.open(uploaded_file.stream)
                img = img.convert('RGB')  # Ensure JPEG compatibility
                img = img.resize((100, 100))
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                img_io.seek(0)
                file = img_io.getvalue()


        db.update_payee(data, file)
        flash('Payee updated successfully!', 'success')
    except Exception as e:
        flash(f'Update error: {e}', 'danger')
    return redirect(url_for('payee.view_payees'))


@payee_bp.route('/payee/fetch_member', methods=['POST'])
def fetch_member():
    member_id = request.form.get('member_id')
    member = None
    if member_id:
        member = db.get_member_by_id(member_id)
 #       member = db.get_member_data(member_id)
    return jsonify(member or {})
