from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Создание зависимости для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/token/")
def login(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверные учетные данные")
    access_token = crud.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



# import os
# from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from typing import List
# from PIL import Image
# import jwt
# import shutil
# from . import models, crud
# from .database import SessionLocal, engine
# from .schemas import ImageCreate, ImageUpdate, ImageOut, Token, UserCreate
# from .config import SECRET_KEY#, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # JWT authentication
# def authenticate_user(username: str, password: str, db: Session):
#     user = crud.get_user_by_username(db, username=username)
#     if not user or not user.verify_password(password):
#         return False
#     return user

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     user = crud.get_user_by_username(db, username=username)
#     if user is None:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return user

# # User registration
# @app.post("/register", response_model=Token)
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     user = crud.create_user(db=db, user=user)
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# # Login for access token
# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# # Image upload and processing
# @app.post("/images/", response_model=ImageOut)
# async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     filename = f"uploads/{file.filename}"
#     with open(filename, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     image = Image.open(filename)
#     width, height = image.size
#     image = image.convert("L")
#     image.save(f"processed/{file.filename}")
#     image_data = ImageCreate(
#         name=file.filename,
#         path=filename,
#         upload_date=datetime.utcnow(),
#         resolution=f"{width}x{height}",
#         size=os.path.getsize(filename)
#     )
#     db_image = crud.create_image(db=db, image=image_data)
#     return db_image

# # Get all images
# @app.get("/images/", response_model=List[ImageOut])
# def read_images(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     images = crud.get_images(db)
#     return images

# # Get a specific image by ID
# @app.get("/images/{image_id}", response_model=ImageOut)
# def read_image(image_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     db_image = crud.get_image(db, image_id=image_id)
#     if db_image is None:
#         raise HTTPException(status_code=404, detail="Image not found")
#     return db_image

# # Update an image's name or tags
# @app.put("/images/{image_id}", response_model=ImageOut)
# def update_image(image_id: int, image: ImageUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     db_image = crud.get_image(db, image_id=image_id)
#     if db_image is None:
#         raise HTTPException(status_code=404, detail="Image not found")
#     updated_image = crud.update_image(db=db, image_id=image_id, image=image)
#     return updated_image

# # Delete an image
# @app.delete("/images/{image_id}", response_model=ImageOut)
# def delete_image(image_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
#     db_image = crud.get_image(db, image_id=image_id)
#     if db_image is None:
#         raise HTTPException(status_code=404, detail="Image not found")
#     crud.delete_image(db=db, image_id=image_id)
#     return db_image
