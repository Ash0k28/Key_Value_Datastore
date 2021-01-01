import os
import sys
import json
from datetime import date
import datetime as dt
from Default_Configs import DEFAULT_PATH

#Function to check Time_to_live
def Check_Time_to_live(Created_time):
    Current_time = list(Get_Current_Time().split(':'))
    Created_time = list(str(Created_time).split(':'))
    a = dt.datetime(int(Current_time[0]),int(Current_time[1]),int(Current_time[2]),int(Current_time[3]),int(Current_time[4]),int(Current_time[5]))
    b = dt.datetime(int(Created_time[0]),int(Created_time[1]),int(Created_time[2]),int(Created_time[3]),int(Created_time[4]),int(Created_time[5]))
    return  (a-b).total_seconds()

#Function to delete the data for the specified key
def Delete_Data(Path,Key):
    file=open(Path,'r')
    data=file.read()
    data=list(data.split('-'))
    file.close()
    for i in range(len(data)-1):
       Data_parse=json.loads(data[i])
       if(Data_parse['Key']==Key):
          Time_to_live=Data_parse['Time_to_live']
          Created_time=Data_parse['Created_Time']
          if(Time_to_live != "Unlimited"):
              if(Check_Time_to_live(Created_time)<=int(Time_to_live)):
                  file = open(Path,'w')
                  file.write('')
                  file.close()
                  file = open(Path,"a+")
                  for i in range(len(data)-1):
                      Data_parse = json.loads(data[i])
                      if(Data_parse['Key']!=Key):
                          file.write(data[i])
                          file.write('-')

                  file.close()
                  return json.dumps({"Message":"Key-Value is deleted"})
              else:

                  return json.dumps({"Error":"This Key Value Pair Is Expired"})
          else:
                  file = open(Path,'w')
                  file.write('')
                  file.close()
                  file = open(Path,"a+")
                  for i in range(len(data)-1):
                      Data_parse = json.loads(data[i])
                      if(Data_parse['Key']!=Key):
                          file.write(data[i])
                          file.write('-')
                          file.close()

                  return json.dumps({"Message":"Key-Value is deleted"})
    return json.dumps({"Error":"The specified Key does not exists in the file"})



#Function to view data for specified  Key
def View_Data(Path,Key):

    file=open(Path,'r')
    data=file.read()
    data=list(data.split('-'))
    file.close()
    for i in range(len(data)-1):
       Data_parse=json.loads(data[i])
       if(Data_parse['Key']==Key):
          value = Data_parse['Value']
          Time_to_live=Data_parse['Time_to_live']
          Created_time=Data_parse['Created_Time']
          if(Time_to_live != "Unlimited"):
              if(Check_Time_to_live(Created_time)<=int(Time_to_live)):
                  return json.dumps(value)
              else:
                  return json.dumps({"Error":"This Key Value Pair Is Expired"})
          else:
              return json.dumps(value)
    return json.dumps({"Error":"The specified key is not in the file"})
#Function to check whether the key already exists in the file
def CheckKey(Key,Path):

    file=open(Path,'r')
    data=file.read()
    data=list(data.split('-'))
    for i in range(len(data)-1):
       Data_parse=json.loads(data[i])
       if(Data_parse['Key']==Key):
          file.close()
          return False
    file.close()
    return True

#Function to get the current date and time
def Get_Current_Time():
    today = list(str(date.today()).split('-'))
    now = dt.datetime.now()
    current_time = list(str(now.strftime("%H:%M:%S")).split(":"))

    Final_Time=today+current_time
    Final_Time_Str=''
    for i in range(len(Final_Time)):
        if(i == len(Final_Time)-1):
            Final_Time_Str+=str(Final_Time[i])
        else:
            Final_Time_Str+=str(Final_Time[i])+':'
    return Final_Time_Str

#Function to create a new file
def CreateFile(Path):
        file=open(Path,"x")
        file.close()
        return "Success"

# Create the directory for given path
def CreateFolder(Path):

 try:
    os.mkdir(Path)
    return "Success"
 except OSError as error:
    return error

#Function to Store the data in file
def Store_Data(Path,Key,Value,Time_to_live):
    Current_Time=Get_Current_Time()
    data=json.dumps({'Key':Key,'Value':Value,'Created_Time':Current_Time,'Time_to_live':Time_to_live})
    file=open(Path,'a+')
    file.write(data)
    file.write('-')
    file.close()
    return json.dumps({"Message":"Key-Value data stored sucessfully"})

#Function to validate the input Key-Value Pair
def validate(Path, Key, Value, Time_to_live):

     Dir_path=list(str(Path).split('/'))
     Dir_path_Final=''
     for i in range(len(Dir_path)-1):
         Dir_path_Final+=str(Dir_path[i])+'/'

     if(isinstance(Key,str) and len(Key)<=32):
         Value=json.dumps(Value)
         if(sys.getsizeof(Value)<=16000):

                  if(Time_to_live.isnumeric() or Time_to_live == "Unlimited"):
                    Final_path=Path
                    if(os.path.isdir(Dir_path_Final)==False):
                        if(CreateFolder(Dir_path_Final)!="success"):
                           return json.dumps({"Error":"System cannot find the specified path"})

                    if(str(Dir_path[len(Dir_path)-1]).split('.')[1].lower()!="txt" and str(Dir_path[len(Dir_path)-1]).split('.')[1].lower()!="text"):
                        return json.dumps({"Error":"File should be of type .TEXT or .TXT"})
                    file_exists = os.path.isfile(Final_path)
                    if(file_exists == False):
                        CreateFile(Path)

                    File_size=os.stat(Final_path)
                    File_size=File_size.st_size
                    if(File_size == 0):

                        return "Valid"
                    else:
                        if(File_size+len(Value)< 1000000000 ):
                           if(CheckKey(Key,Path) == True):
                               return "Valid"
                           else:
                               return json.dumps({"Error":"Key already exists in the file"})
                        else:
                            return json.dumps({"Error":"File Size Exceeds 1GB"})
                  else:
                    return json.dumps({"Error":"Time to live is not in integer format"})

         else:
             return json.dumps({"Error":"value's size is greater than 16KB"})
     else:
         return json.dumps({"Error":"Key is not in specified format"})



