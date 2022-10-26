from fastapi import APIRouter, HTTPException, File, UploadFile
# pip install python-multipart
robot_end_points = APIRouter()

@robot_end_points.post("/upload/robot")
def robot_upload (config: UploadFile, avatar: UploadFile):
    return {"filename_config": config.filename, "filename_avatar": avatar.filename}