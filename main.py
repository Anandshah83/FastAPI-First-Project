from database import engine,SessionLocal
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session 
import models,Schemas


# create a table 
models.Base.metadata.create_all(bind=engine)


app=FastAPI()



# DB dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HOme route
@app.get('/')
def home():
    return{
        "message":"blog api start"
    }


# Create blog
@app.post('/blogs',response_model=Schemas.BlogResponse)
def create_blog(blog:Schemas.BlogCreate,db:Session=Depends(get_db)):
    new_blog=models.Blog(
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Read all the blogs
@app.get('/blogs',response_model=list[Schemas.BlogResponse])
def read_blogs(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs



# Read a single blog
@app.get('/blogs/{id}',response_model=Schemas.BlogResponse)
def read_blog(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=404,detail=f"Blog with the id {id} is not available")
    return blog


# update blog api
@app.put('/blogs/{id}',response_model=Schemas.BlogResponse)
def update_blog(id:int,blog:Schemas.BlogCreate,db:Session=Depends(get_db)):
    existing_blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not existing_blog:
        raise HTTPException(status_code=404,detail=f"Blog with the id {id} is not available")
    existing_blog.title=blog.title
    existing_blog.content=blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog
