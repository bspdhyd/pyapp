from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash
from io import BytesIO
import base64
import db

images_bp = Blueprint('images', __name__)

@images_bp.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        member_id = request.form['member_id']
        image = request.files['image']
        if image and member_id:
            image_data = image.read()
            success = db.upload_member_image(member_id, image_data)
            if success:
                flash('Image uploaded successfully.', 'success')
            else:
                flash('Failed to upload image.', 'danger')
        return redirect(url_for('images.upload_image'))
    return render_template('images.html', action='upload')

@images_bp.route('/update_image', methods=['GET', 'POST'])
def update_image():
    if request.method == 'POST':
        member_id = request.form['member_id']
        image = request.files['image']
        if image and member_id:
            image_data = image.read()
            success = db.upload_member_image(member_id, image_data)
            if success:
                flash('Image updated successfully.', 'success')
            else:
                flash('Failed to update image.', 'danger')
        return redirect(url_for('images.update_image'))
    return render_template('images.html', action='update')

@images_bp.route('/view_image', methods=['GET', 'POST'])
def view_image():
    image_data = None
    member_id = None
    if request.method == 'POST':
        member_id = request.form['member_id']
        raw_image = db.fetch_member_image(member_id)
        if raw_image:
            image_data = base64.b64encode(raw_image).decode('utf-8')
        else:
            flash('No image found for the given Member ID.', 'warning')
    return render_template('images.html', action='view', image_data=image_data, member_id=member_id)
