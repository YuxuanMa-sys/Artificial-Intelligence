'''
This is the module you'll submit to the autograder.

There are several function definitions, here, that raise RuntimeErrors.  You should replace
each "raise RuntimeError" line with a line that performs the function specified in the
function's docstring.
'''
import numpy as np

def k_nearest_neighbors(image, train_images, train_labels, k):
    '''
    Parameters:
    image - one image
    train_images - a list of N images
    train_labels - a list of N labels corresponding to the N images
    k - the number of neighbors to return

    Output:
    neighbors - 1-D array of k images, the k nearest neighbors of image
    labels - 1-D array of k labels corresponding to the k images
    '''
    

    distances = []
    neighbors = []
    labels = []
    for i in range(len(train_images)):
        distances.append(np.linalg.norm(image - train_images[i]))
        
    d_1 = distances.copy()
    d_1.sort()
    for j in range(k):
        ind = distances.index(d_1[j])
        neighbors.append(train_images[ind])
        labels.append(train_labels[ind])
        
    return np.array(neighbors), np.array(labels)


def classify_devset(dev_images, train_images, train_labels, k):
    '''
    Parameters:
    dev_images (list) -M images
    train_images (list) -N images
    train_labels (list) -N labels corresponding to the N images
    k (int) - the number of neighbors to use for each dev image

    Output:
    hypotheses (list) -one majority-vote labels for each of the M dev images
    scores (list) -number of nearest neighbors that voted for the majority class of each dev image
    '''
    hypotheses = []
    scores = []
    for i in range(len(dev_images)):
        neighbor, label = k_nearest_neighbors(dev_images[i], train_images, train_labels, k)
        hypothese = np.bincount(label).argmax()
        hypotheses.append(hypothese)
        scores.append(np.count_nonzero(label == hypothese))
        
    return hypotheses, scores


def confusion_matrix(hypotheses, references):
    '''
    Parameters:
    hypotheses (list) - a list of M labels output by the classifier
    references (list) - a list of the M correct labels

    Output:
    confusions (list of lists, or 2d array) - confusions[m][n] is 
    the number of times reference class m was classified as
    hypothesis class n.
    accuracy (float) - the computed accuracy
    f1(float) - the computed f1 score from the matrix
    '''

    confusions = np.zeros((2, 2))
    for m in range(len(hypotheses)):
        if references[m] == 0 and hypotheses[m] == 0:
            confusions[0][0] += 1

        elif references[m] == 0 and hypotheses[m] == 1:
            confusions[0][1] += 1
        elif references[m] == 1 and hypotheses[m] == 0:
            confusions[1][0] += 1
        elif references[m] == 1 and hypotheses[m] == 1:
            confusions[1][1] += 1
                
    accuracy = float((confusions[1][1] + confusions[0][0])/(confusions[0][0] + confusions[0][1] + confusions[1][0] + confusions[1][1]))
    precision = float(confusions[1][1]/(confusions[1][1] + confusions[0][1]))
    recall = float(confusions[1][1]/(confusions[1][1] + confusions[1][0]))
    f1 = float(2/(1/precision + 1/recall))
    
    return confusions, accuracy, f1
