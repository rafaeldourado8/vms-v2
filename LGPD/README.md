# 📋 LGPD - Lei Geral de Proteção de Dados

Documentação de compliance do GT-Vision VMS com a LGPD (Lei nº 13.709/2018).

## 📚 Documentos

1. **[Princípios LGPD](01-principios-lgpd.md)** - 10 princípios fundamentais
2. **[Dados Pessoais](02-dados-pessoais.md)** - Classificação e tratamento
3. **[Direitos dos Titulares](03-direitos-titulares.md)** - 9 direitos garantidos
4. **[Base Legal](04-base-legal.md)** - Fundamentos legais para tratamento
5. **[Consentimento](05-consentimento.md)** - Coleta e gestão de consentimento
6. **[Segurança](06-seguranca.md)** - Medidas técnicas e organizacionais
7. **[Anonimização](07-anonimizacao.md)** - Técnicas de anonimização
8. **[Incidentes](08-incidentes.md)** - Gestão de incidentes de segurança
9. **[Auditoria](09-auditoria.md)** - Logs e rastreabilidade
10. **[Checklist](10-checklist.md)** - Verificação de compliance

## 🎯 Dados Tratados pelo GT-Vision VMS

### Dados Pessoais
- **Operadores**: Nome, CPF, email, telefone, cargo
- **Gestores Municipais**: Nome, CPF, email, telefone, secretaria
- **Cidadãos (LPR)**: Placa de veículo, data/hora, localização

### Dados Sensíveis
- **Imagens de Câmeras**: Podem capturar biometria facial (dados sensíveis)
- **Localização**: Rastreamento de veículos via LPR

## ⚖️ Papéis LGPD

- **Controlador**: Prefeitura Municipal (cliente)
- **Operador**: GT-Vision (fornecedor do sistema)
- **Encarregado (DPO)**: A ser designado pela prefeitura
- **Titular**: Operadores, gestores e cidadãos

## 🔒 Medidas Implementadas

### Técnicas
- ✅ Criptografia em trânsito (TLS 1.3)
- ✅ Criptografia em repouso (PostgreSQL + MinIO)
- ✅ Autenticação JWT
- ✅ Controle de acesso (RBAC)
- ✅ Rate limiting
- ✅ Logs de auditoria
- ✅ Anonimização de dados

### Organizacionais
- ✅ Política de privacidade
- ✅ Termo de consentimento
- ✅ Procedimento de incidentes
- ✅ Treinamento de equipe
- ✅ Avaliação de impacto (RIPD)

## 📞 Contatos

- **DPO**: dpo@gtvision.com.br
- **Suporte**: suporte@gtvision.com.br
- **ANPD**: https://www.gov.br/anpd

## 📖 Referências

- [Lei nº 13.709/2018](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [ANPD - Guias](https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/guias)
- [Resolução CD/ANPD nº 2/2022](https://www.in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-2-de-27-de-janeiro-de-2022-376562019)
