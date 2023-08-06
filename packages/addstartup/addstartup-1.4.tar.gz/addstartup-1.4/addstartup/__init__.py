import winreg as reg

def add(name,location):
    loca = str(location).replace("/","\\")
    key = reg.OpenKey(reg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" ,0 , reg.KEY_ALL_ACCESS) # Open The Key
    reg.SetValueEx(key ,name , 0 , reg.REG_SZ ,loca) # Appending Script Address
    reg.CloseKey(key)
