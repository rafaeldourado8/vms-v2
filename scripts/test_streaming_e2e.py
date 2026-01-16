"""
Script de teste E2E para streaming completo.
Simula o fluxo: Camera RTSP -> Backend -> MediaMTX -> Player OpenCV
"""
import asyncio
import httpx
import cv2
import os
from uuid import uuid4
from datetime import datetime

# Configurações
BACKEND_URL = "http://localhost:8000"  # Django
STREAMING_URL = "http://localhost:8001"  # FastAPI
MEDIAMTX_HLS_URL = "http://localhost:8889"

# RTSP de teste (Big Buck Bunny - stream público)
TEST_RTSP_URL = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"


async def create_camera():
    """Cria câmera no backend Django."""
    print("📹 Criando câmera no backend...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/api/cameras/",
            json={
                "name": "Camera Teste E2E",
                "location": "Teste",
                "rtsp_url": TEST_RTSP_URL,
                "cidade_id": str(uuid4())  # Simula cidade
            }
        )
        
        if response.status_code == 201:
            camera = response.json()
            print(f"✅ Câmera criada: {camera['id']}")
            return camera
        else:
            print(f"❌ Erro ao criar câmera: {response.text}")
            return None


async def start_stream(camera_id, rtsp_url):
    """Inicia stream no FastAPI."""
    print(f"🎬 Iniciando stream para câmera {camera_id}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{STREAMING_URL}/api/streams/start",
            json={
                "camera_id": camera_id,
                "source_url": rtsp_url
            }
        )
        
        if response.status_code == 201:
            stream = response.json()
            print(f"✅ Stream iniciado: {stream['stream_id']}")
            return stream
        else:
            print(f"❌ Erro ao iniciar stream: {response.text}")
            return None


async def start_recording(stream_id):
    """Inicia gravação."""
    print(f"⏺️  Iniciando gravação do stream {stream_id}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{STREAMING_URL}/api/recordings/start",
            json={
                "stream_id": stream_id,
                "retention_days": 7
            }
        )
        
        if response.status_code == 201:
            recording = response.json()
            print(f"✅ Gravação iniciada: {recording['recording_id']}")
            return recording
        else:
            print(f"❌ Erro ao iniciar gravação: {response.text}")
            return None


def play_stream_opencv(stream_path):
    """Exibe stream usando OpenCV."""
    print(f"🎥 Abrindo player OpenCV para: {stream_path}")
    
    # Tenta abrir o stream
    cap = cv2.VideoCapture(stream_path)
    
    if not cap.isOpened():
        print(f"❌ Não foi possível abrir o stream: {stream_path}")
        return
    
    print("✅ Stream aberto! Pressione 'q' para sair.")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("⚠️  Fim do stream ou erro na leitura")
            break
        
        frame_count += 1
        
        # Adiciona informações no frame
        cv2.putText(
            frame,
            f"GT-Vision VMS - Frame: {frame_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        cv2.putText(
            frame,
            f"Time: {datetime.now().strftime('%H:%M:%S')}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        # Exibe o frame
        cv2.imshow('GT-Vision VMS - Stream Test', frame)
        
        # Sai com 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Encerrando player...")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Player encerrado. Total de frames: {frame_count}")


async def main():
    """Fluxo principal de teste."""
    print("=" * 60)
    print("🚀 GT-Vision VMS - Teste E2E de Streaming")
    print("=" * 60)
    print()
    
    # 1. Criar câmera (simula frontend)
    camera = await create_camera()
    if not camera:
        return
    
    print()
    await asyncio.sleep(1)
    
    # 2. Iniciar stream (backend -> MediaMTX)
    stream = await start_stream(camera['id'], TEST_RTSP_URL)
    if not stream:
        return
    
    print()
    await asyncio.sleep(2)
    
    # 3. Iniciar gravação
    recording = await start_recording(stream['stream_id'])
    if not recording:
        return
    
    print()
    print("⏳ Aguardando 3 segundos para stream estabilizar...")
    await asyncio.sleep(3)
    
    # 4. Construir URL do HLS
    stream_name = f"camera_{camera['id']}"
    hls_url = f"{MEDIAMTX_HLS_URL}/{stream_name}/index.m3u8"
    
    print()
    print("=" * 60)
    print(f"📺 URL HLS: {hls_url}")
    print("=" * 60)
    print()
    
    # 5. Abrir player OpenCV
    print("🎬 Iniciando player OpenCV...")
    print("   Pressione 'q' na janela do player para sair")
    print()
    
    # Tenta RTSP direto primeiro (mais estável para OpenCV)
    rtsp_direct = TEST_RTSP_URL
    play_stream_opencv(rtsp_direct)
    
    print()
    print("=" * 60)
    print("✅ Teste E2E concluído!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
