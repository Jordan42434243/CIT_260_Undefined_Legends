from user import User

class Database:

    def __init__(self, file_name = "database.txt"):
        self.file_name = file_name

        with open(self.file_name, "w") as f:
            f.write("Database\n\n")

    def add_user(self, user):
        with open(self.file_name, "a") as f:
            f.write("Email: " + user.email + " Password: " + user.password + "\n")
        


        
    
        
        
        
    

        

        
    
    


   
