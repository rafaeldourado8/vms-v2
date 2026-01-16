"""
Teste E2E simplificado usando containers Docker.
"""
import asyncio
import httpx
import time
from uuid import uuid4
from datetime import datetime

STREAMING_URL = "http://localhost:8001"
DETECTION_URL = "http://localhost:8002"
TEST_RTSP = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"


async def test_streaming():
    print("=" * 60)
    print("🎬 Teste de Streaming")
    print("=" * 60)
    
    camera_id = str(uuid4())
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Iniciar stream
        print(f"\n1. Iniciando stream para câmera {camera_id[:8]}...")
        response = await client.post(
            f"{STREAMING_URL}/api/streams/start",
            json={"camera_id": camera_id, "source_url": TEST_RTSP}
        )
        
        if response.status_code == 201:
            stream = response.json()
            stream_id = stream['stream_id']
            print(f"✅ Stream iniciado: {stream_id[:8]}...")
            
            # 2. Iniciar gravação
            print(f"\n2. Iniciando gravação...")
            response = await client.post(
                f"{STREAMING_URL}/api/recordings/start",
                json={"stream_id": stream_id, "retention_days": 7}
            )
            
            if response.status_code == 201:
                recording = response.json()
                print(f"✅ Gravação iniciada: {recording['recording_id'][:8]}...")
                
                # 3. Aguardar
                print(f"\n3. Aguardando 5 segundos...")
                await asyncio.sleep(5)
                
                # 4. Verificar stream
                print(f"\n4. Verificando stream...")
                response = await client.get(f"{STREAMING_URL}/api/streams/{stream_id}")
                if response.status_code == 200:
                    print(f"✅ Stream ativo")
                
                # 5. URL HLS
                stream_name = f"camera_{camera_id}"
                hls_url = f"http://localhost:8889/{stream_name}/index.m3u8"
                print(f"\n📺 URL HLS: {hls_url}")
                print(f"   Abra no VLC ou navegador")
                
                return True
        
        print("❌ Erro no teste de streaming")
        return False


async def test_detection():
    print("\n" + "=" * 60)
    print("🎯 Teste de Detecção")
    print("=" * 60)
    
    camera_id = str(uuid4())
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Verificar health
        print(f"\n1. Verificando Detection API...")
        response = await client.get(f"{DETECTION_URL}/health")
        if response.status_code == 200:
            print(f"✅ Detection API online")
        else:
            print(f"❌ Detection API offline")
            return False
        
        # 2. Enviar evento LPR
        print(f"\n2. Enviando evento LPR...")
        response = await client.post(
            f"{DETECTION_URL}/api/webhooks/lpr",
            json={
                "camera_id": camera_id,
                "plate": "ABC1234",
                "confidence": 0.95,
                "timestamp": datetime.utcnow().isoformat(),
                "location": "Teste E2E"
            }
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Evento recebido: {result['event_id'][:8]}...")
            
            # 3. Listar eventos
            print(f"\n3. Listando eventos...")
            response = await client.get(f"{DETECTION_URL}/api/events/lpr")
            if response.status_code == 200:
                events = response.json()
                print(f"✅ Total de eventos: {events['total']}")
                return True
        
        print("❌ Erro no teste de detecção")
        return False


async def main():
    print("\n🚀 GT-Vision VMS - Teste E2E Docker\n")
    
    # Aguardar serviços
    print("⏳ Aguardando serviços iniciarem (10s)...")
    await asyncio.sleep(10)
    
    # Testes
    streaming_ok = await test_streaming()
    detection_ok = await test_detection()
    
    # Resultado
    print("\n" + "=" * 60)
    print("📊 Resultado dos Testes")
    print("=" * 60)
    print(f"Streaming: {'✅ OK' if streaming_ok else '❌ FALHOU'}")
    print(f"Detection: {'✅ OK' if detection_ok else '❌ FALHOU'}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
