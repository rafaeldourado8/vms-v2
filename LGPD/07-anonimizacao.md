# 7️⃣ Anonimização

Técnicas de anonimização de dados pessoais (Art. 12 e 13 da LGPD).

## 📖 Definições

### Dado Anonimizado (Art. 5º, III)
Dado que não permite identificação do titular, considerando meios técnicos razoáveis e disponíveis.

### Pseudonimização (Art. 13, § 4º)
Tratamento que oculta a identidade, mas permite re-identificação com informação adicional.

**⚠️ IMPORTANTE**: Pseudonimização NÃO é anonimização. Dados pseudonimizados ainda são dados pessoais.

## 🎯 Quando Anonimizar

### Obrigatório
- Direito à eliminação (Art. 18, IV)
- Fim da finalidade do tratamento
- Fim do período de retenção

### Recomendado
- Estatísticas e BI
- Pesquisas acadêmicas
- Dados históricos
- Treinamento de IA

## 🔧 Técnicas de Anonimização

### 1. Generalização

Reduzir a precisão dos dados.

```python
# Antes
user = {
    "age": 27,
    "city": "São Paulo",
    "neighborhood": "Vila Mariana"
}

# Depois
user_anonymized = {
    "age_range": "25-30",
    "city": "São Paulo",
    "neighborhood": None  # Removido
}
```

**Aplicação no GT-Vision**:
```python
def anonymize_lpr_event(event: LPREvent) -> dict:
    return {
        "hour": event.timestamp.hour,  # Apenas hora, não minuto/segundo
        "day_of_week": event.timestamp.strftime("%A"),
        "location_zone": get_zone(event.location),  # Zona, não endereço exato
        "plate": None  # Removido
    }
```

### 2. Supressão

Remover dados identificadores.

```python
def anonymize_user(user: User) -> dict:
    return {
        "id": None,  # Removido
        "name": None,  # Removido
        "cpf": None,  # Removido
        "email": None,  # Removido
        "role": user.role,  # Mantido
        "created_at": user.created_at.year  # Apenas ano
    }
```

### 3. Agregação

Combinar dados de múltiplos indivíduos.

```python
def aggregate_lpr_stats(events: List[LPREvent]) -> dict:
    """Estatísticas agregadas de LPR"""
    return {
        "total_events": len(events),
        "by_hour": group_by_hour(events),
        "by_location": group_by_location(events),
        "avg_per_day": calculate_avg_per_day(events)
    }

# Resultado
{
    "total_events": 1500,
    "by_hour": {
        "08:00": 120,
        "09:00": 150,
        "10:00": 130
    },
    "by_location": {
        "Centro": 500,
        "Zona Sul": 600,
        "Zona Norte": 400
    },
    "avg_per_day": 50
}
```

### 4. Perturbação

Adicionar ruído aos dados.

```python
import random

def add_noise_to_location(lat: float, lon: float, radius_km: float = 1.0) -> tuple:
    """Adiciona ruído à localização"""
    # Adicionar offset aleatório
    lat_offset = random.uniform(-radius_km/111, radius_km/111)
    lon_offset = random.uniform(-radius_km/111, radius_km/111)
    
    return (lat + lat_offset, lon + lon_offset)

# Uso
original = (-23.5505, -46.6333)  # São Paulo exato
anonymized = add_noise_to_location(*original)  # Aproximado
```

### 5. Mascaramento

Ocultar parte dos dados.

```python
def mask_cpf(cpf: str) -> str:
    """Mascara CPF: 123.456.789-00 -> ***.456.***-**"""
    return f"***.{cpf[4:7]}.***-**"

def mask_email(email: str) -> str:
    """Mascara email: joao@example.com -> j***@example.com"""
    local, domain = email.split("@")
    return f"{local[0]}***@{domain}"

def mask_plate(plate: str) -> str:
    """Mascara placa: ABC1234 -> ***1234"""
    return f"***{plate[-4:]}"
```

### 6. Blur de Imagens

Anonimizar faces em vídeos.

```python
import cv2

def blur_faces(image_path: str, output_path: str):
    """Aplica blur em faces detectadas"""
    # Carregar imagem
    image = cv2.imread(image_path)
    
    # Detectar faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(image, 1.1, 4)
    
    # Aplicar blur
    for (x, y, w, h) in faces:
        face_region = image[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        image[y:y+h, x:x+w] = blurred_face
    
    # Salvar
    cv2.imwrite(output_path, image)
```

### 7. Tokenização

Substituir dados por tokens.

```python
import hashlib
import hmac

class Tokenizer:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def tokenize(self, data: str) -> str:
        """Gera token irreversível"""
        return hmac.new(
            self.secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

# Uso
tokenizer = Tokenizer(settings.SECRET_KEY)
token = tokenizer.tokenize("ABC1234")  # Placa -> Token
```

## 💻 Implementação no GT-Vision

### Serviço de Anonimização

