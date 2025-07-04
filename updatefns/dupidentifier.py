from flask import Blueprint, render_template, request, flash
import db
import cfs

dupidentifier_bp = Blueprint('dupidentifier', __name__)

@dupidentifier_bp.route('/dupidentifier', methods=['GET', 'POST'])
def dupidentifier():
    data = []
    criteria = ""

    if request.method == 'POST':
        criteria = request.form.get("Criteria")

        if 'Update' in request.form:
            dup_counter = db.get_max_dup_indicator()
            selected = request.form.getlist('DupInd')

            if selected:
                for item in selected:
                    parts = item.split("-")
                    if len(parts) == 3:
                        mem_id, surname, current_dup = parts
                        if current_dup == "0":
                            dup_counter += 1
                            db.update_member_dup(mem_id, surname, dup_counter)
                flash ("Duplicate indicators updated successfully!", "success")
            else:
                flash ("No members selected for update", "warning")

        data = db.search_members(criteria)
        for member in data:
            member["Phone_Num"] = cfs.mask_num(member["Phone_Num"])
            member["Email_ID"] = cfs.mask_email(member["Email_ID"])

    return render_template("dupidentifier.html", data=data, criteria=criteria)
