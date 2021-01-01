import requests
import json
from Default_Configs import DEFAULT_PORT,DEFAULT_PATH
url="http://127.0.0.1:{}/".format(DEFAULT_PORT)

#Class File to pass requests to server
class Key_Value_Datastore:
    def __init__(self):
        return
    def Create_Data(self,key,value,time_to_live="Unlimited",path=DEFAULT_PATH):
        value = json.dumps(value)
        requests.post(url+"create_data",data={"path":path,"key":key,"value":value,"time_to_live":time_to_live})

    def View_Data(self,key,path=DEFAULT_PATH):
        requests.get(url+"view_data",data={"path":path,"key":key})

    def Delete_Data(self,key,path=DEFAULT_PATH):
        requests.get(url+"delete_data",data={"path":path,"key":key})


#Test_Cases

x={ "name":"John", "age":30, "car":227}
key_value_datastore=Key_Value_Datastore()
key_value_datastore.Create_Data(key="abh",value=x,time_to_live=9000,path=DEFAULT_PATH)
key_value_datastore.Create_Data(key="abg",value=x,time_to_live=9000,path=DEFAULT_PATH)
#key_value_datastore.Delete_Data(key="abc",path=DEFAULT_PATH)
#key_value_datastore.View_Data(key="abg",path=DEFAULT_PATH)
#key_value_datastore.Delete_Data(key="abc",path=DEFAULT_PATH)

