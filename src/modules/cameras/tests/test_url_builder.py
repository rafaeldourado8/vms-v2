import pytest
from src.modules.cameras.domain.services.url_builder import (
    UrlBuilderFactory,
    IntelbrasUrlBuilder,
    HikvisionUrlBuilder,
)


class TestUrlBuilder:
    def test_intelbras_url_builder(self):
        builder = IntelbrasUrlBuilder()
        url = builder.build(
            ip="192.168.1.100",
            user="admin",
            password="123456",
            channel=1,
            subtype=0
        )
        assert url == "rtsp://admin:123456@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0"
    
    def test_intelbras_custom_port(self):
        builder = IntelbrasUrlBuilder()
        url = builder.build(
            ip="192.168.1.100",
            user="admin",
            password="123456",
            port=8554
        )
        assert "192.168.1.100:8554" in url
    
    def test_hikvision_url_builder(self):
        builder = HikvisionUrlBuilder()
        url = builder.build(
            ip="192.168.1.200",
            user="admin",
            password="abc123",
            channel=1
        )
        assert url == "rtsp://admin:abc123@192.168.1.200:554/Streaming/Channels/101"
    
    def test_factory_intelbras(self):
        builder = UrlBuilderFactory.get_builder("intelbras")
        assert isinstance(builder, IntelbrasUrlBuilder)
    
    def test_factory_hikvision(self):
        builder = UrlBuilderFactory.get_builder("hikvision")
        assert isinstance(builder, HikvisionUrlBuilder)
    
    def test_factory_case_insensitive(self):
        builder = UrlBuilderFactory.get_builder("INTELBRAS")
        assert isinstance(builder, IntelbrasUrlBuilder)
    
    def test_factory_unsupported_brand(self):
        with pytest.raises(ValueError, match="Marca não suportada"):
            UrlBuilderFactory.get_builder("unknown_brand")
    
    def test_supported_brands(self):
        brands = UrlBuilderFactory.supported_brands()
        assert "intelbras" in brands
        assert "hikvision" in brands
        assert "dahua" in brands
