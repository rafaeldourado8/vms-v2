"""
Teste E2E com câmeras REAIS.
"""
import asyncio
import httpx
from uuid import uuid4

STREAMING_URL = "http://localhost:8001"
DETECTION_URL = "http://localhost:8002"

REAL_CAMERAS = [
    {
        "name": "Camera 1 - Porto 6052",
        "rtsp": "rtsp://admin:Camerite123@45.236.226.75:6052/cam/realmonitor?channel=1&subtype=0"
    },
    {
        "name": "Camera 2 - Porto 6050",
        "rtsp": "rtsp://admin:Camerite123@45.236.226.74:6050/cam/realmonitor?channel=1&subtype=0"
    },
    {
        "name": "Camera 3 - Porto 6048",
        "rtsp": "rtsp://admin:Camerite123@45.236.226.72:6048/cam/realmonitor?channel=1&subtype=0"
    },
    {
        "name": "Camera 4 - Porto 6047",
        "rtsp": "rtsp://admin:Camerite123@45.236.226.71:6047/cam/realmonitor?channel=1&subtype=0"
    },
    {
        "name": "Camera 5 - Porto 6046",
        "rtsp": "rtsp://admin:Camerite123@45.236.226.71:6046/cam/realmonitor?channel=1&subtype=0"
    }
]


async def test_camera(camera_data, index):
    """Testa uma câmera."""
    print(f"\n{'='*60}")
    print(f"📹 [{index+1}/5] {camera_data['name']}")
    print(f"{'='*60}")
    
    camera_id = str(uuid4())
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Iniciar stream
        print(f"\n1. Iniciando stream...")
        try:
            response = await client.post(
                f"{STREAMING_URL}/api/streams/start",
                json={
                    "camera_id": camera_id,
                    "source_url": camera_data['rtsp']
                }
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
                    
                    # 3. URL HLS
                    stream_name = f"camera_{camera_id}"
                    hls_url = f"http://localhost:8889/{stream_name}/index.m3u8"
                    
                    print(f"\n📺 URL HLS:")
                    print(f"   {hls_url}")
                    print(f"\n   Abra no VLC ou navegador")
                    
                    return {
                        "camera_id": camera_id,
                        "stream_id": stream_id,
                        "recording_id": recording['recording_id'],
                        "hls_url": hls_url,
                        "status": "success"
                    }
                else:
                    print(f"❌ Erro ao iniciar gravação: {response.status_code}")
            else:
                print(f"❌ Erro ao iniciar stream: {response.status_code}")
                print(f"   {response.text}")
        
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    return {"status": "failed"}


async def simulate_lpr_events(camera_results):
    """Simula eventos LPR das câmeras."""
    print(f"\n{'='*60}")
    print(f"🎯 Simulando Eventos LPR")
    print(f"{'='*60}")
    
    plates = ["ABC1234", "XYZ5678", "DEF9012", "GHI3456", "JKL7890"]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for i, result in enumerate(camera_results):
            if result.get("status") == "success":
                camera_id = result["camera_id"]
                plate = plates[i % len(plates)]
                
                print(f"\n📸 Câmera {i+1}: Detectou placa {plate}")
                
                try:
                    response = await client.post(
                        f"{DETECTION_URL}/api/webhooks/lpr",
                        json={
                            "camera_id": camera_id,
                            "plate": plate,
                            "confidence": 0.95,
                            "timestamp": "2025-01-16T12:00:00Z",
                            "location": f"Camera {i+1}"
                        }
                    )
                    
                    if response.status_code == 201:
                        print(f"✅ Evento enviado")
                    else:
                        print(f"❌ Erro: {response.status_code}")
                
                except Exception as e:
                    print(f"❌ Erro: {e}")
        
        # Listar eventos
        print(f"\n📊 Listando todos os eventos...")
        try:
            response = await client.get(f"{DETECTION_URL}/api/events/lpr")
            if response.status_code == 200:
                events = response.json()
                print(f"✅ Total de eventos: {events['total']}")
        except Exception as e:
            print(f"❌ Erro: {e}")


async def main():
    print("\n🚀 GT-Vision VMS - Teste com Câmeras REAIS\n")
    
    # Aguardar serviços
    print("⏳ Aguardando serviços (5s)...")
    await asyncio.sleep(5)
    
    # Testar cada câmera
    results = []
    for i, camera in enumerate(REAL_CAMERAS):
        result = await test_camera(camera, i)
        results.append(result)
        await asyncio.sleep(2)
    
    # Simular eventos LPR
    await simulate_lpr_events(results)
    
    # Resumo
    print(f"\n{'='*60}")
    print(f"📊 RESUMO")
    print(f"{'='*60}")
    
    success_count = sum(1 for r in results if r.get("status") == "success")
    print(f"\n✅ Câmeras ativas: {success_count}/5")
    
    print(f"\n📺 URLs HLS:")
    for i, result in enumerate(results):
        if result.get("status") == "success":
            print(f"   {i+1}. {result['hls_url']}")
    
    print(f"\n🔗 APIs:")
    print(f"   Streaming: {STREAMING_URL}/docs")
    print(f"   Detection: {DETECTION_URL}/docs")
    print()


if __name__ == "__main__":
    asyncio.run(main())
