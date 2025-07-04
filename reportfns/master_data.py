from flask import Blueprint, render_template, request
import db
import cfs

master_data_bp = Blueprint('master_data', __name__, template_folder='templates')

@master_data_bp.route('/master_data', methods=['GET', 'POST'])
def master_data():
    vaidika_details = []
    pravara_details = []
    pending_expenses = []
    transaction_code_master = []

    selected_option = request.form.get('master_type', '')

    if request.method == 'POST':
        if selected_option == 'vaidika':
            vaidika_details = db.get_all_vaidika_details()
            for vaidik in vaidika_details:
                vaidik['Phone_Num'] = cfs.mask_num(vaidik['Phone_Num'])
                vaidik['Email_ID'] = cfs.mask_email(vaidik['Email_ID'])
        elif selected_option == 'pravara':
            pravara_details = db.get_all_pravara_gotra()
        elif selected_option == 'pending_expenses':
            pending_expenses = db.get_pending_expenses()
            for exp in pending_expenses:
                if exp['Phone_Num']:
                    exp['Phone_Num'] = cfs.mask_num(exp['Phone_Num'])
        elif selected_option == 'transaction_code_master':
            transaction_code_master = db.get_transaction_code_master()

    return render_template( 'master_data.html', master_type=selected_option, vaidika_details=vaidika_details, pravara_details=pravara_details,
        pending_expenses=pending_expenses, transaction_code_master=transaction_code_master )
