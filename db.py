import shelve

class Database:
    
    def __init__(self):
        self.users = "users"
        self.public_key_db = "public_keys" 

    def write_object_into_file(self,user):
        #Add user to database
        db = shelve.open(self.users)
        db[user.name] = [user.name,user.passwd,user.identity]
        db.close()
        
        #Add public key to database
        db_public_key = shelve.open(self.public_key_db)
        db_public_key[user.name] = user.public_key
        db_public_key.close()

    def get_user(self,name):

        db = shelve.open(self.users)
        user = db[name]
        db.close()

        return user

    def get_public_key(self,name):

        db = shelve.open(self.public_key_db)
        user_public_key = db[name]
        db.close()

        return user_public_key
