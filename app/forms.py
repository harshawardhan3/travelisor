from pydantic import BaseModel, validator

# Register user model class for validating user input data
class UserModel(BaseModel):
    name:str
    username: str
    email: str
    password: str

    @validator('username')
    def username_check(cls, uname_input):
        if len(uname_input) <= 5:
            raise ValueError("Username must be greater than 5 characters.")
        if len(uname_input) > 15:
            raise ValueError("Username must be less than 15 characters.")

        return uname_input

    @validator('email')
    def email_check(cls, email_input):
        if '@' not in email_input:
            raise ValueError("Email must contain '@'.")
        return email_input


    @validator('password')
    def password_check(cls, pw_input):
        if len(pw_input) <= 6:
            raise ValueError("Password must be greater than 6 characters.")
        if len(pw_input) > 20:
            raise ValueError("Password must be less than 20 characters.")
        return pw_input

# Login user model class for validating user input data
# Don't need to check parameters for login

# class LoginModel(BaseModel):
#     username_email:str
#     password:str

#     @validator('password')
#     def password_check(cls, pw_input):
#         if len(pw_input) <= 6:
#             raise ValueError("Password must be greater than 6 characters.")
#         if len(pw_input) > 20:
#             raise ValueError("Password must be less than 20 characters.")
#         return pw_input
