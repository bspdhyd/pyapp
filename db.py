#All database calls
from flask import Flask, session
import mysql.connector
from mysql.connector import Error
from datetime import datetime

def create_connection():
    return mysql.connector.connect(
        host='184.168.115.30',
#        user='devbspd',
#        password='Dev4bspd@2025',
#        database='DevDB'
        user='madhup',
        password='madhup',
        database='bspdhyd_wp1',
    )

def run_fetchall_query(query, params):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def run_fetchone_query(query, params):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result

def run_crud_query(query, params):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
def get_user_by_credentials(member_id, password):
    query = """SELECT MEMBER_ID, MEMBER_TYPE, Alias, Email_ID, Referrer_ID, Phone_Num FROM BSPD_Member 
                      WHERE MEMBER_ID = %s AND Status = 'Active' AND Password = MD5(%s) """
    params = [member_id, password]   
    return run_fetchone_query(query, params)

def get_member_data(member_id):
    query = """SELECT MEMBER_ID, MEMBER_TYPE, Name, Surname, Alias, Email_ID, Year_Of_Birth, Referrer_ID, Father_ID, Mother_ID, Spouse_ID, Phone_Num,
                    Gotram_ID, BloodGroup, Notes, Gender, Nakshatra, Pada, Status, DupIndicator, Address1, Address2, Location, City, State, PIN_or_ZIP, Country
                FROM BSPD_Member WHERE MEMBER_ID = %s """
    params = [member_id]   
    return run_fetchone_query(query, params)

def create_tokens(logid,ipaddress):
    created_on = datetime.now()
    query = "INSERT INTO bspd_tokens ( emp_uid, createdon, token) VALUES (%s, %s, %s)"
    params = [logid, created_on, ipaddress]
    return run_crud_query(query, params)

def get_events():
    query = "SELECT * FROM BSPD_Event ORDER BY Event_date DESC LIMIT 7"
    params = []
    return run_fetchall_query(query, params)
    
def get_future_events():
    query = "SELECT * FROM BSPD_Event where Event_Status = '0' "
    params = []
    return run_fetchall_query(query, params)

def create_event (event_id, entity_id, event_date, event_description, event_loc,event_notes):
    query = "INSERT INTO BSPD_Event (EVENT_ID, DEShCode, Event_date, Event_Description, Event_Location, Event_Notes) VALUES (%s, %s, %s, %s, %s, %s)"
    params = [event_id, entity_id, event_date, event_description, event_loc, event_notes]
    run_crud_query(query, params)
    
def get_event_by_id(event_id):
    query = "SELECT * FROM BSPD_Event WHERE EVENT_ID = %s"
    params = [event_id]
    return run_fetchone_query(query, params)

def update_event(event_id, entity_id, event_date, event_description, event_loc, event_notes, event_status):
    query = """UPDATE BSPD_Event
    SET Event_Description = %s, Event_Location = %s,
        Event_Notes = %s, Event_status = %s, Event_date = %s
    WHERE EVENT_ID = %s AND DEShCode = %s"""
    params = [event_description, event_loc, event_notes, event_status, event_date, event_id, entity_id]
    run_crud_query(query, params)
    
def delete_event(event_id, entity_id):
    query = "DELETE FROM BSPD_Event WHERE EVENT_ID = %s AND DEShCode = %s"
    params = [event_id, entity_id]
    run_crud_query(query, params)
    
def get_att_reg_event(event_id, entity_id):
    query = "Select * from BSPD_Event_Registration  Where EVENT_ID = %s and DEShCode = %s ORDER by UpdatedDate DESC LIMIT 10"
    params = [event_id, entity_id]
    return run_fetchall_query(query, params)
    
def get_attendcount_event(event_id):
    query = """ SELECT COUNT(*) AS total_attended FROM BSPD_Event_Registration
            WHERE EVENT_ID = %s AND Attended = 'Y' """
    params = [event_id]
    return run_fetchone_query(query, params)   
    
