#!/usr/bin/python3
# Echo client program
# Version con dos threads: uno lee de stdin hacia el socket y el otro al revés
import jsockets
import sys
import threading
import time
import auxiliary as aux


def stopAndWaitUDP(s, pack_sz, nbytes, timeout, loss, fileout):
    print("Starting UDP")

    print(aux.loss_rate)
    aux.loss_rate = float(loss)
    print(aux.loss_rate)

    s_msg, en_msg = aux.encode_package_time(pack_sz, timeout)

    s.send(en_msg)
    print("propuse paquete:", s_msg)
    act_pack_sz = s.recv(10).decode('utf-8')
    print("recibo paquete:", act_pack_sz[1:])
    s.send(bytearray("N" + str(nbytes), encoding='utf-8'))
    print("recibiendo", nbytes, "nbytes")

    # Recepcion de paquetes
    total_bytes, errores, start, end = aux.pack_rec(
        s, fileout, int(act_pack_sz[1:]))

    print("bytes recibidos =", total_bytes, ", time =", end-start,
          " , bw = ", total_bytes/((end-start)*1024*1024), " , errores = ", errores)


# Program start: asking for parameters and creating a link
if len(sys.argv) != 8:
    print('Use: '+sys.argv[0]+' pack_sz nbytes timeout loss fileout host port')
    sys.exit(1)

s = jsockets.socket_udp_connect(sys.argv[6], sys.argv[7])


if s is None:
    print('could not open socket')
    sys.exit(1)


fileout = open(sys.argv[5], 'wb')


stopAndWaitUDP(s, int(sys.argv[1]), int(
    sys.argv[2]), int(sys.argv[3]), sys.argv[4], fileout)

print("Message sent")
s.close()
fileout.close()
