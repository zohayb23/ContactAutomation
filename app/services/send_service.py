from datetime import datetime, timedelta

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import CampaignRun, Contact, EmailLog
from app.services.mailer import send_email


def create_campaign_run(db: Session, campaign_name: str, dry_run: bool, requested_limit: int) -> CampaignRun:
    run = CampaignRun(
        campaign_name=campaign_name,
        dry_run=dry_run,
        requested_limit=requested_limit,
        status="queued",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def execute_campaign_run(run_id: int, subject: str, body: str) -> None:
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        run = db.get(CampaignRun, run_id)
        if not run:
            return

        run.status = "running"
        db.commit()

        cutoff = datetime.utcnow() - timedelta(days=settings.dedupe_window_days)
        contact_limit = run.requested_limit

        contacts = list(
            db.scalars(
                select(Contact).where(Contact.active.is_(True)).order_by(Contact.id.asc()).limit(contact_limit)
            )
        )

        attempted = 0
        sent = 0
        skipped = 0
        failed = 0

        for contact in contacts:
            attempted += 1
            already_sent = db.scalar(
                select(EmailLog.id).where(
                    and_(
                        EmailLog.campaign_name == run.campaign_name,
                        EmailLog.contact_id == contact.id,
                        EmailLog.status == "sent",
                        EmailLog.sent_at >= cutoff,
                    )
                )
            )
            if already_sent:
                skipped += 1
                db.add(
                    EmailLog(
                        run_id=run.id,
                        campaign_name=run.campaign_name,
                        contact_id=contact.id,
                        contact_email=contact.email,
                        status="skipped",
                        message="Skipped due to dedupe window.",
                    )
                )
                db.commit()
                continue

            if run.dry_run:
                sent += 1
                db.add(
                    EmailLog(
                        run_id=run.id,
                        campaign_name=run.campaign_name,
                        contact_id=contact.id,
                        contact_email=contact.email,
                        status="dry_run",
                        message="Validated recipient in dry-run mode.",
                    )
                )
                db.commit()
                continue

            try:
                send_email(contact.email, subject, body)
                sent += 1
                db.add(
                    EmailLog(
                        run_id=run.id,
                        campaign_name=run.campaign_name,
                        contact_id=contact.id,
                        contact_email=contact.email,
                        status="sent",
                        message="Delivered via SMTP.",
                    )
                )
            except Exception as exc:
                failed += 1
                db.add(
                    EmailLog(
                        run_id=run.id,
                        campaign_name=run.campaign_name,
                        contact_id=contact.id,
                        contact_email=contact.email,
                        status="failed",
                        message=str(exc),
                    )
                )
            db.commit()

        run.status = "completed"
        run.finished_at = datetime.utcnow()
        run.detail = (
            f"attempted={attempted}, sent_or_validated={sent}, skipped={skipped}, failed={failed}, "
            f"dry_run={run.dry_run}"
        )
        db.commit()
    except Exception as exc:
        if run_id:
            run = db.get(CampaignRun, run_id)
            if run:
                run.status = "failed"
                run.finished_at = datetime.utcnow()
                run.detail = f"fatal_error={exc}"
                db.commit()
    finally:
        db.close()
