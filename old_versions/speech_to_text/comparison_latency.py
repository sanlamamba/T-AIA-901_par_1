import pandas as pd
import matplotlib.pyplot as plt

# Re-creating the dataset since the file wasn't found
data = {
    "Test_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "Audio_Length_Seconds": [
        147,
        240,
        56,
        231,
        22,
        157,
        193,
        109,
        69,
        166,
        105,
        261,
        282,
        89,
        77,
        72,
        248,
        87,
        247,
        278,
    ],
    "Vosk_Latency_ms": [
        545,
        353,
        255,
        505,
        419,
        344,
        461,
        707,
        433,
        788,
        237,
        536,
        518,
        689,
        569,
        315,
        402,
        246,
        679,
        379,
    ],
    "Whisper_Latency_ms": [
        920,
        1149,
        948,
        1186,
        655,
        992,
        430,
        1137,
        762,
        409,
        678,
        552,
        435,
        1116,
        514,
        557,
        879,
        1085,
        1026,
        1187,
    ],
    "Google_Cloud_Latency_ms": [
        511,
        166,
        527,
        344,
        147,
        425,
        430,
        355,
        270,
        359,
        588,
        127,
        517,
        587,
        342,
        108,
        370,
        309,
        227,
        500,
    ],
}

# Convert to DataFrame
latency_data = pd.DataFrame(data)

# Plotting the data
plt.figure(figsize=(12, 6))

# Plot latency for each system
plt.plot(
    latency_data["Test_ID"],
    latency_data["Vosk_Latency_ms"],
    marker="o",
    color="blue",
    label="Vosk Latency",
)
plt.plot(
    latency_data["Test_ID"],
    latency_data["Whisper_Latency_ms"],
    marker="s",
    color="green",
    label="Whisper Latency",
)
plt.plot(
    latency_data["Test_ID"],
    latency_data["Google_Cloud_Latency_ms"],
    marker="^",
    color="red",
    label="Google Cloud Latency",
)

# Add titles and labels
plt.title("Comparison of Latency Across Speech-to-Text Systems")
plt.xlabel("Test ID")
plt.ylabel("Latency (ms)")
plt.legend(title="System")
plt.grid(True)

# Save the plot to a file
output_image_path = "./latency_chart.png"
plt.savefig(output_image_path)

plt.close()

output_image_path
