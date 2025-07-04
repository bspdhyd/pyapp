from flask import Blueprint, render_template, request, redirect, url_for, session

van_bp = Blueprint('van', __name__,)

# Bank details (fixed)
BANK_DETAILS = {
    "Name of Account": "BSPD",
    "IFSC Code": "SIBL0000722",
    "Bank": "South India Bank",
    "Branch": "Hyderabad"
}

CONTRIBUTION_CODES = {
    'ChandiHomam': 'CHMA',
    'BikshaVandanam': 'BVMA',
    'General': 'GNMA'
}

@van_bp.route('/van', methods=['GET', 'POST'])
def generate_van():
    van_number = None
    bank_details = None
    member_id = None
    contribution_type = None
    error = None

    if request.method == 'POST':
        member_id = request.form.get('member_id', '').strip()
        contribution_type = request.form.get('contribution_type')
        
        if not member_id:
            error = "Please enter a Member ID."
        elif contribution_type not in CONTRIBUTION_CODES:
            error = "Please select a valid contribution type."
        else:
            member_id_padded = str(member_id).zfill(8)
            van_number = f"A345A11{CONTRIBUTION_CODES[contribution_type]}{member_id_padded}"
            bank_details = BANK_DETAILS

    return render_template('van.html', van_number=van_number, bank_details=bank_details,
                           member_id=member_id, contribution_type=contribution_type, error=error, user=session['user'])
