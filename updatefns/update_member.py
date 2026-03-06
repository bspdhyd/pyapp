from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
import db
from PIL import Image
import base64
from io import BytesIO

update_member_bp = Blueprint('update_member', __name__)

@update_member_bp.route('/update_member', methods=['GET', 'POST'])
def update_member():
    if 'user' not in session:
        return redirect(url_for('login'))

    gotras = db.get_gotras()
    nakshatras = db.get_nakshatras()
    member = None

    if request.method == 'POST':
        mem_id = request.form.get('MEMBER_ID')
        search_id = request.form.get('search_id')
        action = request.form.get('action')
        image = request.files.get('image')
        captured_image_data = request.form.get('captured_image')  # base64 image from webcam


        if mem_id and search_id:
            mem_id = int(mem_id)
            search_id = int(search_id)

            if mem_id != search_id:
                flash("Please retrieve the data before updating.", "warning")
                #return redirect(url_for('update_member.update_member', search_id=search_id))
            else:
            # Editable fields
                first_name=request.form.get('Name')
                last_name = request.form.get('Surname')
                dupindicator = request.form.get('DupIndicator')
                gender=request.form.get('Gender')
                phone_num=request.form.get('PhoneNum')
                gotram_id = request.form.get('GotramID')
                Email_ID = request.form.get('Email_ID')
                Father_id=request.form.get('Father_ID')
                Mother_id=request.form.get('Mother_ID')
                Spouse_id=request.form.get('Spouse_ID')
                Member_Type = request.form.get('Member_Type')
                YOB = request.form.get('YOB')
                nakshatra_id = request.form.get('Nakshatra')
                Pada = request.form.get('Pada')
                notes = request.form.get('Notes')
                address1 = request.form.get('Address_Line1')
                address2 = request.form.get('Address_Line2')
                location = request.form.get('Location')
                city = request.form.get('City')
                state = request.form.get('State')
                zipcode = request.form.get('Zip_Code')
                country = request.form.get('Country')
                status = request.form.get('Status') 
                smarta_purohit = request.form.get('Smarta_Purohit')
                veda_pandit = request.form.get('Veda_Pandit')

                if action == 'update':
                    try:
#                        db.update_member_by_id(mem_id, Member_Type, first_name, gender, phone_num, gotram_id, Father_id, Mother_id, Spouse_id, YOB, nakshatra_id, Pada, Email_ID, notes, address1, address2, location, city, state, zipcode, country)
                        db.update_member_by_id(
                            mem_id, first_name, last_name, gender, dupindicator, phone_num, gotram_id,
                            Father_id, Mother_id, Spouse_id, YOB, nakshatra_id, Pada,
                            Email_ID, notes, address1, address2, location, city, state,
                            zipcode, country, status
                        )
                        db.update_member_privileges(mem_id, smarta_purohit, veda_pandit)
                        # 1. Uploaded Image
                        if image and image.filename != '':
                            try:
                                img = Image.open(image)
                                img = img.convert('RGB')  # Ensure JPEG compatibility
                                img = img.resize((100, 90))

                                img_io = BytesIO()
                                img.save(img_io, format='JPEG')
                                img_io.seek(0)

                                db.upload_member_image(mem_id, img_io.read())
                                flash("Uploaded image resized and saved successfully.", "success")
                            except Exception as e:
                                flash(f"Error processing uploaded image: {e}", "danger")

                        # 2. Captured Image (base64 from webcam)
                        elif captured_image_data:
                            try:
                                header, encoded = captured_image_data.split(",", 1)  # Separate base64 header
                                img_bytes = base64.b64decode(encoded)

                                img = Image.open(BytesIO(img_bytes))
                                img = img.convert('RGB')
                                img = img.resize((100, 90))

                                img_io = BytesIO()
                                img.save(img_io, format='JPEG')
                                img_io.seek(0)

                                db.upload_member_image(mem_id, img_io.read())
                                flash("Captured image resized and saved successfully.", "success")
                            except Exception as e:
                                flash(f"Error processing captured image: {e}", "danger")

                        flash('Member updated successfully.', 'success')

                    except Exception as e:
                        flash(f'Error updating Member: Please try again: {e}', 'danger')                    
        member = db.get_member_data(search_id)
        if member:
            None
        else:
            flash (f'Search Member - {search_id} - does not exist ', 'danger')
            search_id = mem_id
            member = db.get_member_data(search_id)
        privileges = db.get_member_privileges(search_id)
    else:
        search_id = session['user']['MEMBER_ID']
        member = db.get_member_data(int(search_id))
        privileges = db.get_member_privileges(int(search_id))
    
    image_data = []    
    raw_image = db.fetch_member_image(search_id)
    if raw_image:
        image_data = base64.b64encode(raw_image).decode('utf-8')
#        image_data = BytesIO(image_data), mimetype='image/jpeg'
    else:
        flash('No image found for the given Member ID.', 'warning')

    return render_template('update_member.html',
                               member=member,
                               image_data=image_data,
                               gotras=gotras,
                               nakshatras=nakshatras,
                               search_id=search_id,
                               privileges=privileges)