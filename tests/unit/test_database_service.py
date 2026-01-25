"""
Unit tests for database service.
"""
import pytest
import tempfile
import os
from pathlib import Path
from services.database_service import DatabaseService


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    db_service = DatabaseService(db_path=db_path)
    yield db_service

    db_service.close()
    if os.path.exists(db_path):
        os.unlink(db_path)


class TestDatabaseService:
    """Test cases for DatabaseService."""

    def test_database_initialization(self, temp_db):
        """Test that database tables are created."""
        conn = temp_db._get_connection()
        cursor = conn.cursor()

        # Check that tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name IN ('artists', 'beats', 'email_history', 'artist_beat_history')
        """)
        tables = [row[0] for row in cursor.fetchall()]

        assert 'artists' in tables
        assert 'beats' in tables
        assert 'email_history' in tables
        assert 'artist_beat_history' in tables

    def test_add_artist(self, temp_db):
        """Test adding an artist."""
        artist_id = temp_db.add_artist("Test Artist", "test@example.com")
        assert artist_id is not None

        artist = temp_db.get_artist_by_email("test@example.com")
        assert artist is not None
        assert artist['name'] == "Test Artist"
        assert artist['email'] == "test@example.com"
        assert artist['last_pack_number'] == 0

    def test_add_duplicate_artist(self, temp_db):
        """Test that duplicate emails are rejected."""
        temp_db.add_artist("Artist 1", "same@example.com")

        with pytest.raises(Exception):  # Should raise IntegrityError
            temp_db.add_artist("Artist 2", "same@example.com")

    def test_get_all_artists(self, temp_db):
        """Test getting all artists."""
        temp_db.add_artist("Artist A", "a@example.com")
        temp_db.add_artist("Artist B", "b@example.com")

        artists = temp_db.get_all_artists()
        assert len(artists) == 2
        assert artists[0]['name'] == "Artist A"
        assert artists[1]['name'] == "Artist B"

    def test_update_artist_pack_number(self, temp_db):
        """Test updating artist pack number."""
        artist_id = temp_db.add_artist("Test Artist", "test@example.com")
        temp_db.update_artist_pack_number(artist_id, 5)

        artist = temp_db.get_artist_by_email("test@example.com")
        assert artist['last_pack_number'] == 5

    def test_add_beat(self, temp_db):
        """Test adding a beat."""
        beat_id = temp_db.add_beat(
            filename="test_beat.mp3",
            beat_name="Test Beat",
            bpm=140,
            key="Cmin",
            style_category="trap",
            file_type="mp3",
            file_size=3000000
        )
        assert beat_id is not None

        beat = temp_db.get_beat_by_filename("test_beat.mp3")
        assert beat is not None
        assert beat['beat_name'] == "Test Beat"
        assert beat['bpm'] == 140
        assert beat['key'] == "Cmin"
        assert beat['style_category'] == "trap"

    def test_get_all_beats(self, temp_db):
        """Test getting all beats."""
        temp_db.add_beat("beat1.mp3", "Beat 1", file_type="mp3")
        temp_db.add_beat("beat2.mp3", "Beat 2", file_type="mp3")

        beats = temp_db.get_all_beats()
        assert len(beats) == 2

    def test_get_beats_by_ids(self, temp_db):
        """Test getting beats by IDs."""
        id1 = temp_db.add_beat("beat1.mp3", "Beat 1", file_type="mp3")
        id2 = temp_db.add_beat("beat2.mp3", "Beat 2", file_type="mp3")
        id3 = temp_db.add_beat("beat3.mp3", "Beat 3", file_type="mp3")

        beats = temp_db.get_beats_by_ids([id1, id3])
        assert len(beats) == 2
        assert {b['id'] for b in beats} == {id1, id3}

    def test_add_email_history(self, temp_db):
        """Test adding email history."""
        artist_id = temp_db.add_artist("Test Artist", "test@example.com")
        beat_id = temp_db.add_beat("beat.mp3", "Beat", file_type="mp3")

        history_id = temp_db.add_email_history(
            artist_id=artist_id,
            pack_number=1,
            beats_sent=[beat_id],
            status='sent'
        )
        assert history_id is not None

    def test_get_email_history(self, temp_db):
        """Test getting email history."""
        artist_id = temp_db.add_artist("Test Artist", "test@example.com")
        beat_id = temp_db.add_beat("beat.mp3", "Beat", file_type="mp3")

        temp_db.add_email_history(artist_id, 1, [beat_id], 'sent')
        temp_db.add_email_history(artist_id, 2, [beat_id], 'sent')

        history = temp_db.get_email_history(artist_id=artist_id)
        assert len(history) == 2

        # Check that both records exist (order may vary due to timing)
        pack_numbers = {h['pack_number'] for h in history}
        assert pack_numbers == {1, 2}

        # Check beats_sent is properly parsed
        for record in history:
            assert record['beats_sent'] == [beat_id]

    def test_duplicate_prevention(self, temp_db):
        """Test duplicate prevention tracking."""
        artist_id = temp_db.add_artist("Test Artist", "test@example.com")
        beat_id = temp_db.add_beat("beat.mp3", "Beat", file_type="mp3")

        # Record beat sent
        temp_db.add_artist_beat_history(artist_id, beat_id)

        # Get recently sent beats
        recent = temp_db.get_recently_sent_beats(artist_id, days=30)
        assert beat_id in recent

    def test_get_last_send_date(self, temp_db):
        """Test getting last send date."""
        artist_id = temp_db.add_artist("Test Artist", "test@example.com")
        beat_id = temp_db.add_beat("beat.mp3", "Beat", file_type="mp3")

        # No sends yet
        assert temp_db.get_last_send_date(artist_id) is None

        # Send email
        temp_db.add_email_history(artist_id, 1, [beat_id], 'sent')

        # Should have a date now
        last_date = temp_db.get_last_send_date(artist_id)
        assert last_date is not None

    def test_context_manager(self):
        """Test database service as context manager."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name

        try:
            with DatabaseService(db_path=db_path) as db:
                db.add_artist("Test", "test@example.com")

            # Connection should be closed
            assert db.connection is None
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
