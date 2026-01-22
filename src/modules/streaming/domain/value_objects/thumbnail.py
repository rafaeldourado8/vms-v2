"""Thumbnail value object."""
from datetime import datetime
from src.shared_kernel.domain.value_object import ValueObject


class Thumbnail(ValueObject):
    """Thumbnail for video preview."""
    
    def __init__(self, timestamp: datetime, url: str, width: int = 160, height: int = 90):
        self._timestamp = timestamp
        self._url = url
        self._width = width
        self._height = height
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height
    
    def _get_equality_components(self):
        return [self._timestamp, self._url]
