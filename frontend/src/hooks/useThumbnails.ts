import { useQuery } from '@tanstack/react-query';
import api from '@/lib/axios';

interface Thumbnail {
  timestamp: string;
  url: string;
}

export const useThumbnails = (cameraId: string | number | undefined) => {
  return useQuery({
    queryKey: ['thumbnails', cameraId],
    queryFn: async () => {
      if (!cameraId) return [];
      
      const response = await api.get(`/api/v1/cameras/${cameraId}/timeline`, {
        params: {
          start: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
          end: new Date().toISOString()
        }
      });
      
      return response.data.thumbnails || [];
    },
    enabled: !!cameraId,
    staleTime: 1000 * 60 * 5, // 5 minutos
  });
};

export const useSnapshot = (cameraId: string | number | undefined) => {
  return useQuery({
    queryKey: ['snapshot', cameraId],
    queryFn: async () => {
      if (!cameraId) return null;
      
      const response = await api.get(`/api/v1/snapshots/${cameraId}`, {
        responseType: 'blob'
      });
      
      return URL.createObjectURL(response.data);
    },
    enabled: !!cameraId,
    staleTime: 1000 * 30, // 30 segundos
  });
};