def create_attendence(event_id, entity_id, member_id, registered, attended):
    memid = session['user']['MEMBER_ID']
    query = """INSERT INTO BSPD_Event_Registration (EVENT_ID, DEShCode, MEMBER_ID, Registered, Attended, CreatedBy, UpdatedBy)
                VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Attended = %s, UpdatedBy = %s"""
    params = [event_id, entity_id, member_id, registered, attended, memid, memid, attended, memid]
    run_crud_query(query, params)
    
def create_registration(event_id, member_id, registered, eventrole):
    crid = session['user']['MEMBER_ID']
    entity_id = session['entity_id']
    query = """INSERT INTO BSPD_Event_Registration 
        (EVENT_ID, MEMBER_ID, Registered, PrimaryRole, CreatedBy, DEShCode, UpdatedBy)
        VALUES (%s, %s, %s, %s, %s, %s, %s) """
    params = [event_id, member_id, registered, eventrole, crid, entity_id, crid]
    run_crud_query(query, params)
    
def update_registration(event_id, member_id, registered, role):
    updid = session['user']['MEMBER_ID']
    query = """UPDATE BSPD_Event_Registration SET Registered = %s, PrimaryRole = %s, UpdatedBy = %s
        WHERE EVENT_ID = %s AND MEMBER_ID = %s """
    params = [registered, role, updid, event_id, member_id]
    run_crud_query(query, params)
    
def get_all_registrations():
    query = """ SELECT * FROM BSPD_Event_Registration
        ORDER BY UpdatedDate DESC LIMIT 10 """
    params = []
    return run_fetchall_query(query, params)
    
def search_members(criteria):
    search = criteria.strip()
    value = f"%{search}%"
    query = """ SELECT m.MEMBER_ID, m.Surname, m.Alias, m.Year_Of_Birth, m.Email_ID,
                    m.Gotram_ID, g.Gotra, m.Phone_Num, m.DupIndicator
            FROM BSPD_Member m JOIN BSPD_Pravara_Gotra g ON m.Gotram_ID = g.PG_ID
            WHERE m.MEMBER_ID LIKE %s OR m.Phone_Num LIKE %s OR m.Surname LIKE %s 
               OR m.Name LIKE %s OR m.Email_ID LIKE %s OR g.Gotra LIKE %s 
            ORDER BY m.Year_Of_Birth """
    params = [value, value, value, value, value, value]
    return run_fetchall_query(query, params)

def create_expense(event_id, voucher_num, payee_id, amount, amount_details, expense_type):
    query = """ INSERT INTO BSPD_Expenses (EVENT_ID, Voucher_Num, PAYEE_ID, Amount, Amount_Details, Expense_Type, DEShCode)
        VALUES (%s, %s, %s, %s, %s, %s, %s) """
    params = [event_id, voucher_num, payee_id, amount, amount_details, expense_type, 'BHBNR001']
    run_crud_query(query, params)
    
def update_expense(amount, amount_details, expense_type, voucher_num, trn_id):
    query = """ UPDATE BSPD_Expenses
        SET Amount=%s, Amount_Details=%s, Expense_Type=%s, Voucher_Num=%s
        WHERE TRN_ID=%s """
    params = [amount, amount_details, expense_type, voucher_num, trn_id]
    run_crud_query(query, params)
    
def delete_expense(trn_id):
    query = "DELETE FROM BSPD_Expenses WHERE TRN_ID=%s"
    params = [trn_id]
    run_crud_query(query, params)
    
def get_expenses_by_event_id(event_id):
    query = "SELECT * FROM BSPD_Expenses WHERE EVENT_ID = %s ORDER BY TRN_ID DESC"
    params = [event_id]
    return run_fetchall_query(query, params)
    
def get_all_expenses():
    query = "SELECT * FROM BSPD_Expenses ORDER BY TRN_ID DESC LIMIT 5"
    params = []
    return run_fetchall_query(query, params)
    
