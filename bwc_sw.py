#!/usr/bin/python3
# Echo client program
# Version con dos threads: uno lee de stdin hacia el socket y el otro al revés
import jsockets
import sys
import threading
import time
import auxiliary as aux

loss_rate = 0


def stopAndWaitUDP(s, pack_sz, nbytes, timeout, loss, fileout):
    s_msg, en_msg = aux.encode_package_time(pack_sz, timeout)

    global loss_rate
    loss_rate = float(loss)

    print("propuse paquete:", s_msg)
    s.send(en_msg)
    act_pack_sz = s.recv(10).decode('utf-8')
    print("recibo paquete:", act_pack_sz)
    s.send("N" + nbytes)
    print("recibiendo", nbytes, "nbytes")

    # Recepcion de paquetes
    total_bytes, errores, start, end = aux.pack_rec(
        s, fileout, int(act_pack_sz[1:]))

    print("bytes recibidos =", total_bytes, ", time =", end-start,
          " , bw = ", total_bytes/(end-start), " , errores = ", errores)


# Program start: asking for parameters and creating a link
if len(sys.argv) != 8:
    print('Use: '+sys.argv[0]+' pack_sz nbytes timeout loss fileout host port')
    sys.exit(1)

s = jsockets.socket_udp_connect(sys.argv[6], sys.argv[7])

if s is None:
    print('could not open socket')
    sys.exit(1)

# Esto es para dejar tiempo al server para conectar el socket
s.send(b'hola')
s.recv(1024)

fileout = open(sys.argv[5], 'wb')
stopAndWaitUDP(s, float(sys.argv[1]), float(
    sys.argv[2]), float(sys.argv[3]), sys.argv[4], fileout)

print("Message sent")
s.close()
fileout.close()
