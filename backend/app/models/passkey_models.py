from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class PasskeyRegisterOptionsRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email for passkey registration if not authenticated")

class PasskeyRegisterVerifyRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email for passkey registration if not authenticated")
    credential: Dict[str, Any] = Field(..., description="WebAuthn registration credential from navigator.credentials.create")

class PasskeyLoginOptionsRequest(BaseModel):
    email: str = Field(..., description="Email of the user logging in")

class PasskeyLoginVerifyRequest(BaseModel):
    email: str = Field(..., description="Email of the user logging in")
    credential: Dict[str, Any] = Field(..., description="WebAuthn assertion credential from navigator.credentials.get")
