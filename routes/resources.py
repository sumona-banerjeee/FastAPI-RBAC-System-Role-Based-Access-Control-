# app/routes/resources.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(tags=["Resources"])



def check_permission(user: models.User, db: Session, resource_name: str, action: str):
    assignment = (
        db.query(models.UserResource)
        .join(models.Resource)
        .filter(models.UserResource.user_id == user.id,
                models.Resource.name == resource_name)
        .first()
    )
    if not assignment or action not in assignment.permissions:
        raise HTTPException(status_code=403, detail=f"Missing permission: {action}")




@router.post("/create_post", response_model=schemas.PostResponse)
def create_post(data: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "create_post", "C")
    post = models.Post(title=data.title, content=data.content, owner_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/create_post", response_model=List[schemas.PostResponse])
def read_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "create_post", "R")
    return db.query(models.Post).all()

@router.put("/create_post/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, data: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "create_post", "U")
    post = db.query(models.Post).filter_by(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = data.title
    post.content = data.content
    db.commit()
    db.refresh(post)
    return post

@router.delete("/create_post/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "create_post", "D")
    post = db.query(models.Post).filter_by(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}




@router.post("/comment_post")
def create_comment(data: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "comment_post", "C")
    comment = models.Comment(post_id=data.post_id, content=data.content, user_id=current_user.id)
    db.add(comment)
    db.commit()
    return {"message": "Comment added"}

@router.get("/comment_post")
def read_comments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "comment_post", "R")
    return db.query(models.Comment).all()

@router.put("/comment_post/{comment_id}")
def update_comment(comment_id: int, data: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "comment_post", "U")
    comment = db.query(models.Comment).filter_by(id=comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.content = data.content
    db.commit()
    return {"message": "Comment updated"}

@router.delete("/comment_post/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "comment_post", "D")
    comment = db.query(models.Comment).filter_by(id=comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}




@router.post("/manage_post")
def create_manage_post(data: schemas.ManagePostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "manage_post", "C")
    manage = models.ManagePost(post_id=data.post_id, action=data.action, user_id=current_user.id)
    db.add(manage)
    db.commit()
    return {"message": "Manage action created"}

@router.get("/manage_post")
def read_manage_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "manage_post", "R")
    return db.query(models.ManagePost).all()

@router.put("/manage_post/{manage_id}")
def update_manage_post(manage_id: int, data: schemas.ManagePostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "manage_post", "U")
    manage = db.query(models.ManagePost).filter_by(id=manage_id).first()
    if not manage:
        raise HTTPException(status_code=404, detail="ManagePost not found")
    manage.action = data.action
    db.commit()
    return {"message": "Manage action updated"}

@router.delete("/manage_post/{manage_id}")
def delete_manage_post(manage_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "manage_post", "D")
    manage = db.query(models.ManagePost).filter_by(id=manage_id).first()
    if not manage:
        raise HTTPException(status_code=404, detail="ManagePost not found")
    db.delete(manage)
    db.commit()
    return {"message": "ManagePost deleted"}




@router.post("/creating_event")
def create_event(data: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_event", "C")
    event = models.Event(title=data.title, description=data.description, owner_id=current_user.id)
    db.add(event)
    db.commit()
    return {"message": "Event created"}

@router.get("/creating_event")
def read_events(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_event", "R")
    return db.query(models.Event).all()

@router.put("/creating_event/{event_id}")
def update_event(event_id: int, data: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_event", "U")
    event = db.query(models.Event).filter_by(id=event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.title = data.title
    event.description = data.description
    db.commit()
    return {"message": "Event updated"}

@router.delete("/creating_event/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_event", "D")
    event = db.query(models.Event).filter_by(id=event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}




@router.post("/creating_poll")
def create_poll(data: schemas.PollCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_poll", "C")
    poll = models.Poll(question=data.question, options=data.options, owner_id=current_user.id)
    db.add(poll)
    db.commit()
    return {"message": "Poll created"}

@router.get("/creating_poll")
def read_polls(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_poll", "R")
    return db.query(models.Poll).all()

@router.put("/creating_poll/{poll_id}")
def update_poll(poll_id: int, data: schemas.PollCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_poll", "U")
    poll = db.query(models.Poll).filter_by(id=poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    poll.question = data.question
    poll.options = data.options
    db.commit()
    return {"message": "Poll updated"}

@router.delete("/creating_poll/{poll_id}")
def delete_poll(poll_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "creating_poll", "D")
    poll = db.query(models.Poll).filter_by(id=poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    db.delete(poll)
    db.commit()
    return {"message": "Poll deleted"}




@router.post("/reaction_post")
def create_reaction(data: schemas.ReactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "reaction_post", "C")
    reaction = models.Reaction(post_id=data.post_id, user_id=current_user.id, reaction_type=data.reaction_type)
    db.add(reaction)
    db.commit()
    return {"message": "Reaction added"}

@router.get("/reaction_post")
def read_reactions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "reaction_post", "R")
    return db.query(models.Reaction).all()

@router.put("/reaction_post/{reaction_id}")
def update_reaction(reaction_id: int, data: schemas.ReactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "reaction_post", "U")
    reaction = db.query(models.Reaction).filter_by(id=reaction_id).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    reaction.reaction_type = data.reaction_type
    db.commit()
    return {"message": "Reaction updated"}

@router.delete("/reaction_post/{reaction_id}")
def delete_reaction(reaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    check_permission(current_user, db, "reaction_post", "D")
    reaction = db.query(models.Reaction).filter_by(id=reaction_id).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    db.delete(reaction)
    db.commit()
    return {"message": "Reaction deleted"}
