import socket
import config
import time
import random
import urllib.request
import json

class Utils:
    ''' class  '''
    #answer anout 8magic ball
    pstv_anws = ('Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да', 'Можешь быть уверен в этом')
    ind_pstv_anws = ('Мне кажется — «да»', 'Вероятнее всего', 'Хорошие перспективы', 'Знаки говорят — «да»', 'Да')
    ntrl = ('Пока не ясно, попробуй снова', 'Спроси позже', 'Лучше не рассказывать', 'Сейчас нельзя предсказать', 'Сконцентрируйся и спроси опять')
    ngtv = ('Даже не думай', 'Мой ответ — «нет»', 'По моим данным — «нет»', 'Перспективы не очень хорошие', 'Весьма сомнительно')
    magic_answ = {'Positive':pstv_anws, 'Hesitantly':ind_pstv_anws, 'Negative':ngtv, 'Neutral':ntrl}
    
    #answer.
    lovely_answ = ('И я тебя KappaPride', 'А ты мне не нравишься DansGame ')
    
    oplist = {}
    
    def __init__(self, sock, chan, startTime):
        ''' Creater class utils and associate socket, name of channel and working time bot'''
        
        self.chan = chan
        self.sock = sock
        self.startTime = startTime
        random.seed()
    
    def mess(self,message):
        """ Send message on channel """
        self.sock.send("PRIVMSG #{} :{}\r\n".format(self.chan, message).encode("utf-8"))

    def currentTime(self):
        """ Return current time"""
        str_time = time.gmtime()
        self.mess('@'+self.user+" Текущее время по СЕТ "+str(str_time.tm_hour+1)+'h '+str(str_time.tm_min)
             +'m '+str(str_time.tm_sec)+'s')

    def ban(self,user):
        """ Ban user in chat """
        self.mess(".ban {}".format(user))
        
    def timeout(self, user, seconds = 500):
        """ Timeout user on chat on default 500 sec """
        self.mess(".timeout {}".format(user, seconds))

    def time(self):
        """ Return how much working stream """
        
        current_time = time.time()
        working_time = current_time - self.startTime
        hours = round (working_time/3600, 0)
        working_time -= 3600*hours
        minutes = round (working_time/60, 0)
        working_time -= 60*minutes
        self.mess('Стрим идет '+str(hours)+'h '+str(minutes)+'m '+str(round(working_time,2))+'s')

    def magic8ball(self):
        """ Return message this answer on chat about user question """
        
        keys = tuple(self.magic_answ.keys())
        answGp = random.randint(0,3)
        answ = random.randint(0,4)
        message = self.magic_answ[keys[answGp]][answ]
        self.mess('@'+self.user+' '+message)

    def lovely (self):
        """ Return answer about lovely"""
        answGp = random.randint(0,1)# random answer about question
        self.mess(self.lovely_answ[answGp])

    def plus(self):
        """ answer people + """
        self.mess('+')

    def countOnline(self):
        """ Return message on chat about who much people watch channel """
        self.mess('@'+self.user+' В чатике сейчас '+str(self.chatter_count) + ' непорабощенных душ PogChamp')
    
    def sayHi(self):
        self.mess('@'+self.user+' Привет привет Kappa')

    def sayBye(self):
        self.mess('@'+self.user+' Досвидули Kappa')
        
    def listCommand(self, commands):
        """Return result about working commands for jar bot """
        cmd = tuple(commands.keys())
        str1 = '@'+self.user+' Доcтупные команды бота на текущий момент : '
        for i in cmd:
            str1 += str(i)
            str1 += ', '
            
        self.mess(str1)
        

    def mySize(self):
        """ Return message on chat size about breast - 0 or dick - 1 :) """
        
        about = random.randint(0,1)
        if about : 
            size = random.randint(0,1) + random.gauss(2,1)
            self.mess('@'+self.user+' Твой размер груди ' + str(int(size)) + ' Kappa')
        else :
            size = random.randint(0,20) + random.gauss(5,2.5)
            self.mess('@'+self.user+' Твой размер шланга ' + str(round(size, 2)) + ' KappaPride')
 

    def fillOpList(self):
        ''' List about user on channel and law groups people  '''
        try:
            url = "http://tmi.twitch.tv/group/user/"+self.chan+'/chatters'
            req = urllib.request.Request(url, headers={"accept": "*/*"})
            res = urllib.request.urlopen(req).read()
            self.oplist.clear()
            data = json.loads(res.decode('utf-8'))
            #print(data)
            self.chatter_count = data['chatter_count']
            for p in data["chatters"]["moderators"]:
                self.oplist[p] = "mod"
            for p in data["chatters"]["global_mods"]:
                self.oplist[p] = "global_mod"
            for p in data["chatters"]["admins"]:
                self.oplist[p] = "admin"
            for p in data["chatters"]["staff"]:
                self.oplist[p] = "staff"
        except:
            print('something error in gets information law list')
             
    def isOp(user):
        '''Return existence someone user on connect chat'''
        return user in self.oplist
        
