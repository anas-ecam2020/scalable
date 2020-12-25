import socket, json, pickle
from numpy import reshape
import time
import numpy as np
from PIL import Image as im 


HOST = '127.0.0.1' # Loopback interface address (localhost)
PORT = 65432


image_properties = {
    "xmin": -2.0,
    "xmax": 0.5,
    "ymin": -1.25,
    "ymax": 1.25,
    "nx": 1000,
    "ny": 1000,
    "maxiter": 50,
}



def receive_data():
    
    total_bytes = 2002284
    total_received = 0
    full_data = b''

    qty = 60000

    while total_received <= total_bytes:
        
        if 0 < (total_bytes - total_received) < 60000:
            remain = total_bytes - total_received
            received = s.recv(remain)
            #print('Received:', remain)
            full_data += received
            total_received += remain
            #print('Total received: ', total_received)
        else:
            data_to_receive = qty
            received = s.recv(data_to_receive)
            #print('Received:', data_to_receive)
            full_data += received
            #print('Total received: ', total_received)

            if received == 0:
                print('Connection broken')
    
            total_received += qty

        if total_received == total_bytes:
            print('All data received!')
    
    return full_data




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print('Connecting to server...')
    s.connect((HOST, PORT))
    print('Connected!')
    print('Sending data to server...')
    # data to send
    to_send = json.dumps(image_properties).encode('utf-8')
    s.sendall(to_send)
    print('Data sent to server!')
    print('Receiving data...')
    data = receive_data()
    result = pickle.loads(data)
    #print(result)
    #print('Type result :', type(result))
    s.close()

N = reshape(result, (image_properties["nx"], image_properties["ny"])) # change to rectangular array
print('Converting to image...')
data = im.fromarray((N*255).astype(np.uint16))
print('Saving image...')
data.save('mandelbrot.png') 
print('Image successfully saved!')

finish = time.perf_counter()
print(f'Finished running after seconds:', finish)