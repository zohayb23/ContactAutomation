"""
Gmail service for sending emails with attachments.
Handles authentication, email composition, and rate limiting.
"""
import base64
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from services.auth_service import get_credentials
from utils.logger import setup_logger

logger = setup_logger(__name__)


class GmailService:
    """Service for sending emails via Gmail API."""

    def __init__(
        self,
        rate_limit_delay: float = 2.0,
        batch_pause_every: int = 10,
        batch_pause_seconds: int = 30,
    ):
        """
        Initialize Gmail service.

        Args:
            rate_limit_delay: Seconds between each email
            batch_pause_every: Pause every N emails
            batch_pause_seconds: Seconds to pause between batches
        """
        creds = get_credentials()
        if not creds:
            raise ValueError("Authentication required. Run 'python main.py configure' first.")
        self.service = build("gmail", "v1", credentials=creds)
        self.rate_limit_delay = rate_limit_delay
        self.batch_pause_every = batch_pause_every
        self.batch_pause_seconds = batch_pause_seconds

    @classmethod
    def from_config(cls) -> "GmailService":
        """Create service from config.yaml."""
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        gmail_config = config["gmail"]
        return cls(
            rate_limit_delay=gmail_config.get("rate_limit_delay", 2),
            batch_pause_every=10,
            batch_pause_seconds=config["gmail"].get("batch_pause", 30),
        )

    def _create_message(
        self,
        to: str,
        subject: str,
        body_text: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, str]:
        """
        Create a MIME message for sending.

        Args:
            to: Recipient email
            subject: Subject line
            body_text: Plain text body
            attachments: List of {"filename": str, "content": bytes} or {"filename": str, "path": str}

        Returns:
            Dict with 'raw' key (base64url encoded message)
        """
        message = MIMEMultipart()
        message["to"] = to
        message["subject"] = subject
        message.attach(MIMEText(body_text, "plain"))

        if attachments:
            for att in attachments:
                filename = att.get("filename", "attachment")
                content = att.get("content")
                if content is None and "path" in att:
                    with open(att["path"], "rb") as f:
                        content = f.read()
                if content is None:
                    continue
                part = MIMEBase("application", "octet-stream")
                part.set_payload(content)
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{filename}"',
                )
                message.attach(part)

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {"raw": raw}

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[str]:
        """
        Send an email via Gmail API.

        Args:
            to: Recipient email
            subject: Subject line
            body: Plain text body
            attachments: Optional list of attachments

        Returns:
            Message ID if sent, None on failure
        """
        try:
            msg = self._create_message(to, subject, body, attachments)
            sent = self.service.users().messages().send(userId="me", body=msg).execute()
            logger.info(f"Email sent to {to}, message id: {sent.get('id')}")
            return sent.get("id")
        except HttpError as error:
            logger.error(f"Failed to send to {to}: {error}")
            return None

    def apply_rate_limit(self, email_index: int) -> None:
        """Apply delay between emails; longer pause every N emails."""
        time.sleep(self.rate_limit_delay)
        if self.batch_pause_every and (email_index + 1) % self.batch_pause_every == 0:
            logger.info(f"Batch pause: waiting {self.batch_pause_seconds}s...")
            time.sleep(self.batch_pause_seconds)
