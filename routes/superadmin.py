import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(tags=["Super Admin"])
SUPERADMIN_APPROVAL_TOKEN = os.getenv("SUPERADMIN_APPROVAL_TOKEN")


@router.post("/approve-and-assign")
def approve_and_assign_user(
    data: schemas.ApproveUserRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    if current_user.role.lower() != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can approve users")

    
    if data.approval_token != SUPERADMIN_APPROVAL_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid approval token")

    
    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    user.role = data.role
    user.is_active = True  
    db.flush()  

    
    for res in data.resources:
        resource = db.query(models.Resource).filter_by(name=res.resource_name).first()
        if not resource:
            resource = models.Resource(name=res.resource_name)
            db.add(resource)
            db.flush()

        existing_assignment = db.query(models.UserResource).filter_by(
            user_id=user.id,
            resource_id=resource.id
        ).first()

        if existing_assignment:
            existing_assignment.permissions = res.permissions
        else:
            new_assignment = models.UserResource(
                user_id=user.id,
                resource_id=resource.id,
                permissions=res.permissions
            )
            db.add(new_assignment)


    db.commit()

    return {
        "message": f"User {user.email} approved, activated, and resources assigned",
        "role": user.role,
        "is_active": user.is_active,
        "resources": [{"name": r.resource_name, "permissions": r.permissions} for r in data.resources]
    }
