# 4️⃣ Base Legal

Fundamentos legais para tratamento de dados pessoais (Art. 7º e 11º da LGPD).

## 📜 Bases Legais para Dados Pessoais (Art. 7º)

### I - Consentimento

**Definição**: Manifestação livre, informada e inequívoca.

**Quando usar**: Dados opcionais (newsletter, notificações).

**Características**:
- ✅ Específico para cada finalidade
- ✅ Destacado das demais cláusulas
- ✅ Revogável a qualquer momento
- ✅ Documentado

**Exemplo no GT-Vision**:
```python
# Consentimento para notificações por email
consent = {
    "purpose": "Envio de alertas e notificações por email",
    "optional": True,
    "can_revoke": True,
    "granted_at": "2024-01-15T10:30:00Z"
}
```

### II - Obrigação Legal

**Definição**: Cumprimento de obrigação legal ou regulatória.

**Quando usar**: Dados exigidos por lei.

**Exemplo no GT-Vision**:
- Retenção de logs de acesso (Marco Civil da Internet)
- Dados fiscais (Receita Federal)

### III - Execução de Políticas Públicas

**Definição**: Pela administração pública para políticas públicas.

**Quando usar**: Prefeituras usando o sistema.

**Exemplo no GT-Vision**:
- Monitoramento urbano pela prefeitura
- Gestão de tráfego municipal

### IV - Estudos por Órgão de Pesquisa

**Definição**: Realização de estudos com anonimização quando possível.

**Quando usar**: Pesquisas acadêmicas.

**Exemplo no GT-Vision**:
- Estatísticas de tráfego (dados anonimizados)
- Análise de padrões urbanos

### V - Execução de Contrato

**Definição**: Necessário para contrato do qual o titular é parte.

**Quando usar**: Dados de operadores e gestores.

**Exemplo no GT-Vision**:
```python
# Dados necessários para o contrato de trabalho
contract_data = {
    "name": "João Silva",
    "cpf": "123.456.789-00",
    "email": "joao@prefeitura.gov.br",
    "role": "Operador",
    "legal_basis": "Execução de contrato (Art. 7º, V)"
}
```

### VI - Exercício Regular de Direito

**Definição**: Exercício regular de direitos em processo judicial, administrativo ou arbitral.

**Quando usar**: Fiscalização, segurança pública.

**Exemplo no GT-Vision**:
- LPR para fiscalização de trânsito (CTB)
- Câmeras para segurança pública
- Logs para investigações

```python
# LPR baseado no Código de Trânsito Brasileiro
lpr_event = {
    "plate": "ABC1234",
    "timestamp": "2024-01-15T14:30:00Z",
    "location": "Av. Principal, 100",
    "legal_basis": "Exercício regular de direito (Art. 7º, VI) - CTB"
}
```

### VII - Proteção da Vida

**Definição**: Proteção da vida ou incolumidade física.

**Quando usar**: Emergências médicas, salvamento.

**Exemplo no GT-Vision**:
- Acesso emergencial a câmeras para localizar pessoa desaparecida

### VIII - Tutela da Saúde

**Definição**: Por profissionais de saúde ou entidades sanitárias.

**Quando usar**: Não aplicável ao GT-Vision.

### IX - Legítimo Interesse

**Definição**: Interesse legítimo do controlador ou terceiro.

**Quando usar**: Com cautela, após teste de balanceamento.

**Teste de Balanceamento**:
1. ✅ Finalidade legítima?
2. ✅ Necessário para a finalidade?
3. ✅ Expectativa razoável do titular?
4. ✅ Direitos do titular não prevalecem?

**Exemplo no GT-Vision**:
```python
# Logs de acesso para segurança do sistema
access_log = {
    "user_id": "uuid",
    "action": "login",
    "ip_address": "192.168.1.1",
    "timestamp": "2024-01-15T10:00:00Z",
    "legal_basis": "Legítimo interesse (Art. 7º, IX) - Segurança do sistema"
}
```

