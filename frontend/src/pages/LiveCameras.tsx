import React, { useState, useEffect, useRef } from "react";
import { useQuery, keepPreviousData } from "@tanstack/react-query";
import { Edit, Trash2, Loader2, PlayCircle, AlertCircle, Video } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import api from "@/lib/axios";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import VideoPlayer from "@/components/VideoPlayer";

interface CameraType {
  id: number;
  name: string;
  location: string;
  status: "online" | "offline" | "warning";
  thumbnail_url?: string | null;
  stream_url_frontend: string;
}

// --- Componente de Thumbnail Inteligente (Lazy + 5s Stream + Snapshot) ---
const StreamingThumbnail = ({ 
  streamUrl, 
  posterUrl, 
  alt 
}: { 
  streamUrl: string; 
  posterUrl?: string | null; 
  alt: string; 
}) => {
  const [mode, setMode] = useState<'idle' | 'streaming' | 'snapshot'>('idle');
  const [snapshotSrc, setSnapshotSrc] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  // 1. Lazy Loading: Ativa stream apenas quando entra na tela
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && mode === 'idle') {
          setMode('streaming');
        }
      },
      { threshold: 0.1, rootMargin: '50px' }
    );

    if (containerRef.current) observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [mode]);

  // 2. Lógica: Toca 5s -> Tira Foto -> Para Stream
  useEffect(() => {
    if (mode === 'streaming' && videoRef.current) {
      const videoEl = videoRef.current;
      
      // Mudo é obrigatório para autoplay
      videoEl.muted = true; 
      videoEl.volume = 0;

      const handlePlaying = () => {
        const timer = setTimeout(() => {
          captureSnapshot(videoEl);
        }, 5000); // 5 segundos de "preview" vivo
        return () => clearTimeout(timer);
      };

      videoEl.play().catch(() => console.log("Autoplay retido"));
      videoEl.addEventListener('playing', handlePlaying, { once: true });
      
      // Timeout de segurança caso stream falhe
      const safety = setTimeout(() => setMode('snapshot'), 15000);

      return () => {
        videoEl.removeEventListener('playing', handlePlaying);
        clearTimeout(safety);
      };
    }
  }, [mode]);

  const captureSnapshot = (videoEl: HTMLVideoElement) => {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = videoEl.videoWidth || 640;
      canvas.height = videoEl.videoHeight || 360;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);
        setSnapshotSrc(canvas.toDataURL('image/jpeg', 0.7));
      }
    } catch (e) {
      console.warn("Erro no snapshot (CORS?):", e);
    } finally {
      setMode('snapshot');
    }
  };

  return (
    <div ref={containerRef} className="w-full sm:w-48 h-32 sm:h-28 bg-black/40 rounded-lg overflow-hidden relative shrink-0 border border-white/10 shadow-inner">
      {mode === 'idle' && (
        <div className="w-full h-full flex items-center justify-center backdrop-blur-sm">
          <Loader2 className="w-5 h-5 animate-spin text-white/30" />
        </div>
      )}

      {mode === 'streaming' && (
        <VideoPlayer
          url={streamUrl}
          poster={posterUrl}
          videoRefProp={videoRef}
          className="w-full h-full pointer-events-none object-cover" 
        />
      )}

      {mode === 'snapshot' && (
        <div className="relative w-full h-full group">
          <img 
            src={snapshotSrc || posterUrl || '/placeholder.jpg'} 
            alt={alt} 
            className="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity" 
          />
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/40">
             <Video className="w-6 h-6 text-white drop-shadow-lg" />
          </div>
        </div>
      )}
    </div>
  );
};

