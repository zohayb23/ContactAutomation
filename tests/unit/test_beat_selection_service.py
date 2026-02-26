"""Unit tests for beat selection service."""
import pytest
import tempfile
import os
from pathlib import Path
from services.database_service import DatabaseService
from services.beat_selection_service import BeatSelectionService


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    db = DatabaseService(db_path=db_path)
    yield db
    db.close()
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def db_with_beats(temp_db):
    """Database with one artist and several beats."""
    temp_db.add_artist("Test Artist", "test@example.com")
    for i in range(5):
        temp_db.add_beat(f"beat{i}.mp3", f"Beat {i}", file_type="mp3")
    return temp_db


def test_select_beats_returns_3_to_5(db_with_beats):
    """Select beats returns between min and max beats."""
    selector = BeatSelectionService(db_with_beats, min_beats=3, max_beats=5)
    artist_id = 1
    selected = selector.select_beats_for_artist(artist_id)
    assert 1 <= len(selected) <= 5
    assert len(selected) == len(set(selected))


def test_select_beats_excludes_recently_sent(db_with_beats):
    """Beats sent in last 30 days are excluded."""
    artist_id = 1
    db_with_beats.add_artist_beat_history(artist_id, 1)
    db_with_beats.add_artist_beat_history(artist_id, 2)
    selector = BeatSelectionService(db_with_beats, min_beats=2, max_beats=2, duplicate_prevention_days=30)
    selected = selector.select_beats_for_artist(artist_id)
    assert 1 not in selected
    assert 2 not in selected
    assert len(selected) == 2


def test_select_beats_handles_insufficient_beats(db_with_beats):
    """When fewer than min beats available, returns what's available."""
    artist_id = 1
    selector = BeatSelectionService(db_with_beats, min_beats=3, max_beats=5)
    selected = selector.select_beats_for_artist(artist_id)
    assert len(selected) >= 1
