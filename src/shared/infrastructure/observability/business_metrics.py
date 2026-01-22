"""Business metrics for GT-Vision VMS."""
from prometheus_client import Gauge, Counter


# Business Metrics
gtvision_active_streams = Gauge('gtvision_active_streams', 'Active streams')
gtvision_recordings_active = Gauge('gtvision_recordings_active', 'Active recordings')
gtvision_lpr_events_total = Counter('gtvision_lpr_events_total', 'Total LPR events')
gtvision_cameras_online = Gauge('gtvision_cameras_online', 'Online cameras')
gtvision_cameras_offline = Gauge('gtvision_cameras_offline', 'Offline cameras')
gtvision_cameras_total = Gauge('gtvision_cameras_total', 'Total cameras')
gtvision_recording_errors_total = Counter('gtvision_recording_errors_total', 'Recording errors')


class BusinessMetrics:
    """Business metrics helper."""
    
    @staticmethod
    def update_active_streams(count: int) -> None:
        """Update active streams count."""
        gtvision_active_streams.set(count)
    
    @staticmethod
    def update_active_recordings(count: int) -> None:
        """Update active recordings count."""
        gtvision_recordings_active.set(count)
    
    @staticmethod
    def increment_lpr_events() -> None:
        """Increment LPR events counter."""
        gtvision_lpr_events_total.inc()
    
    @staticmethod
    def update_cameras_status(online: int, offline: int, total: int) -> None:
        """Update cameras status."""
        gtvision_cameras_online.set(online)
        gtvision_cameras_offline.set(offline)
        gtvision_cameras_total.set(total)
    
    @staticmethod
    def increment_recording_errors() -> None:
        """Increment recording errors counter."""
        gtvision_recording_errors_total.inc()