def create_contribution(member_id, event_id, amount, contribution_type, contribution_date, reference_details, receipt_pdf_url, deshcode='BHBNR001'):
    query = """ INSERT INTO BSPD_Member_Contribution 
                (Member_id, EVENT_ID, Amount, Contribution_Type, Contribution_Date, Reference_Details, Receipt_PDF_URL, DEShCode, Approved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'N') """
    params = [member_id, event_id, amount, contribution_type, contribution_date, reference_details, receipt_pdf_url, deshcode]
    run_crud_query(query, params)
    
def update_contribution(amount, contribution_type, reference_details, approved, receipt_pdf_url, member_id, event_id):
    query = """ UPDATE BSPD_Member_Contribution
        SET Amount=%s, Contribution_Type=%s, Reference_Details=%s, Approved=%s, Receipt_PDF_URL=%s
        WHERE Member_id=%s AND EVENT_ID=%s """
    params = [amount, contribution_type, reference_details, approved, receipt_pdf_url, member_id, event_id]
    run_crud_query(query, params)
    
def get_all_contributions():
    query = "SELECT * FROM BSPD_Member_Contribution ORDER BY Contribution_Date DESC LIMIT 10"
    params = []
    return run_fetchall_query(query, params)
    
def get_contributions_by_member_or_event(search_value):
    query = """ SELECT * FROM BSPD_Member_Contribution
        WHERE Member_id = %s OR EVENT_ID = %s
        ORDER BY Contribution_Date DESC """
    params = [search_value, search_value]
    return run_fetchall_query(query, params)
    
def delete_contribution(member_id, event_id):
    query = """ DELETE FROM BSPD_Member_Contribution
        WHERE Member_id = %s AND EVENT_ID = %s """
    params = [member_id, event_id]
    run_crud_query(query, params)
    
def get_contribution_report(member_id=None, event_id=None):
    query = """ SELECT MEMBER_ID, EVENT_ID, Amount, Contribution_Type, Reference_Details, Transaction_Code
        FROM BSPD_Member_Contribution
        WHERE 1=1 """
    params = []
    if member_id:
        query += " AND MEMBER_ID = %s"
        params.append(member_id)
    if event_id:
        query += " AND EVENT_ID = %s"
        params.append(event_id)
    return run_fetchall_query(query, params)
    
def get_expenses_report(member_id=None, event_id=None):
    query = """ SELECT TRN_ID, EVENT_ID, TRN_DATE, Voucher_Num, Amount, Amount_Details
        FROM BSPD_Expenses
        WHERE 1=1 """
    params = []
    if member_id:
        query += " AND PAYEE_ID = %s"
        params.append(member_id)
    if event_id:
        query += " AND EVENT_ID = %s"
        params.append(event_id)
    return run_fetchall_query(query, params)
    
def get_attendance_report(member_id=None, event_id=None):
    query = """ SELECT EVENT_ID, MEMBER_ID, Registered, Attended
        FROM BSPD_Event_Registration
        WHERE 1=1 """
    params = []
    if member_id:
        query += " AND MEMBER_ID = %s"
        params.append(member_id)
    if event_id:
        query += " AND EVENT_ID = %s"
        params.append(event_id)
    return run_fetchall_query(query, params)
    
def get_recognition_report(member_id=None, event_id=None):
    query = """ SELECT EVENT_ID, BSPD_Member_ID, Sub_Category_ID, Notes
        FROM BSPD_Event_Recognition
        WHERE 1=1 """
    params = []
    if member_id:
        query += " AND BSPD_Member_ID = %s"
        params.append(member_id)
    if event_id:
        query += " AND EVENT_ID = %s"
        params.append(event_id)
    return run_fetchall_query(query, params)
    
def get_references_report(member_id):
    query = """ SELECT MEMBER_ID, Surname, Name, Gender, Year_Of_Birth
        FROM BSPD_Member WHERE Referrer_ID = %s """
    params = [member_id]
    return run_fetchall_query(query, params)

