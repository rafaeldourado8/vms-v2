// VMS/frontend/src/hooks/useVideoTimeline.ts
import { useState, useEffect, useCallback, useRef, MutableRefObject } from 'react';

export interface TimelineState {
  currentTime: number;      // Tempo atual do vídeo em segundos
  duration: number;         // Duração total em segundos
  isPlaying: boolean;       // Estado de reprodução
  isLive: boolean;          // Se está no modo ao vivo
  bufferedEnd: number;      // Até onde foi carregado
  playbackRate: number;     // Velocidade de reprodução
}

export interface ClipRange {
  start: number;  // Tempo inicial do clip em segundos
  end: number;    // Tempo final do clip em segundos
}

export interface UseVideoTimelineProps {
  videoRef: MutableRefObject<HTMLVideoElement | null>;
  selectedDate: Date;
  onClipSave?: (clip: ClipRange, date: Date) => Promise<void>;
}

export interface UseVideoTimelineReturn {
  state: TimelineState;
  clipRange: ClipRange | null;
  isClipMode: boolean;
  // Controles de playback
  play: () => void;
  pause: () => void;
  togglePlay: () => void;
  seek: (time: number) => void;
  seekToLive: () => void;
  setPlaybackRate: (rate: number) => void;
  // Controles de clip
  startClipMode: () => void;
  cancelClipMode: () => void;
  setClipStart: (time: number) => void;
  setClipEnd: (time: number) => void;
  saveClip: () => Promise<void>;
  // Utilitários
  formatTime: (seconds: number) => string;
  getProgressPercent: () => number;
}

export const useVideoTimeline = ({
  videoRef,
  selectedDate,
  onClipSave,
}: UseVideoTimelineProps): UseVideoTimelineReturn => {
  const [state, setState] = useState<TimelineState>({
    currentTime: 0,
    duration: 0,
    isPlaying: false,
    isLive: true,
    bufferedEnd: 0,
    playbackRate: 1,
  });

  const [isClipMode, setIsClipMode] = useState(false);
  const [clipRange, setClipRange] = useState<ClipRange | null>(null);
  
  const animationFrameRef = useRef<number | null>(null);
  const isLiveRef = useRef(true);

  // Loop de atualização de estado (usa requestAnimationFrame para performance)
  const updateState = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;

    const buffered = video.buffered;
    const bufferedEnd = buffered.length > 0 ? buffered.end(buffered.length - 1) : 0;
    
    // Considera "ao vivo" se estiver dentro de 3 segundos do final do buffer
    const isNearLive = bufferedEnd - video.currentTime < 3;
    isLiveRef.current = isNearLive && !video.paused;

    setState(prev => ({
      ...prev,
      currentTime: video.currentTime,
      duration: video.duration || 86400, // Para live, considera 24h
      isPlaying: !video.paused,
      isLive: isNearLive,
      bufferedEnd,
      playbackRate: video.playbackRate,
    }));

    animationFrameRef.current = requestAnimationFrame(updateState);
  }, [videoRef]);

  // Inicia/para o loop de atualização
  useEffect(() => {
    animationFrameRef.current = requestAnimationFrame(updateState);
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [updateState]);

  // Eventos do vídeo para sincronização precisa
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handlePlay = () => setState(prev => ({ ...prev, isPlaying: true }));
    const handlePause = () => setState(prev => ({ ...prev, isPlaying: false }));
    const handleRateChange = () => setState(prev => ({ ...prev, playbackRate: video.playbackRate }));

    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);
    video.addEventListener('ratechange', handleRateChange);

    return () => {
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
      video.removeEventListener('ratechange', handleRateChange);
    };
  }, [videoRef]);

  // Controles de playback
  const play = useCallback(() => {
    videoRef.current?.play().catch(console.error);
  }, [videoRef]);

  const pause = useCallback(() => {
    videoRef.current?.pause();
  }, [videoRef]);

  const togglePlay = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;
    
    if (video.paused) {
      video.play().catch(console.error);
    } else {
      video.pause();
    }
  }, [videoRef]);

  const seek = useCallback((time: number) => {
    const video = videoRef.current;
    if (!video) return;
    
    video.currentTime = Math.max(0, Math.min(time, video.duration || time));
  }, [videoRef]);

  const seekToLive = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;
    
    const buffered = video.buffered;
    if (buffered.length > 0) {
      video.currentTime = buffered.end(buffered.length - 1) - 0.5;
      if (video.paused) {
        video.play().catch(console.error);
      }
    }
  }, [videoRef]);

  const setPlaybackRate = useCallback((rate: number) => {
    const video = videoRef.current;
    if (video) {
      video.playbackRate = rate;
    }
  }, [videoRef]);

  // Controles de clip
  const startClipMode = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;
    
    video.pause();
    setIsClipMode(true);
    
    // Define range inicial de 30 segundos a partir da posição atual
    const currentTime = video.currentTime;
    setClipRange({
      start: Math.max(0, currentTime - 15),
      end: currentTime + 15,
    });
  }, [videoRef]);

  const cancelClipMode = useCallback(() => {
    setIsClipMode(false);
    setClipRange(null);
  }, []);

  const setClipStart = useCallback((time: number) => {
    setClipRange(prev => {
      if (!prev) return { start: time, end: time + 30 };
      return { ...prev, start: Math.min(time, prev.end - 1) };
    });
  }, []);

  const setClipEnd = useCallback((time: number) => {
    setClipRange(prev => {
      if (!prev) return { start: Math.max(0, time - 30), end: time };
      return { ...prev, end: Math.max(time, prev.start + 1) };
    });
  }, []);

  const saveClip = useCallback(async () => {
    if (!clipRange || !onClipSave) return;
    
    await onClipSave(clipRange, selectedDate);
    setIsClipMode(false);
    setClipRange(null);
  }, [clipRange, selectedDate, onClipSave]);

  // Utilitários
  const formatTime = useCallback((seconds: number): string => {
    if (!isFinite(seconds) || isNaN(seconds)) return '00:00:00';
    
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }, []);

  const getProgressPercent = useCallback((): number => {
    if (!state.duration || state.duration === 0) return 0;
    return (state.currentTime / state.duration) * 100;
  }, [state.currentTime, state.duration]);

  return {
    state,
    clipRange,
    isClipMode,
    play,
    pause,
    togglePlay,
    seek,
    seekToLive,
    setPlaybackRate,
    startClipMode,
    cancelClipMode,
    setClipStart,
    setClipEnd,
    saveClip,
    formatTime,
    getProgressPercent,
  };
};
