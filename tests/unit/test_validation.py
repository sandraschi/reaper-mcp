"""
Unit tests for reaper_mcp.validation module
Tests input validation functions for MCP server
"""

import pytest
from reaper_mcp.validation import (
    TrackValidation,
    TransportValidation,
    ProjectValidation,
    CommonValidation,
    ValidationError,
)


class TestTrackValidation:
    """Test track-related validation functions"""

    def test_validate_track_id_valid(self):
        """Test valid track ID validation"""
        assert TrackValidation.validate_track_id(1) == 1
        assert TrackValidation.validate_track_id(100) == 100
        assert TrackValidation.validate_track_id("5") == 5
        assert TrackValidation.validate_track_id("track 3") == 3

    def test_validate_track_id_invalid(self):
        """Test invalid track ID validation"""
        with pytest.raises(ValidationError, match="Track ID must be 1 or greater"):
            TrackValidation.validate_track_id(0)

        with pytest.raises(ValidationError, match="Track ID must be 1 or greater"):
            TrackValidation.validate_track_id(-1)

        with pytest.raises(ValidationError, match="Track ID seems too high"):
            TrackValidation.validate_track_id(1001)

        with pytest.raises(ValidationError, match="Could not extract track number"):
            TrackValidation.validate_track_id("invalid")

        with pytest.raises(ValidationError, match="Track ID must be a number"):
            TrackValidation.validate_track_id([1, 2, 3])

    def test_validate_track_id_allow_zero(self):
        """Test track ID validation with allow_zero=True"""
        assert TrackValidation.validate_track_id(0, allow_zero=True) == 0
        assert TrackValidation.validate_track_id(1, allow_zero=True) == 1

    def test_validate_track_range_valid(self):
        """Test valid track range validation"""
        assert TrackValidation.validate_track_range([1, 2, 3]) == [1, 2, 3]
        assert TrackValidation.validate_track_range(["1", "2", "3"]) == [1, 2, 3]

    def test_validate_track_range_invalid(self):
        """Test invalid track range validation"""
        with pytest.raises(ValidationError, match="Track IDs must be a list"):
            TrackValidation.validate_track_range(1)

        with pytest.raises(ValidationError, match="cannot be empty"):
            TrackValidation.validate_track_range([])

        with pytest.raises(ValidationError, match="Too many tracks specified"):
            TrackValidation.validate_track_range(list(range(1, 102)))

        with pytest.raises(ValidationError, match="Track ID 1:"):
            TrackValidation.validate_track_range([0, 1, 2])


class TestTransportValidation:
    """Test transport-related validation functions"""

    def test_validate_position_valid(self):
        """Test valid position validation"""
        assert TransportValidation.validate_position(0) == "0"
        assert TransportValidation.validate_position(90.5) == "90.5"
        assert TransportValidation.validate_position("1:30") == "1:30"
        assert TransportValidation.validate_position("1:30:45") == "1:30:45"

    def test_validate_position_invalid(self):
        """Test invalid position validation"""
        with pytest.raises(ValidationError, match="cannot be negative"):
            TransportValidation.validate_position(-1)

        with pytest.raises(ValidationError, match="seems too large"):
            TransportValidation.validate_position(90000)  # 25 hours

        with pytest.raises(ValidationError, match="Invalid time format"):
            TransportValidation.validate_position("invalid")

        with pytest.raises(ValidationError, match="must be a number or time string"):
            TransportValidation.validate_position([1, 2, 3])


class TestProjectValidation:
    """Test project-related validation functions"""

    def test_validate_marker_name_valid(self):
        """Test valid marker name validation"""
        assert ProjectValidation.validate_marker_name("Verse 1") == "Verse 1"
        assert ProjectValidation.validate_marker_name("  Chorus  ") == "Chorus"
        assert (
            ProjectValidation.validate_marker_name("Marker with 123")
            == "Marker with 123"
        )

    def test_validate_marker_name_invalid(self):
        """Test invalid marker name validation"""
        with pytest.raises(ValidationError, match="must be a string"):
            ProjectValidation.validate_marker_name(123)

        with pytest.raises(ValidationError, match="cannot be empty"):
            ProjectValidation.validate_marker_name("")

        with pytest.raises(ValidationError, match="cannot be empty"):
            ProjectValidation.validate_marker_name("   ")

        with pytest.raises(ValidationError, match="too long"):
            ProjectValidation.validate_marker_name("a" * 201)

        with pytest.raises(ValidationError, match="invalid character"):
            ProjectValidation.validate_marker_name("Test\nMarker")

    def test_validate_render_format_valid(self):
        """Test valid render format validation"""
        valid_formats = ["wav", "mp3", "flac", "ogg", "wma", "aiff", "au"]
        for fmt in valid_formats:
            assert ProjectValidation.validate_render_format(fmt) == fmt.lower()
            assert ProjectValidation.validate_render_format(fmt.upper()) == fmt.lower()

    def test_validate_render_format_invalid(self):
        """Test invalid render format validation"""
        with pytest.raises(ValidationError, match="Unsupported format"):
            ProjectValidation.validate_render_format("invalid")

    def test_validate_quality_valid(self):
        """Test valid quality validation"""
        valid_qualities = ["high", "medium", "low", "fast"]
        for quality in valid_qualities:
            assert ProjectValidation.validate_quality(quality) == quality.lower()
            assert (
                ProjectValidation.validate_quality(quality.upper()) == quality.lower()
            )

    def test_validate_quality_invalid(self):
        """Test invalid quality validation"""
        with pytest.raises(ValidationError, match="Invalid quality"):
            ProjectValidation.validate_quality("invalid")


class TestCommonValidation:
    """Test common validation functions"""

    def test_validate_boolean_valid(self):
        """Test valid boolean validation"""
        # True values
        true_values = [
            True,
            1,
            "true",
            "True",
            "TRUE",
            "yes",
            "Yes",
            "YES",
            "1",
            "on",
            "On",
            "ON",
            "enabled",
            "Enabled",
        ]
        for value in true_values:
            assert CommonValidation.validate_boolean(value) is True

        # False values
        false_values = [
            False,
            0,
            "false",
            "False",
            "FALSE",
            "no",
            "No",
            "NO",
            "0",
            "off",
            "Off",
            "OFF",
            "disabled",
            "Disabled",
        ]
        for value in false_values:
            assert CommonValidation.validate_boolean(value) is False

    def test_validate_boolean_invalid(self):
        """Test invalid boolean validation"""
        with pytest.raises(ValidationError, match="Integer boolean must be 0 or 1"):
            CommonValidation.validate_boolean(2)

        with pytest.raises(ValidationError, match="Cannot interpret"):
            CommonValidation.validate_boolean("maybe")

        with pytest.raises(ValidationError, match="Boolean expected"):
            CommonValidation.validate_boolean([1, 2, 3])


if __name__ == "__main__":
    pytest.main([__file__])
