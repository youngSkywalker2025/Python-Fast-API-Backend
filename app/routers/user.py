from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # What is UserCreate? -> Pydantic model used to validate incoming data
    # When a request comes in, FastAPI takes the JSON you send and FastAPI turns it into a Python object of type UserCreate
    # user.email contains the email, user.password contains the password
    # "FastAPI" please validate the incoming JSON using the UserCreate Model, and give me a python object called user that contains the validated data
    
    # hash the password from the request body
    hashed_password = utils.hash(user.password)

    # turn the pydantic model into a dict
    user_dict = user.dict()
    # replace the raw password with the hashed one
    user_dict["password"] = hashed_password
    # use that dict to create a SQLAlchemy User object
    new_user = models.User(**user_dict)
    # converts the Pydantic model (user) into a dictionary
    # use that dictionary to create a new SQLAlchemy User object
    # the dictionary looks really similar to the JSON -> yes thats correct
    # well instead of converting it into a pydantic model why cant we just directly take the JSON and convert it into a dictionary?
    # Ultimately, because Pydantic protects your API, a Plain Dictionary does not (a plain dict has no validation) someone can send bad JSON and our Database will store it
    # try a bad email address such as johnadams@@gmail.com and see the validator do its magic
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user