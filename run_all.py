import subprocess
import os
import datetime

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Define the log file name
log_file = 'run_all.log'


# Function to write a message to the log file with a timestamp
def log_message(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")


try:
    # Define the Python scripts to run
    preprocessing_script = r'preprocessing.py'
    dashboard_script = r'dashboard_dataframe.py'

    # Run the preprocessing script
    log_message("Starting preprocessing script...")
    subprocess.run(['python', preprocessing_script], check=True)
    log_message("Preprocessing completed successfully.")

    # Run the dashboard data preparation script
    log_message("Starting dashboard script...")
    subprocess.run(['python', dashboard_script], check=True)
    log_message("Dashboard data updated successfully.")

# Catch and log any errors during the script executions
except subprocess.CalledProcessError as e:
    log_message(f"Script failed with error: {e}")

# Log the end of the run
log_message("Run completed.\n")
