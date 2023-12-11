import matplotlib.pyplot as plt

# Data
domains = ['smith.edu', 'harvard.edu', 'chicago.gov', 'lacity.gov', 'columbia.edu', 'gov.ie', 'unam.mx', 'gov.kg', 'msu.ru', 'seoulsolution.kr']
distances = [0, 77.15, 70.63, 210.42, 125.39, 3337.58, 2211.69, 6208.15, 4534.75, 6784.23]
hops_to_target = [3, 10, 9, 18, 13, 15, 20, 17, 27, 14]
ping_dates = ['12/03/2023'] * len(domains)

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(distances, hops_to_target, color='blue')

# Adding labels and title
plt.title('Geographic Distance vs Hops to Target')
plt.xlabel('Geographic Distance (miles)')
plt.ylabel('# Hops to Target')

# Adding domain labels
for i in range(len(domains)):
    plt.text(distances[i], hops_to_target[i], domains[i], ha='right', va='bottom')

plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()
