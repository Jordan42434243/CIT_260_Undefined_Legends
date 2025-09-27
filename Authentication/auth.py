from user import User
from database import Database

class Auth:

    def prompt_account_creation(self, user, database):
        user.email = input("Enter student email (Format: NSHE#@student.csn.edu): ")
        user.password = input("Enter password (Format: 10 digit NSH#E): ")
        self.validate_account(user, database)
    
    def validate_account(self, user, database):
        if not (len(user.password) == 10):
            print("\nError: password must be exactly 10 digits\n")
            self.prompt_account_creation(user, database)

        elif not (user.email[0:10] == user.password):
            print("\nError: NSHE# in email must match password\n")
            self.prompt_account_creation(user, database)

        elif not (user.email[10:len(user.email)] == "@student.csn.edu"):
            print("\nError: Follow format: NSHE#@student.csn.edu\n")
            self.prompt_account_creation(user, database)
        
        else: database.add_user(user)

    
    

        


        

        


        
        

