"""
Beat parser service for extracting metadata from filenames.
Parses pattern: @zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3
"""
import re
from typing import Dict, Optional
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BeatParser:
    """Service for parsing beat filenames and extracting metadata."""

    # Pattern: @zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3
    FILENAME_PATTERN = re.compile(
        r'@(\w+)\s*-\s*([^-]+?)\s*-\s*(\d+)\s*-\s*([^-]+?)\s*-\s*([^.]+)\.(\w+)$',
        re.IGNORECASE
    )

    @staticmethod
    def parse_filename(filename: str) -> Optional[Dict[str, str]]:
        """
        Parse beat filename and extract metadata.
        
        Expected format: @zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3
        
        Args:
            filename: Beat filename (e.g., "@zobi - tundra - 136 - Cmin - travis.mp3")
            
        Returns:
            Dictionary with parsed metadata:
            - producer: Producer name (e.g., "zobi")
            - beat_name: Name of the beat (e.g., "tundra")
            - bpm: Beats per minute as string (e.g., "136")
            - key: Musical key (e.g., "Cmin")
            - style_category: Style/artist category (e.g., "travis")
            - file_type: File extension (e.g., "mp3")
            
            Returns None if filename doesn't match pattern
            
        Examples:
            >>> BeatParser.parse_filename("@zobi - tundra - 136 - Cmin - travis.mp3")
            {
                'producer': 'zobi',
                'beat_name': 'tundra',
                'bpm': '136',
                'key': 'Cmin',
                'style_category': 'travis',
                'file_type': 'mp3'
            }
        """
        match = BeatParser.FILENAME_PATTERN.match(filename.strip())
        
        if not match:
            logger.warning(f"Filename doesn't match pattern: {filename}")
            return None
        
        groups = match.groups()
        
        result = {
            'producer': groups[0].strip(),
            'beat_name': groups[1].strip(),
            'bpm': groups[2].strip(),
            'key': groups[3].strip(),
            'style_category': groups[4].strip(),
            'file_type': groups[5].strip().lower()
        }
        
        logger.debug(f"Parsed filename '{filename}': {result}")
        return result

    @staticmethod
    def parse_bpm(bpm_str: str) -> Optional[int]:
        """
        Convert BPM string to integer.
        
        Args:
            bpm_str: BPM as string
            
        Returns:
            BPM as integer, or None if invalid
        """
        try:
            return int(bpm_str)
        except (ValueError, TypeError):
            logger.warning(f"Invalid BPM value: {bpm_str}")
            return None

    @staticmethod
    def extract_beat_name(filename: str) -> str:
        """
        Extract beat name from filename, even if pattern doesn't match.
        Falls back to filename without extension.
        
        Args:
            filename: Beat filename
            
        Returns:
            Beat name (best guess)
        """
        parsed = BeatParser.parse_filename(filename)
        if parsed:
            return parsed['beat_name']
        
        # Fallback: remove extension
        return Path(filename).stem

    @staticmethod
    def is_valid_beat_file(filename: str) -> bool:
        """
        Check if filename appears to be a valid beat file.
        
        Args:
            filename: Filename to check
            
        Returns:
            True if filename matches expected pattern
        """
        return BeatParser.parse_filename(filename) is not None

    @staticmethod
    def batch_parse(filenames: list[str]) -> Dict[str, Optional[Dict[str, str]]]:
        """
        Parse multiple filenames at once.
        
        Args:
            filenames: List of filenames to parse
            
        Returns:
            Dictionary mapping filename to parsed metadata (or None if invalid)
        """
        results = {}
        for filename in filenames:
            results[filename] = BeatParser.parse_filename(filename)
        return results
