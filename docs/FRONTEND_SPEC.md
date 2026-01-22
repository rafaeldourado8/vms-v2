# Frontend GT-Vision VMS - Especificação

## 🎯 Visão Geral

Frontend moderno para VMS com foco em **Sala de Controle Tática** usando Google Maps como base.

## 🗺️ Arquitetura Frontend

### Stack Tecnológico
- **Framework**: React 18 + TypeScript
- **Mapas**: Google Maps JavaScript API
- **Player**: Video.js + HLS.js
- **UI**: Tailwind CSS + shadcn/ui
- **Estado**: Zustand (leve e simples)
- **WebSocket**: native WebSocket API
- **Build**: Vite

### Estrutura de Pastas
```
frontend/
├── public/
│   ├── service-worker.js      # Push notifications
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Map/
│   │   │   ├── TacticalMap.tsx        # Mapa principal
│   │   │   ├── CameraMarker.tsx       # Marcador de câmera
│   │   │   └── DetectionHeatmap.tsx   # Heatmap de detecções
│   │   ├── Video/
│   │   │   ├── VideoPlayer.tsx        # Player HLS
│   │   │   ├── VideoGrid.tsx          # Mosaico 2x2/4x4
│   │   │   └── VideoControls.tsx
│   │   ├── Dashboard/
│   │   │   ├── HealthDashboard.tsx    # Métricas tempo real
│   │   │   ├── CameraList.tsx
│   │   │   └── AlertPanel.tsx
│   │   └── Shared/
│   │       ├── Sidebar.tsx
│   │       └── Notification.tsx
│   ├── hooks/
│   │   ├── useWebSocket.ts            # WebSocket hook
│   │   ├── useGoogleMaps.ts
│   │   └── useVideoPlayer.ts
│   ├── services/
│   │   ├── api.ts                     # Axios client
│   │   └── websocket.ts
│   ├── stores/
│   │   ├── cameraStore.ts
│   │   └── alertStore.ts
│   └── App.tsx
└── package.json
```

## 🎨 Telas Principais

### 1. Mapa Tático (Tela Principal)
**Componente**: `TacticalMap.tsx`

**Features**:
- Google Maps com marcadores de câmeras
- Cores por status (verde=online, vermelho=offline, amarelo=warning)
- Click no marcador → Popup com preview da câmera
- Heatmap de detecções LPR (últimas 24h)
- Filtros: status, marca, detecções
- Clustering de marcadores (muitas câmeras próximas)

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ [Logo] GT-Vision    [Filtros] [User] [Notif]   │
├─────────────────────────────────────────────────┤
│                                                 │
│                                                 │
│              GOOGLE MAPS                        │
│         (Marcadores de Câmeras)                 │
│                                                 │
│                                                 │
├─────────────────────────────────────────────────┤
│ [Alertas LPR em tempo real - WebSocket]        │
└─────────────────────────────────────────────────┘
```

### 2. Visualização de Câmera (Modal/Sidebar)
**Componente**: `VideoPlayer.tsx`

**Features**:
- Player HLS com auto-recover
- Controles: play/pause, fullscreen, snapshot
- Informações: nome, IP, status, latência
- Botão "Adicionar ao Mosaico"
- Timeline de thumbnails (scroll horizontal)
- Exportar clipe (selecionar período)

### 3. Mosaico (Grid View)
**Componente**: `VideoGrid.tsx`

**Features**:
- Layouts: 1x1, 2x2, 3x3, 4x4
- Drag & drop para reorganizar
- Click duplo → Fullscreen
- Salvar configuração de mosaico
- Sincronização de tempo (PTZ futuro)

### 4. Dashboard de Saúde
**Componente**: `HealthDashboard.tsx`

**Features**:
- Cards com métricas:
  - Câmeras Online/Offline
  - Detecções 24h
  - Storage usado
  - Falhas de gravação
- Gráficos (Chart.js):
  - Detecções por hora
  - Status de câmeras (timeline)
- Lista de câmeras com status
- Alertas de sistema

### 5. Histórico de Detecções
**Componente**: `DetectionHistory.tsx`

**Features**:
- Tabela de detecções LPR
- Filtros: data, câmera, placa
- Busca por placa
- Click → Ver snapshot + vídeo
- Exportar relatório (PDF)
- Marcar como incidente

## 🔌 Integrações

### Google Maps API
```typescript
// useGoogleMaps.ts
import { Loader } from '@googlemaps/js-api-loader';

const loader = new Loader({
  apiKey: process.env.VITE_GOOGLE_MAPS_API_KEY,
  version: 'weekly',
  libraries: ['places', 'visualization']
});

// Marcador customizado
const marker = new google.maps.Marker({
  position: { lat: camera.latitude, lng: camera.longitude },
  map: map,
  icon: {
    url: `/markers/${camera.status}.svg`,
    scaledSize: new google.maps.Size(40, 40)
  },
  title: camera.nome
});

