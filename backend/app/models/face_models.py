from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class FaceRegisterRequest(BaseModel):
    email: str
    frames: List[str] = Field(..., description="List of Base64 encoded images")
    angles: List[str] = Field(..., description="Corresponding angle names: front, left, right, smile, neutral, low-light, glasses")
    device_fingerprint: str

class FaceLoginRequest(BaseModel):
    email: str = Field(..., description="Email for biometric verification")
    frame: str = Field(..., description="Base64 encoded image frame")
    device_fingerprint: str

class FaceVerifyRequest(BaseModel):
    frame: str = Field(..., description="Base64 encoded image frame")
    device_fingerprint: str

class LivenessChallengeStartRequest(BaseModel):
    email: str

class LivenessChallengeVerifyRequest(BaseModel):
    email: str
    challenge_type: str = Field(..., description="blink, turn_left, turn_right, smile, move_closer")
    frames: List[str] = Field(..., description="Sequence of Base64 encoded frames captured during the challenge")
    device_fingerprint: str

class FaceSessionResponse(BaseModel):
    success: bool
    user_id: Optional[str] = None
    face_registered: bool
    last_login: Optional[datetime] = None
