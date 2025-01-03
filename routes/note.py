from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from database import notes_collection
from utils.auth import decode_token
from datetime import datetime

router = APIRouter()

@router.post("/notes/")
async def create_note(note: dict, user=Depends(decode_token)):
    note["note_id"] = str(uuid4())
    note["user_id"] = user["user_id"]
    note["created_on"] = note["last_update"] = datetime.utcnow()
    await notes_collection.insert_one(note)
    return {"message": "Note created successfully"}

@router.get("/notes/")
async def view_notes(user=Depends(decode_token)):
    notes = await notes_collection.find({"user_id": user["user_id"]}).to_list(100)
    return notes

@router.put("/notes/{note_id}/")
async def update_note(note_id: str, note: dict, user=Depends(decode_token)):
    result = await notes_collection.update_one(
        {"note_id": note_id, "user_id": user["user_id"]},
        {"$set": note}
    )
    if not result.modified_count:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note updated successfully"}

@router.delete("/notes/{note_id}/")
async def delete_note(note_id: str, user=Depends(decode_token)):
    result = await notes_collection.delete_one({"note_id": note_id, "user_id": user["user_id"]})
    if not result.deleted_count:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
