from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import db

vmt_bp = Blueprint('vmt', __name__)


# ------------------- VIEW PAGE -------------------
@vmt_bp.route('/vmt-details', methods=['GET', 'POST'])
def view_vmt_details():

    # RESET
    if request.args.get("reset") == "1":
        session.pop("last_search", None)
        return render_template("vmt_details.html", members=[])

    # PREVIOUS SEARCH
    if request.method == "GET" and "last_search" in session:
        search_query = session["last_search"]
    else:
        search_query = request.form.get("search", "").strip()

    # NO SEARCH → show logged in user
    if not search_query:
        if "user" not in session:
            flash("Session expired. Please login again.", "danger")
            return redirect(url_for("login"))

        member = db.get_vmt_member_by_id(session["user"]["MEMBER_ID"])
        return render_template("vmt_details.html", members=[member] if member else [])

    session["last_search"] = search_query

    # PROCESS TOKEN LIST
    terms = [t.strip() for t in search_query.replace(",", " ").split() if t.strip()]

    members = db.search_vmt_members(terms)

    return render_template("vmt_details.html", members=members)


# ------------------- SAVE ALL MEMBERS -------------------
@vmt_bp.route('/vmt-details/update-all', methods=['POST'])
def update_all_vmt_members():

    member_ids = request.form.getlist("member_id[]")
    fathers = request.form.getlist("father[]")
    mothers = request.form.getlist("mother[]")
    spouses = request.form.getlist("spouse[]")
    referrers = request.form.getlist("referrer[]")

    for i in range(len(member_ids)):

        db.update_vmt_member(
            member_ids[i],
            fathers[i],
            mothers[i],
            spouses[i],
            referrers[i]
        )

    flash("All members updated successfully!", "success")
    return redirect(url_for("vmt.view_vmt_details"))
