import socket
import sys
from datetime import datetime

# Configuração de Cores
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def scan_port(ip, port):
    """Verifica se uma porta está aberta e tenta pegar o Banner (versão do serviço)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0) # Timeout para agilizar
        result = s.connect_ex((ip, port))
        
        if result == 0:
            # Tenta pegar o banner (o que o serviço responde)
            try:
                s.send(b'HEAD / HTTP/1.0\r\n\r\n') # Tenta falar HTTP
                banner = s.recv(1024).decode().strip().split('\n')[0]
            except:
                banner = "Serviço detectado (Sem Banner)"
            
            s.close()
            return True, banner
        else:
            s.close()
            return False, ""
    except:
        return False, ""

def generate_report(ip, open_ports, start_time, end_time):
    """Cria um arquivo Markdown bonito para o GitHub"""
    filename = f"Analise_{ip.replace('.', '_')}.md"
    
    with open(filename, "w") as f:
        f.write(f"# Relatório de Análise Técnica: {ip}\n\n")
        f.write(f"**Data da Análise:** {start_time}\n")
        f.write(f"**Duração:** {end_time - start_time}\n\n")
        
        f.write("## 1. Resumo Executivo\n")
        f.write(f"Foi realizada uma varredura de portas no ativo `{ip}`. ")
        f.write(f"Foram identificadas **{len(open_ports)}** portas abertas acessíveis externamente.\n\n")
        
        f.write("## 2. Detalhes dos Serviços Encontrados\n")
        f.write("| Porta | Estado | Banner/Serviço |\n")
        f.write("|-------|--------|----------------|\n")
        
        for port, banner in open_ports:
            # Limpa caracteres estranhos do banner para não quebrar o Markdown
            safe_banner = banner.replace('|', '-') 
            f.write(f"| **{port}** |  ABERTA | `{safe_banner}` |\n")
            
        f.write("\n## 3. Recomendação Inicial\n")
        f.write("- [ ] Verificar se estes serviços precisam estar expostos.\n")
        f.write("- [ ] Comparar versões dos banners com CVEs conhecidos.\n")
        
    print(f"\n{GREEN} Relatório gerado com sucesso: {filename}{RESET}")
    print(f" Dica: Use 'cat {filename}' para ver ou suba para o GitHub!")

def main():
    print(f"{BLUE}--- GERADOR DE RELATÓRIOS SOC AUTOMATIZADO ---{RESET}")
    
    if len(sys.argv) < 2:
        target = input("Digite o IP alvo (ex: sua VM do VirtualBox): ")
    else:
        target = sys.argv[1]

    # Lista de portas comuns para ser rápido (pode aumentar se quiser)
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
    
    print(f"\nIniciando varredura em {target}...")
    start_time = datetime.now()
    found_ports = []

    try:
        for port in common_ports:
            is_open, banner = scan_port(target, port)
            if is_open:
                print(f" Porta {port} ABERTA! ({banner})")
                found_ports.append((port, banner))
            else:
                # Opcional: printar portas fechadas (polui muito a tela)
                pass 
                
    except KeyboardInterrupt:
        print(f"\n{RED}Cancelado pelo usuário.{RESET}")
        sys.exit()

    end_time = datetime.now()
    
    if found_ports:
        generate_report(target, found_ports, start_time, end_time)
    else:
        print(f"\n{RED}Nenhuma porta comum encontrada aberta. O firewall pode estar ativo.{RESET}")

if __name__ == "__main__":
    main()
