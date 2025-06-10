#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Código Original do Usuário - Adaptado com Debugs Detalhados
Gera prints das empresas em modo invisível com logs completos
"""

import time
import os
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def gerar_prints_com_debug(modo_invisivel=True):
    """Gera prints das empresas com debug detalhado"""
    
    print("🚀 INICIANDO GERAÇÃO DE PRINTS COM DEBUG DETALHADO")
    print("=" * 70)
    if modo_invisivel:
        print("👻 MODO INVISÍVEL ATIVADO - Colaborador não verá nada!")
    else:
        print("👁️ MODO VISÍVEL ATIVADO - Navegador aparecerá na tela!")
    
    # Lista original do usuário
    empresas = [
        [27119, "Matercaldas", "27119 - Matercaldas.png"],
        [26412, "Guimaraes 85", "26412 - Guimaraes 85.png"],
        [26413, "Guimaraes 63", "26413 - Guimaraes 63.png"],
        [7520, "Auto Posto Serra dos Pirineus", "7520 - Auto Posto Serra dos Pirineus.png"],
        [27138, "Mineira Materiais", "27138 - Mineira Materiais.png"],
        [24718, "Guifrii 50", "24718 - Guifrii 50.png"],
        [25992, "MARQUES E COSTA 81", "25992 - MARQUES E COSTA 81.png"],
        [26498, "MARQUES E COSTA 62", "26498 - MARQUES E COSTA 62.png"],
        [16289, "Equilibrio", "16289 - Equilibrio Homeopatia.png"],
        [17606, "MONTE CRISTO", "17606 - MONTE CRISTO.png"],
        [25991, "Mariana Joias", "25991 - Mariana Joias.png"],
        [15944, "CANTINHO FRIO", "15944 - CANTINHO FRIO.png"],
        [25715, "Casa Dibs", "25715 - Casa Dibs.png"],
        [26520, "Chao Nativo", "26520 - Chao Nativo.png"],
        [23980, "MERCEARIA E CONVENIENCIA DOS GAUCHOS", "23980 - MERCEARIA E CONVENIENCIA DOS GAUCHOS.png"],
        [17609, "Farmacia Essencial - 176", "17609 - Farmacia Essencial - 176.png"],
        [23703, "Farmacia Essencial - 257", "23703 - Farmacia Essencial - 257.png"],
        [26306, "Madeimanas Madeireira 60", "26306 - Madeimanas Madeireira 60.png"],
        [26305, "Madeimanas Madeireira 80", "26305 - Madeimanas Madeireira 80.png"],
        [26304, "Oliveira Casa", "26304 - Oliveira Casa e Construção.png"],
        [25716, "Posto Serra City", "25716 - Posto Serra City.png"],
        [23025, "Clinica San Francesco", "23025 - Clinica San Francesco.png"],
        [7517, "Posto Aderup", "7517 - Posto Aderup.png"],
        [16096, "Supermercado Feliz", "16096 - Supermercado Feliz.png"],
        [16660, "Posto Primavera 000170", "16660 - Posto Primavera 000170.png"],
        [16791, "Posto Petro Bessa", "16791 - Posto Petro Bessa.png"],
        [25488, "Drogaria Legitima - 00", "25488 - Drogaria Legitima - 00.png"],
        [25489, "Drogaria Legitima - 83", "25489 - Drogaria Legitima - 83.png"],
        [25490, "Drogaria Legitima - 46", "25490 - Drogaria Legitima - 46.png"]
    ]
    
    print(f"🏢 Total de empresas a processar: {len(empresas)}")
    
    # Pasta de destino
    pasta_prints = r"C:\Users\Luiz Marcelo\Desktop\PROJETO AUDIT PRICIPAL\prints"
    if not os.path.exists(pasta_prints):
        os.makedirs(pasta_prints)
        print(f"📁 Pasta criada: {pasta_prints}")
    else:
        print(f"📁 Pasta existente: {pasta_prints}")
    
    # Configurações do Chrome
    if modo_invisivel:
        print("🔧 Configurando Chrome em modo INVISÍVEL...")
    else:
        print("🔧 Configurando Chrome em modo VISÍVEL...")
    chrome_options = Options()
    
    # Controle do modo headless
    if modo_invisivel:
        chrome_options.add_argument("--headless=new")
        print("👻 Modo HEADLESS ativado - navegador será INVISÍVEL!")
    else:
        print("👁️ Modo VISÍVEL ativado - navegador aparecerá na tela!")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceLogging")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Inicializa o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Configurações de timeout robustas
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(30)
    
    # Remove propriedades que indicam automação
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    sucessos = []
    falhas = []
    
    try:
        # 1. LOGIN
        print("\n1️⃣ FAZENDO LOGIN NO SISTEMA...")
        url = 'https://audit.conciliadora.com.br/Login/Index'
        driver.get(url)
        
        # Aguarda página carregar completamente
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(5)
        
        print(f"🔍 [DEBUG] URL carregada: {driver.current_url}")
        print(f"🔍 [DEBUG] Título: {driver.title}")
        
        # Campos de login
        print("🔍 [DEBUG] Procurando campos de login...")
        login_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'login'))
        )
        password_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'password'))
        )
        print("✅ [DEBUG] Campos de login encontrados!")
        
        # Preenche credenciais
        print("⌨️ [DEBUG] Preenchendo credenciais...")
        login_field.clear()
        login_field.send_keys('joao.vitor@consultoriaexpansao.com.br')
        time.sleep(2)
        
        password_field.clear()
        password_field.send_keys('Acesso#13')
        time.sleep(3)
        
        # Botão de login
        print("🔍 [DEBUG] Procurando botão de login...")
        btn_login = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'btnLogin'))
        )
        print("🖱️ [DEBUG] Clicando no botão de login...")
        btn_login.click()
        
        # Aguarda redirecionamento
        print("⏳ [DEBUG] Aguardando redirecionamento...")
        WebDriverWait(driver, 30).until(
            lambda d: d.current_url != url
        )
        time.sleep(6)
        
        print(f"✅ Login realizado com sucesso!")
        print(f"🔍 [DEBUG] URL após login: {driver.current_url}")
        
        # 2. NAVEGAÇÃO PARA RELATÓRIOS
        print("\n2️⃣ NAVEGANDO PARA RELATÓRIOS...")
        
        # Menu lateral
        print("🔍 [DEBUG] Procurando menu lateral...")
        try:
            menu_lateral = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "kt_aside_menu"))
            )
            print("✅ [DEBUG] Menu lateral encontrado!")
            menu_lateral.click()
            time.sleep(10)
        except TimeoutException:
            print("❌ [DEBUG] Menu lateral não encontrado!")
            raise Exception("Menu lateral não encontrado")
        
        # Menu Vendas
        print("🔍 [DEBUG] Procurando menu Vendas...")
        try:
            vendas_menu = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='nomeGrupoSideBar' and text()='Vendas']"))
            )
            print("✅ [DEBUG] Menu Vendas encontrado!")
            vendas_menu.click()
            time.sleep(6)
        except TimeoutException:
            print("❌ [DEBUG] Menu Vendas não encontrado!")
            raise Exception("Menu Vendas não encontrado")
        
        # Submenu
        print("🔍 [DEBUG] Procurando submenu...")
        try:
            submenu = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[2]/div/ul/li[1]/a/span'))
            )
            print("✅ [DEBUG] Submenu encontrado!")
            submenu.click()
            time.sleep(5)
        except TimeoutException:
            print("❌ [DEBUG] Submenu não encontrado!")
            raise Exception("Submenu não encontrado")
        
        print("✅ Navegação para relatórios concluída!")
        
        # 3. CONFIGURAR FILTRO DE DATA
        print("\n3️⃣ CONFIGURANDO FILTRO DE DATA...")
        data_atual = datetime.now()
        dia_atual = data_atual.day
        mes_atual = f"{data_atual.month:02d}"
        ano_atual = data_atual.year
        dias_anterior = (data_atual - timedelta(days=3)).strftime("%d")
        
        print(f"📅 [DEBUG] Data atual: {dia_atual}/{mes_atual}/{ano_atual}")
        print(f"📅 [DEBUG] Data a filtrar: {dias_anterior}/{mes_atual}/{ano_atual}")
        
        data_xpath = f"//td[@data-value='{ano_atual}/{mes_atual}/{dias_anterior}']"
        print(f"🔍 [DEBUG] XPath da data: {data_xpath}")
        
        try:
            data_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, data_xpath))
            )
            print("✅ [DEBUG] Elemento de data encontrado!")
            
            # Aguarda um pouco para elementos carregarem
            time.sleep(3)
            
            # Tenta fechar qualquer dropdown ou overlay que possa estar aberto
            print(f"🔍 [DEBUG] Verificando se há overlays abertos...")
            try:
                # Clica em uma área neutra para fechar dropdowns
                body = driver.find_element(By.TAG_NAME, "body")
                driver.execute_script("arguments[0].click();", body)
                time.sleep(2)
            except:
                pass
            
            # Scroll para o elemento
            print(f"📜 [DEBUG] Fazendo scroll para o elemento de data...")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", data_element)
            time.sleep(3)
            
            # Tenta clicar usando diferentes métodos
            print(f"🖱️ [DEBUG] Tentando clicar na data...")
            
            # Método 1: Clique normal
            try:
                data_element.click()
                print(f"✅ [DEBUG] Data clicada com sucesso (método normal)!")
                time.sleep(8)
                print("✅ Data filtrada com sucesso!")
            except Exception as e:
                print(f"⚠️ [DEBUG] Método normal falhou: {e}")
                
                # Método 2: JavaScript click
                try:
                    print(f"🔧 [DEBUG] Tentando clique via JavaScript...")
                    driver.execute_script("arguments[0].click();", data_element)
                    print(f"✅ [DEBUG] Data clicada com sucesso (método JavaScript)!")
                    time.sleep(8)
                    print("✅ Data filtrada com sucesso!")
                except Exception as e2:
                    print(f"⚠️ [DEBUG] Método JavaScript falhou: {e2}")
                    
                    # Método 3: ActionChains
                    try:
                        print(f"🔧 [DEBUG] Tentando clique via ActionChains...")
                        from selenium.webdriver.common.action_chains import ActionChains
                        actions = ActionChains(driver)
                        actions.move_to_element(data_element).click().perform()
                        print(f"✅ [DEBUG] Data clicada com sucesso (método ActionChains)!")
                        time.sleep(8)
                        print("✅ Data filtrada com sucesso!")
                    except Exception as e3:
                        print(f"⚠️ [DEBUG] Método ActionChains falhou: {e3}")
                        
                        # Método 4: Aguarda elemento ser clicável
                        try:
                            print(f"⏳ [DEBUG] Aguardando elemento ser clicável...")
                            clickable_element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, data_xpath))
                            )
                            clickable_element.click()
                            print(f"✅ [DEBUG] Data clicada com sucesso (método aguarda clicável)!")
                            time.sleep(8)
                            print("✅ Data filtrada com sucesso!")
                        except Exception as e4:
                            print(f"⚠️ [DEBUG] Todos os métodos falharam!")
                            print(f"❌ [DEBUG] Último erro: {e4}")
                            raise Exception(f"Não foi possível clicar na data {dias_anterior}/{mes_atual}/{ano_atual}")
            
        except TimeoutException:
            print(f"❌ [DEBUG] Data não encontrada: {data_xpath}")
            raise Exception(f"Data {dias_anterior}/{mes_atual}/{ano_atual} não encontrada")
        
        # 4. PROCESSAR EMPRESAS
        print(f"\n4️⃣ PROCESSANDO {len(empresas)} EMPRESAS...")
        print("=" * 70)
        
        for i, empresa in enumerate(empresas, 1):
            codigo, nome, arquivo = empresa
            
            print(f"\n[{i}/{len(empresas)}] 🏢 PROCESSANDO: {nome}")
            print(f"📋 Código: {codigo}")
            print(f"📁 Arquivo: {arquivo}")
            
            try:
                # Campo de busca
                print(f"🔍 [DEBUG] Procurando campo de busca...")
                input_xpath = '//*[@id="dropDownSearch"]/div[1]/div/div[1]/input'
                
                try:
                    caixa_de_texto = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, input_xpath))
                    )
                    print(f"✅ [DEBUG] Campo de busca encontrado!")
                except TimeoutException:
                    print(f"❌ [DEBUG] Campo de busca não encontrado!")
                    print(f"🔍 [DEBUG] URL atual: {driver.current_url}")
                    falhas.append(f"{nome}: Campo de busca não encontrado")
                    continue
                
                # Scroll e interação
                print(f"📜 [DEBUG] Fazendo scroll para o campo...")
                driver.execute_script("arguments[0].scrollIntoView(true);", caixa_de_texto)
                time.sleep(2)
                
                print(f"🖱️ [DEBUG] Clicando no campo de busca...")
                caixa_de_texto.click()
                time.sleep(2)
                
                print(f"🧹 [DEBUG] Limpando campo...")
                caixa_de_texto.clear()
                time.sleep(2)
                
                print(f"⌨️ [DEBUG] Digitando: '{nome}'")
                caixa_de_texto.send_keys(nome)
                time.sleep(3)
                
                print(f"⬇️ [DEBUG] Pressionando ARROW_DOWN...")
                caixa_de_texto.send_keys(Keys.ARROW_DOWN)
                
                print(f"↩️ [DEBUG] Pressionando ENTER...")
                caixa_de_texto.send_keys(Keys.ENTER)
                time.sleep(4)
                
                # Botão Apply
                print(f"🔍 [DEBUG] Procurando botão Apply...")
                try:
                    btn_apply = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, 'btnApply'))
                    )
                    print(f"✅ [DEBUG] Botão Apply encontrado!")
                except TimeoutException:
                    print(f"❌ [DEBUG] Botão Apply não encontrado!")
                    falhas.append(f"{nome}: Botão Apply não encontrado")
                    continue
                
                print(f"🖱️ [DEBUG] Clicando no Apply...")
                btn_apply.click()
                time.sleep(8)
                
                # Aguarda carregar
                print(f"⏳ [DEBUG] Aguardando página carregar...")
                WebDriverWait(driver, 30).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                time.sleep(3)
                
                # Verifica se há dados
                print(f"🔍 [DEBUG] Verificando dados na tela...")
                data_elements = driver.find_elements(By.XPATH, "//table//tr | //div[contains(@class, 'data')] | //div[contains(@class, 'result')]")
                print(f"📊 [DEBUG] Elementos de dados encontrados: {len(data_elements)}")
                
                # Screenshot
                caminho_completo = os.path.join(pasta_prints, arquivo)
                print(f"📸 [DEBUG] Salvando screenshot: {caminho_completo}")
                
                driver.save_screenshot(caminho_completo)
                
                # Verifica arquivo
                if os.path.exists(caminho_completo):
                    tamanho = os.path.getsize(caminho_completo)
                    print(f"✅ [DEBUG] Screenshot salvo! Tamanho: {tamanho} bytes")
                    
                    if tamanho > 10000:
                        sucessos.append(nome)
                        print(f"🎉 {arquivo} - SUCESSO!")
                    else:
                        falhas.append(f"{nome}: Arquivo muito pequeno ({tamanho} bytes)")
                        print(f"⚠️ {arquivo} - Arquivo pequeno, pode estar vazio!")
                else:
                    falhas.append(f"{nome}: Arquivo não foi criado")
                    print(f"❌ {arquivo} - Arquivo não foi criado!")
                
            except Exception as e:
                falhas.append(f"{nome}: {str(e)}")
                print(f"❌ ERRO ao processar {nome}: {e}")
                
                # Screenshot de erro
                try:
                    erro_path = os.path.join(pasta_prints, f"ERRO_{codigo}_{nome.replace(' ', '_')}.png")
                    driver.save_screenshot(erro_path)
                    print(f"📸 [DEBUG] Screenshot de erro salvo: {erro_path}")
                except:
                    pass
                
                continue
        
        # RESUMO FINAL
        print("\n" + "=" * 70)
        print("🎊 PROCESSO FINALIZADO!")
        print("=" * 70)
        print(f"✅ SUCESSOS: {len(sucessos)}")
        print(f"❌ FALHAS: {len(falhas)}")
        print(f"📁 Pasta de prints: {pasta_prints}")
        
        if sucessos:
            print(f"\n✅ EMPRESAS PROCESSADAS COM SUCESSO:")
            for sucesso in sucessos:
                print(f"  - {sucesso}")
        
        if falhas:
            print(f"\n❌ EMPRESAS COM FALHA:")
            for falha in falhas:
                print(f"  - {falha}")
        
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        
        # Screenshot de erro crítico
        try:
            erro_critico = os.path.join(pasta_prints, f"ERRO_CRITICO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            driver.save_screenshot(erro_critico)
            print(f"📸 Screenshot de erro crítico salvo: {erro_critico}")
        except:
            pass
        
    finally:
        driver.quit()
        print("\n🔇 Navegador fechado - processo invisível concluído!")
        
        return sucessos, falhas

# Funções auxiliares para compatibilidade com interface robusta
import threading

should_stop = threading.Event()

def initialize_system():
    """Inicializa o sistema - compatibilidade com interface"""
    try:
        print("🔧 Sistema inicializado")
        return True
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        return False

def get_empresas_ativas():
    """Retorna lista de empresas ativas - compatibilidade com interface"""
    empresas = [
        [27119, "Matercaldas", "27119 - Matercaldas.png"],
        [26412, "Guimaraes 85", "26412 - Guimaraes 85.png"],
        [26413, "Guimaraes 63", "26413 - Guimaraes 63.png"],
        [7520, "Auto Posto Serra dos Pirineus", "7520 - Auto Posto Serra dos Pirineus.png"],
        [27138, "Mineira Materiais", "27138 - Mineira Materiais.png"],
        [24718, "Guifrii 50", "24718 - Guifrii 50.png"],
        [25992, "MARQUES E COSTA 81", "25992 - MARQUES E COSTA 81.png"],
        [26498, "MARQUES E COSTA 62", "26498 - MARQUES E COSTA 62.png"],
        [16289, "Equilibrio", "16289 - Equilibrio Homeopatia.png"],
        [17606, "MONTE CRISTO", "17606 - MONTE CRISTO.png"],
        [25991, "Mariana Joias", "25991 - Mariana Joias.png"],
        [15944, "CANTINHO FRIO", "15944 - CANTINHO FRIO.png"],
        [25715, "Casa Dibs", "25715 - Casa Dibs.png"],
        [26520, "Chao Nativo", "26520 - Chao Nativo.png"],
        [23980, "MERCEARIA E CONVENIENCIA DOS GAUCHOS", "23980 - MERCEARIA E CONVENIENCIA DOS GAUCHOS.png"],
        [17609, "Farmacia Essencial - 176", "17609 - Farmacia Essencial - 176.png"],
        [23703, "Farmacia Essencial - 257", "23703 - Farmacia Essencial - 257.png"],
        [26306, "Madeimanas Madeireira 60", "26306 - Madeimanas Madeireira 60.png"],
        [26305, "Madeimanas Madeireira 80", "26305 - Madeimanas Madeireira 80.png"],
        [26304, "Oliveira Casa", "26304 - Oliveira Casa e Construção.png"],
        [25716, "Posto Serra City", "25716 - Posto Serra City.png"],
        [23025, "Clinica San Francesco", "23025 - Clinica San Francesco.png"],
        [7517, "Posto Aderup", "7517 - Posto Aderup.png"],
        [16096, "Supermercado Feliz", "16096 - Supermercado Feliz.png"],
        [16660, "Posto Primavera 000170", "16660 - Posto Primavera 000170.png"],
        [16791, "Posto Petro Bessa", "16791 - Posto Petro Bessa.png"],
        [25488, "Drogaria Legitima - 00", "25488 - Drogaria Legitima - 00.png"],
        [25489, "Drogaria Legitima - 83", "25489 - Drogaria Legitima - 83.png"],
        [25490, "Drogaria Legitima - 46", "25490 - Drogaria Legitima - 46.png"]
    ]
    return empresas

def get_total_empresas():
    """Retorna total de empresas - compatibilidade com interface"""
    return len(get_empresas_ativas())

def get_status_sistema():
    """Retorna status do sistema - compatibilidade com interface"""
    return "👻 Sistema Invisível Ativo - Colaborador não vê nada!"

def gerar_prints(progress_callback=None, modo_invisivel=True):
    """Wrapper para gerar_prints_com_debug com callback de progresso"""
    return gerar_prints_com_debug(modo_invisivel)

def load_grupos_whatsapp():
    """Carrega grupos do WhatsApp do arquivo JSON"""
    try:
        if os.path.exists('grupos_whatsapp.json'):
            with open('grupos_whatsapp.json', 'r', encoding='utf-8') as f:
                grupos_data = json.load(f)
                # Filtra apenas grupos ativos
                return [(g['grupo'], g['arquivo']) for g in grupos_data if g.get('ativo', True)]
        else:
            # Lista padrão caso arquivo não exista
            return [
                ("voc", "16289 - Equilibrio Homeopatia.png"),
                ("GUIMA", "26412 - Guimaraes 85.png"),
                ("GUIMA", "26413 - Guimaraes 63.png"),
                ("Materca", "27119 - Matercaldas.png"),
                ("Serra dos Pirineus", "7520 - Auto Posto Serra dos Pirineus.png"),
                ("Mineira Mat", "27138 - Mineira Materiais.png"),
                ("CANTINHO FRIO", "15944 - CANTINHO FRIO.png"),
                ("Casa Dibs", "25715 - Casa Dibs.png"),
                ("Chao Nativo", "26520 - Chao Nativo.png"),
                ("CONVENIENCIA", "23980 - MERCEARIA E CONVENIENCIA DOS GAUCHOS.png"),
                ("Farmacia Essencial", "17609 - Farmacia Essencial - 176.png"),
                ("Farmacia Essencial", "23703 - Farmacia Essencial - 257.png"),
                ("Madeimanas", "26306 - Madeimanas Madeireira 60.png"),
                ("Madeimanas", "26305 - Madeimanas Madeireira 80.png"),
                ("Oliveira Casa", "26304 - Oliveira Casa e Construção.png"),
                ("Serra City", "25716 - Posto Serra City.png"),
                ("San Francesco", "23025 - Clinica San Francesco.png"),
                ("Posto 8", "7517 - Posto Aderup.png"),
                ("Supermercado Feliz", "16096 - Supermercado Feliz.png"),
                ("Posto Primavera", "16660 - Posto Primavera 000170.png"),
                ("Petro Bessa", "16791 - Posto Petro Bessa.png"),
                ("Drogaria Legitima", "25488 - Drogaria Legitima - 00.png"),
                ("Drogaria Legitima", "25489 - Drogaria Legitima - 83.png"),
                ("Drogaria Legitima", "25490 - Drogaria Legitima - 46.png"),
            ]
    except Exception as e:
        print(f"❌ Erro ao carregar grupos WhatsApp: {e}")
        return []

def save_grupos_whatsapp(grupos_data):
    """Salva grupos do WhatsApp no arquivo JSON"""
    try:
        with open('grupos_whatsapp.json', 'w', encoding='utf-8') as f:
            json.dump(grupos_data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar grupos WhatsApp: {e}")
        return False

def enviar_whatsapp(progress_callback=None, modo_invisivel=True):
    """Envia prints pelo WhatsApp"""
    
    print("📱 INICIANDO ENVIO PELO WHATSAPP")
    print("=" * 70)
    if modo_invisivel:
        print("👻 MODO INVISÍVEL ATIVADO - Colaborador não verá nada!")
    else:
        print("👁️ MODO VISÍVEL ATIVADO - Navegador aparecerá na tela!")
    
    # Configurações do Chrome para WhatsApp
    if modo_invisivel:
        print("🔧 Configurando Chrome em modo INVISÍVEL para WhatsApp...")
    else:
        print("🔧 Configurando Chrome em modo VISÍVEL para WhatsApp...")
    chrome_options = Options()
    
    # Controle do modo headless para WhatsApp
    if modo_invisivel:
        chrome_options.add_argument("--headless=new")
        print("👻 Modo HEADLESS ativado para WhatsApp - navegador será INVISÍVEL!")
    else:
        print("👁️ Modo VISÍVEL ativado para WhatsApp - navegador aparecerá na tela!")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceLogging")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Configurações específicas para WhatsApp
    user_data_dir = r"C:\Users\Luiz Marcelo\AppData\Local\Google\Chrome\User Data\Default"
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f'--profile-directory=Default')
    
    # Pasta de prints
    caminho_pasta = r"C:\Users\Luiz Marcelo\Desktop\PROJETO AUDIT PRICIPAL\prints"
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
        print(f"📁 Pasta criada: {caminho_pasta}")
    else:
        print(f"📁 Pasta existente: {caminho_pasta}")
    
    # Carrega grupos do WhatsApp do arquivo JSON
    empresas_whatsapp = load_grupos_whatsapp()
    
    print(f"📱 Total de envios WhatsApp a processar: {len(empresas_whatsapp)}")
    
    # Data da mensagem
    data_dois_dias_atras = datetime.now() - timedelta(days=3)
    data_formatada = data_dois_dias_atras.strftime("%d/%m/%Y")
    mensagem_texto = f"Olá, segue o quanto foi de vendas com as adquirentes no dia {data_formatada}, estamos enviando para que você confira com o que foi vendido em seu PDV"
    
    print(f"📅 Data da mensagem: {data_formatada}")
    print(f"💬 Mensagem: {mensagem_texto[:50]}...")
    
    sucessos = []
    falhas = []
    
    # Inicializa o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Configurações de timeout robustas
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(30)
    
    # Remove propriedades que indicam automação
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # 1. ACESSA WHATSAPP WEB
        print("\n1️⃣ ACESSANDO WHATSAPP WEB...")
        driver.get("https://web.whatsapp.com/")
        
        # Aguarda página carregar completamente
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(10)
        
        print(f"🔍 [DEBUG] URL carregada: {driver.current_url}")
        print(f"🔍 [DEBUG] Título: {driver.title}")
        
        # Aguarda WhatsApp estar logado
        print("⏳ [DEBUG] Aguardando WhatsApp estar logado...")
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "side"))
            )
            print("✅ WhatsApp logado com sucesso!")
            time.sleep(5)
        except TimeoutException:
            print("❌ [DEBUG] WhatsApp não logou a tempo!")
            raise Exception("WhatsApp não logou - verifique se está logado no navegador")
        
        # 2. PROCESSAR ENVIOS
        print(f"\n2️⃣ PROCESSANDO {len(empresas_whatsapp)} ENVIOS...")
        print("=" * 70)
        
        def enviar_print_invisivel(grupo, arquivo_print, index):
            """Envia print para um grupo específico"""
            print(f"\n[{index+1}/{len(empresas_whatsapp)}] 📱 ENVIANDO PARA: {grupo}")
            print(f"📁 Arquivo: {arquivo_print}")
            
            try:
                # Callback de progresso
                if progress_callback:
                    progress_callback(index+1, len(empresas_whatsapp), grupo)
                
                # Busca o grupo
                print(f"🔍 [DEBUG] Procurando barra de busca...")
                barra_busca = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div/p'))
                )
                print(f"✅ [DEBUG] Barra de busca encontrada!")
                
                # Limpa e digita o grupo
                print(f"🧹 [DEBUG] Limpando barra de busca...")
                barra_busca.clear()
                barra_busca.send_keys(Keys.CONTROL, 'a')
                time.sleep(1)
                
                print(f"⌨️ [DEBUG] Digitando grupo: '{grupo}'")
                barra_busca.send_keys(grupo)
                time.sleep(3)
                
                print(f"↩️ [DEBUG] Pressionando ENTER...")
                barra_busca.send_keys(Keys.ENTER)
                time.sleep(3)
                
                # Verifica se o arquivo existe
                caminho_print = os.path.join(caminho_pasta, arquivo_print)
                print(f"🔍 [DEBUG] Verificando arquivo: {caminho_print}")
                
                if not os.path.exists(caminho_print):
                    print(f"❌ [DEBUG] Arquivo NÃO encontrado: {arquivo_print}")
                    falhas.append(f"{grupo}: Arquivo não encontrado - {arquivo_print}")
                    return
                
                print(f"✅ [DEBUG] Arquivo encontrado!")
                
                # Botão de anexo
                print(f"🔍 [DEBUG] Procurando botão de anexo...")
                try:
                    attach_button = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button'))
                    )
                    print(f"✅ [DEBUG] Botão de anexo encontrado!")
                    time.sleep(2)
                    attach_button.click()
                    time.sleep(3)
                except TimeoutException:
                    print(f"❌ [DEBUG] Botão de anexo não encontrado!")
                    falhas.append(f"{grupo}: Botão de anexo não encontrado")
                    return
                
                # Input de imagem
                print(f"🔍 [DEBUG] Procurando input de imagem...")
                try:
                    image_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
                    )
                    print(f"✅ [DEBUG] Input de imagem encontrado!")
                    image_input.send_keys(caminho_print)
                    time.sleep(3)
                except TimeoutException:
                    print(f"❌ [DEBUG] Input de imagem não encontrado!")
                    falhas.append(f"{grupo}: Input de imagem não encontrado")
                    return
                
                # Botão de enviar imagem
                print(f"🔍 [DEBUG] Procurando botão de enviar imagem...")
                try:
                    send_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span'))
                    )
                    print(f"✅ [DEBUG] Botão de enviar imagem encontrado!")
                    send_button.click()
                    time.sleep(3)
                    print(f"📸 [DEBUG] Imagem {arquivo_print} enviada para {grupo}!")
                except TimeoutException:
                    print(f"❌ [DEBUG] Botão de enviar imagem não encontrado!")
                    falhas.append(f"{grupo}: Botão de enviar imagem não encontrado")
                    return
                
                # Enviar mensagem de texto
                print(f"🔍 [DEBUG] Procurando campo de mensagem...")
                try:
                    mensagem_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]'))
                    )
                    print(f"✅ [DEBUG] Campo de mensagem encontrado!")
                    mensagem_input.send_keys(mensagem_texto)
                    time.sleep(2)
                except TimeoutException:
                    print(f"❌ [DEBUG] Campo de mensagem não encontrado!")
                    falhas.append(f"{grupo}: Campo de mensagem não encontrado")
                    return
                
                # Botão de enviar mensagem
                print(f"🔍 [DEBUG] Procurando botão de enviar mensagem...")
                try:
                    mensagem_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[4]/button'))
                    )
                    print(f"✅ [DEBUG] Botão de enviar mensagem encontrado!")
                    time.sleep(2)
                    mensagem_button.click()
                    time.sleep(3)
                    print(f"💬 [DEBUG] Mensagem enviada para {grupo}!")
                except TimeoutException:
                    print(f"❌ [DEBUG] Botão de enviar mensagem não encontrado!")
                    falhas.append(f"{grupo}: Botão de enviar mensagem não encontrado")
                    return
                
                sucessos.append(grupo)
                print(f"🎉 {grupo} - ENVIO COMPLETO!")
                
            except Exception as e:
                falhas.append(f"{grupo}: {str(e)}")
                print(f"❌ ERRO ao enviar para {grupo}: {e}")
        
        # Processa todos os envios
        for i, (grupo, arquivo_print) in enumerate(empresas_whatsapp):
            if should_stop.is_set():
                print("⏹️ Processo interrompido pelo usuário")
                break
                
            try:
                enviar_print_invisivel(grupo, arquivo_print, i)
                time.sleep(2)  # Pausa entre envios
            except Exception as e:
                falhas.append(f"{grupo}: {str(e)}")
                print(f"❌ ERRO ao processar {grupo}: {e}")
                continue
        
        # RESUMO FINAL
        print("\n" + "=" * 70)
        print("📱 ENVIO WHATSAPP FINALIZADO!")
        print("=" * 70)
        print(f"✅ SUCESSOS: {len(sucessos)}")
        print(f"❌ FALHAS: {len(falhas)}")
        print(f"📁 Pasta de prints: {caminho_pasta}")
        
        if sucessos:
            print(f"\n✅ GRUPOS COM ENVIO REALIZADO:")
            for sucesso in sucessos:
                print(f"  - {sucesso}")
        
        if falhas:
            print(f"\n❌ GRUPOS COM FALHA:")
            for falha in falhas:
                print(f"  - {falha}")
        
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO NO WHATSAPP: {e}")
        
        # Screenshot de erro crítico
        try:
            erro_critico = os.path.join(caminho_pasta, f"ERRO_WHATSAPP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            driver.save_screenshot(erro_critico)
            print(f"📸 Screenshot de erro crítico salvo: {erro_critico}")
        except:
            pass
        
    finally:
        driver.quit()
        print("\n🔇 Navegador WhatsApp fechado - processo invisível concluído!")
        
        return sucessos, falhas

if __name__ == "__main__":
    print("🚀 EXECUTANDO GERAÇÃO DE PRINTS COM DEBUG...")
    sucessos, falhas = gerar_prints_com_debug()
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"✅ Sucessos: {len(sucessos)}")
    print(f"❌ Falhas: {len(falhas)}")
    
    if falhas:
        print(f"\n🔍 DETALHES DAS FALHAS:")
        for falha in falhas:
            print(f"  - {falha}") 