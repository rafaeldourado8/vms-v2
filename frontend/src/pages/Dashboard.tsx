import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';
import api from '@/lib/axios';
import MapViewer, { Camera as CameraType } from '@/components/MapViewer';

const Dashboard = () => {
  const navigate = useNavigate();

  // Busca Câmeras (Cacheada para performance)
  const { data: cameras = [], isLoading } = useQuery({
    queryKey: ['cameras'],
    queryFn: async () => {
      const response = await api.get('/cameras/');
      const list = response.data.results || response.data || [];
      return list.map((c: any) => ({
        ...c,
        // Garante compatibilidade de campos
        stream_url: c.stream_url_frontend || c.stream_url,
        latitude: c.latitude ? Number(c.latitude) : null,
        longitude: c.longitude ? Number(c.longitude) : null,
      }));
    },
    staleTime: 60000, // 1 minuto de cache
  });

  const handleCameraClick = (camera: CameraType) => {
    // Redireciona para a rota /live passando o ID da câmera como parâmetro
    navigate(`/live?cameraId=${camera.id}`);
  };

  if (isLoading) {
    return (
      <div className="w-full h-screen flex items-center justify-center bg-zinc-950 text-zinc-400 gap-2">
        <Loader2 className="animate-spin w-6 h-6" />
        <span>Carregando mapa...</span>
      </div>
    );
  }

  return (
    <div className="w-full h-full relative overflow-hidden bg-zinc-950">
      <MapViewer 
        cameras={cameras} 
        height="100%" 
        // Ação única: Clicar no pino leva ao monitoramento
        onCameraClick={handleCameraClick}
        onCameraDoubleClick={handleCameraClick} 
      />
      
      {/* Overlay informativo minimalista */}
      <div className="absolute top-6 left-1/2 -translate-x-1/2 z-10 pointer-events-none">
        <div className="bg-black/60 backdrop-blur-md px-6 py-2 rounded-full border border-white/10 shadow-xl">
          <p className="text-white/90 text-sm font-medium">
            Selecione uma câmera no mapa para visualizar
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;