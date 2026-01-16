# GT-Vision VMS - Análise de Arquitetura Multi-Tenant

## 🎯 Resposta Direta

**Nossa arquitetura é: MULTI-TENANT com SHARED DATABASE + TENANT ISOLATION**

- ✅ **Multi-tenant**: Sim (múltiplas prefeituras no mesmo sistema)
- ❌ **Hub-and-Spoke**: Não (não temos hub central com spokes distribuídos)
- ❌ **Sharding per Tenant**: Não (todos os tenants no mesmo banco)

**Padrão**: **Shared Database, Shared Schema com Row-Level Tenant Isolation**

---

## 📊 Diagrama de Multi-Tenancy

```mermaid
graph TB
    subgraph "Tenant Isolation Layer"
        TENANT_A[🏛️ Prefeitura A<br/>cidade_id: uuid-1]
        TENANT_B[🏛️ Prefeitura B<br/>cidade_id: uuid-2]
        TENANT_C[🏛️ Prefeitura C<br/>cidade_id: uuid-3]
    end
    
    subgraph "Application Layer - Shared"
        DJANGO[Django API<br/>Multi-tenant aware]
        FASTAPI[FastAPI<br/>Multi-tenant aware]
    end
    
    subgraph "Data Layer - Shared Database"
        POSTGRES[(PostgreSQL<br/>Single Database<br/>Shared Schema)]
        
        subgraph "Tables with Tenant Isolation"
            CIDADES[cidades<br/>id, nome, plano]
            CAMERAS[cameras<br/>id, cidade_id ⚠️]
            STREAMS[streams<br/>id, camera_id]
            RECORDINGS[recordings<br/>id, stream_id]
            LPR[lpr_events<br/>id, city_id ⚠️]
        end
    end
    
    subgraph "Storage Layer - Shared"
        MINIO[MinIO S3<br/>Buckets per Tenant]
        BUCKET_A[bucket: cidade-uuid-1]
        BUCKET_B[bucket: cidade-uuid-2]
        BUCKET_C[bucket: cidade-uuid-3]
    end
    
    TENANT_A -->|cidade_id filter| DJANGO
    TENANT_B -->|cidade_id filter| DJANGO
    TENANT_C -->|cidade_id filter| DJANGO
    
    DJANGO --> POSTGRES
    FASTAPI --> POSTGRES
    
    POSTGRES --> CIDADES
    CIDADES -->|FK| CAMERAS
    CAMERAS -->|FK| STREAMS
    STREAMS -->|FK| RECORDINGS
    CAMERAS -.->|FK| LPR
    
    TENANT_A -.->|isolated| BUCKET_A
    TENANT_B -.->|isolated| BUCKET_B
    TENANT_C -.->|isolated| BUCKET_C
    
    BUCKET_A --> MINIO
    BUCKET_B --> MINIO
    BUCKET_C --> MINIO
    
    classDef tenantStyle fill:#e1bee7,stroke:#7b1fa2,stroke-width:3px
    classDef appStyle fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    classDef dataStyle fill:#b3e5fc,stroke:#0277bd,stroke-width:3px
    classDef storageStyle fill:#ffe0b2,stroke:#f57c00,stroke-width:3px
    
    class TENANT_A,TENANT_B,TENANT_C tenantStyle
    class DJANGO,FASTAPI appStyle
    class POSTGRES,CIDADES,CAMERAS,STREAMS,RECORDINGS,LPR dataStyle
    class MINIO,BUCKET_A,BUCKET_B,BUCKET_C storageStyle
```

---

## 🔍 Análise Detalhada

### 1. Modelo de Multi-Tenancy

**Tipo**: **Shared Database, Shared Schema**

