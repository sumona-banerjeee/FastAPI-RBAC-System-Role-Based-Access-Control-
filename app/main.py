from fastapi import FastAPI
from sqlalchemy.orm import Session
from app import models, database, crud, schemas, config
from routes import auth, superadmin, resources


models.Base.metadata.create_all(bind=database.engine)


app = FastAPI(
    title="FastAPI RBAC System",
    description="Role-Based Access Control with CRUD permissions for each resource",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the FastAPI RBAC API",
        "docs_url": "http://127.0.0.1:8000/docs"
    }

@app.on_event("startup")
def startup_tasks():
    db: Session = database.SessionLocal()
    try:
        
        superadmin_user = crud.get_user_by_email(db, config.SUPERADMIN_EMAIL)
        if not superadmin_user:
            crud.create_user(
                db,
                schemas.UserCreate(
                    name="Super Admin",
                    email=config.SUPERADMIN_EMAIL,
                    password=config.SUPERADMIN_PASSWORD,
                    role="superadmin"
                ),
                role="superadmin"
            )
            print("Superadmin created successfully.")

        
        default_resources = [
            "create_post",
            "comment_post",
            "manage_post",
            "creating_event",
            "creating_poll",
            "reaction_post"
        ]
        for res in default_resources:
            if not db.query(models.Resource).filter_by(name=res).first():
                db.add(models.Resource(name=res))
        db.commit()
        print("Default resources created successfully.")
    finally:
        db.close()


app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(superadmin.router, prefix="/api/superadmin", tags=["Super Admin"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])
