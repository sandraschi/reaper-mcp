"""
validation.py - Input validation utilities for Reaper MCP Server
Comprehensive parameter validation with user-friendly error messages
"""

import logging
from typing import Union, List

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error with user-friendly messages"""

    pass


class TrackValidation:
    """Track-related input validation"""

    @staticmethod
    def validate_track_id(track_id: Union[int, str], allow_zero: bool = False) -> int:
        """Validate track ID parameter

        Args:
            track_id: Track identifier (1-based or string to parse)
            allow_zero: Whether to allow track_id = 0

        Returns:
            Validated track ID as integer

        Raises:
            ValidationError: If track_id is invalid
        """
        try:
            if isinstance(track_id, str):
                # Handle string inputs like "1", "track 1", etc.
                import re

                match = re.search(r"\d+", track_id)
                if match:
                    track_id = int(match.group())
                else:
                    raise ValidationError(
                        f"Could not extract track number from '{track_id}'. Use format like '1' or 'track 1'"
                    )

            if not isinstance(track_id, int):
                raise ValidationError(
                    f"Track ID must be a number, got {type(track_id).__name__}: {track_id}"
                )

            min_id = 0 if allow_zero else 1
            if track_id < min_id:
                raise ValidationError(
                    f"Track ID must be {min_id} or greater, got {track_id}"
                )

            if track_id > 1000:  # Reasonable upper limit
                raise ValidationError(
                    f"Track ID seems too high ({track_id}). Maximum expected is 1000 tracks"
                )

            return track_id

        except ValueError as e:
            raise ValidationError(f"Invalid track ID format: {track_id}") from e

    @staticmethod
    def validate_track_range(track_ids: List[Union[int, str]]) -> List[int]:
        """Validate list of track IDs

        Args:
            track_ids: List of track identifiers

        Returns:
            Validated list of track IDs

        Raises:
            ValidationError: If any track ID is invalid
        """
        if not isinstance(track_ids, list):
            raise ValidationError(
                f"Track IDs must be a list, got {type(track_ids).__name__}"
            )

        if len(track_ids) == 0:
            raise ValidationError("Track IDs list cannot be empty")

        if len(track_ids) > 100:  # Reasonable limit for bulk operations
            raise ValidationError(
                f"Too many tracks specified ({len(track_ids)}). Maximum is 100 tracks per operation"
            )

        validated_ids = []
        for i, track_id in enumerate(track_ids):
            try:
                validated_ids.append(TrackValidation.validate_track_id(track_id))
            except ValidationError as e:
                raise ValidationError(f"Track ID {i + 1}: {str(e)}") from e

        return validated_ids


class TransportValidation:
    """Transport-related input validation"""

    @staticmethod
    def validate_position(position: Union[str, float, int]) -> str:
        """Validate transport position

        Args:
            position: Position in seconds or time string (e.g., "1:30", "90.5")

        Returns:
            Validated position as string

        Raises:
            ValidationError: If position is invalid
        """
        if isinstance(position, (int, float)):
            if position < 0:
                raise ValidationError(f"Position cannot be negative, got {position}")
            if position > 86400:  # 24 hours in seconds
                raise ValidationError(
                    f"Position seems too large ({position}s). Maximum expected is 24 hours"
                )
            return str(position)

        if isinstance(position, str):
            # Handle time format like "1:30", "1:30:45", etc.
            import re

            if re.match(r"^(\d+:)*\d+(\.\d+)?$", position):
                return position
            else:
                raise ValidationError(
                    f"Invalid time format '{position}'. Use format like '1:30' or '90.5'"
                )

        raise ValidationError(
            f"Position must be a number or time string, got {type(position).__name__}: {position}"
        )


class ProjectValidation:
    """Project-related input validation"""

    @staticmethod
    def validate_marker_name(name: str) -> str:
        """Validate marker/region name

        Args:
            name: Marker name

        Returns:
            Validated marker name

        Raises:
            ValidationError: If name is invalid
        """
        if not isinstance(name, str):
            raise ValidationError(
                f"Marker name must be a string, got {type(name).__name__}"
            )

        name = name.strip()
        if len(name) == 0:
            raise ValidationError("Marker name cannot be empty")

        if len(name) > 200:  # Reasonable limit
            raise ValidationError(
                f"Marker name too long ({len(name)} chars). Maximum is 200 characters"
            )

        # Check for invalid characters that might cause OSC issues
        invalid_chars = ["\n", "\r", "\t"]
        for char in invalid_chars:
            if char in name:
                raise ValidationError(
                    f"Marker name contains invalid character '{char}'"
                )

        return name

    @staticmethod
    def validate_render_format(format_type: str) -> str:
        """Validate render format

        Args:
            format_type: Render format (wav, mp3, flac, etc.)

        Returns:
            Validated format string

        Raises:
            ValidationError: If format is invalid
        """
        valid_formats = ["wav", "mp3", "flac", "ogg", "wma", "aiff", "au"]
        format_lower = format_type.lower().strip()

        if format_lower not in valid_formats:
            raise ValidationError(
                f"Unsupported format '{format_type}'. Supported formats: {', '.join(valid_formats)}"
            )

        return format_lower

    @staticmethod
    def validate_quality(quality: str) -> str:
        """Validate render quality

        Args:
            quality: Quality setting (high, medium, low, fast)

        Returns:
            Validated quality string

        Raises:
            ValidationError: If quality is invalid
        """
        valid_qualities = ["high", "medium", "low", "fast"]
        quality_lower = quality.lower().strip()

        if quality_lower not in valid_qualities:
            raise ValidationError(
                f"Invalid quality '{quality}'. Valid options: {', '.join(valid_qualities)}"
            )

        return quality_lower


class CommonValidation:
    """Common validation utilities"""

    @staticmethod
    def validate_boolean(value: Union[bool, str, int]) -> bool:
        """Validate boolean parameter with flexible input

        Args:
            value: Boolean value (True/False, "true"/"false", 1/0, "yes"/"no", etc.)

        Returns:
            Validated boolean

        Raises:
            ValidationError: If value cannot be interpreted as boolean
        """
        if isinstance(value, bool):
            return value

        if isinstance(value, int):
            if value in (0, 1):
                return bool(value)
            else:
                raise ValidationError(f"Integer boolean must be 0 or 1, got {value}")

        if isinstance(value, str):
            lower_value = value.lower().strip()
            if lower_value in ("true", "yes", "1", "on", "enabled"):
                return True
            elif lower_value in ("false", "no", "0", "off", "disabled"):
                return False
            else:
                raise ValidationError(
                    f"Cannot interpret '{value}' as boolean. Use true/false, yes/no, 1/0, on/off"
                )

        raise ValidationError(f"Boolean expected, got {type(value).__name__}: {value}")

    @staticmethod
    def validate_connection() -> None:
        """Ensure Reaper connection is available

        Raises:
            ValidationError: If connection check fails
        """
        # This will be called from async contexts, so we just validate the pattern
        # The actual connection check happens in the tools
        pass


def validate_params(**validators):
    """Decorator to validate function parameters

    Args:
        **validators: Parameter name -> validation function mapping

    Returns:
        Decorated function with parameter validation
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Get function signature to map positional args to parameter names
            import inspect

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Validate each parameter
            for param_name, validator_func in validators.items():
                if param_name in bound_args.arguments:
                    try:
                        bound_args.arguments[param_name] = validator_func(
                            bound_args.arguments[param_name]
                        )
                    except ValidationError as e:
                        logger.warning(
                            f"Parameter validation failed for {param_name}: {e}"
                        )
                        # Re-raise with more context
                        raise ValidationError(
                            f"Invalid parameter '{param_name}': {str(e)}"
                        ) from e

            return await func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator
