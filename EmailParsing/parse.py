import win32com.client
import os
import re
import numpy as np

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
#set directory of the emails
directory = r'C:\Users\kddc053\OneDrive - AZCollaboration\Desktop\shiftreports'

#initialize variables for iteration
countShiftReports = 0
valveArray = np.array([])

valveStringIndex = 9

print("Iterating through the files...")
#iterate through the files in the directory
for file in os.listdir(directory):
    f = os.path.join(directory, file)
    #if the object is a valid file
    if os.path.isfile(f):
        try:
            #try to open the file, if the file is in use this will break
            msg = outlook.OpenSharedItem(f)
            #making sure the file has these key words ensure it's a valid shift report
            if msg.Body.find("Facilities SharePoint") > -1:
                    countShiftReports+=1
                    #looking for at least one HV- or skip
                    if msg.Body.find("HV-") > -1:
                        #use regex to find each instance of the HV- and feedback an array of indexes
                        HVindexes = [m.start() for m in re.finditer('HV-', msg.Body)]
                        #iterate through the indexes and add the substring of HV- plus 9 characters
                        for i in HVindexes:
                            #building array of valves
                            valveArray = np.append(valveArray, msg.Body[i:i+valveStringIndex])

                        # print(file, ":\t\t" , len(HVindexes))
        except:
            print("File ", file, " could not be opened. Please close it.")
                    
print("Parsed ", countShiftReports, " shift reports.")
print("Found ", valveArray.size, " mentions of valves.")

#create unique list of valves
uniqueValve = np.unique(valveArray)
#defineing datatype map for the valve counts
dt = np.dtype([('valve', '<U10'), ('count','<i4')])
#create empty array with datatype mapping
uniqueValveCount = np.empty([0,], dtype=dt)

print("There were ", uniqueValve.size, " unique valves.")

#iterate through the uniquevalves
for valve in uniqueValve:
    #append the sub-array of valve and count to the main array
    uniqueValveCount = np.append(uniqueValveCount,np.array([(valve, np.count_nonzero(valveArray == valve))], dt))

#sort the array in place
uniqueValveCount.sort(order='count')
#reverse the order to higher valve count is on top
uniqueValveCount = uniqueValveCount[::-1]

#print the ordred list of valves to the screen
i = 1
for valve in uniqueValveCount:
    print(i, ") ", valve)
    i = i + 1