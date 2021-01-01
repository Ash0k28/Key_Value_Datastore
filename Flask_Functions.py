from flask import Flask,request
import json
from Default_Configs import DEFAULT_PORT
import  Functions as functions

app = Flask(__name__)

#Global List to store the files in use
File_In_Use=[]

#View_Function To Store Data
@app.route('/create_data',methods=['GET','POST'])
def Create_Data():

    Data_Path = request.form['path']
    if(Data_Path not in File_In_Use):
        File_In_Use.append(Data_Path)
    else:
        return json.dumps({"Error":"The specified file is already in use"})
    Data_key =  request.form['key']
    Data_Value = request.form['value']
    Data_Time_to_live = request.form['time_to_live']
    try:
       Data_Value = json.loads(Data_Value)
    except:
        return json.dumps({"Error":"Value is not in JSON  format "})
    Data_Value = dict(Data_Value)
    validate_data=functions.validate(Data_Path,Data_key,Data_Value,Data_Time_to_live)

    if(validate_data == "Valid"):

      Result = functions.Store_Data(Data_Path,Data_key,Data_Value,Data_Time_to_live)
      File_In_Use.remove(Data_Path)
      return Result
    else:
         Result = json.loads(validate_data)
         File_In_Use.remove(Data_Path)
         return Result

#View_Function to View Data
@app.route('/view_data',methods=['GET','POST'])
def View_Data():
    Data_Path = request.form['path']

    if(Data_Path not in File_In_Use):
        File_In_Use.append(Data_Path)
    else:
        return json.dumps({"Error":"The specified file is already in use"})
    Data_key =  request.form['key']
    Result = functions.View_Data(Data_Path,Data_key)

    File_In_Use.remove(Data_Path)
    return json.dumps(Result)

#View_Function to Delete Data
@app.route('/delete_data',methods=['GET','POST'])
def Delete_Data():
    Data_Path = request.form['path']

    if(Data_Path not in File_In_Use):
        File_In_Use.append(Data_Path)
    else:
        return json.dumps({"Error":"The specified file is already in use"})
    Data_key =  request.form['key']
    Result = functions.Delete_Data(Data_Path,Data_key)

    File_In_Use.remove(Data_Path)
    return json.dumps(Result)

if __name__ == '__main__':
    app.run(port = DEFAULT_PORT)
