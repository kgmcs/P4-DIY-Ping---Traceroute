import matplotlib.pyplot as plt

# Data
domains = [
    'smith.edu', 'harvard.edu', 'chicago.gov', 'lacity.gov', 'columbia.edu',
    'gov.ie', 'unam.mx', 'gov.kg', 'msu.ru', 'seoulsolution.kr'
]
distances = [
    0, 77.15, 70.63, 210.42, 125.39, 3337.58, 2211.69, 6208.15, 4534.75, 6784.23
]
rtt = [
    0.0059825579325358, 0.0074937343597412, 0.014238993326823, 0.023211479187012,
    0.01745351155599, 0.075531403223674, 0.1035209496816, 0.16757782300313,
    0.13738997777303, 0.2001039981842
]

# Convert RTT from seconds to milliseconds
rtt_ms = [val * 1000 for val in rtt]

# Create scatterplot
plt.figure(figsize=(10, 6))
plt.scatter(distances, rtt_ms, marker='o', c='blue', edgecolors='black')

# Set labels and title
plt.xlabel('Geographic Distance (miles)')
plt.ylabel('Average RTT (milliseconds)')
plt.title('Average RTT vs. Geographic Distance')

# Annotate points with domain names
for i, domain in enumerate(domains):
    plt.annotate(domain, (distances[i], rtt_ms[i]), textcoords="offset points", xytext=(5,5), ha='center')

# Show grid
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
