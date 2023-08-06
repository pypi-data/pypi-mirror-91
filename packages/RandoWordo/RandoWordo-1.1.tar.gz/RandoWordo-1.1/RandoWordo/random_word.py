from random import randint


def RandWord(file):
    try:
        with open(file, 'r') as Readfile:
            words = Readfile.readlines()
            

             
            return words[randint(0,len(words))].strip("\n")
    except:
        return "Invalid File"

def RandoWord():
    try:
        with open("20K.txt","r") as Reader:
            words = Reader.readline()
            return words[randint(0,len(words))].strip("\n")
    except:
        return "Something went wrong."