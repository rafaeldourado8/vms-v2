# 🐍 Instalar Python 3.12 no Windows

## ⚠️ Problema Atual

Você tem Python 3.10.11, mas o projeto requer Python 3.12+

## ✅ Solução: Instalar Python 3.12

### Opção 1: Instalador Oficial (RECOMENDADO)

1. **Download Python 3.12**
   - Acesse: https://www.python.org/downloads/
   - Baixe: Python 3.12.x (latest)

2. **Instalar**
   - Execute o instalador
   - ✅ **IMPORTANTE**: Marque "Add Python 3.12 to PATH"
   - Clique "Install Now"

3. **Verificar Instalação**
   ```bash
   python --version
   # Deve mostrar: Python 3.12.x
   ```

4. **Reinstalar Poetry**
   ```bash
   pip install --upgrade poetry
   ```

5. **Instalar Dependências**
   ```bash
   cd d:\vms-v2
   poetry install
   ```

---

### Opção 2: Chocolatey (Gerenciador de Pacotes)

1. **Instalar Chocolatey** (se não tiver)
   - Abra PowerShell como Administrador
   - Execute:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Instalar Python 3.12**
   ```bash
   choco install python312 -y
   ```

3. **Verificar**
   ```bash
   python --version
   ```

4. **Reinstalar Poetry**
   ```bash
   pip install --upgrade poetry
   ```

5. **Instalar Dependências**
   ```bash
   cd d:\vms-v2
   poetry install
   ```

---

### Opção 3: pyenv-win (Múltiplas Versões)

1. **Instalar pyenv-win**
   ```powershell
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
   ```

2. **Reiniciar terminal**

3. **Instalar Python 3.12**
   ```bash
   pyenv install 3.12.0
   pyenv global 3.12.0
   ```

4. **Verificar**
   ```bash
   python --version
   ```

5. **Reinstalar Poetry**
   ```bash
   pip install --upgrade poetry
   ```

6. **Instalar Dependências**
   ```bash
   cd d:\vms-v2
   poetry install
   ```

---

## 🔧 Troubleshooting

### Problema: Python 3.10 ainda aparece

**Solução 1: Remover Python 3.10 do PATH**
1. Pesquisar "Variáveis de Ambiente"
2. Editar "Path" do usuário
3. Remover entradas do Python 3.10
4. Adicionar Python 3.12 no topo

**Solução 2: Usar caminho completo**
```bash
# Encontrar Python 3.12
where python

# Usar caminho completo
C:\Python312\python.exe --version
```

### Problema: Poetry não encontra Python 3.12

```bash
# Recriar ambiente Poetry
poetry env remove python
poetry env use python3.12
poetry install
```

### Problema: Múltiplas versões Python

```bash
# Listar versões
py -0

# Usar versão específica
py -3.12 --version

# Configurar Poetry para usar 3.12
poetry env use py -3.12
```

---

## ✅ Verificação Final

Execute estes comandos para confirmar:

```bash
# 1. Versão Python
python --version
# Esperado: Python 3.12.x

# 2. Versão Poetry
poetry --version
# Esperado: Poetry (version 1.7.x)

# 3. Ambiente Poetry
cd d:\vms-v2
poetry env info
# Esperado: Python 3.12.x

# 4. Instalar dependências
poetry install
# Deve instalar sem erros
```

---

## 🚀 Próximos Passos

Após instalar Python 3.12:

1. **Instalar dependências**:
   ```bash
   cd d:\vms-v2
   poetry install
   ```

2. **Iniciar ambiente de desenvolvimento**:
   ```bash
   scripts\start-dev.bat
   ```

3. **Iniciar Django** (Terminal 1):
   ```bash
   poetry run python manage.py runserver
   ```

4. **Iniciar FastAPI** (Terminal 2):
   ```bash
   cd src/streaming
   poetry run uvicorn infrastructure.web.main:app --reload --port 8001
   ```

---

## 📝 Notas

- Python 3.12 é mais rápido que 3.10 (~25% performance)
- Melhor suporte a type hints
- Novas features de sintaxe
- Melhor compatibilidade com dependências modernas

---

**Recomendação**: Use a Opção 1 (Instalador Oficial) para simplicidade.
