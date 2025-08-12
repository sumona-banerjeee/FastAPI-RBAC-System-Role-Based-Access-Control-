from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, utils, models, schemas
from app.models import User
from app.dependencies import get_db, get_current_user
from typing import List

router = APIRouter()



@router.post("/create_post", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    utils.check_permission(db, current_user.id, "create_post", "C")
    new_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/create_post", response_model=List[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    utils.check_permission(db, current_user.id, "create_post", "R")
    return db.query(models.Post).all()


@router.put("/create_post/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    utils.check_permission(db, current_user.id, "create_post", "U")
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/create_post/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    utils.check_permission(db, current_user.id, "create_post", "D")
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": f"Post {post_id} deleted successfully"}





@router.post("/comment_post")
def create_comment(data: schemas.CommentPostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "comment_post", "C")
    comment = models.Comment(post_id=data.post_id, user_id=current_user.id, content=data.content)
    db.add(comment)
    db.commit()
    return {"message": "Comment created successfully"}

@router.get("/comment_post/{post_id}")
def read_comments(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "comment_post", "R")
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

@router.put("/comment_post/{comment_id}")
def update_comment(comment_id: int, data: schemas.CommentPostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "comment_post", "U")
    comment = db.query(models.Comment).get(comment_id)
    if not comment:
        return {"error": "Comment not found"}
    comment.content = data.content
    db.commit()
    return {"message": "Comment updated successfully"}

@router.delete("/comment_post/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "comment_post", "D")
    comment = db.query(models.Comment).get(comment_id)
    if not comment:
        return {"error": "Comment not found"}
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}



@router.post("/manage_post")
def create_manage(data: schemas.ManagePostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "manage_post", "C")
    record = models.ManagePost(post_id=data.post_id, user_id=current_user.id, action=data.action)
    db.add(record)
    db.commit()
    return {"message": "Post management record created"}

@router.get("/manage_post")
def read_manage(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "manage_post", "R")
    return db.query(models.ManagePost).all()

@router.put("/manage_post/{id}")
def update_manage(id: int, data: schemas.ManagePostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "manage_post", "U")
    record = db.query(models.ManagePost).get(id)
    if not record:
        return {"error": "Record not found"}
    record.action = data.action
    db.commit()
    return {"message": "Management record updated"}

@router.delete("/manage_post/{id}")
def delete_manage(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "manage_post", "D")
    record = db.query(models.ManagePost).get(id)
    if not record:
        return {"error": "Record not found"}
    db.delete(record)
    db.commit()
    return {"message": "Management record deleted"}



@router.post("/creating_event")
def create_event(data: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_event", "C")
    event = models.Event(title=data.title, description=data.description, owner_id=current_user.id)
    db.add(event)
    db.commit()
    return {"message": "Event created"}

@router.get("/creating_event")
def read_events(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_event", "R")
    return db.query(models.Event).all()

@router.put("/creating_event/{id}")
def update_event(id: int, data: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_event", "U")
    event = db.query(models.Event).get(id)
    if not event:
        return {"error": "Event not found"}
    event.title = data.title
    event.description = data.description
    db.commit()
    return {"message": "Event updated"}

@router.delete("/creating_event/{id}")
def delete_event(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_event", "D")
    event = db.query(models.Event).get(id)
    if not event:
        return {"error": "Event not found"}
    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}



@router.post("/creating_poll")
def create_poll(data: schemas.PollCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_poll", "C")
    poll = models.Poll(question=data.question, options=data.options, owner_id=current_user.id)
    db.add(poll)
    db.commit()
    return {"message": "Poll created"}

@router.get("/creating_poll")
def read_polls(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_poll", "R")
    return db.query(models.Poll).all()

@router.put("/creating_poll/{id}")
def update_poll(id: int, data: schemas.PollCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_poll", "U")
    poll = db.query(models.Poll).get(id)
    if not poll:
        return {"error": "Poll not found"}
    poll.question = data.question
    poll.options = data.options
    db.commit()
    return {"message": "Poll updated"}

@router.delete("/creating_poll/{id}")
def delete_poll(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "creating_poll", "D")
    poll = db.query(models.Poll).get(id)
    if not poll:
        return {"error": "Poll not found"}
    db.delete(poll)
    db.commit()
    return {"message": "Poll deleted"}



@router.post("/reaction_post")
def create_reaction(data: schemas.ReactionPostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "reaction_post", "C")
    reaction = models.Reaction(post_id=data.post_id, user_id=current_user.id, reaction_type=data.reaction_type)
    db.add(reaction)
    db.commit()
    return {"message": "Reaction added"}

@router.get("/reaction_post/{post_id}")
def read_reactions(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "reaction_post", "R")
    return db.query(models.Reaction).filter(models.Reaction.post_id == post_id).all()

@router.put("/reaction_post/{id}")
def update_reaction(id: int, data: schemas.ReactionPostRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "reaction_post", "U")
    reaction = db.query(models.Reaction).get(id)
    if not reaction:
        return {"error": "Reaction not found"}
    reaction.reaction_type = data.reaction_type
    db.commit()
    return {"message": "Reaction updated"}

@router.delete("/reaction_post/{id}")
def delete_reaction(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    utils.check_permission(db, current_user.id, "reaction_post", "D")
    reaction = db.query(models.Reaction).get(id)
    if not reaction:
        return {"error": "Reaction not found"}
    db.delete(reaction)
    db.commit()
    return {"message": "Reaction deleted"}

