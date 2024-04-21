import pyautogui
import time
import pyperclip
import ipaddress
import multiprocessing
import netifaces as ni
from scapy.all import Ether, ARP, srp, conf
from concurrent.futures import ThreadPoolExecutor
import csv
import datetime
import pandas


# Obtém o nome da interface de rede
interface = ni.gateways()['default'][ni.AF_INET][1]

# Obter o endereço IP e a máscara de rede da interface de rede
endereco_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
mascara_rede = ni.ifaddresses(interface)[ni.AF_INET][0]['netmask']
print(endereco_ip)
# Encontra todos os IPs no range da máscara de rede
rede = ipaddress.IPv4Network(endereco_ip + '/' + mascara_rede, strict=False)

#ips_na_rede = [str(ip) for ip in rede.hosts()]
ips_na_rede = ['192.168.1.1'] # todo: remover!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
dispositivos_conectados = []

def ping_um_ip(ip):
    
    resposta = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=7, verbose=0)[0]
    if resposta:
        dispositivos_conectados.append({'IP': resposta[0][1].psrc, 'MAC': resposta[0][1].hwsrc})
    
num_nucleos = multiprocessing.cpu_count()
print("Número de núcleos:", num_nucleos)
with ThreadPoolExecutor(max_workers=num_nucleos) as executor:
    executor.map(ping_um_ip, ips_na_rede)

for dispositivo in dispositivos_conectados:
    print("IP:", dispositivo['IP'], "| MAC:", dispositivo['MAC'])

# Use datetime para obter a data e hora atual
agora = datetime.datetime.now()

# Combine o caminho específico com o nome do arquivo usando f-string
caminho_completo = r"C:\Users\JoãoVictorSoaresJord\Documents\ArquivoDaAutomação\relatorio_rede.csv"
# Abra o arquivo usando o caminho completo
with open(caminho_completo, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['IP', 'MAC'])

    for obj in dispositivos_conectados:
        writer.writerow([obj['IP'], obj['MAC']])

# time.sleep(3)
# pyautogui.position() 

pyautogui.PAUSE = 1
#seleciona ícone do navegador, abre nova guia e acessa o gmail
pyautogui.click(967,1063,1)
pyautogui.hotkey('ctrl', 't')
pyperclip.copy(text="https://mail.google.com/mail/u/0/?ogbl#inbox")
pyautogui.hotkey('ctrl', 'v')
pyautogui.PAUSE = 5
pyautogui.press('enter')    
pyautogui.PAUSE = 1

#cria nova mensagem, adiciona email para envio e adiciona um título
pyautogui.click(183,188,1)
pyperclip.copy(text="victorsoaresrj@hotmail.com")
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('tab')
pyperclip.copy(text="Informações atualizadas dos ips encontrados")
pyautogui.hotkey('ctrl', 'v')
pyautogui.PAUSE = 1

#abre pagina de anexo, navega até o arquivo, e sobe no corpo do email
pyautogui.click(894,990,1)
pyautogui.click(556,52,1)
pyperclip.copy(text=r"C:\Users\JoãoVictorSoaresJord\Documents\ArquivoDaAutomação")
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
pyautogui.click(368,160 ,1)
pyautogui.press('enter')
pyautogui.click(753,993,1)