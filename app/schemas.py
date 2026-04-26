from pydantic import BaseModel, Field


class TriggerSendRequest(BaseModel):
    campaign_name: str = Field(min_length=1, max_length=100)
    subject: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=5000)
    dry_run: bool = True
    max_send_per_run: int | None = Field(default=None, ge=1, le=1000)


class TriggerSendResponse(BaseModel):
    run_id: int
    queue_job_id: str
    status: str


class CampaignRunStatus(BaseModel):
    run_id: int
    campaign_name: str
    status: str
    detail: str | None
