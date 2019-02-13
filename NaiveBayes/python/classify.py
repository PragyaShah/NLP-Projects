import sys
import pprint

count_kd = {} # no of docs of speaker k
count_kw = {} # no of words of speaker k
count_k_w = {} # frequency of word w in overall docs of speaker k
docs = 0 # total no of docs
p_k = {}# prbability of speaker k
p_wgivenk = {}# probability of a word given it was spoken by speaker k
vocab = {}#a list of words present in the corpus

def training(train_path):
# k is the class name i.e. the speaker
    global docs
    f_train = open(train_path, 'r')
    for line in f_train:
        line = list(line.strip().split(' '))
        i=0#first word flag
        for word in line:
            if(i==0):#first word
                i=1
                k = word#the speaker
                docs+=1
                if (k in count_kd):
                    count_kd[k]+=1
                else:
                    count_kd[k] = 1
                    count_k_w[k] = {}
                    count_kw[k] = 0
                continue
            else:
                if(len(word)==1): #ommiting words of length 1, treating them as stop words
                    continue
                if (word not in vocab):
                    vocab[word]=1
                count_kw[k]+=1
                if(word in count_k_w[k]):
                    count_k_w[k][word]+=1
                else:
                    count_k_w[k][word] = 1
    f_train.close()

def compute_p():    
    for k in count_kd.keys():
        p_k[k] = count_kd[k]*1.0/docs
        p_wgivenk[k]={}
        for word in count_k_w[k].keys():
            p_wgivenk[k][word] = (count_k_w[k][word]+1)*1.0/(count_kw[k]+1+len(vocab))
        p_wgivenk[k]['xyz_word'] = 1.0/(count_kw[k]+1+len(vocab))

# remember : p(k) = count_kd[k]*1.0/docs
# remember : p(w/k) = (count_k_w[k][word]+1)*1.0/(count_kw[k]+v+1)...for smoothing
# remember : p(unknown_word/k) = 1.0/(count_kw[k]+v+1)...for smoothing


#the prnt variable specifies if the inner details like the p(k/d) for each speaker needs to be printed
def testsample(line,prnt):
    line = list(line.strip().split(' '))
    ans = ''
    #local dictionaries for this particular doc
    p_kd = {} #P(K,D)
    p_kgivend = {} #P(K/D)
    p_kd_sum = 0
    p_kgivend_sum = 0
    for k in count_kd.keys():
        p_kd[k] = p_k[k]
        i=0
        for word in line:
            if(i!=0):
                if(len(word)==1):#ommiting words of length 1, treating them as stop words
                    continue
                if (word in p_wgivenk[k]):
                    p_kd[k]*=p_wgivenk[k][word]*1000 #to prevent underflow
                else:
                    p_kd[k]*=p_wgivenk[k]['xyz_word']*1000 #to prevent underflow
            else:#first word
                i=1
                ans = word
                continue
        p_kd_sum+= p_kd[k]
    #p_kgivend['ans']=ans

        # finding the argmax of p(k/d) for all k
        maxpkd = 0.0
        estimate = ''
    for k in count_kd.keys():
        p_kgivend[k] = p_kd[k]/p_kd_sum
        if (maxpkd<p_kgivend[k]):
            maxpkd = p_kgivend[k]
            estimate = k
        if (prnt):
            print ("P("+k+"/D) = " + str(p_kgivend[k]))
           # print ("P("+k+"D) = " + str(p_kd[k]))
        p_kgivend_sum += p_kgivend[k]
    if (prnt):
        print ("sum of these probabilities = "+str(p_kgivend_sum))
    print ("Estimate :\t"+estimate+"\t\tAnswer :\t"+ans)
    if (estimate==ans):
        return(1)
    else:
        return(0)

def finaltest(test_path):
    f_test = open(test_path, 'r')
    score=0
    i=0
    for line in f_test:
        print i,
        score += testsample(line,0)
        i+=1
    accuracy = score*100.0/i
    print ("\n ACCURACY : "+str(accuracy)+"%")

def main(train_path, dev_path, test_path):

    print ("PART 1.a : ")
    #combining train and dev to form a larger corpus
    training(train_path)
    #print("vocab length : "+str(len(vocab)))
    training(dev_path)
    #print("vocab length : "+str(len(vocab)))
    
    print ("no of docs for clinton = "+(str)(count_kd['clinton']))
    print ("no of docs for trump = "+(str)(count_kd['trump']))
    print ("no of times word 'country' was used by clinton = "+(str)(count_k_w['clinton']['country']))
    print ("no of times word 'president' was used by clinton = "+(str)(count_k_w['clinton']['president']))
    print ("no of times word 'country' was used by trump = "+(str)(count_k_w['trump']['country']))
    print ("no of times word 'president' was used by trump = "+(str)(count_k_w['trump']['president']))

    #print("\nno of docs : "+str(docs))
    #print("no of docs of k : ")
    #pprint.pprint(count_kd)
    #print("total no of words of k : ")
    #pprint.pprint(count_kw)
    #print("frequency of word w in overall docs of trump : ")
    #pprint.pprint(count_k_w['trump'])
    

    print ("\nPART 1.b : ")
    compute_p()
    print ("Probability of clinton = "+(str)(p_k['clinton']))
    print ("Probability of trump = "+(str)(p_k['trump']))
    print ("Probability of word 'country' given the speaker is clinton = "+(str)(p_wgivenk['clinton']['country']))
    print ("Probability of word 'president' given the speaker is clinton = "+(str)(p_wgivenk['clinton']['president']))
    print ("Probability of word 'country' given the speaker is trump = "+(str)(p_wgivenk['trump']['country']))
    print ("Probability of word 'president' given the speaker is trump = "+(str)(p_wgivenk['trump']['president']))

    #print("probability of k : ")
    #pprint.pprint(p_k)
    #print("probability of w given trump : ")
    #pprint.pprint(p_wgivenk['trump'])

    print ("\nPART 1.c")
    f_dev = open(dev_path, 'r')
    i=0
    for line in f_dev:
        if (i==0):
            score = testsample(line,1)
        i+=1
    f_dev.close()

    print ("\nPART 1.d")
    finaltest(test_path)


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        main('../data/train', '../data/dev', '../data/test')
    elif (len(sys.argv) == 4):
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        print ('usage:\tClassify.py <train_file> <dev_file> <test_file>')
        sys.exit(0)
