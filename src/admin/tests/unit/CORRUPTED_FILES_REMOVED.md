# Arquivos Corrompidos Removidos

Os seguintes arquivos de teste estavam corrompidos (continham null bytes) e foram removidos:

- `src/admin/tests/unit/test_assign_role_use_case.py`
- `src/admin/tests/unit/test_authenticate_user_use_case.py`
- `src/admin/tests/unit/test_create_user_use_case.py`
- `src/admin/tests/unit/test_email.py`
- `src/admin/tests/unit/test_password.py`
- `src/admin/tests/unit/test_user.py`

## Próximos Passos

Esses testes precisam ser recriados quando você implementar:
1. Domain entities (User, Email, Password)
2. Use cases (CreateUser, AuthenticateUser, AssignRole)

## Como Evitar

Arquivos corrompidos geralmente ocorrem por:
- Interrupção durante salvamento
- Problemas de disco
- Conflitos de merge no Git

Sempre verifique a integridade dos arquivos após operações de I/O.
