import { useState, useCallback, useEffect, useRef } from "react";
import { GoogleMap, useJsApiLoader, MarkerF, InfoWindowF } from "@react-google-maps/api";
import { Camera as CameraIcon, Maximize2, MapPin } from "lucide-react";
import CameraStatusBadge from "./CameraStatusBadge";

const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "";

export interface Camera {
  id: number;
  name: string;
  location: string;
  latitude?: number;
  longitude?: number;
  status: "online" | "offline" | "lpr";
  stream_url?: string;
  thumbnail_url?: string | null;
}

interface MapViewerProps {
  cameras?: Camera[];
  height?: string;
  zoom?: number;
  onCameraClick?: (camera: Camera) => void;
  onCameraDoubleClick?: (camera: Camera) => void;
}

const mapContainerStyle = {
  width: "100%",
  height: "100%",
};

const defaultCenter = { lat: -15.7801, lng: -47.9292 };
const PIN_SVG_PATH = "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z";

export default function MapViewer({
  cameras = [],
  height = "500px",
  zoom = 13,
  onCameraClick,
  onCameraDoubleClick,
}: MapViewerProps) {
  const [selectedCamera, setSelectedCamera] = useState<Camera | null>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const clickTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const { isLoaded, loadError } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: API_KEY,
  });

  const validCameras = cameras.filter(
    (c) => c.latitude !== undefined && c.latitude !== null && 
           c.longitude !== undefined && c.longitude !== null
  );

  const onLoad = useCallback((mapInstance: google.maps.Map) => {
    setMap(mapInstance);
  }, []);

  const handleZoomChanged = useCallback(() => {
    if (map) {
      const currentZoom = map.getZoom();
      if (currentZoom && currentZoom < 10 && selectedCamera) {
        setSelectedCamera(null);
      }
    }
  }, [map, selectedCamera]);

  useEffect(() => {
    if (map && validCameras.length > 0 && !selectedCamera) {
      const bounds = new google.maps.LatLngBounds();
      let hasValidBounds = false;

      validCameras.forEach((c) => {
        const lat = Number(c.latitude);
        const lng = Number(c.longitude);
        if (!isNaN(lat) && !isNaN(lng) && lat !== 0 && lng !== 0) {
            bounds.extend({ lat, lng });
            hasValidBounds = true;
        }
      });

      if (hasValidBounds) {
          map.fitBounds(bounds);
      }
    }
  }, [map, validCameras.length, selectedCamera]); 

  const handleMarkerClick = useCallback((camera: Camera) => {
    setSelectedCamera(camera);
    
    if (map) {
        const lat = Number(camera.latitude);
        const lng = Number(camera.longitude);
        
        map.panTo({ lat, lng });
        
        const currentZoom = map.getZoom();
        if (currentZoom && currentZoom < 16) {
            setTimeout(() => map.setZoom(16), 300);
        }
    }

    // Trigger onCameraClick callback se existir
    if (onCameraClick) {
      onCameraClick(camera);
    }
  }, [map, onCameraClick]);

  const handleInfoWindowClick = useCallback((e: React.MouseEvent, camera: Camera) => {
    if ((e.target as HTMLElement).closest('button')) return;

    if (clickTimeoutRef.current) {
        clearTimeout(clickTimeoutRef.current);
        clickTimeoutRef.current = null;
        if (onCameraDoubleClick) onCameraDoubleClick(camera);
    } else {
        clickTimeoutRef.current = setTimeout(() => {
            clickTimeoutRef.current = null;
        }, 250); 
    }
  }, [onCameraDoubleClick]);

  if (!isLoaded) {
    return (
      <div style={{ height }} className="w-full h-full bg-muted animate-pulse rounded-lg flex items-center justify-center text-muted-foreground">
        Carregando Mapa...
      </div>
    );
  }
  
  if (loadError) {
    return (
      <div className="flex items-center justify-center h-full text-red-500 bg-red-50 rounded-lg border border-red-200">
        Erro ao carregar Google Maps API
      </div>
    );
  }

  return (
    <div style={{ height }} className="w-full h-full relative z-0">
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={defaultCenter}
        zoom={zoom}
        onLoad={onLoad}
        onZoomChanged={handleZoomChanged}
        options={{
          mapTypeControl: false,
          fullscreenControl: false,
          streetViewControl: false,
          zoomControl: true,
          zoomControlOptions: { position: 9 },
          gestureHandling: "cooperative",
          styles: [
            { featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }] },
            { featureType: "transit", elementType: "labels", stylers: [{ visibility: "off" }] }
          ],
        }}
      >
        {validCameras.map((camera) => (
          <MarkerF
            key={camera.id}
            position={{ lat: Number(camera.latitude), lng: Number(camera.longitude) }}
            onClick={() => handleMarkerClick(camera)}
            icon={{
              path: PIN_SVG_PATH,
              fillColor: camera.status === 'online' ? "#10b981" : "#ef4444",
              fillOpacity: 1,
              strokeColor: "#FFFFFF",
              strokeWeight: 2,
              scale: 2,
              anchor: new google.maps.Point(12, 22), 
              labelOrigin: new google.maps.Point(12, 9),
            }}
          >
            {selectedCamera?.id === camera.id && (
              <InfoWindowF
                onCloseClick={() => setSelectedCamera(null)}
                options={{ 
                    pixelOffset: new google.maps.Size(0, -30), 
                    disableAutoPan: false,
                    maxWidth: 320 
                }}
              >
                <div 
                    className="bg-white rounded-lg overflow-hidden flex flex-col font-sans shadow-sm cursor-pointer group w-[260px]"
                    onClick={(e) => handleInfoWindowClick(e as any, camera)}
                >
                  {/* Miniatura da câmera com thumbnail real */}
                  <div className="relative h-36 w-full bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center overflow-hidden">
                    {camera.thumbnail_url ? (
                      <img 
                        src={camera.thumbnail_url} 
                        alt={camera.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          // Fallback se imagem falhar
                          (e.target as HTMLImageElement).style.display = 'none';
                          const parent = (e.target as HTMLElement).parentElement;
                          if (parent) {
                            parent.innerHTML = `
                              <div class="flex flex-col items-center justify-center h-full w-full">
                                <svg class="w-12 h-12 text-slate-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                                <span class="text-xs font-medium text-slate-400 uppercase tracking-widest">
                                  ${camera.status === 'online' ? 'Clique para Ver' : 'Câmera Offline'}
                                </span>
                              </div>
                            `;
                          }
                        }}
                      />
                    ) : (
                      <>
                        <CameraIcon size={48} strokeWidth={1.5} className="text-slate-300 mb-2" />
                        <span className="text-xs font-medium text-slate-400 uppercase tracking-widest">
                            {camera.status === 'online' ? 'Clique para Ver' : 'Câmera Offline'}
                        </span>
                      </>
                    )}

                    {camera.status === 'online' && (
                        <div className="absolute top-2 left-2 z-20 bg-red-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow-sm flex items-center gap-1 animate-pulse">
                            <span className="w-1.5 h-1.5 bg-white rounded-full"/> LIVE
                        </div>
                    )}

                    <div className="absolute inset-0 bg-black/40 z-20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-[2px]">
                        <span className="bg-white text-black text-xs font-bold px-3 py-1.5 rounded-full flex items-center gap-1.5 shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-transform">
                            <Maximize2 className="w-3.5 h-3.5"/> Abrir Player
                        </span>
                    </div>
                  </div>
                  
                  <div className="p-3 border-t border-slate-100">
                    <div className="flex justify-between items-start mb-1">
                        <h3 className="font-bold text-slate-800 text-sm leading-tight truncate pr-2 flex-1">
                            {camera.name}
                        </h3>
                        <CameraStatusBadge status={camera.status} />
                    </div>
                    
                    <div className="flex items-center gap-1.5 text-slate-500 mt-1">
                        <MapPin className="w-3 h-3 shrink-0" />
                        <p className="text-xs font-medium uppercase tracking-wide truncate">
                            {camera.location || "Localização não definida"}
                        </p>
                    </div>
                  </div>
                </div>
              </InfoWindowF>
            )}
          </MarkerF>
        ))}
      </GoogleMap>
    </div>
  );
}