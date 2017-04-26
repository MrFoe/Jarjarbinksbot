import config #config bot (name bot's channel, token, etc.)
from utils import Utils #function bot
import socket
import re
import time
import threading
from time import sleep

HOST = "irc.twitch.tv" #standart protocol for connect twitch
PORT = 6667 # standatr port for connect to twitch
CHAN = "" #input name channel 
        
def main():

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(CHAN).encode("utf-8"))

    commands = {'бот время':'u.time()',
                'бот текущее время':'u.currentTime()',
                '+':'u.plus()',
                'бот люблю тебя': 'u.lovely()',
                'бот онлайн': 'u.countOnline()',
                'бот привет': 'u.sayHi()',
                'бот пока': 'u.sayBye()',
                'бот размер': 'u.mySize()',
                'бот команды': 'u.listCommand(commands)'}
    #smiles = []
    start_time = time.time()
    
    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    u = Utils(s, CHAN, start_time)
    u.mess("Джа Джа здеся и готов служить Kappa")# check message on channel
    work_bot = True #working bot's flag

    #Main cycle programm
    while True:
        try:
            response = s.recv(1024).decode("utf-8")
            
            if response == "PING :tmi.twitch.tv\r\n":
                s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
                
            else:
                #user = re.sub(r'^:\w+',response)
                #user = user[1:]
                #print(user)
                #u.setUser(user)
                message = chat_message.sub('',response)
                #print(response)
                if message.strip().lower() == 'бот умри' and work_bot and u.isOp(user):
                    u.mess("неееет, Джа Джа умеееееер! BibleThump BibleThump BibleThump")
                    work_bot = False
                    
                if message.strip().lower() in commands and work_bot:
                    exec(commands[message.strip().lower()])
                #
                if re.compile(r'^(бот стоит ли)').search(message.strip().lower()) and work_bot:
                    u.magic8ball()
                
                if message.strip().lower() == 'бот живи' and not work_bot and u.isOp(user):
                    u.mess("Джа Джа вернулся, чтобы поработить галактику! SMOrc SMOrc SMOrc")
                    work_bot = True
                u.fillOpList()#Update list user on chan
            
            sleep(1)
            
         except:   
            s.close()
        
if __name__ == "__main__":
    main()