def get_lstmembers():
    query = "SELECT MEMBER_ID, Alias from BSPD_Member order by MEMBER_ID DESC LIMIT 10"
    params = []
    return run_fetchall_query(query, params)

def get_gotras():
    query = "SELECT * from BSPD_Pravara_Gotra where PG_ID > 0 order by Gotra"
    params = []
    return run_fetchall_query(query, params)

def create_member(surname, name, gender, year_of_birth, gotram_id, email, phone_num, referrer, bloodgroup, notes, addloc, addline1, addline2, addcity, addstate, addpin, addcntry):
    memid = session['user']['MEMBER_ID']
    query = """ INSERT INTO BSPD_Member 
        ( Surname, Name, Gender, Year_Of_Birth, Gotram_ID, Email_ID, Phone_Num, Referrer_ID, Location, Address1, Address2, City, State, PIN_or_ZIP, Country, BloodGroup, Password, Created_By, Updated_By, Notes) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, MD5(%s), %s, %s, %s) """
    params = [surname, name, gender, year_of_birth, gotram_id, email, phone_num, referrer, addloc, addline1, addline2, addcity, addstate, addpin, addcntry, bloodgroup, phone_num, memid, memid, notes]
    run_crud_query(query, params)

def check_dup_member(surname, gender, yob, gotramid, email, phonenum):
    query = """SELECT Alias from BSPD_Member 
                where Surname = %s and Gender = %s and Year_Of_Birth = %s and Gotram_ID = %s and Email_ID = %s and Phone_Num = %s """
    params = [surname, gender, yob, gotramid, email, phonenum]
    return run_fetchone_query(query, params)

def get_podili_assignment(year_of_birth=None, alias=None, assigned_status='all'):
    current_year = datetime.now().year
    max_year = current_year - 9
    min_year = current_year - 17

    query = """ SELECT m.MEMBER_ID, m.Alias, m.Surname, m.Year_Of_Birth,m.Phone_Num,
                m.Mother_ID, m.Father_ID, m.Notes, c.Assigned_MemID, CONCAT(a.Name, ' ', a.Surname) AS Assigned_Name
                FROM BSPD_Member m LEFT JOIN BSPD_College_Admission c ON m.MEMBER_ID = c.Student_MemID
                    LEFT JOIN BSPD_Member a ON c.Assigned_MemID = a.MEMBER_ID
                WHERE m.Gender = 'M' AND m.Status = "Active" AND m.Year_Of_Birth BETWEEN %s AND %s """
    params = [min_year, max_year]

    if year_of_birth is not None:
        query += " AND m.Year_Of_Birth = %s"
        params.append(year_of_birth)

    if alias:
        query += " AND (LOWER(m.Alias) LIKE %s OR CAST(m.MEMBER_ID AS CHAR) LIKE %s)"
        alias_param = f"%{alias.lower()}%"
        params.extend([alias_param, alias_param])
    
    if assigned_status == 'pending':
        query += " AND (c.Assigned_MemID IS NULL)"
    elif assigned_status == 'assigned':
        query += " AND (c.Assigned_MemID IS NOT NULL)"

    query += " ORDER BY m.Phone_Num ASC"

    return run_fetchall_query(query, params)


def update_notes_and_assigned(member_id, notes, assigned_memid):
    memid = session['user']['MEMBER_ID']
    # Update Notes in BSPD_Member
    query_notes = " UPDATE BSPD_Member SET Notes = %s WHERE MEMBER_ID = %s "
    params_notes = (notes, member_id)
    run_crud_query(query_notes, params_notes)

    # Insert or update Assigned_MemID in BSPD_College_Admission
    query = """ INSERT INTO BSPD_College_Admission (Student_MemID, Assigned_MemID, Created_By, Updated_By)
        VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE Assigned_MemID = %s, Updated_By = %s """
    params = (member_id, assigned_memid, memid, memid, assigned_memid, memid)
    run_crud_query(query, params)
    

