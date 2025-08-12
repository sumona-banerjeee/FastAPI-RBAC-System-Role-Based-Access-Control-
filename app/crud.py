from sqlalchemy.orm import Session
from app import models, utils, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()




def create_user(db: Session, user: schemas.UserCreate, role: str, is_active: bool = True):
    hashed_pwd = utils.hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_pwd,
        role=role,
        is_active=is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def approve_user(db: Session, user_id: int):
    user = db.query(models.User).get(user_id)
    if not user:
        return None
    user.is_active = True
    db.commit()
    return user



def assign_resource(db: Session, user_id: int, resource_name: str, permissions: str):
    user = db.query(models.User).get(user_id)
    if not user:
        return None

    
    resource = db.query(models.Resource).filter_by(name=resource_name).first()
    if not resource:
        resource = models.Resource(name=resource_name)
        db.add(resource)
        db.commit()
        db.refresh(resource)

    
    existing_assignment = db.query(models.UserResource).filter_by(
        user_id=user.id,
        resource_id=resource.id
    ).first()

    if existing_assignment:
        
        existing_assignment.permissions = permissions
    else:
        
        user_resource = models.UserResource(
            user_id=user.id,
            resource_id=resource.id,
            permissions=permissions
        )
        db.add(user_resource)

    db.commit()
    return {
        "user": user.email,
        "resource": resource.name,
        "permissions": permissions
    }



def approve_and_assign(db: Session, user_id: int, role: str, resources: list):
    user = db.query(models.User).get(user_id)
    if not user:
        return None
    
    user.is_active = True
    user.role = role
    db.commit()

    for res in resources:
        resource = db.query(models.Resource).filter_by(name=res.resource_name).first()
        if not resource:
            resource = models.Resource(name=res.resource_name)
            db.add(resource)
            db.commit()
            db.refresh(resource)

        existing_assignment = db.query(models.UserResource).filter_by(
            user_id=user.id,
            resource_id=resource.id
        ).first()

        if existing_assignment:
            existing_assignment.permissions = res.permissions
        else:
            user_resource = models.UserResource(
                user_id=user.id,
                resource_id=resource.id,
                permissions=res.permissions
            )
            db.add(user_resource)

    db.commit()
    return user
