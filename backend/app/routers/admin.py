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

from fastapi import APIRouter, Depends, Body
from app.middleware.admin import AdminMiddleware
from app.controllers.admin import AdminController

router = APIRouter(prefix="/admin", tags=["Admin Operations"])

# Protect all operations inside this router via dependencies
@router.get("/users", dependencies=[Depends(AdminMiddleware.is_admin)])
async def list_users():
    return await AdminController.list_users()

@router.patch("/users/{user_id}", dependencies=[Depends(AdminMiddleware.is_admin)])
async def update_user(user_id: str, payload: dict = Body(...)):
    return await AdminController.update_user_status(user_id, payload)

# ─── INTERVIEW PRESETS ────────────────────────────────────────────────
@router.get("/presets", dependencies=[Depends(AdminMiddleware.is_admin)])
async def list_presets():
    return await AdminController.list_presets()

@router.post("/presets/{preset_id}", dependencies=[Depends(AdminMiddleware.is_admin)])
async def save_preset(preset_id: str, payload: dict = Body(...)):
    return await AdminController.save_preset(preset_id, payload)

@router.delete("/presets/{preset_id}", dependencies=[Depends(AdminMiddleware.is_admin)])
async def delete_preset(preset_id: str):
    return await AdminController.delete_preset(preset_id)

# ─── SYSTEM DESIGN CHALLENGES ──────────────────────────────────────────
@router.get("/system-design/challenges", dependencies=[Depends(AdminMiddleware.is_admin)])
async def list_system_design_challenges():
    return await AdminController.list_system_design_challenges()

@router.post("/system-design/challenges/{id}", dependencies=[Depends(AdminMiddleware.is_admin)])
async def save_system_design_challenge(id: str, payload: dict = Body(...)):
    return await AdminController.save_system_design_challenge(id, payload)

@router.delete("/system-design/challenges/{id}", dependencies=[Depends(AdminMiddleware.is_admin)])
async def delete_system_design_challenge(id: str):
    return await AdminController.delete_system_design_challenge(id)

# ─── SYSTEM DESIGN TEMPLATES ───────────────────────────────────────────
@router.get("/system-design/templates", dependencies=[Depends(AdminMiddleware.is_admin)])
async def list_system_design_templates():
    return await AdminController.list_system_design_templates()

@router.post("/system-design/templates/{id}", dependencies=[Depends(AdminMiddleware.is_admin)])
async def save_system_design_template(id: str, payload: dict = Body(...)):
    return await AdminController.save_system_design_template(id, payload)

@router.delete("/system-design/templates/{id}", dependencies=[Depends(AdminMiddleware.is_admin)])
async def delete_system_design_template(id: str):
    return await AdminController.delete_system_design_template(id)
