from fastapi import HTTPException,status



class FeedbackNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Feedback not found")
        
class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Invalid username or password")
        
class RatelimitExceeded(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail="Too many requests. Please try again later.")   
        