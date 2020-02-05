from socket import AF_INET,SOCK_STREAM,socket
from threading import Thread
import tkinter


def receive():
    run = True
    try:
        while run:
            try:
                msg = client_socket.recv(message_limit).decode('utf8')
                msg_list.insert(tkinter.END,msg)
            except OSError :
                break
    except Exception as e :
        print(f'error {e}')


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg,'utf8'))
    if msg == '{quit}':
        client_socket.close();
        top.quit()


def on_closing(event=None):
    my_msg = set('{quit}')
    send()


top = tkinter.Tk()
top.title('Chatter')

message_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set('Type your message here.')
scrollbar = tkinter.Scrollbar(message_frame)


msg_list = tkinter.Listbox(message_frame,height=16,width=50,yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
msg_list.pack()


message_frame.pack()


entry_field = tkinter.Entry(top,textvariable=my_msg)
entry_field.bind("<Return>",send)
entry_field.pack()
send_button = tkinter.Button(top,text="Send",command=send)
send_button.pack()


top.protocol("WM_DELETE_WINDOW",on_closing)


HOST = input('Enter host : ')
PORT = input('Enter port : ')

if not PORT:
    PORT = 5512
else:
    PORT = int(PORT)


message_limit = 1024
address = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)


receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()