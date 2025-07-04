# Common Flask Routines.py
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, send_file
import db
import cfs

cflskrtn_bp = Blueprint('cflskrtn', __name__,)

@cflskrtn_bp.route('/cflskrtn/view/<receipt_id>', methods=['GET', 'POST'])
def view_receipt(receipt_id):
    selected_receipt = db.get_receipt_data(receipt_id)
    notes = db.get_receipt_notes(selected_receipt['Reference_Details'])

    full_text = f"Received from Smt./Shri. {selected_receipt['Full_Name']} ( Member Id {selected_receipt['BSPD_Member_id']} ) a sum of Rs. {selected_receipt['Amount']} ( {selected_receipt['Amount_In_Words']} ) through {selected_receipt['Contribution_Type']} contribution towards {selected_receipt['Event_Description']} ( {selected_receipt['DEShCode']} - {selected_receipt['EVENT_ID']} ) at {selected_receipt['Event_Location']} vide Reference : ( {selected_receipt['Reference_Details']} {notes} ) Dated: {selected_receipt['Contribution_Date']}"

    receipt = {
        "no": selected_receipt["Transaction_Code"],
        "recpt_date": selected_receipt["Receipt_Date"]
    }

    return render_template("generate_receipt.html", receipt=receipt, full_text=full_text)