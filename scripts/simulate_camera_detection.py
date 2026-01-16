"""
Simulador de câmera com IA embarcada.
Envia eventos de detecção (LPR) para a Detection API.
"""
import asyncio
import httpx
from uuid import uuid4
from datetime import datetime
import random

DETECTION_API_URL = "http://localhost:8002"

# Placas brasileiras simuladas
SAMPLE_PLATES = [
    "ABC1234", "XYZ5678", "DEF9012", "GHI3456", "JKL7890",
    "MNO1122", "PQR3344", "STU5566", "VWX7788", "YZA9900"
]


async def simulate_lpr_detection(camera_id: str, interval: int = 5):
    """Simula detecção de placas a cada X segundos."""
    print(f"🎥 Câmera {camera_id} iniciada - Simulando detecções LPR")
    print(f"   Enviando eventos para: {DETECTION_API_URL}")
    print()
    
    async with httpx.AsyncClient() as client:
        detection_count = 0
        
        while True:
            # Simula detecção de placa
            plate = random.choice(SAMPLE_PLATES)
            confidence = round(random.uniform(0.85, 0.99), 2)
            
            event = {
                "camera_id": camera_id,
                "plate": plate,
                "confidence": confidence,
                "timestamp": datetime.utcnow().isoformat(),
                "location": "Rua Teste, 123"
            }
            
            try:
                response = await client.post(
                    f"{DETECTION_API_URL}/api/webhooks/lpr",
                    json=event
                )
                
                if response.status_code == 201:
                    detection_count += 1
                    result = response.json()
                    print(f"✅ [{detection_count}] LPR detectado: {plate} (conf: {confidence}) - Event ID: {result['event_id'][:8]}...")
                else:
                    print(f"❌ Erro ao enviar evento: {response.status_code}")
            
            except Exception as e:
                print(f"❌ Erro de conexão: {e}")
            
            await asyncio.sleep(interval)


async def main():
    """Inicia simulador."""
    print("=" * 60)
    print("🚀 GT-Vision - Simulador de Câmera com IA Embarcada")
    print("=" * 60)
    print()
    
    camera_id = str(uuid4())
    print(f"📹 Camera ID: {camera_id}")
    print()
    
    # Verifica se Detection API está rodando
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DETECTION_API_URL}/health")
            if response.status_code == 200:
                print("✅ Detection API está online")
                print()
            else:
                print("⚠️  Detection API não está respondendo corretamente")
                return
    except Exception as e:
        print(f"❌ Detection API não está acessível: {e}")
        print(f"   Certifique-se de iniciar: python src/detection/main.py")
        return
    
    print("🎬 Iniciando simulação de detecções...")
    print("   Pressione Ctrl+C para parar")
    print()
    
    try:
        await simulate_lpr_detection(camera_id, interval=3)
    except KeyboardInterrupt:
        print()
        print("🛑 Simulação encerrada")


if __name__ == "__main__":
    asyncio.run(main())
