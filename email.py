import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 函數來發送電子郵件
def send_email(receiver_email, name, unit):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    subject = "填寫表單通知"
    body = f"你好 {name},\n\n您來自 {unit} 的表單已經成功提交。\n\n此致\n敬禮"

    # 建立 MIMEText 物件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # 附加郵件內容
    message.attach(MIMEText(body, "plain"))

    # 使用 smtplib 發送郵件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()
        return "郵件已發送成功！"
    except Exception as e:
        return f"發送郵件時發生錯誤: {e}"

# Streamlit 頁面
st.title("自動發信表單")

with st.form("email_form"):
    code = st.text_input("姓名代號")
    name = st.text_input("名字")
    unit = st.text_input("單位")
    submitted = st.form_submit_button("提交")

    if submitted:
        if code and name and unit:
            receiver_email = f"u{code}@taipower.com.tw"
            result = send_email(receiver_email, name, unit)
            st.success(result)
        else:
            st.error("請填寫所有欄位。")
