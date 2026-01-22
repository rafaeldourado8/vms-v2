"""Tests for RBAC"""
import pytest
from src.shared_kernel.infrastructure.security.rbac import (
    Role,
    Permission,
    has_permission,
    get_permissions,
)


def test_admin_has_all_permissions():
    """Test admin has all permissions"""
    assert has_permission(Role.ADMIN, Permission.READ_STREAMS)
    assert has_permission(Role.ADMIN, Permission.WRITE_STREAMS)
    assert has_permission(Role.ADMIN, Permission.DELETE_STREAMS)
    assert has_permission(Role.ADMIN, Permission.DELETE_DATA)


def test_gestor_has_limited_permissions():
    """Test gestor has limited permissions"""
    assert has_permission(Role.GESTOR, Permission.READ_STREAMS)
    assert has_permission(Role.GESTOR, Permission.WRITE_STREAMS)
    assert not has_permission(Role.GESTOR, Permission.DELETE_USERS)
    assert not has_permission(Role.GESTOR, Permission.DELETE_DATA)


def test_visualizador_has_read_only():
    """Test visualizador has read-only permissions"""
    assert has_permission(Role.VISUALIZADOR, Permission.READ_STREAMS)
    assert has_permission(Role.VISUALIZADOR, Permission.READ_RECORDINGS)
    assert not has_permission(Role.VISUALIZADOR, Permission.WRITE_STREAMS)
    assert not has_permission(Role.VISUALIZADOR, Permission.DELETE_STREAMS)


def test_get_permissions():
    """Test get all permissions for role"""
    admin_perms = get_permissions(Role.ADMIN)
    gestor_perms = get_permissions(Role.GESTOR)
    visualizador_perms = get_permissions(Role.VISUALIZADOR)
    
    assert len(admin_perms) > len(gestor_perms)
    assert len(gestor_perms) > len(visualizador_perms)
