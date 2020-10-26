from Visualization import get_current_price_data
import numpy as np
import matplotlib.pyplot as plt

def monte_simulation(stock_name, iteration):
    prices_list = get_current_price_data(stock_name)
    rate_simulate = {'low': 0, 'high': 0}
    simulated_price_mean = 0.000
    if prices_list != 0:
        for i in range(iteration):
            if i % 1000 == 0:
                print(i)
            if prices_list != 0:
                S0 = prices_list[-1]
                dt = 1      # published every 2 mins
                T = 720
                N = T / dt
                t = np.arange(1, int(N) + 1)

                returns = []
                for i in range(1,len(prices_list)):
                    returns.append( (prices_list[i] - prices_list[i-1]) / prices_list[i-1])

                mu = np.mean(returns)
                sigma = np.std(returns)

                scen_size = 4
                b = {str(scen): np.random.normal(0, 1, int(N)) for scen in range(1, scen_size + 1)}
                W = {str(scen): b[str(scen)].cumsum() for scen in range(1, scen_size + 1)}

                drift = (mu - 0.5 * sigma**2) * t
                diffusion = {str(scen): sigma * W[str(scen)] for scen in range(1, scen_size + 1)}
                S = np.array([S0 * np.exp(drift + diffusion[str(scen)]) for scen in range(1, scen_size + 1)]) 
                S = np.hstack((np.array([[S0] for scen in range(scen_size)]), S))
                
                count_high = 0
                count_low = 0
                all_mean = 0.0
                for i in range(0, scen_size):
                    for price in S[i]:
                        if price/ S0 <= 0.9:
                            count_low += 1
                        else: count_high += 1
                    all_mean += np.mean(S[i])
                
                rate_simulate['low'] += count_low
                rate_simulate['high'] += count_high
                if simulated_price_mean == 0.0:
                    simulated_price_mean = simulated_price_mean + (all_mean / 4) 
                else: simulated_price_mean = (simulated_price_mean + (all_mean / 4) ) / 2

        print(simulated_price_mean)
        print(rate_simulate)
        print(rate_simulate['low'] / (rate_simulate['high'] + rate_simulate['low']))
        rate_low = rate_simulate['low'] / (rate_simulate['high'] + rate_simulate['low'])

        return [simulated_price_mean, rate_low]
    else: 
        return -1


def plot_model(S,N,sigma):
    plt.figure(figsize = (200,100))
    time = np.arange(0, int(N) + 1)

    plt.title("Daily Volatility: " + str(sigma))
            
    plt.plot(time,S[0],'g')
    plt.plot(time,S[1],'r')
    plt.plot(time,S[2],'b')
    plt.plot(time,S[3],'m')
    plt.ylabel('Stock Prices, THB')
    plt.xlabel('Prediction Days (1 point = 2 minutes)')
            
    plt.show()

if __name__ == "__main__":
    #monte_simulation("VGI")
    pass