```mermaid
graph LR
    subgraph "Single PostgreSQL Instance"
        DB[(gtvision)]
        
        subgraph "Shared Schema"
            T1[Tenant 1 Data<br/>cidade_id = uuid-1]
            T2[Tenant 2 Data<br/>cidade_id = uuid-2]
            T3[Tenant 3 Data<br/>cidade_id = uuid-3]
        end
    end
    
    DB --> T1
    DB --> T2
    DB --> T3
    
    classDef dbStyle fill:#b3e5fc,stroke:#0277bd,stroke-width:2px
    classDef tenantStyle fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    
    class DB dbStyle
    class T1,T2,T3 tenantStyle
```

**Características**:
- ✅ Um único banco de dados PostgreSQL
- ✅ Um único schema compartilhado
- ✅ Isolamento via `cidade_id` (Foreign Key)
- ✅ Queries filtradas por tenant (WHERE cidade_id = ?)

---

### 2. Hierarquia de Dados (Tenant Isolation)

```mermaid
graph TD
    CIDADE[🏛️ Cidade/Prefeitura<br/>Tenant Root]
    
    CIDADE -->|1:N| CAMERAS[📷 Cameras<br/>cidade_id FK]
    CIDADE -->|1:N| USUARIOS[👤 Usuarios<br/>1 Gestor + 5 Visualizadores]
    
    CAMERAS -->|1:N| STREAMS[📡 Streams<br/>camera_id FK]
    STREAMS -->|1:N| RECORDINGS[🎥 Recordings<br/>stream_id FK]
    RECORDINGS -->|1:N| CLIPS[✂️ Clips<br/>recording_id FK]
    
    CAMERAS -.->|1:N| LPR[🚗 LPR Events<br/>camera_id + city_id FK]
    
    CIDADE -->|Plano| RETENTION[⏱️ Retention Policy<br/>7/15/30 dias]
    CIDADE -->|Limite| MAX_CAMERAS[📊 Max Cameras<br/>até 1000]
    
    classDef rootStyle fill:#e1bee7,stroke:#7b1fa2,stroke-width:3px
    classDef entityStyle fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef policyStyle fill:#fff9c4,stroke:#f9a825,stroke-width:2px
    
    class CIDADE rootStyle
    class CAMERAS,USUARIOS,STREAMS,RECORDINGS,CLIPS,LPR entityStyle
    class RETENTION,MAX_CAMERAS policyStyle
```

**Tenant Root**: `Cidade` (Prefeitura)

**Isolamento em Cascata**:
1. `cidades` (tenant root)
2. `cameras` (cidade_id FK) ⚠️ **Ponto de isolamento**
3. `streams` (camera_id FK) → isolado via camera
4. `recordings` (stream_id FK) → isolado via stream
5. `clips` (recording_id FK) → isolado via recording
6. `lpr_events` (city_id FK) ⚠️ **Isolamento direto**

---

### 3. Fluxo de Isolamento de Dados

```mermaid
sequenceDiagram
    participant U as Usuario<br/>(Prefeitura A)
    participant API as Django/FastAPI
    participant AUTH as Auth Middleware
    participant DB as PostgreSQL
    
    Note over U,DB: Fluxo com Tenant Isolation
    
    U->>API: GET /api/cameras
    API->>AUTH: Validate JWT
    AUTH-->>API: User + cidade_id (uuid-1)
    
    Note over API: Inject tenant filter
    
    API->>DB: SELECT * FROM cameras<br/>WHERE cidade_id = 'uuid-1'
    DB-->>API: Cameras (only Tenant A)
    API-->>U: Filtered Response
    
    Note over U,DB: Tentativa de acesso cross-tenant
    
    U->>API: GET /api/cameras/{uuid-tenant-b}
    API->>AUTH: Validate JWT
    AUTH-->>API: User + cidade_id (uuid-1)
    
    API->>DB: SELECT * FROM cameras<br/>WHERE id = 'uuid-tenant-b'<br/>AND cidade_id = 'uuid-1'
    DB-->>API: Empty (403 Forbidden)
    API-->>U: 403 Forbidden
```

**Segurança**:
- ✅ JWT contém `cidade_id` do usuário
- ✅ Todas as queries filtram por `cidade_id`
- ✅ Impossível acessar dados de outro tenant
- ✅ Row-Level Security (RLS) pode ser adicionado

