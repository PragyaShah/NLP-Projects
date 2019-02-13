f_train = open('../data/train', 'r')
for line in f_train:
    line = list(line.strip().split(' '))
    for word in line:
        print (word)
        a=raw_input()
