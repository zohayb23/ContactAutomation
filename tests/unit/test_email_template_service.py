"""Unit tests for email template service."""
import pytest
import tempfile
from pathlib import Path
from services.email_template_service import EmailTemplateService


def test_format_beat_list():
    """Beat list is comma-separated."""
    tpl = EmailTemplateService(template_path="templates/email_template.txt")
    out = tpl.format_beat_list(["a", "b", "c"])
    assert out == "a, b, c"


def test_generate_body_replaces_placeholders():
    """Generate body replaces artist_name and beat_list."""
    tpl = EmailTemplateService(template_path="templates/email_template.txt")
    body = tpl.generate_body("Artist One", ["tundra", "hope"])
    assert "Artist One" in body
    assert "tundra, hope" in body
    assert "{artist_name}" not in body
    assert "{beat_list}" not in body
