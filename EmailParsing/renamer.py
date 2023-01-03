import win32com.client
import os
from datetime import datetime

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
#set directory of the emails
directory = r'C:\Users\kddc053\OneDrive - AZCollaboration\Desktop\shiftreports'

print("Iterating through the files...")
#iterate through the files in the directory
nameList = []
for file in os.listdir(directory):
    f = os.path.join(directory, file)
    #if the object is a valid file
    if os.path.isfile(f):
        #try to open the file, if the file is in use this will break
        msg = outlook.OpenSharedItem(f)
        NewFileName = directory + '\\' + "Shift Report " + datetime.strftime(msg.SentOn,r'%y-%m-%d %H%M%S') + ".msg"
        nameList.append([f,NewFileName])

del outlook

for file in nameList:
    print(file[0], " renamed to ", file[1])
    fromFile = file[0]
    toFile = file[1]
    os.rename(fromFile, toFile)