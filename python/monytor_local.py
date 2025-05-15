import psutil
import logging
import time
import socket


LOG_FILE = "monitoramento_local.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


CPU_THRESHOLD = 80    
MEMORY_THRESHOLD = 80   
DISK_THRESHOLD = 90    

WEBSERVER_PORT = 80
MYSQL_PORT = 3306 

def check_cpu():
    cpu = psutil.cpu_percent(interval=1)
    logging.info(f"Uso de CPU atual: {cpu}%")
    if cpu > CPU_THRESHOLD:
        logging.warning(f"ALERTA: Uso de CPU alto: {cpu}%")
    return cpu

def check_memory():
    mem = psutil.virtual_memory().percent
    logging.info(f"Uso de Memória atual: {mem}%")
    if mem > MEMORY_THRESHOLD:
        logging.warning(f"ALERTA: Uso de Memória alto: {mem}%")
    return mem

def check_disk():
    disk = psutil.disk_usage('/').percent
    logging.info(f"Uso de Disco atual: {disk}%")
    if disk > DISK_THRESHOLD:
        logging.warning(f"ALERTA: Uso de Disco alto: {disk}%")
    return disk

def check_port(port, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        logging.info(f"{name} (porta {port}) está ATIVO.")
        return True
    else:
        logging.error(f"ALERTA: {name} (porta {port}) está INATIVO!")
        return False

def run_monitoring():
    logging.info("=== Iniciando monitoramento local ===")

    check_cpu()
    check_memory()
    check_disk()
    check_port(WEBSERVER_PORT, "Webserver")
    check_port(MYSQL_PORT, "MySQL")

    logging.info("=== Monitoramento concluído ===\n")

def main():
    try:
        while True:
            run_monitoring()
            time.sleep(60)  
    except KeyboardInterrupt:
        logging.info("Monitoramento encerrado pelo usuário.")
        print("Monitoramento finalizado.")

if __name__ == "__main__":
    main()