# Plano de Refatoração Frontend - GT-Vision VMS

## 🎯 Objetivo
Remover mocks, simplificar componentes e integrar com backend real.

## 🔴 Problemas Críticos Identificados

### 1. LiveCameras.tsx
**Problemas**:
- Mock de eventos da timeline (`mockTimelineEvents`)
- Snapshot não salva no backend
- Não usa WebSocket para alertas
- Timeline não mostra dados reais

**Solução**:
```typescript
// REMOVER
const mockTimelineEvents = [...];

// ADICIONAR
const { data: thumbnails } = useQuery({
  queryKey: ['thumbnails', selectedCamera?.id],
  queryFn: () => api.get(`/api/v1/cameras/${selectedCamera?.id}/timeline`),
  enabled: !!selectedCamera
});

// Snapshot real
const handleSnapshot = async () => {
  const response = await api.get(`/api/v1/snapshots/${selectedCamera.id}`);
  // Atualizar thumbnail
};
```

---

### 2. Timeline.tsx
**Problemas**:
- Componente gigante (150+ linhas)
- Lógica de clip trimmer misturada
- Não usa dados reais
- Zoom levels fake

**Solução - Simplificar**:
```typescript
// Timeline.tsx (SIMPLIFICADO)
interface TimelineProps {
  thumbnails: Thumbnail[];  // Do backend
  currentTime: number;
  onSeek: (time: number) => void;
}

const Timeline = ({ thumbnails, currentTime, onSeek }: TimelineProps) => {
  return (
    <div className="timeline-container">
      {/* Barra de progresso simples */}
      <div className="progress-bar" onClick={handleSeek}>
        <div style={{ width: `${progress}%` }} />
      </div>
      
      {/* Thumbnails do backend */}
      <div className="thumbnails-strip">
        {thumbnails.map(thumb => (
          <img 
            key={thumb.timestamp} 
            src={thumb.url} 
            onClick={() => onSeek(thumb.timestamp)}
          />
        ))}
      </div>
    </div>
  );
};
```

---

### 3. CameraMap.tsx
**Problemas**:
- Usa Leaflet (não Google Maps)
- Popup básico sem thumbnails
- Não mostra heatmap

**Solução - Migrar para Google Maps**:
```typescript
// CameraMap.tsx (NOVO - Google Maps)
import { GoogleMap, Marker, InfoWindow } from '@react-google-maps/api';

const CameraMap = ({ cameras }: Props) => {
  const [selected, setSelected] = useState<Camera | null>(null);

  return (
    <GoogleMap
      center={{ lat: -23.5505, lng: -46.6333 }}
      zoom={12}
    >
      {cameras.map(camera => (
        <Marker
          key={camera.id}
          position={{ lat: camera.latitude, lng: camera.longitude }}
          icon={{
            url: `/markers/${camera.status}.svg`,
            scaledSize: new google.maps.Size(40, 40)
          }}
          onClick={() => setSelected(camera)}
        />
      ))}

      {selected && (
        <InfoWindow
          position={{ lat: selected.latitude, lng: selected.longitude }}
          onCloseClick={() => setSelected(null)}
        >
          <CameraPopup camera={selected} />
        </InfoWindow>
      )}
    </GoogleMap>
  );
};
```

---

### 4. CameraPopup (NOVO - Com Thumbnails)
**Criar componente separado**:
```typescript
// components/CameraPopup.tsx
const CameraPopup = ({ camera }: { camera: Camera }) => {
  const { data: snapshot } = useQuery({
    queryKey: ['snapshot', camera.id],
    queryFn: () => api.get(`/api/v1/snapshots/${camera.id}`, {
      responseType: 'blob'
    })
  });

  return (
    <div className="p-4 min-w-[250px]">
      {/* Thumbnail */}
      {snapshot && (
        <img 
          src={URL.createObjectURL(snapshot.data)} 
          className="w-full h-32 object-cover rounded mb-2"
        />
      )}
      
      <h3 className="font-bold">{camera.name}</h3>
      <p className="text-sm text-gray-600">{camera.location}</p>
      
      <div className="flex items-center gap-2 mt-2">
        <StatusBadge status={camera.status} />
        <span className="text-xs">
          {camera.detections_24h} detecções (24h)
        </span>
      </div>

      <Button 
        onClick={() => window.openCamera(camera.id)}
        className="w-full mt-3"
      >
        Ver Câmera
      </Button>
    </div>
  );
};
```

