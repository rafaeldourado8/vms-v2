# 2️⃣ Dados Pessoais

Classificação e tratamento de dados pessoais no GT-Vision VMS.

## 📊 Classificação de Dados

### Dados Pessoais (Art. 5º, I)
Informação relacionada a pessoa natural identificada ou identificável.

### Dados Pessoais Sensíveis (Art. 5º, II)
Dados sobre origem racial/étnica, convicção religiosa, opinião política, filiação sindical, saúde, vida sexual, genética ou biometria.

### Dados Anonimizados (Art. 5º, III)
Dados que não permitem identificação do titular.

## 🗂️ Dados no GT-Vision VMS

### 1. Operadores do Sistema

| Dado | Tipo | Finalidade | Base Legal | Retenção |
|------|------|------------|------------|----------|
| Nome completo | Pessoal | Identificação | Contrato | Enquanto ativo + 5 anos |
| CPF | Pessoal | Identificação única | Contrato | Enquanto ativo + 5 anos |
| Email | Pessoal | Comunicação | Contrato | Enquanto ativo + 5 anos |
| Telefone | Pessoal | Contato | Contrato | Enquanto ativo + 5 anos |
| Cargo | Pessoal | Controle de acesso | Contrato | Enquanto ativo + 5 anos |
| Senha (hash) | Pessoal | Autenticação | Contrato | Enquanto ativo |
| Logs de acesso | Pessoal | Auditoria | Legítimo interesse | 6 meses |

**Base Legal**: Execução de contrato (Art. 7º, V)

### 2. Gestores Municipais

| Dado | Tipo | Finalidade | Base Legal | Retenção |
|------|------|------------|------------|----------|
| Nome completo | Pessoal | Identificação | Exercício regular | Enquanto no cargo + 5 anos |
| CPF | Pessoal | Identificação única | Exercício regular | Enquanto no cargo + 5 anos |
| Email institucional | Pessoal | Comunicação oficial | Exercício regular | Enquanto no cargo + 5 anos |
| Secretaria | Pessoal | Organização | Exercício regular | Enquanto no cargo + 5 anos |

**Base Legal**: Exercício regular de direito (Art. 7º, VI)

### 3. Cidadãos (LPR)

| Dado | Tipo | Finalidade | Base Legal | Retenção |
|------|------|------------|------------|----------|
| Placa do veículo | Pessoal | Fiscalização trânsito | Exercício regular | 30-90 dias |
| Data/hora | Pessoal | Registro de infração | Exercício regular | 30-90 dias |
| Localização | Pessoal | Contexto da infração | Exercício regular | 30-90 dias |
| Imagem da placa | Pessoal | Evidência | Exercício regular | 30-90 dias |

**Base Legal**: Exercício regular de direito (Art. 7º, VI) - Código de Trânsito Brasileiro

**⚠️ IMPORTANTE**: Não armazenar dados do proprietário (nome, CPF, endereço). Apenas a placa.

### 4. Imagens de Câmeras

| Dado | Tipo | Finalidade | Base Legal | Retenção |
|------|------|------------|------------|----------|
| Vídeo de via pública | Pessoal/Sensível* | Segurança pública | Exercício regular | 30-90 dias |
| Timestamp | Pessoal | Contexto temporal | Exercício regular | 30-90 dias |
| Localização da câmera | Não pessoal | Contexto espacial | N/A | Indefinido |

**\*Sensível**: Se capturar biometria facial identificável.

**Base Legal**: Exercício regular de direito (Art. 7º, VI) - Segurança pública

## 🔐 Medidas de Proteção por Tipo

### Dados Pessoais Comuns
- ✅ Criptografia em trânsito (TLS 1.3)
- ✅ Criptografia em repouso (AES-256)
- ✅ Controle de acesso (RBAC)
- ✅ Logs de auditoria
- ✅ Backup criptografado

### Dados Pessoais Sensíveis (Imagens)
- ✅ Todas as medidas acima +
- ✅ Anonimização de faces (blur)
- ✅ Acesso restrito (apenas autoridades)
- ✅ RIPD (Relatório de Impacto)
- ✅ Consentimento explícito (quando aplicável)

### Dados Anonimizados
- ✅ Técnicas de anonimização irreversível
- ✅ Validação de não re-identificação
- ✅ Uso para estatísticas e BI

## 📋 Inventário de Dados

```python
# Modelo de inventário
class DataInventory:
    data_category: str  # "Operadores", "LPR", "Vídeos"
    data_type: str  # "Pessoal", "Sensível", "Anonimizado"
    fields: List[str]  # ["nome", "cpf", "email"]
    purpose: str  # "Autenticação e controle de acesso"
    legal_basis: str  # "Contrato (Art. 7º, V)"
    retention_period: str  # "Enquanto ativo + 5 anos"
    security_measures: List[str]  # ["Criptografia", "RBAC"]
    sharing: Optional[str]  # "Não compartilhado"
    location: str  # "PostgreSQL - AWS RDS"
```

## 🗑️ Política de Retenção

### Operadores e Gestores
- **Ativo**: Dados completos
- **Inativo**: Anonimizar após 5 anos
- **Solicitação de exclusão**: 15 dias

### LPR e Vídeos
- **Padrão**: 30 dias
- **Com infração**: 90 dias
- **Investigação judicial**: Até conclusão do processo
- **Após período**: Exclusão automática

### Logs de Auditoria
- **Acesso**: 6 meses
- **Modificação**: 1 ano
- **Incidentes**: 5 anos

## ✅ Checklist de Dados

- [ ] Inventário completo de dados pessoais
- [ ] Classificação por tipo (pessoal/sensível)
- [ ] Finalidade específica para cada dado
- [ ] Base legal identificada
- [ ] Período de retenção definido
- [ ] Medidas de segurança implementadas
- [ ] Política de exclusão automatizada
- [ ] Documentação atualizada
