from flask import Blueprint, render_template, request, flash
import db
import pandas as pd

sibcollection_report_bp = Blueprint('sibcollection_report', __name__)

@sibcollection_report_bp.route('/sibcollection_report', methods=['GET', 'POST'])
def upload_excel():
    table_data = None
    error = None  
    success = None
    if request.method == 'POST':
        file = request.files.get('excel_file')
        if not file:
            flash ('No file selected.', 'warning')
        elif not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            flash ('Invalid file format. Please upload an Excel file (.xlsx or .xls).', 'danger')
        else:
            try:
                df = pd.read_excel(file)
                df.columns = df.columns.str.strip()
                df = df.fillna('')
                inserted_count = 0
                for _, row in df.iterrows():
                    tranid = str(row.get('TRAN ID', '')).strip()
                    if tranid:
                        db.insert_sib_collection_row(orgname=row.get('ORG.NAME'), slno=row.get('SLNO'), id_value=row.get('ID'), name=row.get('NAME'),
                        tranid=row.get('TRAN ID'), trandate=row.get('TRAN DATE'), tranamt=row.get('TRAN AMT'), source=row.get('SOURCE') )
                        inserted_count += 1
                headers = df.columns.tolist()
                rows = df.values.tolist()
                table_data = {"headers": headers, "rows": rows}
                flash (f'{inserted_count} records inserted into MySQL successfully.', 'success')
            except Exception as e:
                flash (f'Error reading Excel file: {e}', 'danger')

    return render_template('sibcollection_report.html', table_data=table_data, error=error, success=success)
