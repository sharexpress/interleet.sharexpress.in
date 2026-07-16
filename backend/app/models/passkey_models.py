# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class PasskeyRegisterOptionsRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email for passkey registration if not authenticated")

class PasskeyRegisterVerifyRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email for passkey registration if not authenticated")
    credential: Dict[str, Any] = Field(..., description="WebAuthn registration credential from navigator.credentials.create")
    label: Optional[str] = Field(None, description="Custom label for the passkey")


class PasskeyLoginOptionsRequest(BaseModel):
    email: str = Field(..., description="Email of the user logging in")

class PasskeyLoginVerifyRequest(BaseModel):
    email: str = Field(..., description="Email of the user logging in")
    credential: Dict[str, Any] = Field(..., description="WebAuthn assertion credential from navigator.credentials.get")
