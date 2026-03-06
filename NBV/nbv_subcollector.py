from flask import Blueprint, render_template, session, redirect, url_for, flash
import db
from datetime import datetime
import pandas as pd

nbv_subcollector_bp = Blueprint('nbv_subcollector', __name__)

@nbv_subcollector_bp.route('/nbv_subcollector_dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    member_id = session['user'].get('MEMBER_ID')
    
    # For testing as per user's request
    if str(member_id) == '1116':
         pass_id = 1116
    else:
         pass_id = member_id

    try:
        # Call the stored procedure
        query = "CALL bspdhyd_wp1.NBV_SubCollector_Performance(%s)"
        params = [pass_id]
        results = db.run_fetchall_query(query, params)
        
        if not results:
            flash("No performance data found for your ID.", "info")
            return render_template('nbv_subcollector.html', table_headers=[], table_rows=[], graph_data={})

        # Process data into a DataFrame for pivoting
        data = []
        for r in results:
            # Extract year directly from EVENT_ID by stripping "BVCY" (e.g., "BVCY2024" -> 2024)
            event_id = r['EVENT_ID']
            year_str = event_id.replace('BVCY', '')
            try:
                year = int(year_str)
                data.append({
                    'Sub_Collector': r['Sub_CollectorAlias'],
                    'Year': year,
                    'Count': float(r['EvntTot']) if r['EvntTot'] else 0
                })
            except ValueError:
                # If EVENT_ID doesn't follow the BVCYyyyy format, skip it
                continue

        df = pd.DataFrame(data)
        if df.empty:
            flash("No valid event data found for performance reporting.", "warning")
            return render_template('nbv_subcollector.html', table_headers=[], table_rows=[], graph_data={})

        # Pivot the data: Rows = Sub_Collector, Columns = Year
        pivot_df = df.pivot_table(index='Sub_Collector', columns='Year', values='Count', aggfunc='sum', fill_value=0)
        
        # Sort columns (years) in descending order to have current year first
        years = sorted(pivot_df.columns.tolist(), reverse=True)
        pivot_df = pivot_df[years]
        
        # Prepare table data
        table_headers = ['Sub-Collector'] + [str(y) for y in years]
        table_rows = []
        for index, row in pivot_df.iterrows():
            table_rows.append([index] + row.tolist())

        # Prepare graph data (Performance over the years)
        # We can show total performance per year across ALL sub-collectors
        yearly_totals = df.groupby('Year')['Count'].sum().sort_index()
        graph_data = {
            'labels': [str(y) for y in yearly_totals.index],
            'values': yearly_totals.values.tolist()
        }

        return render_template('nbv_subcollector.html', 
                               table_headers=table_headers, 
                               table_rows=table_rows, 
                               graph_data=graph_data)

    except Exception as e:
        flash(f"Error generating report: {e}", "danger")
        return render_template('nbv_subcollector.html', table_headers=[], table_rows=[], graph_data={})