---

### 4. Storage Multi-Tenant (MinIO)

```mermaid
graph TB
    subgraph "MinIO S3 Storage"
        MINIO[MinIO Server<br/>Single Instance]
        
        subgraph "Buckets per Tenant"
            B1[recordings-cidade-uuid-1<br/>Prefeitura A]
            B2[recordings-cidade-uuid-2<br/>Prefeitura B]
            B3[recordings-cidade-uuid-3<br/>Prefeitura C]
            
            B1_LPR[lpr-images-cidade-uuid-1]
            B2_LPR[lpr-images-cidade-uuid-2]
            B3_LPR[lpr-images-cidade-uuid-3]
        end
    end
    
    MINIO --> B1
    MINIO --> B2
    MINIO --> B3
    MINIO --> B1_LPR
    MINIO --> B2_LPR
    MINIO --> B3_LPR
    
    classDef minioStyle fill:#6a1b9a,stroke:#4a148c,stroke-width:2px
    classDef bucketStyle fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px
    
    class MINIO minioStyle
    class B1,B2,B3,B1_LPR,B2_LPR,B3_LPR bucketStyle
```

**Isolamento de Storage**:
- ✅ Buckets separados por tenant
- ✅ Naming: `{resource}-cidade-{uuid}`
- ✅ IAM policies por bucket
- ✅ Lifecycle policies por tenant (7/15/30 dias)

---

### 5. Comparação de Arquiteturas

```mermaid
graph TB
    subgraph "Nossa Arquitetura: Shared DB"
        SHARED_APP[Application Layer]
        SHARED_DB[(Single PostgreSQL<br/>Shared Schema<br/>Row-Level Isolation)]
        
        SHARED_APP --> SHARED_DB
        
        T1[Tenant 1] -.->|cidade_id filter| SHARED_APP
        T2[Tenant 2] -.->|cidade_id filter| SHARED_APP
        T3[Tenant 3] -.->|cidade_id filter| SHARED_APP
    end
    
    subgraph "Alternativa 1: Database per Tenant"
        ALT1_APP[Application Layer]
        ALT1_DB1[(DB Tenant 1)]
        ALT1_DB2[(DB Tenant 2)]
        ALT1_DB3[(DB Tenant 3)]
        
        ALT1_APP --> ALT1_DB1
        ALT1_APP --> ALT1_DB2
        ALT1_APP --> ALT1_DB3
    end
    
    subgraph "Alternativa 2: Sharding"
        ALT2_APP[Application Layer]
        ALT2_SHARD1[(Shard 1<br/>Tenants 1-100)]
        ALT2_SHARD2[(Shard 2<br/>Tenants 101-200)]
        
        ALT2_APP --> ALT2_SHARD1
        ALT2_APP --> ALT2_SHARD2
    end
    
    classDef currentStyle fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    classDef altStyle fill:#e0e0e0,stroke:#757575,stroke-width:2px
    
    class SHARED_APP,SHARED_DB,T1,T2,T3 currentStyle
    class ALT1_APP,ALT1_DB1,ALT1_DB2,ALT1_DB3,ALT2_APP,ALT2_SHARD1,ALT2_SHARD2 altStyle
```

---

## 📋 Características da Nossa Arquitetura

### ✅ Vantagens

1. **Simplicidade**
   - Um único banco de dados
   - Schema único e consistente
   - Migrations simples

2. **Custo-Efetivo**
   - Recursos compartilhados
   - Melhor utilização de hardware
   - Menos overhead operacional

3. **Manutenção**
   - Backups centralizados
   - Updates/patches únicos
   - Monitoramento simplificado

4. **Performance**
   - Connection pooling eficiente
   - Cache compartilhado (Redis)
   - Queries otimizadas com índices

### ⚠️ Limitações

1. **Escalabilidade**
   - Limite de ~1000 prefeituras (estimado)
   - Crescimento vertical (scale-up)
   - Não escala horizontalmente por tenant

