import requests
import time

def testar_deploy():
    urls = [
        "https://web-production-213c2.up.railway.app",
        "https://web-production-213c2.up.railway.app/health",
        "https://web-production-213c2.up.railway.app/ping"
    ]
    
    print("🔍 Testando UPAUDIT no Railway...")
    print("=" * 50)
    
    for url in urls:
        try:
            print(f"\n🌐 Testando: {url}")
            response = requests.get(url, timeout=10)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCESSO!")
                if 'health' in url or 'ping' in url:
                    print(f"📝 Resposta: {response.text[:100]}")
                return True
            else:
                print(f"⚠️ Erro: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Falha: {str(e)}")
    
    print("\n❌ Deploy ainda não está funcionando")
    return False

if __name__ == "__main__":
    testar_deploy() 