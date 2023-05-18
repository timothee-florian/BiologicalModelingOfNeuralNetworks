# Hopfield project
# Exercise 1
# Arreguit Jonathan & Bronner Timothee

# Find the maximum dictionary size p_max the network can handle, without the error exceeding 0.05

from scipy.optimize import curve_fit, minimize, basinhopping

# Results storage
Results_P_errors = np.array([[[None,None] for i in range(len(P))] for j in range(K)])
P_errors = [[None for i in range(len(P))] for j in range(K)] # For plot
P_success = [[None for i in range(len(P))] for j in range(K)]
Mean_P_error = [None for i in range(len(P))]
Std_P_error = [None for i in range(len(P))]
Results = np.zeros((K,len(P)))

# Creation fo a NxN pixel Hopfield network
hn = hopfield.hopfield_network(N=N,c=c,plot=FLAG_plot)

for k in range(K): # Number of iterations
    P_n = 0 #  Counter for number of patterns tested
    for p in P:
        # Create P patterns
        hn.make_pattern(P=p,ratio=ratio)
        print('ITERATION:', k+1,'/',K)
        print('NUMBER OF PATTERNS', p)
        weight_mem = [] # Storage of the weight matrix over Z*c updates. This is only used to analyse the impact of modifying the diagonal of the weights matrix, mentionned in the appendix of the report
        distance_mem = [] # Storage of the Hamming distance at each recall. This is only used to analyse the impact of modifying the diagonal of the weights matrix, mentionned in the appendix of the report

        for z in range(Z):
            if FLAG_progress and z%(Z/10) == 0:
                print(100.0*z/Z, '%')
                loading = 0
            weight_mem.append(hn.weight)
            if rand.randint(0,1000)/1000.0 < P_s: # Storage
                mu = rand.randint(0,hn.count_patterns()-1)
                for r in range(c):
                    hn.update_weight(mu=mu,decay=decay)
            else: # Recall
                hn.recall(mu=rand.randint(0,hn.count_patterns()-1), P_f=P_f,decay=decay)
                distance_mem.append([z,hn.distance])
        
        print('RECALLS:', hn.recalls)
        print('ERROR AVERAGE;', 100.0*hn.distance_sum/hn.recalls, '%')
        print('SUCESS RATE:', 100.0*hn.recognition_success/hn.recalls, '%')
        
        # Results storage
        Results_P_errors[k][P_n][0] = p
        Results_P_errors[k][P_n][1] = 1.0*hn.distance_sum/hn.recalls
        Results[k,P_n] = 1.0*hn.distance_sum/hn.recalls
        
        # Plot
        P_errors[k][P_n] = 1.0*hn.distance_sum/hn.recalls
        P_success[k][P_n] = 1.0*hn.recognition_success/hn.recalls
        # hn.plot_error_rate(P=P,error_rate=P_errors,K=K)
        
        P_n += 1
        print() # Next line

# Statistics
Mean_P_error = np.mean(P_errors, axis=0)
Std_P_error = np.std(P_errors, axis=0)
Mean_P_success = np.mean(P_success, axis=0)
Std_P_success = np.std(P_success, axis=0)
# ax0.errorbar(p, Mean_P_error, yerr=Std_P_error, fmt='-o')

#reset matplotlib parameter
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

# Plot of the Hamming distance for each iteration over the number of patterns
plt.figure('Exercise 1 a Distance') # fig_error_rate = 
plt.title('Recall error in function of number of patterns\nobtained from %i iterations'%K)
plot_error_rate = [None]*(K)
for k in range(K):
    plt.plot(Results_P_errors[k,:,0],Results_P_errors[k,:,1])
plt.axis([min(P),max(P),0,1])
plt.xlabel('Number of patterns')
plt.ylabel('Error (Hamming distance)')
plt.show(block=False)

# Plot of the mean of the Hamming distance for K iterations over the number of patterns
plt.figure('Exercise 1b Error')
plt.title('Average recall error in function of number of patterns\nStatistical result')
plt.plot([min(P)-1,max(P)+1],[0.1,0.1],'g',linewidth=2)
plt.plot([min(P)-1,max(P)+1],[0.05,0.05],'r',linewidth=2)
plt.errorbar(P, Mean_P_error, yerr=Std_P_error, fmt='-o')
plt.axis([min(P)-1,max(P)+1,0,1])
plt.xlabel('Number of patterns')
plt.ylabel('Error (Hamming distance)')
plt.legend(['Original error','5 percent error','Obtained error'])
plt.show(block=False)

# Plot of the reconstruction success rate when the recall gives a final Hamming distance < 0.05 for K iterations
# This is only used to analyse the impact of modifying the diagonal of the weights matrix, mentionned in the appendix of the report
plt.figure('Exercise 1c Reconstruction')
plt.title('Recall reconstruction rate in function of number of patterns\nobtained from %i iterations'%K)
plot_error_rate = [None]*(K)
for k in range(K):
    plt.plot(Results_P_errors[k,:,0],P_success[k][:])
plt.axis([min(P),max(P),0,1])
plt.xlabel('Number of patterns')
plt.ylabel('Recall reconstruction success rate')
plt.show(block=False)

# Plot of the mean of the reconstruction success rate when the recall gives a final Hamming distance < 0.05
# This is only used to analyse the impact of modifying the diagonal of the weights matrix, mentionned in the appendix of the report
plt.figure('Exercise 1d Reconstruction')
plt.title('Recall reconstruction success rate average in function of number of patterns\nStatistical result')
plt.errorbar(P, Mean_P_success, yerr=Std_P_success, fmt='-o')
plt.axis([min(P)-1,max(P)+1,0,1])
plt.xlabel('Number of patterns')
plt.ylabel('Recall reconstruction success rate')
plt.show(block=False)

# Save results
np.savetxt('Results/Ex1Results.txt',Results)

# Plot of certain weight matrix indices over Z*c updates
# This is only used to analyse the impact of modifying the diagonal of the weights matrix, mentionned in the appendix of the report
plt.figure('Exercise 1 Weight')
plt.title('Different weight values over iterations')
weight_mem_plot = [[None] for i in range(hn.N)]
for j in range(0,hn.N,1):
    for i in range(len(weight_mem)):
        weight_mem_plot[j].append(weight_mem[i][j][0])
    plt.plot(weight_mem_plot[j])
plt.xlabel('Z Iteration')
plt.ylabel('Weight value')
plt.show(block=False)


# Plot of the hamming distance over Z*c updates
# This is only used to analyse the impact of modifying the diagonal of the weights matrix, mentionned in the appendix of the report
plt.figure('Z - Hamming distance')
plt.title('Recall error in function of Z iteration')
distance_mem_plot = np.asarray(distance_mem)
plt.plot(distance_mem_plot[:,0],distance_mem_plot[:,1],'r*')
plt.xlabel('Z Iteration')
plt.ylabel('Error (Hamming distance)')
plt.axis([0,Z,0,1])

def func(x, a, b, c, d):
    return a*x**3+b*x**2+c*x+d
popt, pcov = curve_fit(func, distance_mem_plot[:,0], distance_mem_plot[:,1])
f = func(distance_mem_plot[:,0], *popt)
plt.plot(distance_mem_plot[:,0],f, linewidth=3)

plt.show(block=False)