2. **Isolamento**
   - Risco de "noisy neighbor"
   - Tenant grande pode afetar outros
   - Requer cuidado com queries

3. **Compliance**
   - Dados de todos os tenants no mesmo DB
   - Pode não atender requisitos de isolamento físico
   - LGPD: dados misturados (mas isolados logicamente)

---

## 🔧 Implementação Atual

### Código de Isolamento

```python
# src/cidades/domain/aggregates/cidade.py
class Cidade(AggregateRoot):
    """Tenant Root - Prefeitura"""
    
    def __init__(self, entity_id: UUID, nome: str, cnpj: CNPJ):
        self.id = entity_id  # Tenant ID
        self.nome = nome
        self.cameras: List[Camera] = []  # Owned by tenant
        self.usuarios: List[Usuario] = []  # Owned by tenant
```

### Schema SQL

```sql
-- Tenant Root
CREATE TABLE cidades (
    id UUID PRIMARY KEY,
    nome VARCHAR(255),
    plano_retencao_dias INTEGER
);

-- Tenant-scoped data
CREATE TABLE cameras (
    id UUID PRIMARY KEY,
    cidade_id UUID REFERENCES cidades(id),  -- ⚠️ Tenant FK
    nome VARCHAR(255)
);

CREATE INDEX idx_cameras_cidade ON cameras(cidade_id);  -- ⚠️ Performance
```

### Query Pattern

```python
# Sempre filtrar por tenant
cameras = db.query(Camera).filter(
    Camera.cidade_id == current_user.cidade_id  # ⚠️ Tenant filter
).all()
```

---

## 🚀 Evolução Futura

### Opção 1: Adicionar Sharding (se crescer muito)

```mermaid
graph TB
    APP[Application]
    ROUTER[Shard Router<br/>by cidade_id]
    
    SHARD1[(Shard 1<br/>Cidades 1-500)]
    SHARD2[(Shard 2<br/>Cidades 501-1000)]
    SHARD3[(Shard 3<br/>Cidades 1001-1500)]
    
    APP --> ROUTER
    ROUTER --> SHARD1
    ROUTER --> SHARD2
    ROUTER --> SHARD3
```

### Opção 2: Database per Tenant (para clientes enterprise)

```mermaid
graph TB
    APP[Application]
    
    DB_SHARED[(Shared DB<br/>Small Tenants)]
    DB_ENTERPRISE1[(Dedicated DB<br/>Enterprise 1)]
    DB_ENTERPRISE2[(Dedicated DB<br/>Enterprise 2)]
    
    APP --> DB_SHARED
    APP --> DB_ENTERPRISE1
    APP --> DB_ENTERPRISE2
```

---

## 📊 Resumo Executivo

| Aspecto | Nossa Implementação |
|---------|---------------------|
| **Padrão** | Shared Database, Shared Schema |
| **Isolamento** | Row-Level (cidade_id FK) |
| **Escalabilidade** | Vertical (até ~1000 tenants) |
| **Custo** | Baixo (recursos compartilhados) |
| **Complexidade** | Baixa (single DB) |
| **Segurança** | Média (isolamento lógico) |
| **Performance** | Alta (cache compartilhado) |
| **Manutenção** | Fácil (single schema) |

---

## ✅ Conclusão

**Nossa arquitetura é MULTI-TENANT com:**
- ✅ Shared Database (PostgreSQL único)
- ✅ Shared Schema (tabelas compartilhadas)
- ✅ Row-Level Isolation (cidade_id FK)
- ✅ Bucket Isolation (MinIO per tenant)

**NÃO é:**
- ❌ Hub-and-Spoke (não temos hub central)
- ❌ Sharding (não particionamos por tenant)
- ❌ Database per Tenant (não temos DBs separados)

**Adequado para**: 10-1000 prefeituras de pequeno/médio porte

**Migração futura**: Sharding ou DB per Tenant se ultrapassar 1000 tenants
