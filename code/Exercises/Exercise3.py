# Hopfield project
# Exercise 3
# Arreguit Jonathan & Bronner Timothee

# Find how the error changes with the weight decay factor

# Results storage
Results_decay_errorrate = [[None,None] for i in range(len(Decay))]
decay_n = 0 # Counter for number of decays tested

print('NUMBER OF PATTERNS', p, '\n')
for decay in Decay:
    decay *= resolution
    print('DECAY',  decay)
    
    hn = hopfield.hopfield_network(N=N,c=c,plot=FLAG_plot)
    hn.make_pattern(P=p,ratio=ratio)
    
    for z in range(Z):
        xi_start=round(z/T_window)%p
        window = [(i+xi_start)%p for i in range(m)]
        
        if FLAG_progress and z%(Z/10) == 0:
            print(100.0*z/Z, '%')
            loading = 0
        if rand.randint(0,1000)/1000.0 < P_s: # Strorage
            mu = window[rand.randint(0,m-1)]
            for r in range(c):
                hn.update_weight(mu=mu,decay=decay)
        else: # Recall
            hn.recall(mu=window[rand.randint(0,m-1)], P_f=P_f, decay=decay)
            
    print('RECALLS:', hn.recalls )
    print('ERRORS:', hn.distance_sum)
    print('ERROR RATE;', 100.0*hn.distance_sum/hn.recalls, '%')

    # Storage
    Results_decay_errorrate[decay_n][0] = decay
    Results_decay_errorrate[decay_n][1] = 1.0*hn.distance_sum/hn.recalls
    
    decay_n += 1
    
    print # Next line
    
# Plot of the Error rate in function of decay value for a given m
plot_decay = []
plot_error = []
for i in range (len(Results_decay_errorrate)):
    plot_decay.append(Results_decay_errorrate[i][0])
    plot_error.append(Results_decay_errorrate[i][1])

#reset matplotlib parameter
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

plt.figure('Exercise 3')
plt.title('Error in function of decay $\lambda$ for sub-dictionary size m = 5')
plt.plot(plot_decay,plot_error,'-')
plt.axis(ymin=0,ymax=1.0)
plt.xlabel('Decay $\lambda$')
plt.ylabel('Error (Hamming distance)')
plt.show(block=False)