def get_college_admissions():
    query = """ SELECT c.Student_MemID, m.Alias, m.Phone_Num, c.Onboard_Status,
            c.Assigned_MemID, c.Assignee_Notes, c.Admission_Num, c.Admission_Dt
        FROM BSPD_College_Admission c LEFT JOIN BSPD_Member m ON c.Student_MemID = m.MEMBER_ID """
    results = run_fetchall_query(query, params=())
    return results

def update_college_admission(student_memid, admission_dt, assignee_notes, onboard_status, admission_num, updated_by):
    query = """ UPDATE BSPD_College_Admission
        SET Admission_Dt = %s, Assignee_Notes = %s, Onboard_Status = %s,
            Admission_Num = %s, Updated_By = %s
        WHERE Student_MemID = %s """
    updated_dt = datetime.now()
    params = (admission_dt, assignee_notes, onboard_status, admission_num, updated_by, student_memid)
    run_crud_query(query, params)
    
    
def search_college_admissions(alias=None, year_of_birth=None, status=None):
    query = """ SELECT c.Student_MemID, m.Alias, m.Phone_Num, m.Father_ID, m.Mother_ID, c.Onboard_Status, 
            c.Assigned_MemID, c.Assignee_Notes, c.Admission_Num, c.Admission_Dt, m.Year_Of_Birth
        FROM BSPD_College_Admission c LEFT JOIN BSPD_Member m ON c.Student_MemID = m.MEMBER_ID
        WHERE 1=1 """

    params = []
    if alias:
        query += " AND m.Alias LIKE %s"
        params.append(f"%{alias}%")

    if year_of_birth:
        query += " AND m.Year_Of_Birth = %s"
        params.append(year_of_birth)

    if status:
        query += " AND c.Onboard_Status = %s"
        params.append(status)

    results = run_fetchall_query(query, params)
    return results
    
def update_user_password(member_id, new_password):
    query = "UPDATE BSPD_Member SET Password = MD5(%s) WHERE MEMBER_ID = %s"
    params = [new_password, member_id]
    run_crud_query(query, params)

def get_all_children(member_id):
    query = "SELECT MEMBER_ID FROM BSPD_Member WHERE Father_ID = %s OR Mother_ID = %s ORDER BY Year_Of_Birth"
    params = [member_id, member_id]
    return run_fetchall_query(query, params)
    
def get_expenses_by_event(event_id):
    query = """ SELECT Category AS Category_ID, SUM(Amount) AS TotalAmount FROM BSPD_View_Expense_Report
                WHERE EVENT_ID = %s GROUP BY Category ORDER BY Category """
    params = [event_id]
    return run_fetchall_query(query, params)
    
def get_registrations_by_event(event_id):
    query = """ SELECT PrimaryRole AS Role, count(MEMBER_ID) AS TotalRgns FROM BSPD_Event_Registration
                WHERE EVENT_ID = %s and DEShCode = 'BHBNR001' GROUP BY PrimaryRole ORDER BY PrimaryRole """
    params = [event_id]
    return run_fetchall_query(query, params)

def get_contributions_by_event(event_id):
    query = """ SELECT Contribution_Type, SUM(Amount) AS TotalAmount FROM BSPD_View_Contribution_Report
                WHERE EVENT_ID = %s GROUP BY Contribution_Type ORDER BY Contribution_Type """
    params = [event_id]
    return run_fetchall_query(query, params)
    
def get_access_by_member(member_id):
    query = "SELECT * FROM BSPD_Member_Access WHERE Member_ID = %s"
    params = [member_id]
    return run_fetchone_query(query, params)

def update_member_access(member_id, event_value, membercu_value):
    query = """ INSERT INTO BSPD_Member_Access (Member_ID, Event, Member_CU)
                VALUES (%s, %s, %s) ON DUPLICATE KEY
                UPDATE Event = %s, Member_CU = %s """
    params =[member_id, event_value, membercu_value, event_value, membercu_value]
    run_crud_query(query, params)

