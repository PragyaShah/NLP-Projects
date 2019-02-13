import math, collections

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.trigramCounts = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: 0)))
    self.bigramCounts = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datum in sentence.data:
        token = datum.word
        self.unigramCounts[token] = self.unigramCounts[token] + 1
        self.total += 1

    for sentence in corpus.corpus:
        token0 = 'word before 1st word'
        for datum in sentence.data:
            token1 = datum.word
            if token0 != 'word before 1st word':
                self.bigramCounts[token0][token1] = self.bigramCounts[token0][token1] + 1
            token0 = token1

    for sentence in corpus.corpus:
        token0 = 'word 2 place before 1st word'
        token1 = 'word before 1st word'
        for datum in sentence.data:
            token2 = datum.word
            if token0 != 'word before 1st word' and token0 != 'word 2 place before 1st word':
                self.trigramCounts[token0][token1][token2] = self.trigramCounts[token0][token1][token2] + 1
            token0 = token1
            token1 = token2


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    t0 = ''
    t1 = ''
    score = 0.0
    flag = 0
    for token in sentence:
        t2 = token
        if flag is 0:
            count = self.unigramCounts[token]
            x = (count + 1)*1.0 / (self.total)
            flag =1
        elif flag is 1:
            tot = self.unigramCounts[t1]
            count = self.bigramCounts[t1][t2]
            x = (count + 1)*1.0 / (tot)
            flag = 2
        elif self.trigramCounts[t0][t1][t2] is not 0:
            tot = self.bigramCounts[t0][t1]
            count = self.trigramCounts[t0][t1][t2]
            x = (count + 1)*1.0 / (tot)
            flag = 2
        elif self.bigramCounts[t1][t2] is not 0:
            tot = self.unigramCounts[t1]
            count = self.bigramCounts[t1][t2]
            x = (count + 1)*1.0 / (tot)
            flag = 2
        elif self.unigramCounts[token] is not 0:
            count = self.unigramCounts[token]
            x = (count)*1.0/ (self.total)
        else:
            count = self.unigramCounts[token]
            x = (count + 1)*1.0/ (self.total + len(self.unigramCounts))
        t0 = t1
        t1 = t2
        score += math.log(x)

    return score
