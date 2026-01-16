"""
Teste com FFmpeg DIRETO - Sem MediaMTX.
Conecta nas câmeras e salva 10 segundos de vídeo.
"""
import subprocess
import os

CAMERAS = [
    {"name": "Camera 1", "rtsp": "rtsp://admin:Camerite123@45.236.226.75:6052/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 2", "rtsp": "rtsp://admin:Camerite123@45.236.226.74:6050/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 3", "rtsp": "rtsp://admin:Camerite123@45.236.226.72:6048/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 4", "rtsp": "rtsp://admin:Camerite123@45.236.226.71:6047/cam/realmonitor?channel=1&subtype=0"},
    {"name": "Camera 5", "rtsp": "rtsp://admin:Camerite123@45.236.226.71:6046/cam/realmonitor?channel=1&subtype=0"},
]

OUTPUT_DIR = "test_videos"


def test_camera(camera, index):
    """Testa conexão com câmera usando FFmpeg."""
    print(f"\n📹 [{index}/5] {camera['name']}")
    print("-" * 60)
    
    output_file = os.path.join(OUTPUT_DIR, f"camera{index}.mp4")
    
    print(f"1. Testando conexão RTSP...")
    print(f"   URL: {camera['rtsp'][:50]}...")
    
    cmd = [
        "ffmpeg",
        "-rtsp_transport", "tcp",
        "-i", camera['rtsp'],
        "-t", "10",  # 10 segundos
        "-c", "copy",
        "-y",
        output_file
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ Conexão OK - Gravado: {output_file} ({size_mb:.2f} MB)")
            return True
        else:
            print(f"❌ Erro ao conectar")
            if result.stderr:
                print(f"   {result.stderr[:200]}")
            return False
    
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout (30s)")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    print("\n🚀 GT-Vision - Teste com FFmpeg DIRETO\n")
    print("=" * 60)
    
    # Criar diretório
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    success_count = 0
    
    for i, camera in enumerate(CAMERAS, 1):
        if test_camera(camera, i):
            success_count += 1
    
    # Resumo
    print(f"\n{'=' * 60}")
    print(f"📊 RESUMO")
    print(f"{'=' * 60}\n")
    
    print(f"✅ Câmeras conectadas: {success_count}/5")
    
    if success_count > 0:
        print(f"\n📁 Vídeos salvos em: {OUTPUT_DIR}/")
        print(f"   Abra os arquivos .mp4 no VLC para ver")
    
    print()


if __name__ == "__main__":
    main()
