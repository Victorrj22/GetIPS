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
import tqdm as progress_bar


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
print("IPs a serem verificados na rede: ", len(ips_na_rede))
dispositivos_conectados = []

progress = progress_bar.tqdm(ips_na_rede)

def ping_an_ip(ip):
    progress.update(1)
    resposta = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=7, verbose=0)[0]
    if resposta:
        dispositivos_conectados.append({'IP': resposta[0][1].psrc, 'MAC': resposta[0][1].hwsrc})

def open_gmail():
    #seleciona ícone do navegador, abre nova guia e acessa o gmail
    pyautogui.click(1280,1328,1)
    pyautogui.hotkey('ctrl', 't')
    pyperclip.copy(text="https://mail.google.com/mail/u/0/?ogbl#inbox")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.PAUSE = 5
    pyautogui.press('enter')    
    pyautogui.PAUSE = 1

def create_email_message():
    #cria nova mensagem, adiciona email para envio e adiciona um título
    pyautogui.click(249,238,1)
    pyperclip.copy(text="victorsoaresrj@hotmail.com")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('tab')
    pyperclip.copy(text="Informações atualizadas dos ips encontrados")
    pyautogui.hotkey('ctrl', 'v')

def attach_file_and_send_email():
    #abre pagina de anexo, navega até o arquivo, e sobe no corpo do email
    pyautogui.click(1120,1230,1)
    pyautogui.click(610,71,1)
    pyperclip.copy(text=r"C:\Users\JoãoVictorSoaresJord\Documents\ArquivoDaAutomação")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.click(460,205 ,1)
    pyautogui.press('enter')
    pyautogui.click(933,1228,1)
    
num_nucleos = multiprocessing.cpu_count()
print("Verificando dispositivos conectados na rede")
print("Número de núcleos disponíveis para a tarefa:", num_nucleos)
with ThreadPoolExecutor(max_workers=num_nucleos) as executor:
    executor.map(ping_an_ip, ips_na_rede) # para cada ip em ips_na_rede, executa ping_an_ip
    executor.shutdown

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

open_gmail()
pyautogui.PAUSE = 1

create_email_message()
pyautogui.PAUSE = 1

attach_file_and_send_email()

# time.sleep(3)
# pyautogui.position() 

