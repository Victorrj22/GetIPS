# -*- coding: utf-8 -*-

import ipaddress
import netifaces as ni
from scapy.all import Ether, ARP, srp, conf

# Obt�m o nome da interface de rede
interface = ni.gateways()['default'][ni.AF_INET][1]

# Obter o endere�o IP e a m�scara de rede da interface de rede
endereco_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
mascara_rede = ni.ifaddresses(interface)[ni.AF_INET][0]['netmask']

# Encontra todos os IPs no range da m�scara de rede
rede = ipaddress.IPv4Network(endereco_ip + '/' + mascara_rede, strict=False)
ips_na_rede = [str(ip) for ip in rede.hosts()]

dispositivos_conectados = []

# Faz o "ping" nas redes dispon�veis
for ip in ips_na_rede:
    resposta = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=0)[0]
    if resposta:
        dispositivos_conectados.append({'IP': resposta[0][1].psrc, 'MAC': resposta[0][1].hwsrc})

# Exibe os dispositivos conectados
for dispositivo in dispositivos_conectados:
    print("IP:", dispositivo['IP'], "MAC:", dispositivo['MAC'])