""" 
    Python2
    Michel Victor
"""

import threading
import socket
import logging

class UDP():

    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 8886))

    def correnction(self, ip, notebook):
        
        try:
            if notebook:
                note_torf = [line.split(';') for line in notebook.split('\n')]

            with open('gabarito', 'rb') as tamplat:
                templet_torf = [line.split(';') for line in tamplat.read().split('\n')]
            
            
            count, correction = 0 , ''
            question_id, alternatives_id, answers_id = 0,1,2

            for i in range(len(templet_torf)):
                if  note_torf[count][question_id] == templet_torf[i][question_id]:

                    hitss = [x for x in note_torf[count][answers_id]
                        if x in templet_torf[i][answers_id]]
                    
                    correction += "\n{};{};{} ".format(
                        note_torf[count][question_id],
                        len(hitss), 
                        int(note_torf[count][alternatives_id]) - len(hitss))

                    count += 1

            logging.info(correction)
            self.sock.sendto(correction,ip ) 
        except:
            self.sock.sendto(correction,ip ) 

    def listen_clients(self):
        while True:
            notebook, client = self.sock.recvfrom(1024)
            logging.info('Received data from client %s', client)
        
            t = threading.Thread(target=self.correnction, args=(client,notebook))
            t.start()

if __name__ == '__main__':
    # Make sure all log messages show up
    logging.getLogger().setLevel(logging.DEBUG)

    b = UDP()
    b.listen_clients()