const LiveCameras: React.FC = () => {
  const [page, setPage] = useState(1);
  const [selectedCamera, setSelectedCamera] = useState<CameraType | null>(null);

  const { data, isLoading, isError } = useQuery({
    queryKey: ['cameras', page],
    queryFn: async () => {
      const response = await api.get(`/v1/cameras?page=${page}&limit=10`);
      return response.data;
    },
    placeholderData: keepPreviousData, 
  });

  const cameras = data?.results || [];
  const total = data?.total || 0;
  const totalPages = Math.ceil(total / 10);

  // Loading Skeleton Glass
  if (isLoading && !data) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-3 text-white/60">
        <Loader2 className="animate-spin w-8 h-8" />
        <span className="font-light tracking-widest text-sm">SINCRONIZANDO FEEDS...</span>
      </div>
    );
  }

  return (
    // Container principal transparente para mostrar o mapa de fundo
    <div className="p-6 max-w-7xl mx-auto space-y-6 animate-in fade-in duration-700">
      
      {/* Header com efeito Glass */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-black/40 backdrop-blur-xl p-6 rounded-2xl border border-white/10 shadow-2xl">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white drop-shadow-md flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse shadow-[0_0_10px_rgba(239,68,68,0.8)]" />
            Monitoramento Tático
          </h1>
          <p className="text-zinc-400 text-sm mt-1">
            {total} unidades ativas no perímetro
          </p>
        </div>
        <Button 
          variant="outline" 
          onClick={() => setPage(1)} 
          className="bg-white/5 border-white/10 hover:bg-white/10 text-white"
        >
          Atualizar Grade
        </Button>
      </div>
      
      {/* Grid de Câmeras */}
      <div className="grid gap-3">
        {cameras.map((camera: CameraType) => (
          <Card 
            key={camera.id} 
            // ESTILO GLASSMORFISM (Vidro)
            className="group flex flex-col sm:flex-row items-center gap-4 p-3 bg-black/60 backdrop-blur-md border-white/10 hover:bg-black/70 hover:border-white/20 transition-all duration-300 cursor-pointer shadow-lg"
            onDoubleClick={() => setSelectedCamera(camera)}
          >
            {/* Thumbnail */}
            <StreamingThumbnail 
              streamUrl={camera.stream_url_frontend} 
              posterUrl={camera.thumbnail_url}
              alt={camera.name}
            />
            
            {/* Info */}
            <div className="flex-1 w-full text-center sm:text-left space-y-2">
              <div className="flex items-center justify-center sm:justify-start gap-3">
                <h3 className="font-semibold text-lg text-white drop-shadow-sm">{camera.name}</h3>
                
                {/* Badge de Status Neon */}
                <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${
                  camera.status === 'online' 
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30 shadow-[0_0_10px_rgba(16,185,129,0.2)]' 
                    : 'bg-red-500/20 text-red-400 border-red-500/30'
                }`}>
                  <div className={`w-1.5 h-1.5 rounded-full ${camera.status === 'online' ? 'bg-emerald-400' : 'bg-red-400'}`} />
                  {camera.status}
                </div>
              </div>
              
              <p className="text-sm text-zinc-400 flex items-center justify-center sm:justify-start gap-1 font-mono">
                <span className="text-zinc-600">LOC:</span> {camera.location}
              </p>
            </div>

            {/* Ações */}
            <div className="flex gap-2 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
               <Button 
                variant="ghost" 
                size="icon"
                className="hover:bg-white/10 text-zinc-300 hover:text-white"
               >
                 <Edit className="w-4 h-4" />
               </Button>
               <Button 
                variant="ghost" 
                size="icon"
                className="text-red-400/70 hover:text-red-400 hover:bg-red-500/10"
               >
                 <Trash2 className="w-4 h-4" />
               </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Paginação Glass */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-4 mt-8 bg-black/40 backdrop-blur-md p-2 rounded-full border border-white/5 w-fit mx-auto shadow-xl">
          <Button 
            variant="ghost"
            disabled={page === 1} 
            onClick={() => setPage(p => p - 1)}
            className="text-white hover:bg-white/10 rounded-full"
          >
            Anterior
          </Button>
          <span className="text-sm text-zinc-300 font-mono px-2">{page} / {totalPages}</span>
          <Button 
            variant="ghost"
            disabled={page === totalPages} 
            onClick={() => setPage(p => p + 1)}
            className="text-white hover:bg-white/10 rounded-full"
          >
            Próxima
          </Button>
        </div>
      )}

      {/* Modal Player Fullscreen */}
      <Dialog open={!!selectedCamera} onOpenChange={() => setSelectedCamera(null)}>
        <DialogContent className="max-w-6xl bg-black/90 backdrop-blur-xl border-white/10 p-0 overflow-hidden shadow-2xl">
          {selectedCamera && (
            <div className="aspect-video w-full bg-black relative">
              <div className="absolute top-0 left-0 right-0 z-20 p-4 bg-gradient-to-b from-black/90 to-transparent flex justify-between items-start pointer-events-none">
                 <div>
                    <h2 className="text-white font-bold text-lg drop-shadow-md">{selectedCamera.name}</h2>
                    <p className="text-zinc-400 text-xs font-mono">{selectedCamera.location}</p>
                 </div>
                 <div className="px-3 py-1 rounded bg-red-600/80 backdrop-blur text-white text-[10px] font-bold animate-pulse shadow-lg border border-red-500/50">
                    TRANSMISSÃO AO VIVO
                 </div>
              </div>
              <VideoPlayer
                url={selectedCamera.stream_url_frontend}
                poster={selectedCamera.thumbnail_url}
                className="w-full h-full"
              />
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default LiveCameras;