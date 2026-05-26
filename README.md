# SOC Automation & Vulnerability Analysis Lab

Bem-vindo ao meu laboratório de ferramentas de Segurança da Informação. Este repositório contém scripts desenvolvidos
em **Python** para automatizar rotinas diárias de um **Security Operations Center (SOC)**, incluindo detecção de 
intrusão, monitoramento de integridade e relatórios de vulnerabilidade.

## Ferramentas Incluídas

### 1. Lab Report & Vulnerability Scanner (`lab_report.py`)
Ferramenta de automação para varredura de portas e geração de documentação técnica.
- **Funcionalidade:** Realiza scan de portas em ativos alvo, identifica serviços rodando (Banner Grabbing) e gera 
automaticamente um relatório em Markdown.
- **Caso de Uso no SOC:** Redução do tempo de documentação (MTTR) e triagem inicial de ativos suspeitos.
- **Output:** Gera arquivos `Analise_IP.md` prontos para serem anexados a tickets de incidentes.

### 2. LogSec - SOC Real-time Monitor (`logsec.py`)
Ferramenta de monitoramento ativo de servidor baseada em logs e processos.
- **Funcionalidades:**
  - Detecção de Brute-force SSH (análise de `auth.log`).
  - Monitoramento de conexões de rede ativas e portas abertas (Listening).
  - Top 5 processos por consumo de recurso (detecção de Crypto Miners).
  - Auditoria de comandos `sudo` recentes.
  - Verificação de disponibilidade de disco (Log Availability).

---

## Tecnologias Utilizadas
- **Linguagem:** Python 3 (Bibliotecas nativas: `socket`, `subprocess`, `sys`, `re`).
- **Sistema Alvo:** Linux (Ubuntu/Debian).
- **Conceitos Aplicados:** Socket Programming, Log Parsing, System Administration, Report Automation.

## Como Executar

### Pré-requisitos
```bash
# Certifique-se de ter Python 3 instalado
sudo apt update && sudo apt install python3

---

## Exemplo de Relatório Gerado
*Trecho de um relatório automático gerado pelo `lab_report.py`:*

| Porta | Estado | Serviço Detectado |
|-------|--------|-------------------|
| **22** |  ABERTA | `SSH-2.0-OpenSSH_8.2p1` |
| **80** |  ABERTA | `Apache/2.4.41 (Ubuntu)` |

---

**Autor:** Diego Machado
*Estudante de Segurança da Informação e Entusiasta de DevSecOps.*


