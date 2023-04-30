# Hopfield project
# Exercise 3
# Arreguit Jonathan & Bronner Timothee

# Find how the optimal weight decay factor changes as the sub-dictionary size m increases

# Results storage
Results_decay_errorrate = np.zeros((len(M),len(Decay)))
decay_n = 0 # Counter for number of decays tested
m_n = 0 # Counter for m

Decay_jump = Decay[1]- Decay[0]
M_jump = M[1]- M[0]

print 'NUMBER OF PATTERNS', p, '\n'
for m in M:
    for decay in Decay:
        decay *= resolution
        print 'DECAY:',  decay
        print 'M SIZE:', m
        
        hn = hopfield.hopfield_network(N=N,c=c,plot=FLAG_plot)
        hn.make_pattern(P=p,ratio=ratio)
        
        for z in range(Z):
            xi_start=round(z/T_window)%p
            window = [(i+xi_start)%p for i in range(m)]
            
            if FLAG_progress and z%(Z/10) == 0:
                print 100.0*z/Z, '%'
                loading = 0
            if rand.randint(0,1000)/1000.0 < P_s: # Storage
                mu = window[rand.randint(0,m-1)]
                for r in range(c):
                    hn.update_weight(mu=mu,decay=decay)
            else: # Recall
                hn.recall(mu=window[rand.randint(0,m-1)], P_f=P_f,decay=decay)
                
        print 'RECALLS:', hn.recalls
        print 'ERROR RATE;', 100.0*hn.distance_sum/hn.recalls, '%'

        # Storage of results
        Results_decay_errorrate[m_n][decay_n] = 1.0*hn.distance_sum/hn.recalls
        
        decay_n += 1
        
        print # Next line
    
    decay_n = 0
    m_n += 1
    
# Heatmap of the error in function of the decay and the sub-dictionary size m
Decay.append(Decay[-1]+Decay_jump)
M.append(M[-1]+M_jump)
Decay_plot = np.zeros((len(M),len(Decay)))
M_plot = np.zeros((len(M),len(Decay)))

for i in range(len(M)):
    Decay_plot[i,:] = Decay
Decay_plot *= resolution
for i in range(len(Decay)):    
    M_plot[:,i] = M

Error_rate_D_M = Results_decay_errorrate
figex4, ax = plt.subplots()
figex4.canvas.set_window_title('Exercise 4')
heatmap = ax.pcolor(Decay_plot,M_plot,Error_rate_D_M)

cbar = plt.colorbar(heatmap)
cbar.set_label('Error')
plt.title('Error in function of decay value\nand sub-dictionary size')
plt.axis([Decay[0]*resolution,Decay[-1]*resolution,M[0],M[-1]])
plt.xlabel('Decay $\lambda$')
plt.ylabel('Sub-dictionary size m')
plt.show(block=False)