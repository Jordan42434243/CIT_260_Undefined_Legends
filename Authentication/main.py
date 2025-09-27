from database import Database
from user import User
from auth import Auth

def main():
    
    auth = Auth()
    user = User()
    database = Database()

    auth.prompt_account_creation(user, database)



main()