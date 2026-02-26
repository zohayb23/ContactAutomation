"""
Email template service for generating personalized email content.
Handles placeholder replacement and formatting.
"""
from pathlib import Path
from typing import List, Optional
import yaml


class EmailTemplateService:
    """Service for loading and rendering email templates."""

    def __init__(self, template_path: Optional[str] = None):
        """
        Initialize email template service.

        Args:
            template_path: Path to template file. If None, loads from config.
        """
        if template_path is None:
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            template_path = config["email"]["template_path"]
        self.template_path = Path(__file__).parent.parent / template_path

    def load_template(self) -> str:
        """Load email template from file."""
        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    def format_beat_list(self, beat_names: List[str]) -> str:
        """Format beat names as a simple comma-separated list."""
        return ", ".join(beat_names)

    def generate_body(self, artist_name: str, beat_names: List[str]) -> str:
        """
        Generate email body with placeholders replaced.

        Args:
            artist_name: Artist display name
            beat_names: List of beat names to include

        Returns:
            Rendered email body
        """
        template = self.load_template()
        beat_list_str = self.format_beat_list(beat_names)
        body = template.replace("{artist_name}", artist_name).replace(
            "{beat_list}", beat_list_str
        )
        return body
