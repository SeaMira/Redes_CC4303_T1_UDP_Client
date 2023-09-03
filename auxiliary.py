import random
import socket
import sys
import time

loss_rate = 0

# Env´ıa un paquete con loss_rate porcentaje de p´erdida
# si loss_rate = 5, implica un 5% de p´erdida


class Loss(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)


def send_loss(s, data):
    global loss_rate
    if random.random() * 100 > loss_rate:
        s.send(data)
    else:
        # print("[send_loss]")
        raise Loss("[send_loss]")
# Recibe un paquete con loss_rate porcentaje de pérdida
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


def encode_package_time(package_size, time_ms):
    # Asegúrate de que los valores estén en el rango permitido
    if package_size < 0 or package_size > 9999 or time_ms < 0 or time_ms > 9999:
        raise ValueError(
            "Los valores de tamaño de paquete y tiempo deben estar entre 0 y 9999")

    # Convierte los valores en cadenas de 4 dígitos con ceros a la izquierda si es necesario
    package_str = str(package_size).zfill(4)
    # print("package siz:", package_str)
    time_str = str(time_ms).zfill(4)
    # print("time ms:", time_str)

    # Concatena las cadenas y agrega el carácter 'C' al principio
    encoded_str = f'C{package_str}{time_str}'

    # Convierte la cadena codificada en un bytearray de números
    encoded_bytes = bytearray(encoded_str, encoding='utf-8')

    return (package_str, encoded_bytes)


def pack_rec(s, fileout, pack_sz):
    total_bytes = 0
    actual_code = ""
    seq_nmb = "00"
    errores = 0

    start = time.time()
    while True:
        print("try")
        s.settimeout(5)
        rcv_data = recv_loss(s, pack_sz + 3)

        if rcv_data == None:
            print("[Error]")
            errores += 1
        else:
            actual_code = rcv_data.decode('utf-8')[0]
            if actual_code == "E":
                print("[End]")
                send_loss(s, "A".encode('UTF-8') + rcv_data[1:3])
                break

            if rcv_data[1:3].decode('utf-8') == seq_nmb:
                try:
                    send_loss(s, "A".encode('UTF-8') + rcv_data[1:3])
                    seq_nmb = str((int(seq_nmb) + 1) % 100).zfill(2)
                    total_bytes += len(rcv_data[3:])
                    fileout.write(rcv_data[3:])
                except Loss:
                    pass
            else:
                print("[Error]")
                errores += 1
    end = time.time()
    return (total_bytes, errores, start, end)
