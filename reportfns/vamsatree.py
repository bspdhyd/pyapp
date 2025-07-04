#vamsatree.py
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
import db


vamsatree_bp = Blueprint('vamsatree', __name__,)

@vamsatree_bp.route('/vamsatree', methods=['GET'])
def family_tree_page():
    member_id = session['user']['MEMBER_ID']
    root = root_id(member_id)
    
    colors = ["aqua", "yellow", "#ff9999", "#90EE90", "#FFD580", "#ff80ff",
              "#ff3377", "#aa80ff", "navy", "olive", "purple", "red", "silver", "teal", "white", "yellow"]
    
    family_tree_data = build_family_tree(root, 0, colors)

    return render_template("vamsatree.html", tree=family_tree_data, name=session['user']['Alias'])


# Find root ancestor
def root_id(member_id):
    row = db.get_member_data(member_id)
    if row:
        if row["Father_ID"] == 0:
            return member_id
        else:
            return root_id(row["Father_ID"])
        flash("Father ID in the system", {member_id})
    else:
        return member_id  # If member data is missing, return the current ID
    
    

# Recursive function to build family tree structure
def build_family_tree(member_id, count, colors):
    row = db.get_member_data(member_id)
    if not row:
        return None

    member_data = {
        "name": row["Alias"],
        "color": colors[count],
        "spouse": None,
        "children": []
    }

    if row["Spouse_ID"]:
        spouse_row = db.get_member_data(row["Spouse_ID"])
        if spouse_row:
            member_data["spouse"] = spouse_row["Alias"]

    children = db.get_all_children(member_id)

    if children:
        count += 1
        for child in children:
            child_data = build_family_tree(child["MEMBER_ID"], count, colors)
            if child_data:
                member_data["children"].append(child_data)

    return member_data
