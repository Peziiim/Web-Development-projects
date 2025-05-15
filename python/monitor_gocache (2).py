import subprocess
import socket
import logging
import time
import platform
import http.client
import ssl
from datetime import datetime
  
TARGET_IPS = ["170.82.173.10", "170.82.174.10"]
PORTS_TO_CHECK = [80, 443]
LOG_FILE = "gocache_monitoring.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def check_port(ip, port, timeout=5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        logging.error(f"Erro ao verificar porta {port} no IP {ip}: {str(e)}")
        return False

def check_icmp(ip, timeout=5):
    try:
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "2", "-w", str(timeout * 1000), ip]
        else:
            command = ["ping", "-c", "2", "-W", str(timeout), ip]
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False 
        )    
        process.communicate()
        return process.returncode == 0
    except Exception as e:
        logging.error(f"Erro ao executar ping para IP {ip}: {str(e)}")
        return False

def trace_route(ip):
    try:
        if platform.system().lower() == "windows":
            command = ["tracert", "-d", "-w", "500", ip]
        else:
            command = ["traceroute", "-n", "-w", "1", ip]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        stdout, stderr = process.communicate()
        logging.info(f"Rota {stdout}")

        return stdout
    except Exception as e:
        logging.error(f"Erro ao executar traceroute para IP {ip}: {str(stderr)}")
        return f"Falha ao executar traceroute: {str(e)}"

def check_http_status(ip, port):
    try:
        if port == 443:
            conn = http.client.HTTPSConnection(ip, port, timeout=5, context=ssl._create_unverified_context())
        else:
            conn = http.client.HTTPConnection(ip, port, timeout=5)
        
        conn.request("HEAD", "/")
        response = conn.getresponse()
        status = response.status
        conn.close()
        return status
    except Exception as e:
        return f"Erro: {str(e)}"
    

def run_monitoring():
    logging.info("Iniciando ciclo de monitoramento")
    
    for ip in TARGET_IPS:
        logging.info(f"Verificando IP: {ip}")
        
        icmp_ok = check_icmp(ip)
        if not icmp_ok:
            logging.warning(f"ALERTA: ICMP bloqueado para {ip}")
            trace_result = trace_route(ip)
            logging.info(f"Traceroute para {ip}:\n{trace_result}")
        else:
            logging.info(f"ICMP OK para {ip}")
        
        for port in PORTS_TO_CHECK:
            port_ok = check_port(ip, port)
            if not port_ok:
                logging.warning(f"ALERTA: Porta {port} não acessível em {ip}")
            else:
                status = check_http_status(ip, port)
                logging.info(f"Porta {port} OK em {ip} - Status HTTP: {status}")

        
        trace_result = trace_route(ip)
        logging.info(f"Traceroute para {ip}:\n{trace_result}")
        logging.info(f"Monitoramento concluído para {ip}\n")

def main():
    logging.info("=== Iniciando monitoramento de IPs da GoCache ===")
    logging.info(f"IPs monitorados: {', '.join(TARGET_IPS)}")
    logging.info(f"Portas monitoradas: {', '.join(map(str, PORTS_TO_CHECK))}")
    
    try:
        while True:
            try:
                run_monitoring()
                logging.info("Aguardando próximo ciclo de monitoramento (60 segundos)")
                time.sleep(60)  
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logging.error(f"Erro no ciclo de monitoramento: {str(e)}")
                time.sleep(30)  
                
    except KeyboardInterrupt:
        logging.info("Monitoramento interrompido pelo usuário")
        print("\nMonitoramento finalizado. Verifique o log para detalhes.")
    except Exception as e:
        logging.error(f"Erro fatal no monitoramento: {str(e)}")
        print(f"\nErro fatal: {str(e)}")
        print(f"Verifique o log em {LOG_FILE} para mais detalhes.")

if __name__ == "__main__":
    main()
