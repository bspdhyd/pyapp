from flask import Blueprint, render_template, request, session, redirect
import qrcode
import io
import base64

qrcode_bp = Blueprint('qrcode', __name__, url_prefix='/qrcode')

@qrcode_bp.route('/', methods=['GET', 'POST'])
def generate_qr():
    if 'user' not in session:
        return redirect('/login')

    qr_code = None

    if request.method == 'POST' and 'register' in request.form:
#        upi_id = request.form['UPIid']
#        upi_id = 'bspd.ma00001116@sib'
        member_id = request.form['Member']
        amount = request.form['Contri']

        upi_url = f"upi://pay?pa={upi_id}&pn={member_id}&am={amount}&cu=INR&mc=6513&tn={member_id}"

        img = qrcode.make(upi_url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template('qrcode.html', qr_code=qr_code)
