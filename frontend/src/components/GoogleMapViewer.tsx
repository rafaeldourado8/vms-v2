import { useState } from 'react';
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';
import { useSnapshot } from '@/hooks/useThumbnails';
import { Button } from '@/components/ui/button';
import CameraStatusBadge from './CameraStatusBadge';

interface Camera {
  id: number;
  name: string;
  location: string;
  latitude: number;
  longitude: number;
  status: 'online' | 'offline' | 'warning';
  detections_24h?: number;
}

interface GoogleMapViewerProps {
  cameras: Camera[];
  onCameraClick?: (camera: Camera) => void;
  height?: string;
}

const CameraPopup = ({ camera, onViewClick }: { camera: Camera; onViewClick: () => void }) => {
  const { data: snapshotUrl } = useSnapshot(camera.id);

  return (
    <div className="p-3 min-w-[250px]">
      {snapshotUrl && (
        <img 
          src={snapshotUrl} 
          alt={camera.name}
          className="w-full h-32 object-cover rounded-lg mb-3"
        />
      )}
      
      <h3 className="font-bold text-base mb-1">{camera.name}</h3>
      <p className="text-sm text-gray-600 mb-2">{camera.location}</p>
      
      <div className="flex items-center justify-between mb-3">
        <CameraStatusBadge status={camera.status} />
        {camera.detections_24h !== undefined && (
          <span className="text-xs text-gray-500">
            {camera.detections_24h} detecções (24h)
          </span>
        )}
      </div>

      <Button onClick={onViewClick} className="w-full" size="sm">
        Ver Câmera
      </Button>
    </div>
  );
};

const GoogleMapViewer = ({ cameras, onCameraClick, height = '500px' }: GoogleMapViewerProps) => {
  const [selectedCamera, setSelectedCamera] = useState<Camera | null>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);

  const mapContainerStyle = {
    width: '100%',
    height
  };

  const center = {
    lat: -15.7801,
    lng: -47.9292
  };

  const onLoad = (mapInstance: google.maps.Map) => {
    setMap(mapInstance);
    
    // Ajustar bounds para mostrar todas as câmeras
    if (cameras.length > 0) {
      const bounds = new google.maps.LatLngBounds();
      cameras.forEach(camera => {
        bounds.extend({ lat: camera.latitude, lng: camera.longitude });
      });
      mapInstance.fitBounds(bounds);
    }
  };

  const getMarkerIcon = (status: string) => {
    const colors = {
      online: '#10b981',
      offline: '#ef4444',
      warning: '#f59e0b'
    };

    return {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 10,
      fillColor: colors[status as keyof typeof colors] || '#6b7280',
      fillOpacity: 0.9,
      strokeColor: '#ffffff',
      strokeWeight: 2
    };
  };

  // Expor função para piscar marcador (WebSocket)
  (window as any).blinkMarker = (cameraId: string) => {
    const camera = cameras.find(c => c.id.toString() === cameraId);
    if (camera && map) {
      map.panTo({ lat: camera.latitude, lng: camera.longitude });
      setSelectedCamera(camera);
      
      setTimeout(() => setSelectedCamera(null), 3000);
    }
  };

  return (
    <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={center}
        zoom={12}
        onLoad={onLoad}
        options={{
          mapTypeControl: true,
          streetViewControl: false,
          fullscreenControl: true,
          styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }]
            }
          ]
        }}
      >
        {cameras.map(camera => (
          <Marker
            key={camera.id}
            position={{ lat: camera.latitude, lng: camera.longitude }}
            icon={getMarkerIcon(camera.status)}
            onClick={() => setSelectedCamera(camera)}
            animation={camera.status === 'warning' ? google.maps.Animation.BOUNCE : undefined}
          />
        ))}

        {selectedCamera && (
          <InfoWindow
            position={{ lat: selectedCamera.latitude, lng: selectedCamera.longitude }}
            onCloseClick={() => setSelectedCamera(null)}
          >
            <CameraPopup 
              camera={selectedCamera}
              onViewClick={() => {
                onCameraClick?.(selectedCamera);
                setSelectedCamera(null);
              }}
            />
          </InfoWindow>
        )}
      </GoogleMap>
    </LoadScript>
  );
};

export default GoogleMapViewer;
