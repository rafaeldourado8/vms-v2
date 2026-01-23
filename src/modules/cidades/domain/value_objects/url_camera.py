"""URL Camera value object."""
from urllib.parse import urlparse
from src.shared.domain.value_object import ValueObject
from src.shared.domain.domain_exception import DomainException


class URLCamera(ValueObject):
    """URL Camera value object."""

    def __init__(self, value: str):
        if not value:
            raise DomainException("URL da camera nao pode ser vazia")
        
        parsed = urlparse(value)
        
        if parsed.scheme not in ["rtsp", "rtmp"]:
            raise DomainException("URL deve usar protocolo RTSP ou RTMP")
        
        if not parsed.netloc:
            raise DomainException("URL invalida")
        
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, URLCamera):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
