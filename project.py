import numpy as np
import random
from scipy.stats import truncnorm
import matplotlib.pyplot as plt

class Politician: # Politician class
    def __init__(self, age, office=None, years_in_office=0, last_consul_term=None):
        self.age = age
        self.office = office
        self.years_in_office = years_in_office
        self.last_consul_term = last_consul_term
        self.life_expectancy = generate_life_expectancy()

office_limits = { # Postions available for each office
    'Quaestor': 20,
    'Aedile': 10,
    'Praetor': 8,
    'Consul': 2,
}

def generate_life_expectancy(mu=55, sigma=10, lower=25, upper=80): # Life expectency 
    return int(truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs())

def annual_influx_of_candidates(mu=15, sigma=5):
    return int(np.random.normal(mu, sigma))
    return max(0, influx)  # Ensure non-negative influx

def is_eligible_for_office(politician, office, current_year): # Check if meeting the requirements
    age_requirements = {'Quaestor': 30, 'Aedile': 36, 'Praetor': 39, 'Consul': 42}
    
    # Check age requirement
    if politician.age < age_requirements[office]:
        return False

    # Eligibility based on office and experience
    if office == 'Quaestor':
      
        return True
    elif office == 'Aedile' and politician.office == 'Quaestor' and politician.years_in_office >= 2:
       
        return True
    elif office == 'Praetor' and politician.office == 'Aedile' and politician.years_in_office >= 2:

        return True
    elif office == 'Consul':
        if politician.office == 'Praetor' and politician.years_in_office >= 2:
            if not politician.last_consul_term or (current_year - politician.last_consul_term) >= 10:
                return True
    return False


def initialize_political_landscape():
    landscape = {
        'Quaestor': [],
        'Aedile': [],
        'Praetor': [],
        'Consul': []
    }
    
    for office in landscape:
        if office == 'Quaestor':
            min_age, max_age = 30, 34
        elif office == 'Aedile':
            min_age, max_age = 36, 39
        elif office == 'Praetor':
            min_age, max_age = 39, 42
        elif office == 'Consul':
            min_age, max_age = 42, 45
            
        for _ in range(office_limits[office]):
            age = random.randint(min_age, max_age)
            politician = Politician(age=age)
            landscape[office].append(politician)
            politician.office = office
            
    return landscape, 100

def age_and_mortality(landscape):
    for office in landscape:
        landscape[office] = [p for p in landscape[office] if p.age + 1 <= p.life_expectancy]
        for politician in landscape[office]:
            politician.age += 1
            politician.years_in_office += 1
    return landscape


def generate_new_candidates():
    num_candidates = annual_influx_of_candidates()
    return [Politician(age=30) for _ in range(num_candidates)]

def conduct_elections(landscape, new_candidates, current_year):
    for office in ['Consul', 'Praetor', 'Aedile', 'Quaestor']:
        if office == 'Quaestor':
            candidates = new_candidates + [p for p in landscape['Quaestor'] if is_eligible_for_office(p, office, current_year)]
        else:
            candidates = []
            for lower_office, politicians in landscape.items():
                if lower_office != office:  # Consider candidates from all lower offices
                    candidates.extend([p for p in politicians if is_eligible_for_office(p, office, current_year)])
        
        random.shuffle(candidates)
        while len(landscape[office]) < office_limits[office] and candidates:
            candidate = candidates.pop()
            if is_eligible_for_office(candidate, office, current_year):
                if candidate.office != office:  # Update office and years if it's a promotion
                    candidate.office = office
                    candidate.years_in_office = 0  # Reset years in office upon promotion
                landscape[office].append(candidate)
                if office == 'Consul':
                    candidate.last_consul_term = current_year


    for office in landscape.keys():
        landscape[office] = [p for p in landscape[office] if p.office == office]

    return landscape


def update_PSI(landscape, PSI):
    for office in office_limits:
        unfilled_positions = office_limits[office] - len(landscape[office])
        PSI -= unfilled_positions * 5
    return PSI

def simulate_year(landscape, PSI, current_year):
    landscape = age_and_mortality(landscape)
    new_candidates = generate_new_candidates()
    landscape = conduct_elections(landscape, new_candidates, current_year)
    PSI = update_PSI(landscape, PSI)
    return landscape, PSI


def run_simulation():
    landscape, PSI = initialize_political_landscape()
    for current_year in range(1, 201):
        landscape, PSI = simulate_year(landscape, PSI, current_year)
    # Calculate the average fill rates
    avg_fill_rates = {office: len(landscape[office]) / office_limits[office] for office in office_limits}
    return PSI, avg_fill_rates, landscape

def plot_age_distributions(landscape):
    fig, axs = plt.subplots(2, 2, figsize=(10, 7))  # Figure size as needed
    axs = axs.ravel()  # Flatten the array if necessary

    for i, office in enumerate(['Quaestor', 'Aedile', 'Praetor', 'Consul']):
        ages = [politician.age for politician in landscape[office]]
        axs[i].hist(ages, bins=range(25, 81, 5), alpha=0.7)
        axs[i].set_title(f'Age Distribution in {office}')
        axs[i].set_xlabel('Age')
        axs[i].set_ylabel('Number of Politicians')

    plt.tight_layout()
    plt.show()


PSI_final, avg_fill_rates, landscape = run_simulation()
print("Final PSI:", PSI_final)
print("Average Annual Fill Rates:")
for office, rate in avg_fill_rates.items():
    print(f"{office}: {rate:.2f}")

# Plot the age distributions
plot_age_distributions(landscape)
