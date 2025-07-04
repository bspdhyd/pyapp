from flask import Blueprint, render_template, request
import pandas as pd

excelread_bp = Blueprint('excelread', __name__)

@excelread_bp.route('/excelread', methods=['GET', 'POST'])
def upload_excel():
    table_data = None
    error = None  # ✅ Important: Initialize error for GET requests too

    if request.method == 'POST':
        file = request.files.get('excel_file')
        if not file:
            error = "No file selected."
        elif not (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            error = "Invalid file format. Please upload an Excel file (.xlsx or .xls)."
        else:
            try:
                df = pd.read_excel(file)
                headers = df.columns.tolist()
                rows = df.values.tolist()
                table_data = {"headers": headers, "rows": rows}
            except Exception as e:
                error = f"Error reading Excel file: {str(e)}"

    return render_template('excelread.html', table_data=table_data, error=error)


