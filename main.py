from ielts_tools import WordTrainer


if __name__ == "__main__":
    # Training based on UK accent
    UK_Trainer = WordTrainer(1)
    # Choose the test mode
    # 0 -- Dictation mode
    # 1 -- Reading test mode [i.e. training by typing the correct meaning of the word]
    mode = input('Would you like a dictation or a reading-test?\n[Type 0 for the former and 1 for the latter]\n> ')
    mode = eval(mode)
    print('OK! Now please set the batch size u\'d like to take: ')
    batch_size = eval(input('> '))
    # Start the test here
    if mode == 0:
        UK_Trainer.dic_test(batch_size)
    elif mode == 1:
        UK_Trainer.unknow_test(batch_size)
    else:
        # When type an unexpected mode, log the information
        print("There's something wrong in the mode settings")