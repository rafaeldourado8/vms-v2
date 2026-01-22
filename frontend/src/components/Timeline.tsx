import { MouseEvent, useRef } from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Play, Pause } from 'lucide-react';

interface Thumbnail {
  timestamp: string;
  url: string;
}

interface TimelineProps {
  thumbnails: Thumbnail[];
  currentTime: number;
  duration: number;
  isPlaying: boolean;
  onSeek: (time: number) => void;
  onTogglePlay: () => void;
  className?: string;
}

const Timeline = ({ 
  thumbnails,
  currentTime, 
  duration, 
  isPlaying,
  onSeek,
  onTogglePlay,
  className 
}: TimelineProps) => {
  const progressBarRef = useRef<HTMLDivElement>(null);
  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  const handleSeek = (e: MouseEvent<HTMLDivElement>) => {
    if (!progressBarRef.current || duration <= 0) return;
    const rect = progressBarRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = Math.max(0, Math.min(1, x / rect.width));
    onSeek(percentage * duration);
  };

  return (
    <div className={cn("flex flex-col w-full bg-black/50 backdrop-blur-sm", className)}>
      
      {/* Toolbar */}
      <div className="flex items-center gap-2 px-4 py-2">
        <Button 
          size="icon" 
          variant="ghost" 
          className="h-8 w-8 text-white hover:bg-white/10" 
          onClick={onTogglePlay}
        >
          {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
        </Button>
      </div>

      {/* Barra de Progresso */}
      <div className="px-4 pb-2">
        <div 
          ref={progressBarRef}
          className="relative h-2 w-full bg-white/10 rounded-full cursor-pointer hover:h-3 transition-all"
          onClick={handleSeek}
        >
          <div 
            className="absolute top-0 left-0 h-full bg-blue-500 rounded-l-full"
            style={{ width: `${progress}%` }}
          />
          
          <div 
            className="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg"
            style={{ left: `${progress}%`, transform: 'translate(-50%, -50%)' }} 
          />
        </div>
      </div>

      {/* Thumbnails Strip */}
      {thumbnails.length > 0 && (
        <div className="flex gap-1 px-4 pb-2 overflow-x-auto scrollbar-thin scrollbar-thumb-white/20">
          {thumbnails.map((thumb, idx) => (
            <img
              key={idx}
              src={thumb.url}
              alt={`Thumbnail ${idx}`}
              className="h-12 w-20 object-cover rounded cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
              onClick={() => {
                const time = new Date(thumb.timestamp).getTime() / 1000;
                onSeek(time);
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Timeline;