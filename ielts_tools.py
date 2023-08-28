import os
import urllib.request
import urllib.parse
import json
import random
from playsound import playsound, PlaysoundException


'''

@Author: Chris Chen

@Contact: chrischanyedu@gmail.com

@breif: A tool to help excersise for IELTS Exam by dictation and read-training

@release-date: version 1.0 at 8/25/2023

@update-info: version 1.1 at 8/26/2023

'''
class WordTrainer():
    def __init__(self, type=1, word='hellow'):
        '''
        Initialize the trainer for some parameters.
        
        --------------------------------------------
        self._type
        --------------------------------------------
        0: American Accent
        1: England Accent
        --------------------------------------------
        
        --------------------------------------------
        self._word
        --------------------------------------------
        It can be initialized as anything u like.
        It's just a channel used inside of this class.
        --------------------------------------------
        
        --------------------------------------------
        self.dic
        --------------------------------------------
        It will be initialize by reading the dictation_list.txt
        It mainly used for storing the words needed in dictation.
        --------------------------------------------
        
        --------------------------------------------
        self.unknow_dic
        --------------------------------------------
        It will be initialize by reading the read_list.txt
        It mainly used for storing the words needed in reading-test.
        --------------------------------------------
        
        --------------------------------------------
        self.all_meanings
        --------------------------------------------
        It will be initialize by reading the meanings.txt
        It mainly used for storing the meanings of all the words.
        --------------------------------------------
        
        '''
        # Lowercase the word
        word = word.lower()
        # Accent type
        self._type = type 
        self._word = word
        # dictation words dictionary
        self.dic = {}
        # unfamiliar words dictionary
        self.unknow_dic = {}
        
        # Read words from local txt files
        file = open('dictation_list.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            if line == "":
                break
            self.dic[line] = ""
        file.close()
        file = open('read_list.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            if line == "":
                break
            self.unknow_dic[line] = ""
        file.close()
        
        # root path of the file
        self._dirRoot = os.path.dirname(os.path.abspath(__file__))
        if 0 == self._type:
            # The filepath of the US Accent audios
            self._dirSpeech = os.path.join(self._dirRoot, './audios/US') 
        else:
            # The filepath of the UK Accent audios
            self._dirSpeech = os.path.join(self._dirRoot, './audios/UK')  

        # See is there a specified path for US audios
        if not os.path.exists('./audios/US'):
            # Creat while not
            os.makedirs('./audios/US')
        # See is there a specified path for UK audios
        if not os.path.exists('./audios/UK'):
            # Creat while not
            os.makedirs('./audios/UK')
            
        # Store the meanings of all the words
        self.all_meanings = {}
        # Check whether the meaning of it has already existed
        file = open('meanings.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            if line=="":
                break
            # Get the meaning via intercepting
            pos = line.find('|')
            cur_word = line[:pos]
            self.all_meanings[cur_word] = line[pos+1:]
        file.close()
        
        # Fill the dictionary
        for key in self.dic.keys():
            if key not in self.all_meanings.keys():
                self.getInfo(key)
            else:
                self.dic[key] = self.all_meanings[key]
            self.down(key)
        # Fill the dictionary
        for key in self.unknow_dic.keys():
            if key not in self.all_meanings.keys():
                self.getInfo(key, 1)
            else:
                self.unknow_dic[key] = self.all_meanings[key]
    
    # u can call this function to set accent at anytime
    def setAccent(self, type=0):
        '''
        type = 0：American Accent
        type = 1：England Accent
        '''
        # Accent Type
        self._type = type  

        if 0 == self._type:
            # The filepath of the US Accent audios
            self._dirSpeech = os.path.join(self._dirRoot, './audios/US')  
        else:
            # The filepath of the UK Accent audios
            self._dirSpeech = os.path.join(self._dirRoot, './audios/UK') 

    def getAccent(self):
        '''
        type = 0：American Accent
        type = 1：England Accent
        '''
        return self._type

    def down(self, word, print_=False):
        '''
        Download the corresponding audio file(typed .mp3) while there isn't
        an existed one.
        
        print_
        --------------------------------------------
        True: print every download infomation
        False: print nothing
        --------------------------------------------
        '''
        # lowercase the word to make sure the url is legal
        word = word.lower()
        tmp = self._getWordMp3FilePath(word)
        if tmp is None:
            # Combine the url
            self._getURL()  
            # Call the download programm
            urllib.request.urlretrieve(self._url, filename=self._filePath)
            if(print_):
                print('%s.mp3 has already downloaded.' % self._word)
        else:
            if(print_):
                print('There is already a %s.mp3.' % self._word)

        # return the filepath of audio file
        return self._filePath
    
    # Download the meaning of the word
    def getInfo(self, word, memo_dic=0):   
            # Call the youdao API             
            request_url = 'http://dict.youdao.com/suggest?num=1&doctype=json&q='+word
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }
            request = urllib.request.Request(request_url, headers=headers)
            # send a request and get a response
            response = urllib.request.urlopen(request)
            # recieve a json string and decoded it by utf-8
            html = response.read().decode('utf-8')
            # turn the string to a dictionary and extract the meaning
            html = json.loads(html)
            # get the entire meaning by intercepting it through analysing
            meaning = ""
            if(len(html['data'])>0):
                for explains in html['data']['entries']:
                    meaning += explains['explain']+'|'
            else:
                # Can't find the meaning
                meaning = "Not Found."
            # add to dictionary
            if memo_dic == 0:
                self.dic[word] = meaning
            elif memo_dic == 1:
                self.unknow_dic[word] = meaning
            self.all_meanings[word] = meaning
            # add to meanings.txt
            if meaning != "Not Found.":
                file = open('meanings.txt', 'a')
                file.write(word+'|'+meaning+'\n')
                file.close()
    
    def showInfo(self, word):
        if word in self.all_meanings.keys():
            print(self.all_meanings[word].replace('|', '\n').strip())
        else:
            self.getInfo(word, 1)
            if self.all_meanings[word] != "Not Found.":
                # add to read_list.txt
                file = open('read_list.txt', 'a')
                file.write(word+'\n')
                file.close()
            print(self.all_meanings[word].replace('|', '\n').strip())
        
    def getDic(self):
        return self.dic
    
    # Have a test
    def test(self, batch=10, mode = 0, write_meanings=False):
        dic_length = len(self.dic if mode==0 else self.unknow_dic)
        mark = [False]*dic_length
        test_batch_len = dic_length if batch=='all' else min(dic_length, batch)
        test_list = []
        # Get all the words
        words = []
        for key in self.dic.keys() if mode==0 else self.unknow_dic.keys():
            words.append(key)
        # Generate a dictation list
        while(len(test_list)<test_batch_len):
            # Get an index first
            word_id = random.randint(0, dic_length-1)
            while(mark[word_id]):
                # Hash Random index
                word_id = 0 if word_id==dic_length-1 else word_id+1
            mark[word_id] = True
            test_list.append(words[word_id])
        # Start Test
        i = 1
        wrong_ans = []
        # initialize the mixer
        for dic_word in test_list:
            print('################################################################')
            print(str(i)+"/"+str(test_batch_len))
            right_word = self.dic[dic_word].replace('|', '\n').strip() if mode==0 else self.unknow_dic[dic_word].replace('|', '\n').strip()
            # Play the sound while dictation
            if mode==0:
                try:
                    playsound(r'.\\audios\\'+(r'US\\' if self._type==0 else r'UK\\')+dic_word+r'.mp3')
                    # Input answer
                    ans = input('> ')
                except PlaysoundException:
                    print("\033[31mThis audio can\'t play!\033[0m")
                    ans = dic_word.replace('+', ' ')
                print('\033[32mCorrect!\033[0m' if ans == dic_word.replace('+', ' ') else '\033[31mWrong Again!!!\033[0m')
            # Meaning test
            print('\033[35m'+dic_word.replace('+', ' ')+": "+'\033[0m')
            if write_meanings or mode!=0:
                input_meaning = input("What\'s the meaning of it?\n> ")
                print('\033[32mCorrect!\033[0m' if input_meaning in right_word else '\033[31mWrong Again!!!\033[0m')  
            print('Explain of it: ')
            print(right_word)
            # Check and Feedback
            judgement = ans != dic_word.replace('+', ' ') if mode==0 else input_meaning not in right_word
            if write_meanings:
                judgement = judgement or input_meaning not in right_word
            if judgement:
                wrong_ans.append(dic_word)
            # Check Whether go on
            ok = input('Go on?[y for go on] > ')
            while(ok!='y'):
                ok = input('Go on?[y for go on] > ')
            i+=1
        # Done!
        print("################################################################")
        print("Done!")
        # Compute the accuracy and review the wrong words
        print("################################################################")
        print("Acc: {:.2f}%".format(float(1-float(len(wrong_ans))/float(test_batch_len))*100))
        # review the wrong words
        # No one mistake here!
        if wrong_ans==[]:
            print('Perfect!!!')
        else:
            print('Now Let\'s review the wrong words here.')
        for j in range(len(wrong_ans)):
            print("################################################################")
            print(str(j+1)+"/"+str(len(wrong_ans)))
            print(wrong_ans[j].replace('+', ' '))
        
    def _getURL(self):
        '''
        Private function to generate the url of the word
        
        here's the prefix of the url:
        http://dict.youdao.com/dictvoice?type=0&audio=
        '''
        self._url = r'http://dict.youdao.com/dictvoice?type=' + str(
            self._type) + r'&audio=' + self._word

    def _getWordMp3FilePath(self, word):
        '''
        Get the local path of the audio file
        Return an absolute path while it exists and None while not
        '''
        # lowercase the word
        word = word.lower()
        self._word = word
        self._fileName = self._word + '.mp3'
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

        # See whether the file exists
        if os.path.exists(self._filePath):
            # It does exist
            return self._filePath
        else:
            # It doesn't exist
            return None
