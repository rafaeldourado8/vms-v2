import React, { useState, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { List, X, Maximize2, Minimize2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import api from "@/lib/axios";
import { useToast } from "@/hooks/use-toast";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useThumbnails } from "@/hooks/useThumbnails";
import VideoPlayer from "@/components/VideoPlayer";
import Timeline from "@/components/Timeline";
import CameraSideList from "@/components/CameraSideList";
import GoogleMapViewer from "@/components/GoogleMapViewer";
import { cn } from "@/lib/utils";

interface CameraType {
  id: number;
  name: string;
  location: string;
  latitude: number;
  longitude: number;
  status: "online" | "offline" | "warning";
  thumbnail_url?: string | null;
  stream_url_frontend: string;
  stream_key?: string;
}

const glassSheetClasses = "bg-black/30 backdrop-blur-xl border-r border-white/10 text-white shadow-2xl";

const LiveCameras: React.FC = () => {
  const [selectedCamera, setSelectedCamera] = useState<CameraType | null>(null);
  const [isPlayerExpanded, setIsPlayerExpanded] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const { toast } = useToast();

  // WebSocket para alertas LPR
  const token = localStorage.getItem('token');
  const { isConnected, lastDetection } = useWebSocket(token);

  // Buscar câmeras
  const { data: cameras = [], isLoading } = useQuery({
    queryKey: ['cameras'],
    queryFn: async () => {
      const response = await api.get("/cameras/");
      const raw = response.data;
      const list = Array.isArray(raw) ? raw : Array.isArray(raw?.results) ? raw.results : [];

      return list.map((c: any) => {
        let streamUrl = "";
        if (c.stream_key) {
           streamUrl = `/hls/${c.stream_key}/index.m3u8`;
        } else {
           streamUrl = c.stream_url_frontend || "";
        }

        return {
          id: c.id,
          name: c.name,
          location: c.location || "Sem localização",
          latitude: Number(c.latitude ?? 0),
          longitude: Number(c.longitude ?? 0),
          status: c.status || "offline",
          thumbnail_url: c.thumbnail_url ?? c.thumbnail ?? null,
          stream_url_frontend: streamUrl,
          stream_key: c.stream_key,
        };
      }) as CameraType[];
    },
    staleTime: 1000 * 60 * 5,
  });

  // Buscar thumbnails da câmera selecionada
  const { data: thumbnails = [] } = useThumbnails(selectedCamera?.id);

  const handleCameraSelect = (cam: CameraType) => {
    setSelectedCamera(cam);
  };

  const handleClosePlayer = () => {
    setSelectedCamera(null);
    setIsPlayerExpanded(false);
  };

  // Mostrar alerta quando houver detecção LPR
  React.useEffect(() => {
    if (lastDetection) {
      toast({
        title: "🚗 Placa Detectada",
        description: `${lastDetection.placa} - Câmera ${lastDetection.camera_id}`,
        duration: 5000,
      });
    }
  }, [lastDetection, toast]);

  if (isLoading) {
    return <div className="h-full w-full bg-zinc-950 flex items-center justify-center">
      <Loader2 className="animate-spin text-white w-8 h-8"/>
    </div>;
  }

  return (
    <div className="h-full w-full relative bg-zinc-950 overflow-hidden">
      
      {/* MAPA GOOGLE MAPS */}
      <div className="absolute inset-0 z-0">
        <GoogleMapViewer
          cameras={cameras}
          height="100%"
          onCameraClick={handleCameraSelect}
        />
      </div>

      {/* SIDEBAR FLUTUANTE */}
      <div className="absolute top-4 left-4 z-10">
        <Sheet>
          <SheetTrigger asChild>
            <Button size="icon" className="h-10 w-10 rounded-xl shadow-lg bg-black/40 backdrop-blur-md hover:bg-black/60 border border-white/10 text-white transition-all duration-300">
              <List className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className={`p-0 w-[320px] sm:w-[380px] ${glassSheetClasses}`}>
             <div className="h-full pt-12 px-1"> 
                <CameraSideList 
                  cameras={cameras} 
                  selectedId={selectedCamera?.id} 
                  onSelect={(cam) => {
                      const fullCam = cameras.find(c => c.id === cam.id);
                      if (fullCam) handleCameraSelect(fullCam);
                  }} 
                />
             </div>
          </SheetContent>
        </Sheet>
      </div>

      {/* STATUS WEBSOCKET */}
      <div className="absolute top-4 right-4 z-10">
        <div className={cn(
          "px-3 py-1.5 rounded-full text-xs font-medium backdrop-blur-md border",
          isConnected 
            ? "bg-green-500/20 border-green-500/30 text-green-300" 
            : "bg-red-500/20 border-red-500/30 text-red-300"
        )}>
          {isConnected ? "● Conectado" : "○ Desconectado"}
        </div>
      </div>

      {/* PLAYER + TIMELINE */}
      <div 
        className={cn(
          "absolute bottom-0 left-0 right-0 z-20 transition-transform duration-500 ease-in-out bg-black/90 backdrop-blur-xl shadow-2xl border-t border-white/10 flex flex-col",
          selectedCamera ? "translate-y-0" : "translate-y-full",
          isPlayerExpanded ? "h-[90%]" : "h-[50%]"
        )}
      >
        {selectedCamera && (
          <>
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-white/5 border-b border-white/5 shrink-0">
              <div className="flex items-center gap-3">
                <div className={`w-2.5 h-2.5 rounded-full shadow-[0_0_8px_rgba(0,0,0,0.5)] ${selectedCamera.status === 'online' ? 'bg-green-500 shadow-green-500/50' : 'bg-red-500 shadow-red-500/50'} animate-pulse`} />
                <div>
                   <h3 className="font-semibold text-white text-sm leading-none">{selectedCamera.name}</h3>
                   <p className="text-[10px] text-white/50 mt-0.5">{selectedCamera.location}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-1">
                <Button 
                    variant="ghost" 
                    size="icon" 
                    className="h-8 w-8 text-white/50 hover:text-white hover:bg-white/10 rounded-full"
                    onClick={() => setIsPlayerExpanded(!isPlayerExpanded)}
                >
                  {isPlayerExpanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
                </Button>
                <Button 
                    variant="ghost" 
                    size="icon" 
                    className="h-8 w-8 text-white/50 hover:text-red-400 hover:bg-red-500/10 rounded-full"
                    onClick={handleClosePlayer}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Vídeo */}
            <div className="flex-1 relative bg-black overflow-hidden flex items-center justify-center">
               <VideoPlayer
                  url={selectedCamera.stream_url_frontend}
                  poster={selectedCamera.thumbnail_url}
                  className="w-full h-full"
                  videoRefProp={videoRef}
                />
            </div>

            {/* TIMELINE COM THUMBNAILS REAIS */}
            <Timeline
              thumbnails={thumbnails}
              currentTime={0}
              duration={86400}
              isPlaying={false}
              onSeek={(time) => console.log('Seek to:', time)}
              onTogglePlay={() => console.log('Toggle play')}
              className="border-0 bg-transparent"
            />
          </>
        )}
      </div>
    </div>
  );
};

export default LiveCameras;