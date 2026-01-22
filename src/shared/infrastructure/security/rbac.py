"""RBAC - Role-Based Access Control"""
from enum import Enum
from typing import List


class Role(str, Enum):
    ADMIN = "admin"
    GESTOR = "gestor"
    VISUALIZADOR = "visualizador"


class Permission(str, Enum):
    # Streams
    READ_STREAMS = "read:streams"
    WRITE_STREAMS = "write:streams"
    DELETE_STREAMS = "delete:streams"
    
    # Recordings
    READ_RECORDINGS = "read:recordings"
    WRITE_RECORDINGS = "write:recordings"
    DELETE_RECORDINGS = "delete:recordings"
    
    # Users
    READ_USERS = "read:users"
    WRITE_USERS = "write:users"
    DELETE_USERS = "delete:users"
    
    # LGPD
    READ_LGPD = "read:lgpd"
    WRITE_LGPD = "write:lgpd"
    DELETE_DATA = "delete:data"


ROLE_PERMISSIONS: dict[Role, List[Permission]] = {
    Role.ADMIN: [
        Permission.READ_STREAMS,
        Permission.WRITE_STREAMS,
        Permission.DELETE_STREAMS,
        Permission.READ_RECORDINGS,
        Permission.WRITE_RECORDINGS,
        Permission.DELETE_RECORDINGS,
        Permission.READ_USERS,
        Permission.WRITE_USERS,
        Permission.DELETE_USERS,
        Permission.READ_LGPD,
        Permission.WRITE_LGPD,
        Permission.DELETE_DATA,
    ],
    Role.GESTOR: [
        Permission.READ_STREAMS,
        Permission.WRITE_STREAMS,
        Permission.READ_RECORDINGS,
        Permission.WRITE_RECORDINGS,
        Permission.READ_USERS,
    ],
    Role.VISUALIZADOR: [
        Permission.READ_STREAMS,
        Permission.READ_RECORDINGS,
    ],
}


def has_permission(role: Role, permission: Permission) -> bool:
    """Check if role has permission"""
    return permission in ROLE_PERMISSIONS.get(role, [])


def get_permissions(role: Role) -> List[Permission]:
    """Get all permissions for role"""
    return ROLE_PERMISSIONS.get(role, [])
