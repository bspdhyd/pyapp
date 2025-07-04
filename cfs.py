# common functions
import secrets
import smtplib
import io, base64
import pandas as pd
import matplotlib.pyplot as plt
from Crypto.Cipher import AES


def mask_num(unmask_num):
    length = len(unmask_num)
    vis_digits = 5 #number of digits to be visible at end
    return unmask_num if length < vis_digits else ('X' *(length - vis_digits) + unmask_num[-vis_digits:])

def mask_email(email):

    username, domain = email.split('@')  # Split the email into username and domain
    username_length = len(username)

    if username_length > 4:
        # Keep the first two and last two characters, masking the middle part
        masked_username = username[:2] + '*' * (username_length - 4) + username[-2:]
    else:
        masked_username = username  # Show the username as is if it's too short

    return masked_username + '@' + domain

def generate_complex_otp(length):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+"
    otp = "".join(secrets.choice(characters) for _ in range(length))
    return otp

def send_email(receiver_email, subject, message):
    sender_email = "service@bspd.in"
    sender_password = "bspd2012"
    smtp_server = "bspd.in"
    smtp_port = 465  # Using implicit TLS
    reply_to = "bspd.hyd@gmail.com"
    try:
        # Construct the email headers and body manually
        email_body = f"Subject: {subject}\nFrom: {sender_email}\nTo: {receiver_email}\nReply-To: {reply_to}\n\n{message}"
        # Use SMTP_SSL instead of SMTP when using port 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # Implicit SSL/TLS
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, email_body)
        server.quit()
        
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def xls_download (data):
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create in-memory output file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')
    output.seek(0)
    return output    
    
def plot_graph(x, y, xlabel, ylabel, title):
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(x)), y, marker='o')
    plt.xticks(range(len(x)), x, rotation=45, ha='right')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')
    
def encrypt_details(value, key):
    ciphering = "AES-128-CTR"
    encryption_iv = b'1234567891011121'  # IV must be in bytes
    encryption_key = key.encode()[:16]  # Ensure it's 128-bit (16 bytes)

    cipher = AES.new(encryption_key, AES.MODE_CTR, nonce=encryption_iv[:8])
    encrypted_value = cipher.encrypt(value.encode())

    return base64.b64encode(encrypted_value).decode()

def decrypt_details(encrypted_value, key):
    ciphering = "AES-128-CTR"
    decryption_iv = b'1234567891011121'  # IV must be in bytes
    decryption_key = key.encode()[:16]  # Ensure it's 128-bit (16 bytes)

    encrypted_value = base64.b64decode(encrypted_value)

    cipher = AES.new(decryption_key, AES.MODE_CTR, nonce=decryption_iv[:8])
    decrypted_value = cipher.decrypt(encrypted_value).decode()

    return decrypted_value
    
def plot_double_stacked_bar(df):

    # Split contributions and expenses
    df_con = df[df['Source'] == 'Contribution']
    df_exp = df[df['Source'] == 'Expense']

    # Pivot both
    con_pivot = df_con.pivot_table(index='Month', columns='Type', values='Amount', aggfunc='sum', fill_value=0)
    exp_pivot = df_exp.pivot_table(index='Month', columns='Type', values='Amount', aggfunc='sum', fill_value=0)

    # Ensure both have the same months
    all_months = sorted(set(con_pivot.index).union(exp_pivot.index))
    con_pivot = con_pivot.reindex(all_months, fill_value=0)
    exp_pivot = exp_pivot.reindex(all_months, fill_value=0)

    fig, ax = plt.subplots(figsize=(14, 6))
    width = 0.15
    x = range(len(all_months))

    # Stack bars for contributions
    bottom = [0] * len(all_months)
    for col in con_pivot.columns:
        ax.bar([i - width/2 for i in x], con_pivot[col], width, bottom=bottom, label=f'Contribution: {col}')
        bottom = [i + j for i, j in zip(bottom, con_pivot[col])]

    # Stack bars for expenses
    bottom = [0] * len(all_months)
    for col in exp_pivot.columns:
        ax.bar([i + width/2 for i in x], exp_pivot[col], width, bottom=bottom, label=f'Expense: {col}')
        bottom = [i + j for i, j in zip(bottom, exp_pivot[col])]

    ax.set_xticks(list(x))
    ax.set_xticklabels(all_months, rotation=45)
    ax.set_ylabel("Amount")
    ax.set_title("Monthly Contributions and Expenses (Stacked)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"