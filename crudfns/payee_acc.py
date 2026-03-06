from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import db
import base64
import subprocess

payee_acc_bp = Blueprint("payee_acc", __name__, template_folder="templates")

@payee_acc_bp.route("/payee_accounts", methods=["GET", "POST"])
def payee_accounts():
    if request.method == "POST" and "Payee_Acnt_Num" in request.form:
        try:
            payee_id = request.form.get("Payee_ID")
            payee_id = int(payee_id) if payee_id and payee_id.isdigit() else 0

            # Read uploaded image
            account_proof_file = request.files.get("Account_Proof_Img")
            account_proof_data = account_proof_file.read() if account_proof_file else None
            
#encrypt account number            
            key = 'PayeeBankAccountNumber'
            result = subprocess.run(['php', 'phpcfs.php', "encrypt", Payee_Acnt_Num, key], capture_output=True, text=True)
            PayeeActNum = eresult.stdout.strip()
#encrypt account number

            data = {key: request.form.get(key) for key in [
                "PayeeActNum", "Name_In_Account", "Nick_Name",
                "Bank_Name", "Branch", "IFSC_CODE", "Passbook_Img_URL",
                "Bank_Registration_Code", "Account_Status", "Key_Notes"
            ]}
            data["Payee_ID"] = payee_id
            data["CreatedBy"] = session.get("user", {}).get("MEMBER_ID", 0)
            data["Account_Proof_Img"] = account_proof_data

            if payee_id > 0 and db.check_payee_account_exists(payee_id):
                db.update_payee_account(data)
                flash("Payee account updated successfully!", "success")
            else:
                db.insert_payee_account(data)
                flash("Payee account created successfully!", "success")

        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for("payee_acc.payee_accounts"))

    search_query = request.args.get("search", "").strip()
    accounts = db.search_payee_accounts(search_query) if search_query else db.get_all_payee_accounts()
#decrypt account number
    key = 'PayeeBankAccountNumber'
    for member in accounts:
        result = subprocess.run(['php', 'phpcfs.php', "decrypt", member["Payee_Acnt_Num"], key], capture_output=True, text=True)
        member["Payee_Acnt_Num"] = result.stdout.strip()
#decrypt account number

    return render_template("payee_acc.html", accounts=accounts, search_query=search_query)


@payee_acc_bp.route("/fetch_payee_name/<int:payee_id>", methods=["GET"])
def fetch_payee_name(payee_id):
    try:
        name = db.get_payee_name_by_id(payee_id)
        if name:
            return jsonify({"success": True, "name": name})
        else:
            return jsonify({"success": False, "error": "Payee not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
