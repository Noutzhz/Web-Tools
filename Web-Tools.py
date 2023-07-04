import requests
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

print('''
 __      __     _         _____           _     
 \ \    / /___ | |__  ___|_   _|___  ___ | | ___
  \ \/\/ // -_)| '_ \|___| | | / _ \/ _ \| |(_-<
   \_/\_/ \___||_.__/      |_| \___/\___/|_|/__/
                                                

                Make a By: Noutz                

[火] https://github.com/Noutzhz

[火] https://linktr.ee/noutzhz

[火] защищенный авторским правом файл

''')

target_url = input('Digite a URL do alvo: ')

print('''

[火] Buscando subdomínios e portas abertas

''')

print('''

[火] O processo pode demorar devido à sua conexão com a internet ou à velocidade do host do site

''')

print('''

[火] Subdomínios e portas encontrados

''')

def get_subdomains(domain):
    subdomains = []
    try:
        # Realiza uma pesquisa DNS para o domínio fornecido
        _, _, ip_list = socket.gethostbyname_ex(domain)
        for ip in ip_list:
            # Verifica se o endereço IP possui subdomínios
            try:
                subdomain_list = socket.gethostbyaddr(ip)
                subdomains.extend(subdomain_list)
            except socket.herror:
                pass
    except socket.gaierror:
        print("Não foi possível resolver o domínio.")

    return subdomains

try:
    response = requests.get(target_url)
    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc
    print("Domínio:", domain)
    
    # Buscar subdomínios
    subdomains = get_subdomains(domain)
    print("Subdomínios encontrados:")
    for subdomain in subdomains:
        print(subdomain)

    # Escanear portas
    NUM_THREADS = 50

    target_host = parsed_url.netloc.split(':')[0]  # Extrai o nome do host da URL
    port_range = range(1, 8080)  # Esta faixa de porta pode ser alterada pelo usuário

    def scan_port(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((target_host, port))
            return port, result == 0

    open_ports = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(scan_port, port) for port in port_range]
        num_scanned = 0
        for future in as_completed(futures):
            num_scanned += 1
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
            print(f"\rEscaneando porta {port} de {len(port_range)}", end="")

    print("\nPortas abertas:")
    for port in open_ports:
        print(port)

except requests.exceptions.RequestException as e:
    print("Erro de conexão:", e)

input('Pressione Enter para sair. Feito por Noutz.')
