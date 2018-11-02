def read_question(nb):
    with open(f"../{nb}/questions.txt", 'r') as filehandler:
        data = filehandler.read()
    qdata = data.split()
    if qdata[0] == 'Voulez-vous':
        print('0')
        return 0
    elif qdata[0] == 'positions':
        print(data[data.find('{')+1:data.find('}')].split(', ')) 
        return 1, data[data.find('{')+1:data.find('}')].split(', ')
    else:
        print(data[data.find('[')+1:data.find(']')].split(', '))
        return 2, data[data.find('[')+1:data.find(']')].split(', ')        

if __name__=="__main__":
    read_question(3)
