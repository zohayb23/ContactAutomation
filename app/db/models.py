from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    artist_name: Mapped[str] = mapped_column(String(120))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class CampaignRun(Base):
    __tablename__ = "campaign_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    campaign_name: Mapped[str] = mapped_column(String(100), index=True)
    dry_run: Mapped[bool] = mapped_column(Boolean, default=False)
    requested_limit: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30), default="queued", index=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)


class EmailLog(Base):
    __tablename__ = "email_logs"
    __table_args__ = (
        UniqueConstraint("campaign_name", "contact_id", "run_id", name="uq_run_contact"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(Integer, index=True)
    campaign_name: Mapped[str] = mapped_column(String(100), index=True)
    contact_id: Mapped[int] = mapped_column(Integer, index=True)
    contact_email: Mapped[str] = mapped_column(String(320), index=True)
    status: Mapped[str] = mapped_column(String(30), index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
