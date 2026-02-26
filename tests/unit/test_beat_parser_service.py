"""
Unit tests for beat parser service.
"""
import pytest
from services.beat_parser_service import BeatParser


class TestBeatParser:
    """Test cases for BeatParser."""

    def test_parse_valid_filename(self):
        """Test parsing a valid filename."""
        filename = "@zobi - tundra - 136 - Cmin - travis.mp3"
        result = BeatParser.parse_filename(filename)

        assert result is not None
        assert result['producer'] == 'zobi'
        assert result['beat_name'] == 'tundra'
        assert result['bpm'] == '136'
        assert result['key'] == 'Cmin'
        assert result['style_category'] == 'travis'
        assert result['file_type'] == 'mp3'

    def test_parse_filename_with_spaces(self):
        """Test parsing filename with spaces in beat name."""
        filename = "@zobi - canary diamonds - 125 - Dmaj - gunna.wav"
        result = BeatParser.parse_filename(filename)

        assert result is not None
        assert result['beat_name'] == 'canary diamonds'
        assert result['bpm'] == '125'
        assert result['key'] == 'Dmaj'
        assert result['style_category'] == 'gunna'
        assert result['file_type'] == 'wav'

    def test_parse_filename_with_special_chars(self):
        """Test parsing filename with special characters in key."""
        filename = "@zobi - splash - 116 - F#min - afrobeat.mp3"
        result = BeatParser.parse_filename(filename)

        assert result is not None
        assert result['beat_name'] == 'splash'
        assert result['key'] == 'F#min'
        assert result['style_category'] == 'afrobeat'

    def test_parse_invalid_filename(self):
        """Test parsing an invalid filename."""
        filename = "invalid_filename.mp3"
        result = BeatParser.parse_filename(filename)

        assert result is None

    def test_parse_filename_missing_parts(self):
        """Test parsing filename with missing parts."""
        filename = "@zobi - beat.mp3"
        result = BeatParser.parse_filename(filename)

        assert result is None

    def test_parse_bpm_valid(self):
        """Test parsing valid BPM."""
        assert BeatParser.parse_bpm("136") == 136
        assert BeatParser.parse_bpm("75") == 75

    def test_parse_bpm_invalid(self):
        """Test parsing invalid BPM."""
        assert BeatParser.parse_bpm("abc") is None
        assert BeatParser.parse_bpm("") is None

    def test_extract_beat_name_valid(self):
        """Test extracting beat name from valid filename."""
        filename = "@zobi - tundra - 136 - Cmin - travis.mp3"
        beat_name = BeatParser.extract_beat_name(filename)
        assert beat_name == "tundra"

    def test_extract_beat_name_invalid(self):
        """Test extracting beat name from invalid filename (fallback)."""
        filename = "random_file.mp3"
        beat_name = BeatParser.extract_beat_name(filename)
        assert beat_name == "random_file"

    def test_is_valid_beat_file(self):
        """Test checking if filename is valid beat file."""
        assert BeatParser.is_valid_beat_file("@zobi - tundra - 136 - Cmin - travis.mp3") is True
        assert BeatParser.is_valid_beat_file("invalid.mp3") is False

    def test_batch_parse(self):
        """Test batch parsing multiple filenames."""
        filenames = [
            "@zobi - tundra - 136 - Cmin - travis.mp3",
            "@zobi - hope - 75 - Cmin - future.mp3",
            "invalid.mp3"
        ]

        results = BeatParser.batch_parse(filenames)

        assert len(results) == 3
        assert results[filenames[0]] is not None
        assert results[filenames[1]] is not None
        assert results[filenames[2]] is None

    def test_case_insensitive(self):
        """Test that parsing is case-insensitive."""
        filename = "@ZOBI - TUNDRA - 136 - CMIN - TRAVIS.MP3"
        result = BeatParser.parse_filename(filename)

        assert result is not None
        assert result['producer'].lower() == 'zobi'
        assert result['file_type'] == 'mp3'
