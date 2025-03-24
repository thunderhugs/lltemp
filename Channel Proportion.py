import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Data for referral volume by marketing channel
channels = ['Classifieds', 'Direct Mail', 'Email', 'Google Ads Search', 
            'HMN', 'META', 'Organic / Direct', 'Outbound', 'Radio']
volumes = [2, 44, 17, 69, 1845, 594, 408, 4, 3]

# Calculate total for percentage calculation
total = sum(volumes)

# Create figure and axis with a transparent background
plt.figure(figsize=(12, 10), facecolor='none')
ax = plt.subplot(111)
ax.set_facecolor('none')

# Create a custom colormap for a more vibrant look
colors = plt.cm.viridis(np.linspace(0, 1, len(channels)))
# Make the colors more vibrant
for i in range(len(colors)):
    colors[i] = mcolors.to_rgba(mcolors.to_hex(colors[i]), alpha=0.85)

# Sort data to highlight smaller segments
sorted_indices = np.argsort(volumes)
sorted_channels = [channels[i] for i in sorted_indices]
sorted_volumes = [volumes[i] for i in sorted_indices]
sorted_colors = [colors[i] for i in sorted_indices]

# Explode the smaller segments for better visibility
explode = [0.1 if v < 50 else 0.01 for v in sorted_volumes]

# Create doughnut chart with emphasized smaller segments
wedges, texts, autotexts = ax.pie(sorted_volumes, 
                                  labels=None,  # No labels initially
                                  autopct=lambda p: f'{p:.1f}%' if p > 1 else '',
                                  startangle=90,
                                  pctdistance=0.75,
                                  explode=explode,
                                  colors=sorted_colors,
                                  wedgeprops={'width': 0.55, 'edgecolor': 'white', 'linewidth': 1.5})

# Draw a circle at the center with a transparent fill
centre_circle = plt.Circle((0, 0), 0.35, fc='white', ec='black', linewidth=1.5, alpha=0.7)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Add title with stylized appearance
plt.title('Referral Volume by Marketing Channel', 
          fontsize=20, fontweight='bold', color='black', pad=20)

# Create a separate legend for better readability
# Format entries to show channel name, value, and percentage
legend_labels = []
for i, (channel, volume) in enumerate(zip(sorted_channels, sorted_volumes)):
    percentage = (volume / total) * 100
    legend_labels.append(f'{channel}: {volume} ({percentage:.1f}%)')

# Add a styled legend
legend = ax.legend(wedges, legend_labels, 
                  title="Marketing Channels",
                  loc="center left", 
                  bbox_to_anchor=(1.1, 0.5),
                  frameon=True,
                  facecolor='white',
                  edgecolor='black',
                  fontsize=10)

# Add labels directly on the chart for larger segments
threshold = 5  # Only add labels for segments > 5% of total
for i, wedge in enumerate(wedges):
    percentage = (sorted_volumes[i] / total) * 100
    if percentage > threshold:
        # Get the angle of the wedge's center
        angle = np.deg2rad(wedge.theta1 + (wedge.theta2 - wedge.theta1)/2)
        # Get the position for the text (slightly outside the wedge)
        x = np.cos(angle) * 0.65
        y = np.sin(angle) * 0.65
        # Add the channel name
        ax.text(x, y, sorted_channels[i], ha='center', va='center', 
                fontsize=11, fontweight='bold', color='black',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor='none'))

# Improve the appearance of percentage labels
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

# Add a subtle grid effect for more depth
for i in range(1, 6):
    circle = plt.Circle((0, 0), i*0.15, fc='none', ec='gray', alpha=0.2, linewidth=0.5)
    fig.gca().add_artist(circle)

# Add total count in the center
ax.text(0, 0, f'Total\n{total}', ha='center', va='center', fontsize=14, 
       color='black', fontweight='bold')

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')
plt.tight_layout()
plt.savefig('referral_volume_chart.png', transparent=True)  # Save with transparent background
plt.show()