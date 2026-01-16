"""Configuração global do pytest."""
import sys
from pathlib import Path

# Adiciona o diretório src ao PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