```python
from typing import Protocol

class AnonymizationStrategy(Protocol):
    def anonymize(self, data: dict) -> dict:
        ...

class UserAnonymization:
    def anonymize(self, user: User) -> dict:
        return {
            "id": None,
            "name": None,
            "cpf": None,
            "email": None,
            "phone": None,
            "role": user.role,
            "created_year": user.created_at.year
        }

class LPRAnonymization:
    def anonymize(self, event: LPREvent) -> dict:
        return {
            "plate": None,
            "hour": event.timestamp.hour,
            "day_of_week": event.timestamp.strftime("%A"),
            "location_zone": self._get_zone(event.location)
        }
    
    def _get_zone(self, location: str) -> str:
        # Mapear endereço para zona
        if "Centro" in location:
            return "Centro"
        elif "Sul" in location:
            return "Zona Sul"
        # ...

class AnonymizationService:
    def __init__(self):
        self.strategies = {
            "user": UserAnonymization(),
            "lpr": LPRAnonymization()
        }
    
    def anonymize(self, data_type: str, data: dict) -> dict:
        strategy = self.strategies.get(data_type)
        if not strategy:
            raise ValueError(f"Unknown data type: {data_type}")
        return strategy.anonymize(data)
```

### Endpoint de Anonimização

```python
@router.post("/api/lgpd/anonimizar")
async def anonymize_user_data(
    user: User = Depends(get_current_user)
):
    """Anonimiza dados do usuário"""
    
    # Verificar se pode anonimizar
    if user.has_active_contracts():
        raise HTTPException(
            400,
            "Não é possível anonimizar dados com contratos ativos"
        )
    
    # Anonimizar
    anonymization_service = AnonymizationService()
    user_data = user.to_dict()
    anonymized = anonymization_service.anonymize("user", user_data)
    
    # Atualizar no banco
    user.update(anonymized)
    user.anonymized_at = datetime.now()
    user.save()
    
    # Log
    audit_log.record(
        action="DATA_ANONYMIZED",
        user_id=user.id,
        timestamp=datetime.now()
    )
    
    return {"message": "Dados anonimizados com sucesso"}
```

### Anonimização Automática

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def auto_anonymize_expired_data():
    """Task diária para anonimizar dados expirados"""
    
    # LPR events > 90 dias
    expired_lpr = LPREvent.filter(
        created_at__lt=datetime.now() - timedelta(days=90)
    )
    
    for event in expired_lpr:
        anonymized = LPRAnonymization().anonymize(event)
        event.update(anonymized)
        event.anonymized_at = datetime.now()
        event.save()
    
    # Usuários inativos > 5 anos
    expired_users = User.filter(
        last_login__lt=datetime.now() - timedelta(days=1825),
        anonymized_at__isnull=True
    )
    
    for user in expired_users:
        anonymized = UserAnonymization().anonymize(user)
        user.update(anonymized)
        user.anonymized_at = datetime.now()
        user.save()
    
    logger.info(f"Anonymized {len(expired_lpr)} LPR events and {len(expired_users)} users")

# Agendar task diária
celery.conf.beat_schedule = {
    'auto-anonymize': {
        'task': 'tasks.auto_anonymize_expired_data',
        'schedule': crontab(hour=2, minute=0)  # 02:00 todos os dias
    }
}
```

## ✅ Validação de Anonimização

### Teste de Re-identificação

```python
def test_anonymization_effectiveness(original: dict, anonymized: dict) -> bool:
    """Testa se dados anonimizados podem ser re-identificados"""
    
    # 1. Verificar se identificadores diretos foram removidos
    direct_identifiers = ["id", "cpf", "email", "phone", "name", "plate"]
    for identifier in direct_identifiers:
        if identifier in anonymized and anonymized[identifier] is not None:
            return False
    
    # 2. Verificar se dados foram generalizados
    if "age" in original and "age" in anonymized:
        if original["age"] == anonymized["age"]:
            return False  # Deveria ser age_range
    
    # 3. Verificar se há dados suficientes para re-identificação
    # (k-anonymity: pelo menos k indivíduos com mesmos atributos)
    k = 5
    similar_records = count_similar_records(anonymized)
    if similar_records < k:
        return False
    
    return True
```

### K-Anonymity

```python
def check_k_anonymity(dataset: List[dict], k: int = 5) -> bool:
    """Verifica se dataset satisfaz k-anonymity"""
    
    # Agrupar por atributos quasi-identificadores
    groups = {}
    for record in dataset:
        key = (record.get("age_range"), record.get("city"), record.get("role"))
        groups[key] = groups.get(key, 0) + 1
    
    # Verificar se todos os grupos têm pelo menos k registros
    return all(count >= k for count in groups.values())
```

## ⚠️ Erros Comuns

### ❌ Pseudonimização como anonimização
```python
# ERRADO - Ainda é dado pessoal
user_id_hash = hashlib.sha256(user.cpf.encode()).hexdigest()
```

### ✅ Anonimização irreversível
```python
# CORRETO - Não permite re-identificação
anonymized_user = {
    "role": user.role,
    "created_year": user.created_at.year
}
```

## ✅ Checklist de Anonimização

- [ ] Técnicas de anonimização definidas
- [ ] Serviço de anonimização implementado
- [ ] Anonimização automática agendada
- [ ] Teste de re-identificação realizado
- [ ] K-anonymity validado (k ≥ 5)
- [ ] Blur de faces em vídeos
- [ ] Documentação de processos
- [ ] Logs de anonimização
