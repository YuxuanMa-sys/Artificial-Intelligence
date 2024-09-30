'''
This is the module you'll submit to the autograder.

There are several function definitions, here, that raise RuntimeErrors.  You should replace
each "raise RuntimeError" line with a line that performs the function specified in the
function's docstring.
'''

import numpy as np

def joint_distribution_of_word_counts(texts, word0, word1):
    '''
    Parameters:
    texts (list of lists) - a list of texts; each text is a list of words
    word0 (str) - the first word to count
    word1 (str) - the second word to count

    Output:
    Pjoint (numpy array) - Pjoint[m,n] = P(X1=m,X2=n), where
      X0 is the number of times that word1 occurs in a given text,
      X1 is the number of times that word2 occurs in the same text.
    '''
    
    a = []
    Pjoint = []
    X0 = []
    X1 = []
    
    for l in texts:
        x0 = 0
        x1 = 0
       
        for ele in l:
            if ele == word0:
                x0 += 1
                
            if ele == word1:
                x1 += 1
                
                
        a.append([x0, x1])
        X0.append(x0)
        X1.append(x1)
        
    b0 = max(X0) + 1
    b1 = max(X1) + 1
    
    for m in range(b0):
        P = []
        for n in range(b1):
            count = 0
            for counts in a:
                if counts == [m, n]:
                    count += 1
                    
            P.append(count/len(texts))
        Pjoint.append(P)
        
    Pjoint = np.array(Pjoint)
    return Pjoint
    
    

def marginal_distribution_of_word_counts(Pjoint, index):
    '''
    Parameters:
    Pjoint (numpy array) - Pjoint[m,n] = P(X0=m,X1=n), where
      X0 is the number of times that word1 occurs in a given text,
      X1 is the number of times that word2 occurs in the same text.
    index (0 or 1) - which variable to retain (marginalize the other) 

    Output:
    Pmarginal (numpy array) - Pmarginal[x] = P(X=x), where
      if index==0, then X is X0
      if index==1, then X is X1
    '''
    X0 = np.sum(Pjoint, axis = 1)
    X1 = np.sum(Pjoint, axis = 0)
    if index == 0:
        Pmarginal = X0
    elif index == 1:
        Pmarginal = X1
    
    return Pmarginal
    
def conditional_distribution_of_word_counts(Pjoint, Pmarginal):
    '''
    Parameters:
    Pjoint (numpy array) - Pjoint[m,n] = P(X0=m,X1=n), where
      X0 is the number of times that word0 occurs in a given text,
      X1 is the number of times that word1 occurs in the same text.
    Pmarginal (numpy array) - Pmarginal[m] = P(X0=m)

    Outputs: 
    Pcond (numpy array) - Pcond[m,n] = P(X1=n|X0=m)
    '''
    Pcond = []
    np.seterr(invalid='ignore')
    for i in range(len(Pmarginal)):
        Pcond.append(np.divide(Pjoint[i], Pmarginal[i]))
    Pcond = np.array(Pcond)
    return Pcond

def mean_from_distribution(P):
    '''
    Parameters:
    P (numpy array) - P[n] = P(X=n)
    
    Outputs:
    mu (float) - the mean of X
    '''
    mu = 0
    for i in range(len(P)):
        mu += i * P[i]
    return mu

def variance_from_distribution(P):
    '''
    Parameters:
    P (numpy array) - P[n] = P(X=n)
    
    Outputs:
    var (float) - the variance of X
    '''
    mu_sq = 0
    mu = 0
    for i in range(len(P)):
        mu += i * P[i]
    for i in range(len(P)):
        mu_sq += i * i * P[i]
    var = mu_sq - mu*mu
    return var

def covariance_from_distribution(P):
    '''
    Parameters:
    P (numpy array) - P[m,n] = P(X0=m,X1=n)
    
    Outputs:
    covar (float) - the covariance of X0 and X1
    '''
    mu_x0 = 0
    mu_x1 = 0
    x0 = np.sum(P, axis = 1)
    x1 = np.sum(P, axis = 0)
    for i in range(len(x0)):
        mu_x0 += i * x0[i]
        
    for j in range(len(x1)):
        mu_x1 += j * x1[j]
    E = 0
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            E += i * j * P[i, j]
    covar = E - (mu_x0 * mu_x1)      
    return covar

def expectation_of_a_function(P, f):
    '''
    Parameters:
    P (numpy array) - joint distribution, P[m,n] = P(X0=m,X1=n)
    f (function) - f should be a function that takes two
       real-valued inputs, x0 and x1.  The output, z=f(x0,x1),
       must be a real number for all values of (x0,x1)
       such that P(X0=x0,X1=x1) is nonzero.

    Output:
    expected (float) - the expected value, E[f(X0,X1)]
    '''
    expected = 0
    
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            expected += f(i, j) * P[i, j]
    return expected
    
