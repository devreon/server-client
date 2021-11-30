import socket
import tqdm
import os
import pkgutil
import numpy as np
import math
import pandas as pd
import gspread
import json
from gspread_dataframe import set_with_dataframe

# device's IP address
SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
# create the server socket
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# accept connection if there is any
client_socket, address = s.accept()
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")
# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))





# close the client socket

client_socket.close()




def main():
    message = ""
    try:
        import function
    except ImportError as ex:
        message = "An import error"
        print(message)

    if (message == "An import error"):
        print('afafaafa')
    else:
        import function

        print('success')
        print(function.f(1, 2, 3))
        sa = gspread.service_account(filename='service_account.json')
        sh = sa.open("data")
        wks = sh.worksheet("list1")
        # print(wks.get_all_records())
        print(" ")
        dataframe = pd.DataFrame(wks.get_all_records())
        print(dataframe)
        # wks.update('A5','gajghnkoa')
        # x_start = int(wks.cell(2, 1).value)
        # x_change = int(wks.cell(2, 2).value)
        # x_end = int(wks.cell(2, 3).value)
        # y_start = int(wks.cell(2, 4).value)
        # y_change = int(wks.cell(2, 5).value)
        # y_end = int(wks.cell(2, 6).value)
        # t_start = int(wks.cell(2, 7).value)
        # t_change = int(wks.cell(2, 8).value)
        # t_end = int(wks.cell(2, 9).value)
        x_start = int(dataframe.iloc[0, 0])
        x_change = int(dataframe.iloc[0, 1])
        x_end = int(dataframe.iloc[0, 2])
        y_start = int(dataframe.iloc[0, 3])
        y_change = int(dataframe.iloc[0, 4])
        y_end = int(dataframe.iloc[0, 5])
        t_start = int(dataframe.iloc[0, 6])
        t_change = int(dataframe.iloc[0, 7])
        t_end = int(dataframe.iloc[0, 8])
        X_input = []
        Y_input = []
        T_input = []

        for i in np.arange(x_start, x_end + x_change, x_change):
            X_input.append(round(i, 5))
        for i in np.arange(y_start, y_end + y_change, y_change):
            Y_input.append(round(i, 5))
        for i in np.arange(t_start, t_end + t_change, t_change):
            T_input.append(round(i, 5))

        Z_input = np.zeros((len(X_input), len(Y_input)))
        function.calculate(X_input, Y_input, Z_input, 1)
        print(X_input)
        print(Y_input)
        Z=Z_input.transpose()
        print(Z)
        dataset = pd.DataFrame()
        dataset['x'] = X_input
        # print(dataset)

        datasety = pd.DataFrame()
        datasety['y'] = Y_input

        datasett = pd.DataFrame()
        datasett['t'] = T_input
        # print(datasety)
        wks = sh.worksheet("listx")
        set_with_dataframe(wks, dataset)
        wks = sh.worksheet("listy")
        set_with_dataframe(wks, datasety)
        wks = sh.worksheet("listt")
        set_with_dataframe(wks, datasett)

        datasetz = pd.DataFrame(Z)


        wks = sh.worksheet("listz")
        set_with_dataframe(wks, datasetz)




main()





os.remove('D:/projects/python/server-client/reciever/function.py')


# close the server socket
s.close()
