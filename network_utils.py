import subprocess
import requests

def networks():
    """
    Returns the names of all the WiFi connections the device has ever connected to
    """
    # added this bc i had a powercut lol

    # getting meta data of the wifi network
    meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])

    # decoding meta data from byte to string
    data = meta_data.decode('utf-8', errors ="backslashreplace")

    # splitting data by line by line
    # string to list
    data = data.split('\n')

    # creating a list of wifi names
    names:list[str] = []

    # traverse the list 
    for i in data:
        
        # find "All User Profile" in each item
        # as this item will have the wifi name
        if "All User Profile" in i :
            
            # if found split the item
            # in order to get only the name
            i = i.split(":")
            
            # item at index 1 will be the wifi name
            i = i[1]
            
            # formatting the name
            # first and last character is use less
            i = i[1:-1]
            
            # appending the wifi name in the list
            names.append(i)
    return names

def hasConnection():
    """
    Tries to send a get request, if it fails it returns false
    """
    try:
        resp = requests.get("https://google.com")
        return True
    except:
        return False