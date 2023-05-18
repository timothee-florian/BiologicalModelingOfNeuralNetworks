# import Image
from copy import copy
from time import sleep
# from pylab import *
import numpy as np
import random as rand

class hopfield_network:
    def __init__(self,N,c=5,plot=False):
        
        """
        DEFINITION
        Initialization of the class

        INPUT
        N: size of the network
        c: Number of repeats every step (storage and recall)
        plot: Activate recall plots (True or False)
        """
        
        self.N = N
        self.c = c
        self.FLAG_plot = plot
    
    def make_pattern(self,P,ratio):
        
        """
        DEFINITION
        Creates and stores patterns

        INPUT
        P: number of patterns
        ratio: probability of a pixel being 1 instead of -1
        """

        self.pattern = -np.ones((P,self.N),int)
        idx = int(ratio*self.N)
        for i in range(P):
            for j in range(self.N):
                if rand.randint(0,1000) < ratio*1000:
                    self.pattern[i,j] = 1
                
        
        self.weight = np.zeros((self.N,self.N))
        self.distance_sum = 0
        self.recognition_success = 0
        self.recalls = 0
        self.update_count = 0
        
    def count_patterns(self):
        
        """
        DEFINITION
        Counts the number of patterns
        
        OUTPUT
        Number of patterns in the class
        """
        
        return len(self.pattern)

    def noise_pattern(self,mu,P_f):
        
        """
        DEFINITION
        Adds noise to patterns to recall

        INPUT
        mu: pattern stored in X, X is then noised by P_f ( Value between 0 and count_patterns()-1 )
        P_f: ratio of pixels whose value has been inverted
        """
        
        self.x = copy(self.pattern[mu])
        flip = np.random.permutation(np.arange(self.N))
        idx = int(self.N*P_f)
        self.x[flip[0:idx]] *= -1

    def update_weight(self,mu,decay):
        
        """
        DEFINITION
        Update of synaptic weights w_ij

        INPUT
        mu: For storage, a pattern mu is sent. Else if no mu is sent, the weights are updated according to the noised pattern X
        decay: Weight decay factor ranging from 0 - 1. 1 represents an equal memory over all time for all weight updates, and 0 represents no memory of previous storage.
        """
        
        self.weight = decay*self.weight
        C = 1./self.N
        
        if mu is not None: # Storage
            self.weight += C*np.multiply(self.pattern[mu][np.newaxis,:].T,self.pattern[mu])
        else: # Recall
            self.weight += C*np.multiply(self.x[np.newaxis,:].T,self.x)
            
        #Confidence and learning phase
        #np.fill_diagonal(self.weight, 0)
        #weight_sum = np.sum(np.abs(self.weight))
        #np.fill_diagonal(self.weight, 30*(np.exp(-1E-3*self.update_count)) + 0.15*weight_sum/self.N) # Means the algorithm needs to be at least 15% confident that the pixel needs to be inverted
        
        #Theory
        #The weights of the memory matrix represent the confidence for an Si should be the same (+) or the inverse (-) of Sj depending on previous knowledge. As such, a minimum confidence threshold can be required for a change to happen by modifying the diagonal, which diverges anyway for the given equation in the assignment. This threshold should be calculated using: (Threshold [0-1, 0 being not confident at all and 1 being absolutely ]) * (The total confidence (sum) of the row of the weights matrix for the Si term). Finally, the first term is added as confidence needs to be higher or mistakes can be made as the memory is just born.
        
        self.update_count += 1
    
    def update_state(self):
        
        """
        DEFINITION
        Network state update for each step of the recall with X
        """
        
        self.x = np.sign(np.dot(self.weight,self.x))

    def overlap(self,mu):
        
        """
        DEFINITION
        computes the overlap of the test pattern with pattern nb mu

        INPUT
        mu: the index of the pattern to compare with the test pattern
        """

        return 1./self.N*np.dot(self.pattern[mu],self.x)
    
    def grid(self,mu=None):
        
        """
        DEFINITION
        reshape an array of length N to a matrix MxM with M = sqrt((N-1)+1)

        INPUT
        mu: None -> reshape the test pattern x
            an integer i < P -> reshape pattern nb i
        """
        
        M = int(math.sqrt(self.N-1)+1) # MxM pixel image for visualization
        
        if mu is not None:
            graphic = zeros(M*M)
            graphic[0:self.N] = self.pattern[mu]
            x_grid = reshape(graphic,(M,M))
        else:
            graphic = zeros(M*M)
            graphic[0:self.N] = self.x
            x_grid = reshape(graphic,(M,M))
        return x_grid
    
    def hamming_distance(self, mu):
        
        """
        DEFINITION
        Computes the Hamming distance between patterns X and mu

        INPUT
        mu: the index of the pattern to compare with the test pattern
        """
        
        return 0.5*(1-self.overlap(mu))
    
    def recall(self,mu,P_f,decay):
        
        """
        DEFINITION
        runs the recall and plots the results (if FLAG_plot = True during initialisation)
        
        INPUT
        mu: pattern number to use as test pattern
        P_f: ratio of flipped pixels
                    ex. for pattern nb 5 with 5% flipped pixels use run(mu=5,P_f=0.05)
        """
        
        try:
            self.pattern[mu]
        except:
            raise IndexError('pattern index too high')
        
        # set the initial state of the net
        self.noise_pattern(mu=mu,P_f=P_f)
        t = [0]
        overlap = [self.overlap(mu)]
        
        if self.FLAG_plot:
            self.plot_recall(mu=mu,t=t,overlap=overlap)
        
        for i in range(self.c):

            # run a step
            self.update_weight(decay=decay,mu=None)
            self.update_state()
            t.append(i+1)
            overlap.append(self.overlap(mu))
            
            # Visualisation if FLAG_plot = True
            if self.FLAG_plot:
                ## update the plotted data
                self.g1.set_data(self.grid())
                self.g2.set_data(t,overlap)
            
                ## update the figure so that we see the changes
                draw()
                show(block=False)
            
            # sleep(0.5) # Can be used to slow down the Visualisation
        
        self.distance = self.hamming_distance(mu)
        
        self.distance_sum += self.distance
        
        if self.distance < 0.05:
            # Counts the number of times the pattern was recovered according to a Hamming distance < 0.05. This is only used to analyse the impact of modifying the diagonal of the weights matrix, mentionned in the appendix of the report
            
            self.recognition_success += 1
        
        # Count number of patterns recalled to later compute the error average
        self.recalls += 1

    def plot_recall(self,mu,t,overlap):
        
        """
        DEFINITION
        Visualisation of the recall results

        INPUT
        mu: Original pattern that X is based on
        t: number of recall update X has gone through
        overlap: The overlap between pattern mu and X
        """
        
        # prepare the figure
        fig_recall = figure('Recall')
        clf()
        
        # plot the current network state
        subplot(221)
        self.g1 = imshow(self.grid(),**plot_dic)# we keep a handle to the image
        axis('off')
        title('Noised pattern to recall')
        
        # plot the target pattern
        subplot(222)
        imshow(self.grid(mu=mu),**plot_dic)
        axis('off')
        title('Original pattern %i'%mu)
        
        # plot the time course of the overlap
        subplot(212)
        self.g2, = plot(t,overlap,'k',lw=2) # we keep a handle to the curve
        axis([0,self.repeats,-1,1])
        xlabel('Time step')
        ylabel('Overlap to original')
        
        # This forces pylab to update and show the figure
        draw()
        #show(block=False) # Can be required depending on users python version
