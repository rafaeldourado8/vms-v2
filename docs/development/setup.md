# Guia de Setup - GT-Vision VMS

## 📋 Pré-requisitos

### Obrigatórios
- Docker Desktop 4.x+
- Python 3.11+
- Poetry 1.7+
- Git

### Recomendados
- VS Code com extensões:
  - Python
  - Docker
  - GitLens
  - Prettier

## 🚀 Setup Passo a Passo

### 1. Clone o Repositório

```bash
git clone <repo-url>
cd GT-Vision-VMS
```

### 2. Instale Dependências Python

```bash
# Instalar Poetry (se não tiver)
pip install poetry

# Instalar dependências do projeto
poetry install

# Ativar ambiente virtual
poetry shell
```

### 3. Configure Pre-commit Hooks

```bash
poetry run pre-commit install
```

### 4. Configure Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com suas configurações
notepad .env
```

### 5. Inicie a Infraestrutura

```bash
# Apenas infraestrutura (para desenvolvimento local)
docker-compose -f docker-compose.dev.yml up -d

# OU todos os serviços
docker-compose up -d
```

### 6. Verifique os Serviços

```bash
# Ver logs
docker-compose logs -f

# Ver status
docker-compose ps
```

## 🧪 Executar Testes

**IMPORTANTE**: Execute os testes sempre da raiz do projeto, não de dentro de subdiretórios!

```bash
# Voltar para a raiz do projeto (se estiver em outro diretório)
cd d:\GT-Vision VMS

# Todos os testes (rápido, sem cobertura)
poetry run pytest

# Apenas unitários
poetry run pytest -m unit

# Apenas integração
poetry run pytest -m integration

# Com cobertura (mais lento)
poetry run pytest --cov=src --cov-report=html --cov-report=term-missing

# Abrir relatório de cobertura
start htmlcov\index.html

# OU use o script automatizado (roda tudo + cobertura)
scripts\test.bat
```

### Sobre Cobertura de Testes

- **Meta do projeto**: 90% de cobertura
- **Durante desenvolvimento**: Cobertura pode estar abaixo da meta
- **Antes de produção**: Deve atingir 90%
- Os testes não falharão por cobertura baixa durante desenvolvimento

## 🔍 Code Quality

```bash
# Formatação automática
poetry run black src/
poetry run isort src/

# Verificar linting
poetry run flake8 src/

# Type checking
poetry run mypy src/

# Security scan
poetry run bandit -r src/
```

## 🐳 Comandos Docker Úteis

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Rebuild de imagens
docker-compose build --no-cache

# Ver logs de um serviço específico
docker-compose logs -f backend

# Executar comando em container
docker-compose exec backend bash
```

## 📝 Workflow de Desenvolvimento

### 1. Antes de Começar
- Leia `.context/PROJECT_CONTEXT.md`
- Verifique `.context/CURRENT_STATE.md`
- Consulte `sprints/sprint-X.md`

### 2. Durante o Desenvolvimento
- Siga arquitetura DDD
- Escreva testes junto com código
- Mantenha complexidade <10
- Use type hints

### 3. Antes de Commit
```bash
# Executar verificações
poetry run black src/
poetry run isort src/
poetry run flake8 src/
poetry run mypy src/
poetry run pytest

# Commit (pre-commit hooks executam automaticamente)
git add .
git commit -m "feat: sua mensagem"
```

### 4. Após Concluir Tarefas
- Atualize `.context/CURRENT_STATE.md`
- Marque tarefas como concluídas
- Documente decisões importantes

## 🔧 Troubleshooting

### Erro: Docker não inicia
```bash
# Verificar se Docker Desktop está rodando
docker --version

# Reiniciar Docker Desktop
```

### Erro: Porta já em uso
```bash
# Verificar portas em uso
netstat -ano | findstr :8000

# Parar processo
taskkill /PID <pid> /F
```

### Erro: Dependências não instaladas
```bash
# Limpar cache e reinstalar
poetry cache clear pypi --all
poetry install
```

### Erro: Testes falhando
```bash
# IMPORTANTE: Execute sempre da raiz do projeto!
cd d:\GT-Vision VMS

# Verificar ambiente
poetry run pytest --collect-only

# Executar teste específico
poetry run pytest src/shared_kernel/tests/test_entity.py -v
```

### Erro: "No module named 'admin'"
```bash
# Certifique-se de estar na raiz do projeto
cd d:\GT-Vision VMS

# NÃO execute de dentro de src/ ou src/admin/
# Execute sempre: poetry run pytest
```

### Cobertura abaixo de 90%
```bash
# Isso é normal durante desenvolvimento
# Os testes não falharão por cobertura baixa

# Para ver quais arquivos precisam de mais testes:
poetry run pytest --cov=src --cov-report=term-missing

# Foque em testar:
# 1. Lógica de negócio (domain/)
# 2. Casos de uso (application/use_cases/)
# 3. Serviços (application/services/)
```

## 📚 Recursos Adicionais

- [Contexto do Projeto](../.context/PROJECT_CONTEXT.md)
- [Planejamento de Sprints](../sprints/README.md)
- [Arquitetura DDD](../docs/architecture/README.md)

## 🆘 Precisa de Ajuda?

1. Consulte `.context/PROJECT_CONTEXT.md`
2. Verifique `sprints/sprint-X.md`
3. Leia documentação em `docs/`
