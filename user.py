from db import Database
from tankersdk import Tanker,PassphraseVerification,EmailVerification
from typing import Optional,List
from identity import TankerIdentityManager
from option import EncryptionOptions
import base64,json
import requests

#### source:https://github.com/TankerHQ/identity-python/blob/master/examples/flask/server.py
def load_config():
    current_path = os.getcwd()
    json_path = os.path.join(current_path, "config-app.json")
    with open(json_path) as stream:
        app_config = json.load(stream)
    app.config["TANKER"] = app_config

load_config()
####

APP_ID = app.config["TANKER"]["app_id"]
#The private keys are saved localy in the following path
PATH_TO_WRITE = "/root/Bureau/python-core/"
# identity serveur
SERVEUR_IDENTITY = "http://127.0.0.1:5000/"

class User():

    def __init__(self):
        self.db = Database()
        self.name = ""
        self.tankerAPP = Tanker(APP_ID,writable_path= PATH_TO_WRITE)
        self.identity = ""

    async def connect(self,name,passwd):

        user = requests.get( SERVEUR_IDENTITY + 'get_user_identity?name='+ name + "&passwd=" + passwd)
        user = user.text
        #Authentification failed server side
        if(user == 1):
            print("connetion refused")
        #Start Session
        else:
            self.session = await self.tankerAPP.start(user)
            self.identity = user

        
    async def create_provisory(self,email):

        result = requests.get( SERVEUR_IDENTITY + 'create_provisory_identity?email=' + email) 
        identity  = json.loads(result.text)

        return identity
       
    async def attach_provisional_identity(self,info_user):
        
        status = await self.tankerAPP.attach_provisional_identity(info_user["identity"])
        #one must proof his identity, a code is sent to his email address and pass to this function to verify
        verification = EmailVerification(info_user["email"],info_user["code"])
        await self.tankerAPP.verify_provisional_identity(verification)

    async def create(self,name,passwd):

        identity = requests.get( SERVEUR_IDENTITY + 'create_identity?name='+ name + "&passwd=" + passwd)
        identity = identity.text

        try:
            self.name = name
            self.identity = identity

            #verify identity, this way of doing must not be implemented in production
            await self.tankerAPP.start(identity)
            await self.tankerAPP.generate_verification_key()
            verification = PassphraseVerification("test")
            await self.tankerAPP.register_identity(verification)
            
        except:
            print("error while creating user")
            identity = 0

        return identity

 
    async def crypt(self,message,receiver_name):

        receiver_public_key = requests.get( SERVEUR_IDENTITY  + 'get_public_key?name='+ receiver_name)
        receiver_public_key = receiver_public_key.text
        message_in_bytes = message.encode()

        #define the receiver object 
        authorizedToDecrypt = EncryptionOptions()
        authorizedToDecrypt.add_user_public_key(receiver_public_key) 

        encrypted_data = await self.tankerAPP.encrypt(message_in_bytes,authorizedToDecrypt)

        return encrypted_data
    
    async def decrypt(self,encrypted_data):

        data = await self.tankerAPP.decrypt(encrypted_data)
        return data.decode("utf-8") 
    
    async def disconnect(self):

        await self.tankerAPP.stop()

    async def get_device_id(self):

        device =  await self.tankerAPP.device_id()
        return device

    async def get_list_device_id(self):

        list_device =  await self.tankerAPP.get_device_list()
        return list_device

