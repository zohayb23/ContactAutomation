from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Base, CampaignRun
from app.db.session import engine, get_db
from app.queue import send_queue
from app.schemas import CampaignRunStatus, TriggerSendRequest, TriggerSendResponse
from app.services.auth import require_api_token
from app.services.rate_limit import enforce_rate_limit
from app.services.send_service import create_campaign_run, execute_campaign_run

app = FastAPI(title="ContactAutomationCloud")
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/campaigns/send", response_model=TriggerSendResponse, dependencies=[Depends(require_api_token)])
def trigger_send(payload: TriggerSendRequest, db: Session = Depends(get_db)) -> TriggerSendResponse:
    enforce_rate_limit()
    requested_limit = payload.max_send_per_run or 50
    run = create_campaign_run(
        db=db,
        campaign_name=payload.campaign_name,
        dry_run=payload.dry_run,
        requested_limit=requested_limit,
    )
    job = send_queue.enqueue(execute_campaign_run, run.id, payload.subject, payload.body)
    return TriggerSendResponse(run_id=run.id, queue_job_id=job.id, status="queued")


@app.get("/campaigns/{run_id}", response_model=CampaignRunStatus, dependencies=[Depends(require_api_token)])
def campaign_status(run_id: int, db: Session = Depends(get_db)) -> CampaignRunStatus:
    run = db.get(CampaignRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return CampaignRunStatus(
        run_id=run.id,
        campaign_name=run.campaign_name,
        status=run.status,
        detail=run.detail,
    )
