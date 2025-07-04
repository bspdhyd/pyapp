from flask import Blueprint, render_template, request, flash
import db
import cfs

multiple_data_bp = Blueprint('multiple_data', __name__, template_folder='templates')

@multiple_data_bp.route('/multiple_data', methods=['GET', 'POST'])
def multiple_data():
    mem_group, recognition_grouped, contribution_grouped, merged_data = {}, {}, {}, {}

    if request.method == 'POST':
        raw_ids = request.form.get('member_ids', '')
        
        try:
            member_ids = [int(mid) for mid in raw_ids.split(',') if mid.strip().isdigit()]
        except ValueError:
            member_ids = []
        
        if not member_ids:
            flash("Please enter at least one valid Member ID.", "warning")
        else:
            for mid in member_ids:
                if member_data:= db.get_member_data(mid):
                    member_data['Phone_Num'] = cfs.mask_num(member_data['Phone_Num'])
                    member_data['Email_ID'] = cfs.mask_email(member_data['Email_ID'])
                    mem_group[mid] = member_data

                if recog := db.get_recognition_report(mid, None):
                    recognition_grouped[mid] = recog
                if contrib := db.get_contribution_report(mid, None):
                    contribution_grouped[mid] = contrib
                merged_data = {}
                for mid in set(mem_group.keys()).union(recognition_grouped.keys()).union(contribution_grouped.keys()):
                    merged_data[mid] = {
                    "member": mem_group.get(mid,[]),
                    "recognition": recognition_grouped.get(mid, []),
                    "contribution": contribution_grouped.get(mid, []) }

    return render_template('multiple_data.html', merged_data=merged_data)
