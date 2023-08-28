from ielts_tools import WordTrainer


# GEt the batch size of training
def batch_input():
    print('OK! Now please set the batch size u\'d like to take: ')
    batch_size = input('> ')
    batch_size = 'all' if batch_size=='all' else eval(batch_size)
    return batch_size


if __name__ == "__main__":
    # Training based on UK accent
    UK_Trainer = WordTrainer(1)
    # Choose the test mode
    # 0 -- Dictation mode
    # 1 -- Reading test mode [i.e. training by typing the correct meaning of the word]
    print('Welcome to IELTS Study!')
    print("################################################################")
    mode = input('How can I help u?\n[Type h or help for more details]\n> ')
    while mode!='exit':
        # Start the test here
        if mode == '0' or 'dic' in mode:
            batch_size = batch_input()
            meaning_write = input('Would u like to write down the meanings as an extra exercise?\n[Type y to confirm]> ')
            UK_Trainer.test(batch_size, 0, meaning_write=='y')
        elif mode == '1' or 'read' in mode:
            batch_size = batch_input()
            UK_Trainer.test(batch_size, 1)
        elif mode == '2' or 'research' in mode:
            req_word = input('> ').replace(" ", "+")
            while req_word != "exit":
                UK_Trainer.showInfo(req_word)
                req_word = input('> ').replace(" ", "+")
        elif mode == 'h' or mode == 'help':
            print("################################################################")
            print("Here are all the valid commands: ")
            print("\'0\' or words contained \'dic\' ----> Have a dictation")
            print("\'1\' or words contained \'read\' ----> Have a reading-test")
            print("\'2\' or words contained \'research\' ----> Require details for a specific word")
            print("\'exit\' for quit this program")
        else:
            # When type an unexpected mode, log the information
            print("I'm not clear about your command.")
        # New Epoch Here
        print("################################################################")
        mode = input('How can I help u?\n[Type h or help for more details]\n> ')