def get_payee_details(member_id):
    query = "SELECT * FROM BSPD_View_Payee_List where MEMBER_ID = %s"
    params = [member_id]
    return run_fetchone_query(query, params)
    
    
def get_all_payee_details():
    query = """ SELECT Payee_ID, Name, MEMBER_ID, Govt_ID, Govt_ID_Num, Aadhar_Img_URL, Email_ID FROM BSPD_Payee """
    params = []
    return run_fetchall_query(query, params)
    
def get_all_vaidika_details():
    query = "SELECT * FROM BSPD_Vaidika_List WHERE Account_status = %s"
    params = ['Active']
    return run_fetchall_query(query, params)
    
def get_all_pravara_gotra():
    query = "SELECT PG_ID, Gotra, Risheya, Pravara FROM BSPD_Pravara_Gotra"
    params = []
    return run_fetchall_query(query, params)

def get_pending_expenses():
    query = "SELECT * FROM BSPD_View_Pending_Expenses"
    params = []
    return run_fetchall_query(query, params)

def get_transaction_code_master():
    query = """ SELECT Categroy_Type, Category_ID, Category_Desc, Sub_Category_ID, Sub_Category_Desc
                FROM BSPD_Transaction_Code_Master Order by Categroy_Type ASC, Category_ID ASC """
    params = []
    return run_fetchall_query(query, params)
    
def update_member_by_id(member_id, Member_Type, first_name, gender, gotram_id, Father_id, Mother_id, Spouse_id, YOB, nakshatra_id, Pada, Email_ID, notes, address1, address2, location, city, state, zipcode, country):
    
    query = """ UPDATE BSPD_Member SET Name = %s, MEMBER_TYPE = %s, Gender = %s, Gotram_ID = %s, Father_ID = %s, Mother_ID = %s, Spouse_ID = %s, Year_Of_Birth = %s, Nakshatra = %s, Pada = %s, Email_ID = %s, Notes = %s,  Address1 = %s, Address2 = %s, Location = %s, City = %s, State = %s, PIN_or_ZIP = %s, Country = %s WHERE MEMBER_ID = %s """
    params = [ first_name, Member_Type, gender, gotram_id, Father_id, Mother_id, Spouse_id, YOB, nakshatra_id, Pada, Email_ID, notes, address1, address2, location, city, state, zipcode, country, member_id ]
    run_crud_query(query, params)

def get_nakshatras():
    query = "SELECT * from BSPD_Nakshatra where NID > 0 order by All_S_English"
    params = []
    return run_fetchall_query(query, params)

def get_member_privileges(member_id):
    query = """ SELECT Smarta_Purohit, Veda_Pandit FROM BSPD_Member_Privileges
                WHERE MEMBER_ID = %s """
    params = [member_id]
    return run_fetchone_query(query, params)

def update_member_privileges(member_id, smarta_purohit, veda_pandit):
    query = """ UPDATE BSPD_Member_Privileges SET Smarta_Purohit = %s, Veda_Pandit = %s
                WHERE MEMBER_ID = %s """
    params = [smarta_purohit, veda_pandit, member_id]
    run_crud_query(query, params)

def get_all_requests():
    query = "SELECT * FROM BSPD_Request"
    params = []
    return run_fetchall_query(query, params)
    
def insert_request(category, description, status):
    updated_ts = datetime.now()
    updated_by = session['user']['MEMBER_ID']
    query = """ INSERT INTO BSPD_Request (Req_MemberID, Req_Category, Description, Req_Status, Created_Timestamp, Updated_By, Updated_Timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s) """
    params = [updated_by, category, description, status, updated_ts, updated_by, updated_ts]
    run_crud_query(query, params)
    
