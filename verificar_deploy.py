import requests
import time
from datetime import datetime

def verificar_deploy():
    """Verifica se o deploy está funcionando"""
    urls = [
        "https://web-production-213c2.up.railway.app",
        "https://upaudit.up.railway.app"  # Caso tenha domínio customizado
    ]
    
    print("🔍 Verificando status do deploy...")
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)
    
    for url in urls:
        try:
            print(f"🌐 Testando: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ SUCESSO! Status: {response.status_code}")
                print(f"📊 Sistema UPAUDIT está online!")
                print(f"🔗 Acesse: {url}")
                return True
            else:
                print(f"⚠️ Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Conexão falhou - Deploy ainda não está pronto")
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout - Servidor pode estar iniciando")
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    print("🔄 Deploy ainda não está disponível")
    return False

def monitorar_deploy(max_tentativas=10, intervalo=30):
    """Monitora o deploy até ficar online"""
    print("🚀 Iniciando monitoramento do deploy...")
    
    for tentativa in range(1, max_tentativas + 1):
        print(f"\n📡 Tentativa {tentativa}/{max_tentativas}")
        
        if verificar_deploy():
            print("\n🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
            print("🌟 Sistema UPAUDIT está funcionando online!")
            return True
        
        if tentativa < max_tentativas:
            print(f"⏳ Aguardando {intervalo} segundos...")
            time.sleep(intervalo)
    
    print("\n❌ Deploy não ficou online no tempo esperado")
    print("💡 Verifique os logs no Railway para mais detalhes")
    return False

if __name__ == "__main__":
    monitorar_deploy() 