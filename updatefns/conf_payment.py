from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import pandas as pd
import db

conf_payment_bp = Blueprint('conf_payment', __name__, url_prefix='/conf_payment')

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@conf_payment_bp.route('/upload', methods=['GET', 'POST'])
def upload_payment_confirmation():
    if 'user' not in session:
        return redirect(url_for('login'))

    table_header = []
    table_data = []

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            try:
                # Read file directly from memory, do not save
                df = pd.read_excel(file, header=None)

                # Update database row by row
                for _, row in df.iterrows():
                    trn_id          = str(row[0]).strip()
                    utr_number      = str(row[1]).strip()
                    confirmation_id = str(row[2]).strip()
                    payment_date    = str(row[3]).strip()

                    db.update_payment_confirmation(
                        trn_id,
                        utr_number,
                        confirmation_id,
                        payment_date
                    )

                flash("Payment confirmation uploaded successfully", "success")

                # Prepare data for preview
                # table_header = ["TRN_ID", "UTR Number", "Payment Confirmation ID", "Payment Date"]
                table_data = df.values.tolist()

            except Exception as e:
                flash(f"Error reading Excel file: {str(e)}", "danger")
                return redirect(request.url)

        else:
            flash("Invalid file type — Only .xls or .xlsx allowed", "danger")
            return redirect(request.url)

    return render_template('conf_payment.html',
                        #   table_header=table_header,
                           table_data=table_data)