def update_request(request_num, status, resolution, resolver_id):
    updated_ts = datetime.now()
    updated_by = session['user']['MEMBER_ID']
    query = """ UPDATE BSPD_Request SET Req_Status = %s, Req_Resolution = %s, Req_ResolverID = %s, Updated_By = %s, Updated_Timestamp = %s
                WHERE Request_Num = %s """
    params = [status, resolution, resolver_id, updated_by, updated_ts, request_num]
    run_crud_query(query, params)

def get_all_requests_filtered(req_member_id=None, category=None, status=None):
    query = "SELECT * FROM BSPD_Request WHERE 1=1"
    params = []

    if req_member_id:
        query += " AND Req_MemberID = %s"
        params.append(req_member_id)
    if category:
        query += " AND Req_Category = %s"
        params.append(category)
    if status:
        query += " AND Req_Status = %s"
        params.append(status)

    return run_fetchall_query(query, params)
    
def get_contributions_by_month_range(start_month, end_month):
    query = """ SELECT DATE_FORMAT(Event_date, '%Y-%m') AS Month, Contribution_Type AS Type, SUM(Amount) AS Amount FROM BSPD_View_Contribution_Report
                WHERE DATE_FORMAT(Event_date, '%Y-%m') BETWEEN %s AND %s GROUP BY Month, Type ORDER BY Month """
    params = [start_month, end_month]
    return run_fetchall_query(query, params)

def get_expenses_by_month_range(start_month, end_month):
    query = """ SELECT DATE_FORMAT(TRN_DATE, '%Y-%m') AS Month, Category AS Type, SUM(Amount) AS Amount FROM BSPD_View_Expense_Report
                WHERE DATE_FORMAT(TRN_DATE, '%Y-%m') BETWEEN %s AND %s GROUP BY Month, Type ORDER BY Month """
    params = [start_month, end_month]
    return run_fetchall_query(query, params)
    
def get_members_with_status_issues():
    query = """ SELECT MEMBER_ID, Year_Of_Birth, Surname, Name, Gender, Status, Referrer_ID FROM BSPD_Member 
                WHERE Status IN ('Expired', 'Inactive', 'Not valid') LIMIT 100 """
    params = []
    return run_fetchall_query(query, params)

def get_members_with_referrer_issues():
    query = """ SELECT MEMBER_ID, Surname, Name, Year_Of_Birth, Gender, Status, Referrer_ID FROM BSPD_Member 
                WHERE Referrer_ID = 0 LIMIT 100 """
    params = []
    return run_fetchall_query(query, params)

def get_members_with_birthyear_issues():
    query = """ SELECT MEMBER_ID, Surname, Name, Year_Of_Birth, Gender FROM BSPD_Member 
                WHERE Year_Of_Birth IN (1900, 1980) LIMIT 100 """
    params = []
    return run_fetchall_query(query, params)
    
def get_members_with_surname_issues():
    query = """ SELECT MEMBER_ID, Surname, Name, Gender, Year_Of_Birth FROM BSPD_Member 
                WHERE LENGTH(Surname) < 4 LIMIT 100 """
    params = []
    return run_fetchall_query(query, params)

def get_members_with_no_contributions():
    query = """ SELECT Alias, Year_Of_Birth, Gender FROM BSPD_Member 
                WHERE MEMBER_ID NOT IN (SELECT Member_ID FROM BSPD_View_Contribution_Report) ORDER BY Alias LIMIT 100 """
    params = []
    return run_fetchall_query(query, params)
    
def get_yob_issues(member_id):
    query = """ SELECT Alias, Email_ID, Year_Of_Birth FROM BSPD_Member 
                WHERE Referrer_ID = %s AND Year_Of_Birth IN (1900, 1980) ORDER BY Alias """
    params = [member_id]
    return run_fetchall_query(query, params)

def get_surname_issues(member_id):
    query = """ SELECT Alias, Email_ID, Surname FROM BSPD_Member 
                WHERE Referrer_ID = %s AND LENGTH(Surname) < 4 ORDER BY Alias """
    params = [member_id]
    return run_fetchall_query(query, params)

