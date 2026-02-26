"""
Database service for managing SQLite database operations.
Handles artists, beats, email history, and duplicate prevention.
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseService:
    """Service for managing SQLite database operations."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database service.

        Args:
            db_path: Path to SQLite database file. If None, loads from config.
        """
        if db_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            db_path = config['database']['path']

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = None
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
        return self.connection

    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Artists table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                added_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_pack_number INTEGER DEFAULT 0
            )
        """)

        # Beats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS beats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                beat_name TEXT NOT NULL,
                bpm INTEGER,
                key TEXT,
                style_category TEXT,
                file_type TEXT NOT NULL,
                file_size INTEGER,
                added_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Email history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                pack_number INTEGER NOT NULL,
                beats_sent TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'sent',
                error_message TEXT,
                FOREIGN KEY (artist_id) REFERENCES artists(id)
            )
        """)

        # Artist-beat history table (for duplicate prevention)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artist_beat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist_id INTEGER NOT NULL,
                beat_id INTEGER NOT NULL,
                sent_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artists(id),
                FOREIGN KEY (beat_id) REFERENCES beats(id),
                UNIQUE(artist_id, beat_id, sent_date)
            )
        """)

        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_artists_email ON artists(email)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_beats_filename ON beats(filename)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_email_history_artist ON email_history(artist_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_artist_beat_history_artist ON artist_beat_history(artist_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_artist_beat_history_date ON artist_beat_history(sent_date)
        """)

        conn.commit()
        logger.info("Database initialized successfully")

    # ========== Artists CRUD Operations ==========

    def add_artist(self, name: str, email: str) -> int:
        """
        Add a new artist to the database.

        Args:
            name: Artist name
            email: Artist email address

        Returns:
            ID of the newly created artist

        Raises:
            sqlite3.IntegrityError: If email already exists
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO artists (name, email)
                VALUES (?, ?)
            """, (name, email))
            conn.commit()
            artist_id = cursor.lastrowid
            logger.info(f"Added artist: {name} ({email}) with ID {artist_id}")
            return artist_id
        except sqlite3.IntegrityError as e:
            logger.warning(f"Artist with email {email} already exists")
            raise

    def get_artist_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get artist by email address.

        Args:
            email: Artist email address

        Returns:
            Dictionary with artist data or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM artists WHERE email = ?
        """, (email,))

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_all_artists(self) -> List[Dict[str, Any]]:
        """
        Get all artists from database.

        Returns:
            List of artist dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM artists ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]

    def update_artist_pack_number(self, artist_id: int, pack_number: int):
        """
        Update artist's last pack number.

        Args:
            artist_id: Artist ID
            pack_number: New pack number
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE artists
            SET last_pack_number = ?
            WHERE id = ?
        """, (pack_number, artist_id))
        conn.commit()
        logger.debug(f"Updated pack number for artist {artist_id} to {pack_number}")

    # ========== Beats CRUD Operations ==========

    def add_beat(self, filename: str, beat_name: str, bpm: Optional[int] = None,
                 key: Optional[str] = None, style_category: Optional[str] = None,
                 file_type: str = 'mp3', file_size: Optional[int] = None) -> int:
        """
        Add a new beat to the database.

        Args:
            filename: Beat filename
            beat_name: Name of the beat
            bpm: Beats per minute
            key: Musical key
            style_category: Style/artist category
            file_type: File type (mp3, wav, etc.)
            file_size: File size in bytes

        Returns:
            ID of the newly created beat

        Raises:
            sqlite3.IntegrityError: If filename already exists
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO beats (filename, beat_name, bpm, key, style_category, file_type, file_size)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (filename, beat_name, bpm, key, style_category, file_type, file_size))
            conn.commit()
            beat_id = cursor.lastrowid
            logger.info(f"Added beat: {beat_name} (ID: {beat_id})")
            return beat_id
        except sqlite3.IntegrityError as e:
            logger.warning(f"Beat with filename {filename} already exists")
            raise

    def get_beat_by_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Get beat by filename.

        Args:
            filename: Beat filename

        Returns:
            Dictionary with beat data or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM beats WHERE filename = ?", (filename,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_all_beats(self) -> List[Dict[str, Any]]:
        """
        Get all beats from database.

        Returns:
            List of beat dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM beats ORDER BY beat_name")
        return [dict(row) for row in cursor.fetchall()]

    def get_beats_by_ids(self, beat_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get beats by their IDs.

        Args:
            beat_ids: List of beat IDs

        Returns:
            List of beat dictionaries
        """
        if not beat_ids:
            return []

        conn = self._get_connection()
        cursor = conn.cursor()

        placeholders = ','.join('?' * len(beat_ids))
        cursor.execute(f"""
            SELECT * FROM beats WHERE id IN ({placeholders})
        """, beat_ids)

        return [dict(row) for row in cursor.fetchall()]

    # ========== Email History Operations ==========

    def add_email_history(self, artist_id: int, pack_number: int,
                          beats_sent: List[int], status: str = 'sent',
                          error_message: Optional[str] = None) -> int:
        """
        Add email sending history record.

        Args:
            artist_id: Artist ID
            pack_number: Pack number sent
            beats_sent: List of beat IDs sent
            status: Status ('sent', 'failed')
            error_message: Error message if failed

        Returns:
            ID of the newly created history record
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        beats_json = json.dumps(beats_sent)

        cursor.execute("""
            INSERT INTO email_history (artist_id, pack_number, beats_sent, status, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (artist_id, pack_number, beats_json, status, error_message))
        conn.commit()

        history_id = cursor.lastrowid
        logger.info(f"Added email history: artist {artist_id}, pack #{pack_number}, status: {status}")
        return history_id

    def get_email_history(self, artist_id: Optional[int] = None,
                          limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get email history.

        Args:
            artist_id: Filter by artist ID (optional)
            limit: Maximum number of records to return

        Returns:
            List of email history dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT eh.*, a.name as artist_name, a.email as artist_email
            FROM email_history eh
            JOIN artists a ON eh.artist_id = a.id
        """
        params = []

        if artist_id:
            query += " WHERE eh.artist_id = ?"
            params.append(artist_id)

        query += " ORDER BY eh.timestamp DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Parse beats_sent JSON
        result = []
        for row in rows:
            record = dict(row)
            record['beats_sent'] = json.loads(record['beats_sent'])
            result.append(record)

        return result

    # ========== Duplicate Prevention Operations ==========

    def add_artist_beat_history(self, artist_id: int, beat_id: int, sent_date: Optional[str] = None):
        """
        Record that a beat was sent to an artist (for duplicate prevention).

        Args:
            artist_id: Artist ID
            beat_id: Beat ID
            sent_date: Date sent (defaults to current timestamp)
        """
        if sent_date is None:
            sent_date = datetime.now().isoformat()

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO artist_beat_history (artist_id, beat_id, sent_date)
                VALUES (?, ?, ?)
            """, (artist_id, beat_id, sent_date))
            conn.commit()
            logger.debug(f"Recorded beat {beat_id} sent to artist {artist_id}")
        except sqlite3.IntegrityError:
            # Already recorded, ignore
            logger.debug(f"Beat {beat_id} to artist {artist_id} already recorded")

    def get_recently_sent_beats(self, artist_id: int, days: int = 30) -> List[int]:
        """
        Get list of beat IDs sent to an artist within the last N days.

        Args:
            artist_id: Artist ID
            days: Number of days to look back

        Returns:
            List of beat IDs
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT beat_id
            FROM artist_beat_history
            WHERE artist_id = ?
            AND date(sent_date) >= date('now', '-' || ? || ' days')
        """, (artist_id, days))

        return [row[0] for row in cursor.fetchall()]

    def get_last_send_date(self, artist_id: int) -> Optional[str]:
        """
        Get the last date an email was sent to an artist.

        Args:
            artist_id: Artist ID

        Returns:
            ISO format date string or None if never sent
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(timestamp) as last_send
            FROM email_history
            WHERE artist_id = ?
        """, (artist_id,))

        row = cursor.fetchone()
        if row and row[0]:
            return row[0]
        return None

    # ========== Utility Methods ==========

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
