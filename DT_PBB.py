import random
import socket
import sys

# Env´ıa un paquete con loss_rate porcentaje de p´erdida
# si loss_rate = 5, implica un 5% de p´erdida
def send_loss(s, data):
    global loss_rate
    if random.random() * 100 > loss_rate:
        s.send(data)
    else:
        print("[send_loss]")
# Recibe un paquete con loss_rate porcentaje de p´erdida
# Si decide perderlo, vuelve al recv y no retorna aun
# Retorna None si hay timeout o error
def recv_loss(s, size):
    global loss_rate
    try:
        while True:
            data = s.recv(size)
            if random.random() * 100 <= loss_rate:
                print("[recv_loss]")
            else:
                break
    except socket.timeout:
        print('timeout', file=sys.stderr)
        data = None
    except socket.error:
        print('recv err', file=sys.stderr)
        data = None
    return data