from abc import ABC, abstractmethod
from typing import Optional


class UrlBuilder(ABC):
    @abstractmethod
    def build(
        self,
        ip: str,
        user: str,
        password: str,
        channel: int = 1,
        subtype: int = 0,
        port: Optional[int] = None,
    ) -> str:
        pass


class IntelbrasUrlBuilder(UrlBuilder):
    def build(
        self,
        ip: str,
        user: str,
        password: str,
        channel: int = 1,
        subtype: int = 0,
        port: Optional[int] = None,
    ) -> str:
        port = port or 554
        return f"rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"


class HikvisionUrlBuilder(UrlBuilder):
    def build(
        self,
        ip: str,
        user: str,
        password: str,
        channel: int = 1,
        subtype: int = 0,
        port: Optional[int] = None,
    ) -> str:
        port = port or 554
        stream = "main" if subtype == 0 else "sub"
        return f"rtsp://{user}:{password}@{ip}:{port}/Streaming/Channels/{channel}01"


class DahuaUrlBuilder(UrlBuilder):
    def build(
        self,
        ip: str,
        user: str,
        password: str,
        channel: int = 1,
        subtype: int = 0,
        port: Optional[int] = None,
    ) -> str:
        port = port or 554
        return f"rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}"


class UrlBuilderFactory:
    _builders = {
        "intelbras": IntelbrasUrlBuilder,
        "hikvision": HikvisionUrlBuilder,
        "dahua": DahuaUrlBuilder,
    }

    @staticmethod
    def get_builder(marca: str) -> UrlBuilder:
        marca_lower = marca.lower()
        builder_class = UrlBuilderFactory._builders.get(marca_lower)
        if not builder_class:
            raise ValueError(f"Marca não suportada: {marca}")
        return builder_class()

    @staticmethod
    def supported_brands() -> list[str]:
        return list(UrlBuilderFactory._builders.keys())
