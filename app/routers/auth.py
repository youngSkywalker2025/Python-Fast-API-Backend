from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Take the username and password from the form-data body of the request
    # queries the DB, filters the results to find a user whose email matches the email provided in the request
    # if a row in DB has that email, SQLAlchemy creates a Python object of type models.User
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # verify that the passwords are equal 
    # pass in the plain password, then pass in the hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # passwords match-> access granted
    # at this point we would create a token --> when a user logs in we give them a token
    # return token
    access_token = oauth2.create_access_token(data = {"user_id": user.id}) # We are creating a JWT token that encodes the user_id inside it
    # why encode user_id? -> because later in protected routes, we need to know: who is making the request?, which user is this?, what are they allowed to access?
    return {"access_token": access_token, "token_type": "bearer"}
    