### X - Proteção do Crédito

**Definição**: Para proteção do crédito.

**Quando usar**: Não aplicável ao GT-Vision.

## 🔒 Bases Legais para Dados Sensíveis (Art. 11)

Dados sensíveis exigem bases legais mais restritas.

### I - Consentimento Específico e Destacado

**Diferença**: Mais rigoroso que consentimento comum.

**Exemplo no GT-Vision**:
```python
# Consentimento para reconhecimento facial (biometria)
sensitive_consent = {
    "purpose": "Reconhecimento facial para controle de acesso",
    "data_type": "Biometria facial (dado sensível)",
    "highlighted": True,
    "specific": True,
    "granted_at": "2024-01-15T10:30:00Z"
}
```

### II - Obrigação Legal

**Exemplo**: Dados de saúde exigidos por lei.

### III - Políticas Públicas

**Exemplo**: Prefeitura usando biometria para segurança pública.

### IV - Estudos por Órgão de Pesquisa

**Exemplo**: Pesquisa acadêmica com anonimização.

### V - Exercício Regular de Direito

**Exemplo**: Biometria em processo judicial.

### VI - Proteção da Vida

**Exemplo**: Acesso emergencial a dados de saúde.

### VII - Tutela da Saúde

**Exemplo**: Profissionais de saúde.

### VIII - Prevenção de Fraude

**Exemplo**: Biometria para autenticação.

## 📊 Matriz de Base Legal - GT-Vision VMS

| Dado | Tipo | Base Legal | Artigo |
|------|------|------------|--------|
| Nome do operador | Pessoal | Execução de contrato | Art. 7º, V |
| CPF do operador | Pessoal | Execução de contrato | Art. 7º, V |
| Email do operador | Pessoal | Execução de contrato | Art. 7º, V |
| Senha (hash) | Pessoal | Execução de contrato | Art. 7º, V |
| Placa de veículo | Pessoal | Exercício regular de direito | Art. 7º, VI |
| Imagem de via pública | Pessoal | Exercício regular de direito | Art. 7º, VI |
| Biometria facial | Sensível | Consentimento específico | Art. 11, I |
| Logs de acesso | Pessoal | Legítimo interesse | Art. 7º, IX |
| Notificações por email | Pessoal | Consentimento | Art. 7º, I |

## ⚖️ Hierarquia de Bases Legais

1. **Obrigação legal** - Mais forte
2. **Exercício regular de direito** - Forte
3. **Execução de contrato** - Forte
4. **Legítimo interesse** - Moderado (requer teste)
5. **Consentimento** - Mais fraco (revogável)

## 🚨 Erros Comuns

### ❌ Usar consentimento para dados obrigatórios
```python
# ERRADO
consent = "Concordo em fornecer meu CPF"  # CPF é obrigatório para contrato
```

### ✅ Usar base legal correta
```python
# CORRETO
legal_basis = "Execução de contrato (Art. 7º, V)"  # CPF necessário para contrato
```

### ❌ Legítimo interesse sem teste
```python
# ERRADO
legal_basis = "Legítimo interesse"  # Sem documentar o teste de balanceamento
```

### ✅ Legítimo interesse documentado
```python
# CORRETO
legitimate_interest = {
    "purpose": "Segurança do sistema",
    "necessity": "Prevenir acessos não autorizados",
    "expectation": "Razoável que logs sejam mantidos",
    "balance": "Segurança prevalece sobre privacidade mínima",
    "legal_basis": "Legítimo interesse (Art. 7º, IX)"
}
```

## ✅ Checklist de Base Legal

- [ ] Base legal identificada para cada tratamento
- [ ] Documentação da base legal
- [ ] Consentimento específico para dados sensíveis
- [ ] Teste de balanceamento para legítimo interesse
- [ ] Matriz de base legal atualizada
- [ ] Revisão periódica das bases legais
