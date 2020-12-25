from numpy import linspace
import socket
import json
import pickle



HOST = '127.0.0.1' # Loopback interface address (localhost)
PORT = 65432


def mandelbrot(z, maxiter): # computation for one pixel
  c = z
  for n in range(maxiter):
    #Dans le premier cas,  n'appartient pas à l'ensemble
    if abs(z)>2: return n  # divergence test
    #Dans le second, on considère que  appartient à l'ensemble
    z = z*z + c
  return maxiter

def main_loops(X, Y, maxiter):
# main loops
    N = []
    for y in Y:
        for x in X:
            z  = complex(x,y)
            N += [mandelbrot(z, maxiter)]
    return N

def send_result(bytes_to_send, length , conn):

    ok = False

    total_bytes = length
    total_sent = 0

    start = 0
    stop = 60000

    while total_sent < total_bytes:

        if 0 < (total_bytes - total_sent) < 60000:
            remain = total_bytes - total_sent
            lastval = stop + remain
            #print('lastval :', lastval)
            data_to_send = bytes_to_send[start:lastval]
            sent = conn.send(data_to_send)
            #print('Start value: ', start)
            #print('Last chunk sent!')
            total_sent += sent
            #print('Total sent: ', total_sent)
            #print('Total bytes:', total_bytes)

        else:
            data_to_send = bytes_to_send[start:stop]
            sent = conn.send(data_to_send)
            #print('Sent :', sent)
            #print('Data sent:', total_sent)
            #print('Remaining bytes: ', total_bytes - total_sent)
            #print('Start value: ', start)
        
            if sent == 0:
                print('Connection broken')
        
            start += sent
            stop += sent

            total_sent += sent

        if total_sent == total_bytes:
            ok = True

    return ok

running = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while running:
            print('Receiving image properties from client ...')
            data = conn.recv(60000)
            as_json_string = data.decode('utf-8')
            parameters = json.loads(as_json_string)
            print('Image properties received: ', parameters)
            X = linspace(parameters["xmin"], parameters["xmax"], parameters["nx"])
            Y = linspace(parameters["ymin"], parameters["ymax"], parameters["ny"])
            print('Calculating set...')
            raw_result = main_loops(X, Y, parameters["maxiter"])
            print('Converting to pickle...')
            result_as_pickle = pickle.dumps(raw_result)
            print('Sending back data to client...')
            result = send_result(result_as_pickle, len(result_as_pickle), conn)
            if result:
                print('Data has been sent to client!')
                print('Closing server...')
                conn.close()
                print('Server closed')
                break
            else:
                print('Failed to send data to client')
                print('Closing server...')
                conn.close()
                print('Server closed')
                break
            #if not data:
            #    break
            #print('Sending data to client...')
            #conn.sendall(data)
            #print('Data sent to client!')