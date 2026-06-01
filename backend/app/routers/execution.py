from fastapi import APIRouter, Body, HTTPException

from app.models.execution_jobs import ExecutionRequest
from app.services.code_execution import CodeExecutionService

router = APIRouter(prefix="/api/execution", tags=["Code Execution"])


@router.post("/run")
async def run_code(payload: ExecutionRequest = Body(...)):
    payload.mode = "run"
    try:
        return await CodeExecutionService.create_job(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/submit")
async def submit_code(payload: ExecutionRequest = Body(...)):
    payload.mode = "submit"
    try:
        return await CodeExecutionService.create_job(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/submissions/recent")
async def list_submissions(problem_slug: str | None = None, limit: int = 20):
    return await CodeExecutionService.list_submissions(problem_slug=problem_slug, limit=limit)


@router.get("/submissions/{submission_id}")
async def get_submission(submission_id: str):
    submission = await CodeExecutionService.get_submission(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


@router.get("/{job_id}")
async def get_execution_job(job_id: str):
    job = await CodeExecutionService.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Execution job not found")
    return job