def get_address_issues(member_id):
    query = """ SELECT Alias, Email_ID, Address1, Address2, Pin_Or_Zip FROM BSPD_Member 
                WHERE Referrer_ID = %s AND Pin_Or_Zip IS NULL ORDER BY Alias """
    params = [member_id]
    return run_fetchall_query(query, params)

def get_parent_issues(member_id):
    query = """ SELECT Alias, Email_ID, Father_ID, Mother_ID, Spouse_ID FROM BSPD_Member 
                WHERE Referrer_ID = %s AND (Father_ID = '0' OR Mother_ID = '0') ORDER BY Alias """
    params = [member_id]
    return run_fetchall_query(query, params)

def get_duplicate_issues(member_id):
    query = """ SELECT MEMBER_ID, Alias, Email_ID, DupIndicator FROM BSPD_Member 
                WHERE Referrer_ID = %s AND DupIndicator > 0 ORDER BY Email_ID """
    params = [member_id]
    return run_fetchall_query(query, params)

def upload_member_image(member_id, image_data):
    query = "UPDATE BSPD_Member SET MemImage = %s WHERE MEMBER_ID = %s"
    params = [image_data, member_id]
    run_crud_query(query, params)
    return True

def fetch_member_image(member_id):
    query = "SELECT MemImage FROM BSPD_Member WHERE MEMBER_ID = %s"
    params = [member_id]
    result = run_fetchone_query(query, params)
    if result and result['MemImage']:
        return result['MemImage']
    return None

def upload_member_image(member_id, image_data):
    query = "UPDATE BSPD_Member SET MemImage = %s WHERE MEMBER_ID = %s"
    params = [image_data, member_id]
    run_crud_query(query, params)
    return True

def get_receipt_data(transaction_code):
    query = """ SELECT Transaction_Code, Full_Name, BSPD_Member_id, Amount, Amount_In_Words, Contribution_Type, Event_Description, EVENT_ID, DEShCode, Event_Location,
                    Reference_Details, DATE_FORMAT(Contribution_Date, '%d-%b-%Y') AS Contribution_Date, DATE_FORMAT(Receipt_Date, '%d-%b-%Y') AS Receipt_Date
                FROM BSPD_View_Contribution_Report WHERE Transaction_Code = %s """
    params = [transaction_code]
    return run_fetchone_query(query, params)

def get_receipt_notes(slno):
    query = "SELECT Notes FROM BSPD_SIB_Collection_Report WHERE SLNO = %s"
    params = [slno]
    result = run_fetchone_query(query, params)
    return result['Notes'] if result else ""

def get_max_dup_indicator():
    query = "SELECT MAX(DupIndicator) AS Counter FROM BSPD_Member"
    params = []
    result = run_fetchone_query(query, params)
    return result['Counter'] if result and result['Counter'] else 0

def update_member_dup(member_id, surname, dup_num):
    new_surname = f"Flag* {surname}"
    query = """ UPDATE BSPD_Member
                SET DupIndicator = %s, Surname = %s
                WHERE MEMBER_ID = %s """
    params = [dup_num, new_surname, member_id]
    return run_crud_query(query, params)

def get_transaction_code_data(cattype, catid):
    query = """ SELECT * FROM BSPD_Transaction_Code_Master 
                WHERE Categroy_Type = %s and Category_ID = %s Order by  Sub_Category_ID ASC """
    params = [cattype, catid]
    return run_fetchall_query(query, params)

def insert_sib_collection_row(orgname, slno, id_value, name, tranid, trandate, tranamt, source):
    query = """ INSERT INTO BSPD_SIB_Collection_Report (ORGNAME, SLNO, ID, NAME, TRANID, TRANDATE, TRANAMT, SOURCE)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
    params = [orgname, slno, id_value, name, tranid, trandate, tranamt, source]
    return run_crud_query(query, params)