"""
Teste DIRETO com MediaMTX - Bypass da API.
Conecta câmeras direto no MediaMTX e gera URLs HLS.
"""
import requests
import time

MEDIAMTX_API = "http://localhost:9997"
MEDIAMTX_HLS = "http://localhost:8889"

CAMERAS = [
    {"name": "Camera 1", "rtsp": "rtsp://admin:Camerite123@45.236.226.75:6052/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 2", "rtsp": "rtsp://admin:Camerite123@45.236.226.74:6050/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 3", "rtsp": "rtsp://admin:Camerite123@45.236.226.72:6048/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 4", "rtsp": "rtsp://admin:Camerite123@45.236.226.71:6047/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 5", "rtsp": "rtsp://admin:Camerite123@45.236.226.71:6046/cam/realmonitor?channel=1&subtype=0"},
]


def add_path_to_mediamtx(path_name, source_url):
    """Adiciona path no MediaMTX via API."""
    config = {
        "name": path_name,
        "source": source_url,
        "sourceProtocol": "automatic",
        "sourceOnDemand": False,
        "runOnReady": "",
        "runOnDemand": "",
        "runOnUnDemand": "",
    }
    
    try:
        response = requests.post(
            f"{MEDIAMTX_API}/v3/config/paths/add/{path_name}",
            json=config,
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"   Erro API: {e}")
        return False


def main():
    print("\n🚀 GT-Vision - Teste DIRETO com MediaMTX\n")
    print("=" * 60)
    
    hls_urls = []
    
    for i, camera in enumerate(CAMERAS, 1):
        print(f"\n📹 [{i}/5] {camera['name']}")
        print("-" * 60)
        
        path_name = f"camera{i}"
        
        print(f"1. Adicionando path '{path_name}' no MediaMTX...")
        
        if add_path_to_mediamtx(path_name, camera['rtsp']):
            print(f"✅ Path adicionado")
            
            hls_url = f"{MEDIAMTX_HLS}/{path_name}"
            hls_urls.append({"name": camera['name'], "url": hls_url})
            
            print(f"📺 URL HLS: {hls_url}")
        else:
            print(f"❌ Falha ao adicionar path")
    
    # Resumo
    print(f"\n{'=' * 60}")
    print(f"📊 RESUMO")
    print(f"{'=' * 60}\n")
    
    print(f"✅ Câmeras configuradas: {len(hls_urls)}/5\n")
    
    if hls_urls:
        print("📺 URLs HLS (abra no VLC):\n")
        for item in hls_urls:
            print(f"   {item['name']}: {item['url']}")
        
        print(f"\n💡 Como testar:")
        print(f"   1. Abra o VLC")
        print(f"   2. Mídia > Abrir Fluxo de Rede")
        print(f"   3. Cole uma das URLs acima")
        print(f"   4. Clique em Reproduzir")
    
    print()


if __name__ == "__main__":
    main()
