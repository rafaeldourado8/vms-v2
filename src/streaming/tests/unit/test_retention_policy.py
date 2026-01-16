"""Tests for RetentionPolicy value object."""
import pytest
from src.streaming.domain.value_objects.retention_policy import RetentionPolicy
from src.shared_kernel.domain.domain_exception import DomainException


def test_retention_policy_valid():
    """Test valid retention policy."""
    policy = RetentionPolicy(7)
    assert policy.days == 7
    
    policy = RetentionPolicy(15)
    assert policy.days == 15
    
    policy = RetentionPolicy(30)
    assert policy.days == 30


def test_retention_policy_invalid():
    """Test invalid retention policy."""
    with pytest.raises(DomainException):
        RetentionPolicy(5)
    
    with pytest.raises(DomainException):
        RetentionPolicy(60)


def test_retention_policy_equality():
    """Test retention policy equality."""
    policy1 = RetentionPolicy(7)
    policy2 = RetentionPolicy(7)
    policy3 = RetentionPolicy(15)
    
    assert policy1 == policy2
    assert policy1 != policy3
