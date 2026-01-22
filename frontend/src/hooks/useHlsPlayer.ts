// VMS/frontend/src/hooks/useHlsPlayer.ts
import { useEffect, useRef, useState, MutableRefObject } from 'react';
import Hls from 'hls.js';

interface UseHlsPlayerProps {
  url: string;
  videoRef: MutableRefObject<HTMLVideoElement | null>;
  autoPlay?: boolean;
}

export const useHlsPlayer = ({ url, videoRef, autoPlay = true }: UseHlsPlayerProps) => {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const hlsRef = useRef<Hls | null>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !url) return;

    setIsLoading(true);
    setError(null);

    const cleanup = () => {
      if (hlsRef.current) {
        hlsRef.current.stopLoad();
        hlsRef.current.detachMedia();
        hlsRef.current.destroy();
        hlsRef.current = null;
      }
    };

    const initHls = () => {
      cleanup();

      if (Hls.isSupported()) {
        const hls = new Hls({
          debug: false,
          enableWorker: true,
          lowLatencyMode: true,
          
          // Otimização de memória
          backBufferLength: 10,
          
          // Otimização de latência
          liveSyncDurationCount: 1,
          liveMaxLatencyDurationCount: 3,
          maxLiveSyncPlaybackRate: 1.5,
          
          // Buffer
          maxBufferLength: 5,
          maxMaxBufferLength: 10,
          
          // Recuperação de erros
          manifestLoadingTimeOut: 10000,
          manifestLoadingMaxRetry: 3,
          levelLoadingTimeOut: 10000,
          fragLoadingTimeOut: 10000,
          
          startFragPrefetch: true,
        });

        hlsRef.current = hls;
        hls.loadSource(url);
        hls.attachMedia(video);

        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          setIsLoading(false);
          if (autoPlay) {
            video.muted = true;
            const playPromise = video.play();
            if (playPromise !== undefined) {
              playPromise.catch((e) => {
                console.log("Autoplay bloqueado pelo navegador:", e);
              });
            }
          }
        });

        hls.on(Hls.Events.ERROR, (_event, data) => {
          if (data.fatal) {
            switch (data.type) {
              case Hls.ErrorTypes.NETWORK_ERROR:
                console.warn("Erro de rede HLS, tentando recuperar...");
                hls.startLoad();
                break;
              case Hls.ErrorTypes.MEDIA_ERROR:
                console.warn("Erro de mídia HLS, tentando recuperar...");
                hls.recoverMediaError();
                break;
              default:
                cleanup();
                setError("Erro fatal na stream.");
                break;
            }
          }
        });
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = url;
        video.addEventListener('loadedmetadata', () => {
          setIsLoading(false);
          if (autoPlay) {
            video.muted = true;
            video.play().catch(() => {});
          }
        });
      }
    };

    initHls();

    return () => {
      cleanup();
      if (video) {
        video.removeAttribute('src');
        video.load();
      }
    };
  }, [url]);

  return { isLoading, error };
};
