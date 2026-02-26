"""
Beat selection service for randomly selecting 3-5 beats per artist.
Implements duplicate prevention (30-day rule).
"""
import random
from typing import List, Optional
from pathlib import Path
import yaml
from services.database_service import DatabaseService
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BeatSelectionService:
    """Service for selecting random beats per artist with duplicate prevention."""

    def __init__(
        self,
        db: DatabaseService,
        min_beats: int = 3,
        max_beats: int = 5,
        duplicate_prevention_days: int = 30,
    ):
        """
        Initialize beat selection service.

        Args:
            db: DatabaseService instance
            min_beats: Minimum beats per email
            max_beats: Maximum beats per email
            duplicate_prevention_days: Days to exclude recently sent beats
        """
        self.db = db
        self.min_beats = min_beats
        self.max_beats = max_beats
        self.duplicate_prevention_days = duplicate_prevention_days

    @classmethod
    def from_config(cls, db: DatabaseService) -> "BeatSelectionService":
        """Create service from config.yaml."""
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        beats_config = config["beats"]
        return cls(
            db=db,
            min_beats=beats_config.get("min_beats_per_email", 3),
            max_beats=beats_config.get("max_beats_per_email", 5),
            duplicate_prevention_days=beats_config.get("duplicate_prevention_days", 30),
        )

    def select_beats_for_artist(self, artist_id: int) -> List[int]:
        """
        Select 3-5 random beats for an artist, excluding recently sent beats.

        Args:
            artist_id: Artist ID

        Returns:
            List of beat IDs (3-5 beats)
        """
        all_beats = self.db.get_all_beats()
        if not all_beats:
            logger.warning("No beats in database")
            return []

        all_beat_ids = [b["id"] for b in all_beats]
        recently_sent = self.db.get_recently_sent_beats(
            artist_id, days=self.duplicate_prevention_days
        )
        available_ids = [bid for bid in all_beat_ids if bid not in recently_sent]

        if not available_ids:
            logger.warning(
                f"Artist {artist_id}: no beats available (all sent in last {self.duplicate_prevention_days} days)"
            )
            available_ids = all_beat_ids

        count = min(
            random.randint(self.min_beats, self.max_beats),
            len(available_ids),
        )
        count = max(1, count)
        selected = random.sample(available_ids, count)
        logger.info(f"Selected {len(selected)} beats for artist {artist_id}")
        return selected