---

## 📝 Checklist de Refatoração

### Fase 1: Remover Mocks (1 dia)
- [ ] Remover `mockTimelineEvents` de LiveCameras.tsx
- [ ] Integrar `/api/v1/cameras/{id}/timeline` para thumbnails
- [ ] Integrar `/api/v1/snapshots/{id}` para snapshot real
- [ ] Remover lógica de snapshot local (canvas)

### Fase 2: Simplificar Timeline (1 dia)
- [ ] Extrair ClipTrimmer para componente separado
- [ ] Remover zoom levels fake
- [ ] Usar thumbnails reais do backend
- [ ] Reduzir Timeline.tsx para < 80 linhas

### Fase 3: Migrar para Google Maps (1 dia)
- [ ] Instalar `@react-google-maps/api`
- [ ] Substituir Leaflet por Google Maps
- [ ] Criar CameraPopup.tsx com thumbnails
- [ ] Integrar `/api/v1/map/cameras` (GeoJSON)
- [ ] Adicionar heatmap (`/api/v1/map/heatmap`)

### Fase 4: WebSocket Alertas (1 dia)
- [ ] Criar hook `useWebSocket`
- [ ] Conectar em `ws://localhost/ws/alerts?token=JWT`
- [ ] Mostrar alertas LPR em tempo real
- [ ] Piscar marcador no mapa quando houver detecção

### Fase 5: Dashboard Real (1 dia)
- [ ] Integrar `/api/v1/dashboard/health`
- [ ] Remover dados mock do Dashboard
- [ ] Adicionar gráficos com Chart.js
- [ ] Auto-refresh a cada 30s

---

## 🗂️ Estrutura Final (Limpa)

```
frontend/src/
├── components/
│   ├── Map/
│   │   ├── GoogleMapViewer.tsx      ✅ Novo (Google Maps)
│   │   ├── CameraMarker.tsx         ✅ Novo
│   │   └── CameraPopup.tsx          ✅ Novo (com thumbnail)
│   ├── Video/
│   │   ├── VideoPlayer.tsx          ✅ Manter
│   │   └── Timeline.tsx             🔧 Simplificar (< 80 linhas)
│   ├── Dashboard/
│   │   ├── HealthMetrics.tsx        🔧 Integrar API real
│   │   └── CameraStatusList.tsx     🔧 Integrar API real
│   └── Shared/
│       ├── ClipTrimmer.tsx          ✅ Extrair de Timeline
│       └── WebSocketProvider.tsx    ✅ Novo
├── hooks/
│   ├── useWebSocket.ts              ✅ Novo
│   ├── useThumbnails.ts             ✅ Novo
│   └── useSnapshot.ts               ✅ Novo
└── pages/
    ├── LiveCameras.tsx              🔧 Remover mocks
    └── Dashboard.tsx                🔧 Integrar API real
```

---

## 🚀 Ordem de Execução

1. **Dia 1**: Remover mocks + Integrar thumbnails reais
2. **Dia 2**: Simplificar Timeline + Extrair ClipTrimmer
3. **Dia 3**: Migrar para Google Maps + CameraPopup
4. **Dia 4**: WebSocket + Alertas tempo real
5. **Dia 5**: Dashboard real + Testes finais

---

## 📊 Métricas de Sucesso

- ✅ 0 dados mock no código
- ✅ Timeline < 80 linhas
- ✅ Popup do mapa mostra thumbnail real
- ✅ WebSocket funcionando (< 500ms latência)
- ✅ Dashboard atualiza automaticamente

---

## 🔧 Dependências Necessárias

```bash
npm install @react-google-maps/api
npm install chart.js react-chartjs-2
npm install date-fns
```

---

**Próximo passo**: Começar pela Fase 1 (remover mocks)?
