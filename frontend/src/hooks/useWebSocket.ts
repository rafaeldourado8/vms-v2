import { useEffect, useRef, useState } from 'react';

interface LPRDetection {
  camera_id: string;
  placa: string;
  timestamp: string;
  confianca: number;
  tenant_id: string;
}

interface WebSocketMessage {
  type: 'lpr_detection' | 'connected' | 'pong';
  data?: LPRDetection;
}

export const useWebSocket = (token: string | null) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastDetection, setLastDetection] = useState<LPRDetection | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!token) return;

    const ws = new WebSocket(`ws://localhost/ws/alerts?token=${token}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket conectado');
    };

    ws.onmessage = (event) => {
      const message: WebSocketMessage = JSON.parse(event.data);
      
      if (message.type === 'lpr_detection' && message.data) {
        setLastDetection(message.data);
        
        // Piscar marcador no mapa
        if (window.blinkMarker) {
          window.blinkMarker(message.data.camera_id);
        }
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket erro:', error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket desconectado');
    };

    // Heartbeat (ping a cada 30s)
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping');
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      ws.close();
    };
  }, [token]);

  return { isConnected, lastDetection };
};
