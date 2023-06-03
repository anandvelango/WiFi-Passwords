import subprocess
import re  

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
    passwords = get_passwords()
    for password in passwords:
        print(password)
        
if __name__ == "__main__":
    return_passwords()