// Heatmap
const heatmap = new google.maps.visualization.HeatmapLayer({
  data: detections.map(d => ({
    location: new google.maps.LatLng(d.lat, d.lng),
    weight: d.intensity
  })),
  radius: 50
});
```

### WebSocket (Alertas Tempo Real)
```typescript
// useWebSocket.ts
const ws = new WebSocket(`ws://localhost/ws/alerts?token=${token}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'lpr_detection') {
    // Mostrar notificação
    showNotification({
      title: '🚗 Placa Detectada',
      body: `${data.data.placa} - ${data.data.camera_id}`,
      onClick: () => openCamera(data.data.camera_id)
    });
    
    // Atualizar mapa (piscar marcador)
    blinkMarker(data.data.camera_id);
  }
};
```

### Video Player (HLS.js)
```typescript
// VideoPlayer.tsx
import Hls from 'hls.js';

const player = useRef<HTMLVideoElement>(null);
const hls = useRef<Hls | null>(null);

useEffect(() => {
  if (Hls.isSupported() && player.current) {
    hls.current = new Hls({
      enableWorker: true,
      lowLatencyMode: true,
      backBufferLength: 90
    });
    
    hls.current.loadSource(hlsUrl);
    hls.current.attachMedia(player.current);
    
    // Auto-recover
    hls.current.on(Hls.Events.ERROR, (event, data) => {
      if (data.fatal) {
        setTimeout(() => {
          hls.current?.loadSource(hlsUrl);
        }, 3000);
      }
    });
  }
}, [hlsUrl]);
```

## 🎨 Design System

### Cores
```css
:root {
  --primary: #2563eb;      /* Azul */
  --success: #10b981;      /* Verde - Online */
  --warning: #f59e0b;      /* Amarelo - Warning */
  --danger: #ef4444;       /* Vermelho - Offline */
  --dark: #1f2937;
  --light: #f3f4f6;
}
```

### Componentes (shadcn/ui)
- Button, Card, Badge
- Dialog, Sheet (sidebar)
- Table, Tabs
- Toast (notificações)
- Select, Input

## 📱 Responsividade

### Desktop (> 1024px)
- Mapa ocupa 70% da tela
- Sidebar com lista de câmeras (30%)
- Alertas em barra inferior

### Tablet (768px - 1024px)
- Mapa fullscreen
- Sidebar colapsável
- Mosaico 2x2 máximo

### Mobile (< 768px)
- Lista de câmeras (sem mapa)
- Player fullscreen ao clicar
- Alertas como notificações push

## 🔔 Push Notifications

### Service Worker
```javascript
// service-worker.js
self.addEventListener('push', (event) => {
  const data = event.data.json();
  
  self.registration.showNotification(data.title, {
    body: data.body,
    icon: '/icon.png',
    badge: '/badge.png',
    data: data.data,
    actions: [
      { action: 'view', title: 'Ver Câmera' },
      { action: 'dismiss', title: 'Dispensar' }
    ]
  });
});

self.addEventListener('notificationclick', (event) => {
  if (event.action === 'view') {
    clients.openWindow(`/cameras/${event.notification.data.camera_id}`);
  }
});
```

## 🚀 Features Avançadas

### 1. Busca Inteligente
- Buscar por placa (histórico)
- Buscar por câmera (nome, IP, localização)
- Buscar por período

### 2. Filtros Avançados
- Status (online/offline/warning)
- Marca (Intelbras, Hikvision)
- Com/sem detecções nas últimas 24h
- Por região (desenhar polígono no mapa)

### 3. Atalhos de Teclado
- `Space`: Play/Pause
- `F`: Fullscreen
- `M`: Abrir mapa
- `G`: Abrir grid/mosaico
- `S`: Snapshot
- `/`: Busca

### 4. Temas
- Light mode
- Dark mode (padrão para sala de controle)
- High contrast

### 5. Exportações
- Relatório PDF de detecções
- Exportar clipe MP4
- Exportar dados CSV
- Screenshot do mapa

## 📦 Dependências

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@googlemaps/js-api-loader": "^1.16.2",
    "hls.js": "^1.4.12",
    "video.js": "^8.6.1",
    "axios": "^1.6.2",
    "zustand": "^4.4.7",
    "tailwindcss": "^3.4.0",
    "@radix-ui/react-*": "latest",
    "lucide-react": "^0.294.0",
    "date-fns": "^2.30.0",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/google.maps": "^3.54.10",
    "vite": "^5.0.8",
    "typescript": "^5.3.3"
  }
}
```

## 🎯 Roadmap Frontend

### MVP (1 semana)
- [x] Mapa com marcadores
- [x] Player HLS básico
- [x] WebSocket para alertas
- [x] Dashboard de métricas

### V1.1 (2 semanas)
- [ ] Mosaico 2x2/4x4
- [ ] Heatmap de detecções
- [ ] Histórico de detecções
- [ ] Exportar clipes

### V1.2 (3 semanas)
- [ ] Push notifications
- [ ] Busca avançada
- [ ] Filtros por região
- [ ] Temas (dark/light)

### V2.0 (Futuro)
- [ ] PTZ controls
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Realidade aumentada (AR)

## 🔐 Segurança Frontend

- JWT armazenado em httpOnly cookie
- CSRF protection
- Content Security Policy
- XSS prevention (sanitize inputs)
- Rate limiting no client
- Logout automático (inatividade)

## 📊 Performance

- Code splitting (lazy loading)
- Image optimization (WebP)
- Service Worker (cache)
- Virtual scrolling (listas grandes)
- Debounce em buscas
- Memoização de componentes

---

**Próximo passo**: Implementar protótipo do TacticalMap.tsx?
