#!/usr/bin/env python3
import os
import subprocess
import re
import sys
from datetime import datetime

# --- CORES PARA O TERMINAL ---
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_banner():
    os.system('clear')
    print(f"{CYAN}=" * 60)
    print(f"{BOLD}   🛡️   VERIFICADOR AVANÇADO DE ACESSOS SOC (v2.0)   🛡️{RESET}{CYAN}")
    print(f"=" * 60 + f"{RESET}")
    print(f"Data da Análise: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def run_cmd(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return ""

# 1. ANÁLISE DE LOGINS (Sua versão original melhorada)
def check_auth():
    print(f"{YELLOW}[!] TENTATIVAS RECENTES DE FALHA DE LOGIN (SSH){RESET}")
    # Busca falhas no auth.log
    cmd = "grep 'Failed password' /var/log/auth.log | tail -n 5"
    fails = run_cmd(cmd)
    
    if fails:
        for line in fails.split('\n'):
            # Destaca o IP em vermelho
            parts = line.split()
            print(f"   🔴 {line}")
    else:
        print(f"   {GREEN}Nenhuma falha recente registrada.{RESET}")
    print("-" * 60)

    print(f"{GREEN}[+] ÚLTIMOS LOGINS BEM SUCEDIDOS{RESET}")
    # Quem está logado agora ou logou recentemente
    success = run_cmd("last -n 5 -a | grep -v 'reboot' | grep -v 'wtmp'")
    if success:
        print(success)
    else:
        print("   Nenhum login recente.")
    print("-" * 60)

# 2. ANÁLISE DE REDE (Novidade SOC)
def check_network():
    print(f"{CYAN}[🌐] CONEXÕES DE REDE ATIVAS (ESTABLISHED){RESET}")
    print("Verificando quem está conversando com seu servidor agora...")
    
    # Lista conexões estabelecidas (excluindo localhost)
    net_cmd = "ss -tunap | grep ESTAB"
    net_output = run_cmd(net_cmd)
    
    if net_output:
        print(f"{BOLD}{'PROTO':<6} {'LOCAL IP':<20} {'REMOTE IP':<20} {'PROCESS'}{RESET}")
        for line in net_output.split('\n'):
            parts = line.split()
            if len(parts) > 5:
                proto = parts[0]
                local = parts[4]
                remote = parts[5]
                process = parts[6] if len(parts) > 6 else "Unknown"
                print(f"   {proto:<6} {local:<20} {RED}{remote:<20}{RESET} {process}")
    else:
        print(f"   {GREEN}Nenhuma conexão externa ativa no momento.{RESET}")
    print("-" * 60)

    print(f"{CYAN}[👂] PORTAS ABERTAS (LISTENING){RESET}")
    # Portas que o servidor está "ouvindo" (Portas abertas são vetores de ataque)
    listen_cmd = "ss -lntu | grep LISTEN"
    listen_output = run_cmd(listen_cmd)
    if listen_output:
        for line in listen_output.split('\n'):
             print(f"   🔓 {line}")
    print("-" * 60)

# 3. ANÁLISE DE PROCESSOS (Novidade SOC)
def check_processes():
    print(f"{YELLOW}[⚙️] TOP 5 PROCESSOS (Consumo de CPU/RAM){RESET}")
    # Mostra os processos mais pesados (útil para achar mineradores ou ataques DoS)
    ps_cmd = "ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 6"
    print(run_cmd(ps_cmd))
    print("-" * 60)

# 4. MONITORAMENTO DE SUDO
def check_sudo():
    print(f"{CYAN}[#] USO RECENTE DE SUDO (Últimos 5){RESET}")
    # Busca comandos sudo no auth.log
    cmd = "grep 'COMMAND=' /var/log/auth.log | tail -n 5"
    sudo_logs = run_cmd(cmd)
    
    if sudo_logs:
        for line in sudo_logs.split('\n'):
            # Tenta limpar a linha para mostrar só o comando
            try:
                user = re.search(r'sudo:\s+(.*?)\s+:', line).group(1)
                command = line.split('COMMAND=')[1]
                print(f"   👤 {BOLD}{user}{RESET} executou: {command}")
            except:
                print(f"   {line}")
    else:
        print(f"   {GREEN}Nenhum comando sudo recente.{RESET}")
    print("-" * 60)

# 5. VERIFICAÇÃO DE DISCO (Vital para logs)
def check_disk():
    print(f"{CYAN}[💾] ESPAÇO EM DISCO{RESET}")
    # Se o disco enche, o SOC fica cego (logs param)
    print(run_cmd("df -h / | awk 'NR==2 {print \"   Uso: \" $5 \" de \" $2}'"))
    print("=" * 60)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{RED}ERRO: Execute como root! (sudo python3 logsec.py){RESET}")
        sys.exit(1)
        
    print_banner()
    check_auth()
    check_network()
    check_processes()
    check_sudo()
    check_disk()
    print(f"\n{GREEN}Fim da análise.{RESET}")
