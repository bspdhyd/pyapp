from flask import Blueprint, render_template, request, flash, session
import pandas as pd
import db
import cfs

monthly_report_bp = Blueprint('monthly_report', __name__)

def generate_monthly_summary(contributions, expenses):
    # Aggregating Sum1 and Sum2 by Month using standard dictionaries
    sum1_by_month = {}
    sum2_by_month = {}
    
    # Accumulate sums
    for item in contributions:
        month = item["Month"]
        if month in sum1_by_month:
            sum1_by_month[month] += item["Amount"]
        else:
            sum1_by_month[month] = item["Amount"]
    
    for item in expenses:
        month = item["Month"]
        if month in sum2_by_month:
            sum2_by_month[month] += item["Amount"]
        else:
            sum2_by_month[month] = item["Amount"]
    
    # Merge results
    merged_array = []
    total_contributions = total_expenses = total_balance = 0

    for month in sorted(set(sum1_by_month.keys()).union(sum2_by_month.keys())):
        contributions = sum1_by_month.get(month, 0)
        expenses = sum2_by_month.get(month, 0)
        balance = contributions - expenses
        # Accumulate totals
        total_contributions += contributions
        total_expenses += expenses
        total_balance += balance
        
        merged_array.append({
            "Month": month,
            "Contributions": contributions,
            "Expenses": expenses,
            "Balance": balance
        })
        
    merged_array.append({
        "Month": "Total",
        "Contributions": total_contributions,
        "Expenses": total_expenses,
        "Balance": total_balance
    })

    return merged_array

@monthly_report_bp.route('/monthly_report', methods=['GET', 'POST'])
def monthly_report():
    chart_img = None
    error = ""
    start_month = end_month = ""
    merged_array = []
    total_contributions = 0
    total_expenses = 0
    total_balance = 0

    if request.method == 'POST':
        start_month = request.form.get('start_month')
        end_month = request.form.get('end_month')

        if not start_month or not end_month:
             flash("Please select both start and end months.", "warning")
        else:
            try:
                contributions = db.get_contributions_by_month_range(start_month, end_month)
                expenses = db.get_expenses_by_month_range(start_month, end_month)
                df_con = pd.DataFrame(contributions, columns=['Month', 'Type', 'Amount'])
                df_exp = pd.DataFrame(expenses, columns=['Month', 'Type', 'Amount'])

                if df_con.empty and df_exp.empty:
                    flash("No data found for selected months.", "danger")
                else:
                    merged_array = generate_monthly_summary(contributions, expenses)
                        
                    df_con['Source'] = 'Contribution'
                    df_exp['Source'] = 'Expense'
                    df = pd.concat([df_con, df_exp], ignore_index=True)
                    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
                    df.dropna(subset=['Amount', 'Type', 'Month'], inplace=True)

                    chart_img = cfs.plot_double_stacked_bar(df)
            except Exception as e:
                flash(f"Error: {e}", 'danger')

    return render_template('monthly_report.html', chart_img=chart_img, merged_array=merged_array, start_month=start_month, end_month=end_month)

