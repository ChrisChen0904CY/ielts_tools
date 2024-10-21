import os
import urllib.request
import urllib.parse
import json
import random
from playsound import playsound, PlaysoundException
import re
import utils
import numpy as np
from tqdm import tqdm

# Ignore the divide warning
np.seterr(divide='ignore',invalid='ignore')


# GEt the batch size of training
def batch_input():
    print('OK! Now please set the batch size u\'d like to take: ')
    batch_size = input('> ')
    batch_size = 'all' if batch_size=='all' else eval(batch_size)
    return batch_size

'''

@Author: Chris Chen

@Contact: chrischanyedu@gmail.com

@breif: A tool to help excersise for IELTS Exam by dictation and read-training

@release-date: version 1.0 at 8/25/2023

@update-info: version 1.1 at 8/26/2023

@update-info: version 2.0 at 8/29/2023

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
        # expression words dictionary
        self.expression_dic = {}
        # idioms words dictionary
        self.idioms_dic = {}
        
        # Read words from local txt files
        file = open('dictation_list.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            if line == "":
                break
            self.dic[line] = ""
        file.close()
        # read words
        file = open('read_list.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            if line == "":
                break
            self.unknow_dic[line] = ""
        file.close()
        # read expression
        express = set({})
        cor_words = {}
        file = open('expression.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            if line == "":
                break
            pos = line.find("|")
            s1 = line[:pos]
            s2 = line[pos+1:]
            cor_words[s1] = s2
            express.add(s2)
        file.close()
        # initialize expression_dic
        for key in express:
            self.expression_dic[key] = []
        for word in cor_words.keys():
            self.expression_dic[cor_words[word]].append(word)
        # idioms
        express = set({})
        cor_words = {}
        file = open('idioms.txt', 'r')
        for line in file.readlines():
            line = line.strip()
            if line == "":
                break
            pos = line.find("|")
            s1 = line[:pos]
            s2 = line[pos+1:]
            cor_words[s1] = s2
            express.add(s2)
        file.close()
        # initialize expression_dic
        for key in express:
            self.idioms_dic[key] = []
        for word in cor_words.keys():
            self.idioms_dic[cor_words[word]].append(word)
        
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
        print("本地词意加载中...")
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
        print("本地词意加载完毕.")
        # Fill the dictionary (loading dictation words)
        for key in tqdm(self.dic.keys(), desc="加载听写词汇"):
            if key not in self.all_meanings.keys():
                self.getInfo(key)
            else:
                self.dic[key] = self.all_meanings[key]
            self.down(key)

        # Fill the dictionary (loading unfamiliar words)
        for key in tqdm(self.unknow_dic.keys(), desc="加载阅读词汇"):
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
    
    def showInfo(self, word, add_dic=False):
        if word in self.all_meanings.keys():
            print(self.all_meanings[word].replace('|', '\n').strip())
        else:
            self.getInfo(word, 1)
            if self.all_meanings[word] != "Not Found.":
                # add to read_list.txt
                file = open('read_list.txt', 'a')
                file.write(word+'\n')
                file.close()
                if add_dic==True:
                    # add to dictation_list while needed
                    file = open('dictation_list.txt', 'a')
                    file.write(word+'\n')
                    file.close()
            print(self.all_meanings[word].replace('|', '\n').strip())
    
    def meaning_assert(self, input_words, meanings):
        # return true when the meaning can not be found
        if meanings=="Not Found.":
            return True
        # return false while you inpput nothing
        if input_words.strip()=="":
            return False
        # remain the main meaning
        meanings = re.sub(r"\(.*?\)|\{.*?\}|\[.*?\]|【.*?】|（.*?）|<.*?>", "", meanings)
        means = re.split(r"[，,:：；;、]|(?:或|或者)", meanings)
        res = False
        for mean in means:
            # Deal with "..." and "......"
            mean.replace('......', '什么')
            mean.replace('...', '什么')
            mean = re.sub('[a-zA-Z\d\.\s]','',mean.strip())
            if mean == "":
                continue
            # can't deal with words final with "的地得"
            if mean[-1]=="的" or mean[-1]=="地" or mean[-1]=="得":
                mean = mean[:-1]
            if utils.syn_judge(input_words, mean, utils.session, utils.vocab):
                res = True
                break
        return res
    
    def getDic(self):
        return self.dic
    
    # Have a test
    def test(self, batch=10, mode = 0, write_meanings=False):
        # Get the corresponding length of dic
        if mode==0:
            dic_length = len(self.dic)
        elif mode==1:
            dic_length = len(self.unknow_dic)
        elif mode==2:
            dic_length = len(self.expression_dic)
        elif mode==3:
            dic_length = len(self.idioms_dic)
        else:
            dic_length = batch
        mark = [False]*dic_length
        test_batch_len = dic_length if batch=='all' else min(dic_length, batch)
        test_list = []
        # Get all the words/expressions
        words = []
        if mode == 0 or mode == 1:
            for key in self.dic.keys() if mode==0 else self.unknow_dic.keys():
                words.append(key)
        elif mode == 2 or mode == 3:
            for key in self.expression_dic.keys() if mode==2 else self.idioms_dic.keys():
                words.append(key)
        # Generate a test list
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
        # start test
        for word in test_list:
            print('################################################################')
            print(str(i)+"/"+str(test_batch_len))
            # Play the sound while dictation
            if mode == 0 or mode == 1:
                right_word = self.dic[word].replace('|', '\n').strip() if mode==0 else self.unknow_dic[word].replace('|', '\n').strip()
                if mode==0:
                    try:
                        playsound(r'.\\audios\\'+(r'US\\' if self._type==0 else r'UK\\')+word+r'.mp3')
                        # Input answer
                        ans = input('> ')
                    except PlaysoundException:
                        print("\033[31mThis audio can\'t play!\033[0m")
                        ans = word.replace('+', ' ')
                    print('\033[32mCorrect!\033[0m' if ans == word.replace('+', ' ') else '\033[31mWrong Again!!!\033[0m')
                # Meaning test
                print('\033[35m'+word.replace('+', ' ')+": "+'\033[0m')
                if write_meanings or mode!=0:
                    input_meaning = input("What\'s the meaning of it?\n> ")
                    # deal with words final with 的地得
                    if input_meaning!="":
                        if input_meaning[-1]=="的" or input_meaning[-1]=="地" or input_meaning[-1]=="得":
                            input_meaning=input_meaning[:-1]
                    # Meaning Assert
                    print('\033[32mCorrect!\033[0m' if self.meaning_assert(input_meaning, right_word)==True else '\033[31mWrong Again!!!\033[0m')  
                # Output the meaning
                print('Explain of it: ')
                print(right_word)
                # Check and Feedback
                judgement = ans != word.replace('+', ' ') if mode==0 else self.meaning_assert(input_meaning, right_word)==False
                if write_meanings:
                    judgement = judgement or self.meaning_assert(input_meaning, right_word)==False
                if judgement:
                    wrong_ans.append(word)
                # Check Whether go on
                ok = input('Go on?[y for go on] > ')
                while(ok!='y'):
                    ok = input('Go on?[y for go on] > ')
                i+=1
            elif mode==2 or mode==3:
                right_word_list = self.expression_dic[word] if mode==2 else self.idioms_dic[word]
                print("Please type words to express \'"+word+"\' as more as possible.")
                print("[Tips. Splitted by \',\']")
                s = input('> ')
                input_words = s.split(',')
                # Judgement
                for input_word in input_words:
                    input_word = input_word.strip()
                    if input_word not in right_word_list:
                        print('################################################################')
                        print("The word \033[31m"+input_word+"\033[0m is not recommended here.")
                # View the recommended words
                print('################################################################')
                if input('View the recommended word?\n[Type y to confirm]> ')=='y':
                    k = 1
                    for s in right_word_list:
                        print("\033[32m"+str(k)+". "+s+"\033[0m")
                        k += 1
                # epoch+1
                i += 1
        
        # Rivew of Errors
        if mode==0 or mode==1:
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
                # Ask wheter need a immediate training
                review = input('Re-test now?[Type \'y\' to confirm.]> ')
                if review=='y':
                    i = 1
                    # start re-test
                    for word in wrong_ans:
                        print('################################################################')
                        print(str(i)+"/"+str(len(wrong_ans)))
                        i += 1
                        # Play the sound while dictation
                        right_word = self.dic[word].replace('|', '\n').strip() if mode==0 else self.unknow_dic[word].replace('|', '\n').strip()
                        if mode==0:
                            try:
                                playsound(r'.\\audios\\'+(r'US\\' if self._type==0 else r'UK\\')+word+r'.mp3')
                                # Input answer
                                ans = input('> ')
                            except PlaysoundException:
                                print("\033[31mThis audio can\'t play!\033[0m")
                                ans = word.replace('+', ' ')
                            print('\033[32mCorrect!\033[0m' if ans == word.replace('+', ' ') else '\033[31mWrong Again!!!\033[0m')
                        # Meaning test
                        print('\033[35m'+word.replace('+', ' ')+": "+'\033[0m')
                        if write_meanings or mode!=0:
                            input_meaning = input("What\'s the meaning of it?\n> ")
                            # deal with words final with 的地得
                            if input_meaning!="":
                                if input_meaning[-1]=="的" or input_meaning[-1]=="地" or input_meaning[-1]=="得":
                                    input_meaning=input_meaning[:-1]
                            # Meaning Assert
                            print('\033[32mCorrect!\033[0m' if self.meaning_assert(input_meaning, right_word)==True else '\033[31mWrong Again!!!\033[0m')  
                        # Output the meaning
                        print('Explain of it: ')
                        print(right_word)
                else:
                    for j in range(len(wrong_ans)):
                        print("################################################################")
                        print(str(j+1)+"/"+str(len(wrong_ans)))
                        print(wrong_ans[j].replace('+', ' '))
                
        elif mode==2:
            # Done!
            print("################################################################")
            print("Done!")
    
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
        
    def copy_info(self, info, target=0):
        names = ['./dictation_list.txt', './read_list.txt',
                 './expression.txt', './idioms.txt']
        file = open(names[target], 'a')
        infos = info.split('\n')
        for x in infos:
            if x != "":
                word = x[x.find('.')+1:x.rfind(' ')]
                meaning = x[x.rfind(' ')+1:].strip('。')
                file.write(word+'|'+meaning+'\n')
        file.close()
        
    def easilyUse(self):
        # Choose the test mode
        # 0 -- Dictation mode
        # 1 -- Reading test mode [i.e. training by typing the correct meaning of the word]
        # Successfully loaded the model
        print("################################################################")
        print('Model loaded Successfully!')
        print("################################################################")
        print('Welcome to IELTS Study!')
        print("################################################################")
        # Main Process
        mode = input('How can I help u?\n[Type /h or help for more details]\n> ')
        while mode!='exit':
            # Start the test here
            # Listening Test
            if mode == '0' or 'dic' in mode or mode == "/d":
                batch_size = batch_input()
                meaning_write = input('Would u like to write down the meanings as an extra exercise?\n[Type y to confirm]> ')
                self.test(batch_size, 0, meaning_write=='y')
            # Reading Test
            elif mode == '1' or 'read' in mode or mode == "/r":
                batch_size = batch_input()
                self.test(batch_size, 1)
            # Words Require
            elif mode == '2' or 'search' in mode or mode == "/s":
                req_word = input('> ').replace(" ", "+")
                while req_word != "exit":
                    # Whether need to be added into dictation list
                    add_dic = input('Add to dictation list?\n[Type y to confirm]> ')
                    self.showInfo(req_word, add_dic=='y')
                    req_word = input('> ').replace(" ", "+")
            # Writing Test
            elif mode == '3' or 'write' in mode or mode == "/w":
                batch_size = batch_input()
                self.test(batch_size, 2)
            # Speaking Test
            elif mode == '4' or 'speak' in mode or mode == "/sp":
                batch_size = batch_input()
                self.test(batch_size, 3)
            # Word(s) Adding
            elif mode == '5' or 'add' in mode  or mode == "/a":
                add_list = input('Which list will the word send to?\
                                 \n0 ----> dictation list\
                                 \n1 ----> reading list\
                                 \n2 ----> writing list\
                                 \n3 ----> idioms list\
                                 \nothers ----> return to main process\
                                 \n> ')
                # Listening|Reading
                if add_list == '0' or add_list == '1':
                    list_txt = 'dictation_list' if add_list == '0' else 'read_list'
                    meaning = input('Input the word here.\n> ')
                    while meaning != 'exit':
                        file = open(list_txt+'.txt', 'a')
                        file.write(meaning.strip()+'\n')
                        file.close()
                        meaning = input('Input the word here.\n> ')
                # Writing|Speaking
                elif add_list == '2' or add_list == '3':
                    list_txt = 'expression' if add_list == '2' else 'idioms'
                    meaning = input('Input the expression here.\n> ')
                    while meaning != 'exit':
                        if meaning.strip()=='':
                            meaning = input('Input the expression here.\n> ')
                            continue
                        add_words = input('Input the word(s) you want to add.\n[Splitted by \',\']\n> ').split(',')
                        file = open(list_txt+'.txt', 'a')
                        for add_word in add_words:
                            file.write(add_word.strip()+'|'+meaning.strip()+'\n')
                        file.close()
                        meaning = input('Input the expression here.\n> ')
            # Commands List    
            elif mode == '/h' or mode == 'help':
                print("################################################################")
                print("Here are all the valid commands: ")
                print("\'0\' or words contained \'dic\' or /d ----> Have a dictation")
                print("\'1\' or words contained \'read\' or /r ----> Have a reading-test")
                print("\'2\' or words contained \'search\' or /s ----> Require details for a specific word")
                print("\'3\' or words contained \'write\' or /w ----> Have a express test")
                print("\'4\' or words contained \'speak\' or /sp ----> Have a idioms test")
                print("\'5\' or words contained \'add\' or /a ----> Add a word to respective list")
                print("\'exit\' for quit this program")
            else:
                # When type an unexpected mode, log the information
                print("I'm not clear about your command.")
            # New Epoch Here
            print("################################################################")
            mode = input('How can I help u?\n[Type /h or help for more details]\n> ')
