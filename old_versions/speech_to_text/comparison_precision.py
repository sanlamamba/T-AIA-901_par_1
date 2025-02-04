import pandas as pd
import matplotlib.pyplot as plt

precision_data = pd.read_csv("./old_versions/speech_to_text/data/precision-test.csv")
# Plotting the data with a bar chart for a different visualization style
plt.figure(figsize=(14, 7))

# Plot precision scores for each system
bar_width = 0.25
index = range(len(precision_data["Test_ID"]))

plt.bar(
    [i - bar_width for i in index],
    precision_data["Vosk_Precision"],
    width=bar_width,
    color="blue",
    label="Vosk Precision",
)
plt.bar(
    index,
    precision_data["Whisper_Precision"],
    width=bar_width,
    color="green",
    label="Whisper Precision",
)
plt.bar(
    [i + bar_width for i in index],
    precision_data["Google_Cloud_Precision"],
    width=bar_width,
    color="red",
    label="Google Cloud Precision",
)

# Adding titles and labels
plt.title("Comparison of Precision Across Speech-to-Text Systems")
plt.xlabel("N Essai")
plt.ylabel("Precision")
plt.xticks(index, precision_data["Test_ID"], rotation=45)
plt.legend(title="System", loc="lower right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Save the plot to a file
output_image_precision_path = "./precision_comparison_chart.png"
plt.savefig(output_image_precision_path)

plt.close()

output_image_precision_path
