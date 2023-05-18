# Hopfield project
# Exercise 2
# Arreguit Jonathan & Bronner Timothee

# Find how the maximum number of patterns p_max scale with N for an error smaller than 0.05

# Results storage
Results_N_Pmax = np.array([[None for i in range(2)] for j in range(len(N))]) # [N,P_max]
N_n = 0 # Counter for number of sizes tested

for n in N:
    
    print('Number of fully interconnected units:', n)
    
    # Initialisation of parameters for size n
    error = 0
    previous_min = 0
    previous_max = 0
    found = False
    p = P_init
    
    # Creation of network
    hn = hopfield.hopfield_network(N=n,c=c,plot=FLAG_plot)
    
    # Search for maximum dictionary size for n dimensions
    while not found:
        hn.make_pattern(P=p,ratio=ratio)
        print('Testing for', p, 'patterns with Pmin =',previous_min, 'and Pmax =',previous_max)
        for z in range(Z):
            if FLAG_progress and z%(Z/10) == 0:
                print('\r', 100.0*z/Z, '%\r')
                loading = 0
            if rand.randint(0,1000)/1000.0 < P_s: # Storage
                mu = rand.randint(0,hn.count_patterns()-1)
                for r in range(c):
                    hn.update_weight(mu=mu,decay=decay)
            else: # Recall
                hn.recall(mu=rand.randint(0,hn.count_patterns()-1), P_f = P_f,decay=decay)
        
        # Average Hamming distance over the total number of recalls
        distance_mean = 1.0*hn.distance_sum/hn.recalls
        
        if distance_mean < error_max: # Bigger dictionary size possible
            if previous_min < p and previous_max < p:
                previous_min = p
                previous_max = p
                p = p*2
            elif previous_max > p:
                previous_min = p
                p = (previous_max+p)/2
                if p == previous_max-1:
                    found = True # Found maximum dictionary size

        elif distance_mean > error_max: # Smaller dictionary size required
            print('Maximum error crossed for', p, 'patterns')
            previous_max = p
            p = (previous_min+p)/2
            if p == previous_min:
                found = True # Found maximum dictionary size
    
    # Results storage
    Results_N_Pmax[N_n][0] = n
    Results_N_Pmax[N_n][1] = p
    print('RESULT:\nFor patterns with', n, 'dimensions:\nMaximum dictionaray size is', p, 'patterns\n')
    N_n += 1

#reset matplotlib parameter
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

# Plot of the maximum dictionary size in function the dimension N of patterns
plt.figure('Exercise 2')
plt.title('Maximum dictionary size in function of the number of dimensions\nfor a recall error below 0.05')
plt.plot(N,Results_N_Pmax[:,1])
plt.xlabel('Number of dimensions N')
plt.ylabel('Dictionary size P_{max}')

plt.show(block=False)



