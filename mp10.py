'''
This is the module you'll submit to the autograder.

There are several function definitions, here, that raise RuntimeErrors.  You should replace
each "raise RuntimeError" line with a line that performs the function specified in the
function's docstring.
'''
import numpy as np

epsilon = 1e-3

def compute_transition_matrix(model):
    '''
    Parameters:
    model - the MDP model returned by load_MDP()

    Output:
    P - An M x N x 4 x M x N numpy array. P[r, c, a, r', c'] is the probability that the agent will move from cell (r, c) to (r', c') if it takes action a, where a is 0 (left), 1 (up), 2 (right), or 3 (down).
    
    
    
    '''
    
    
    #raise RuntimeError("You need to write this part!")
    
    P = np.zeros((model.M, model.N, 4, model.M, model.N))
    
    for i in range(model.M):
        for j in range(model.N):
            for k in range(4):
                if model.T[i, j]:
                    P[i, j, k, :, :] = 0
                    continue
                
                if k == 0:
                    if j == 0 or model.W[i, j-1]:
                        P[i, j, k, i, j] += model.D[i, j, 0]
                    else:
                        P[i, j, k, i, j-1] += model.D[i, j, 0]
                   
                    if i + 1 == model.M or model.W[i + 1, j]:
                        P[i, j, k, i, j] += model.D[i, j, 1]
                    else:
                        P[i, j, k, i+1, j] += model.D[i, j, 1]
                 
                    if i == 0 or model.W[i-1, j]:
                        P[i, j, k, i, j] += model.D[i, j, 2]
                    else:
                        P[i, j, k, i-1, j] += model.D[i, j, 2]
                elif k == 1:
                    # up (i-1, j) with prob = model.D[i, j, 0]
                    if i == 0 or model.W[i-1, j]:
                        P[i, j, k, i, j] += model.D[i, j, 0]
                    else:
                        P[i, j, k, i-1, j] += model.D[i, j, 0]
                    
                    if j == 0 or model.W[i, j-1]:
                        P[i, j, k, i, j] += model.D[i, j, 1]
                    else:
                        P[i, j, k, i, j-1] += model.D[i, j, 1]
                    
                    if j + 1 == model.N or model.W[i, j+1]:
                        P[i, j, k, i, j] += model.D[i, j, 2]
                    else:
                        P[i, j, k, i, j+1] += model.D[i, j, 2]
                        
                elif k == 2:
                    
                    if j + 1 == model.N or model.W[i, j+1]:
                        P[i, j, k, i, j] += model.D[i, j, 0]
                    else:
                        P[i, j, k, i, j+1] += model.D[i, j, 0]
                    
                    if i == 0 or model.W[i-1, j]:
                        P[i, j, k, i, j] += model.D[i, j, 1]
                    else:
                        P[i, j, k, i-1, j] += model.D[i, j, 1]
                    
                    if i + 1 == model.M or model.W[i+1, j]:
                        P[i, j, k, i, j] += model.D[i, j, 2]
                    else:
                        P[i, j, k, i+1, j] += model.D[i, j, 2]
                else:
                   
                    if i + 1 == model.M or model.W[i+1, j]:
                        P[i, j, k, i, j] += model.D[i, j, 0]
                    else:
                        P[i, j, k, i+1, j] += model.D[i, j, 0]
                    
                    if j + 1 == model.N or model.W[i, j+1]:
                        P[i, j, k, i, j] += model.D[i, j, 1]
                    else:
                        P[i, j, k, i, j+1] += model.D[i, j, 1]
                    
                    if j == 0 or model.W[i, j-1]:
                        P[i, j, k, i, j] += model.D[i, j, 2]
                    else:
                        P[i, j, k, i, j-1] += model.D[i, j, 2]

    return P

def update_utility(model, P, U_current):
    '''
    Parameters:
    model - The MDP model returned by load_MDP()
    P - The precomputed transition matrix returned by compute_transition_matrix()
    U_current - The current utility function, which is an M x N array

    Output:
    U_next - The updated utility function, which is an M x N array
    '''
#     raise RuntimeError("You need to write this part!")

    U_next = np.zeros((model.M, model.N))
    for i in range(model.M):
        for j in range(model.N):
            a = [0, 0, 0, 0];
            for k in range(4):
                
                for b in range(model.M):
                    for c in range(model.N):
                        a[k] += P[i, j, k, b, c] * U_current[b, c]
                        
                
            U_next[i, j] = model.R[i, j] + model.gamma * max(a)
    return U_next

def value_iteration(model):
    '''
    Parameters:
    model - The MDP model returned by load_MDP()

    Output:
    U - The utility function, which is an M x N array
    '''
#     raise RuntimeError("You need to write this part!")
    U_current = np.zeros((model.M, model.N))
    while(True):
        U_next = update_utility(model, compute_transition_matrix(model), U_current)
        if np.max(np.abs(U_next - U_current)) < epsilon:
            break
    
        U_current = U_next
        
    return U_current
if __name__ == "__main__":
    import utils
    model = utils.load_MDP('models/small.json')
    model.visualize()
    U = value_iteration(model)
    model.visualize(U)
