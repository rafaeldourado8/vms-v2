"""Mosaic entity."""
from uuid import UUID
from typing import List
from src.shared_kernel.domain.entity import Entity
from src.shared_kernel.domain.domain_exception import DomainException


class Mosaic(Entity):
    """Mosaic entity for multi-camera view."""
    
    MAX_CAMERAS = 4
    
    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        name: str,
        layout: str = "2x2",
        camera_ids: List[UUID] = None
    ):
        super().__init__(id)
        self.user_id = user_id
        self.name = name
        self.layout = layout
        self.camera_ids = camera_ids or []
        self._validate()
    
    def _validate(self):
        """Validate mosaic."""
        if len(self.camera_ids) > self.MAX_CAMERAS:
            raise DomainException(f"Maximum {self.MAX_CAMERAS} cameras allowed per mosaic")
    
    def add_camera(self, camera_id: UUID):
        """Add camera to mosaic."""
        if len(self.camera_ids) >= self.MAX_CAMERAS:
            raise DomainException(f"Maximum {self.MAX_CAMERAS} cameras allowed")
        if camera_id in self.camera_ids:
            raise DomainException("Camera already in mosaic")
        self.camera_ids.append(camera_id)
    
    def remove_camera(self, camera_id: UUID):
        """Remove camera from mosaic."""
        if camera_id not in self.camera_ids:
            raise DomainException("Camera not in mosaic")
        self.camera_ids.remove(camera_id)
    
    def update_layout(self, layout: str):
        """Update mosaic layout."""
        self.layout = layout
