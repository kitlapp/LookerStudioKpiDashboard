# LOOKER STUDIO DASHBOARD WITH HOSPITALITY KPIs
It contains all the scripts needed to create a static, yet fully updated Looker Studio (LS) dashboard. The dashboard can be shared with stakeholders at specific time intervals, such as monthly. The KPIs are selected based on both the machine learning outputs from the Booking Cancellations Prediction project and domain research.

As this project complements the BookingCancellationsPredictions project, both workflows are explained in detail in Full_Project_Explained.pdf.

All processes before the cleaned data upload onto Looker Studio are fully automated.

Since the case study focuses on a static yet regularly updated KPI dashboard, the calculated fields needed in LS are prepared outside of it using Python. This approach minimizes dashboard update times, as LS only needs to reconnect to the refreshed data sources after each new data upload. Additionally, the dashboard structure remains stable thanks to proper data source management.

In summary, although the process is not 100% automated, the only human action required after the initial dashboard setup is to upload the new data into Looker Studio and quickly manage the data source reconnections to ensure the dashboard refreshes correctly. The person responsible for this task does not need advanced knowledge of dashboard coding, they only need to follow simple and repeatable steps in Looker Studio’s data management settings. After completing these easy tasks, the static yet fully updated KPI dashboard is ready to be shared with stakeholders.

# SHARED DASHBOARD LINK
Below is my KPI dashboard:  

[Hospitality KPIs](https://lookerstudio.google.com/reporting/8ee13cf9-54e6-41ac-823e-af0706cec66c)


# DATA COLLECTION
https://www.kaggle.com/datasets/mojtaba142/hotel-booking

# FILES INCLUDED
1) Doc_KPIs_Looker.pdf – General documentation for the project.
2) KPIs_Significance.pdf - Explains the meaning of the dashboard KPIs and outlines their objectives.
3) Full_Project_Explained.pdf – Walks through the workflow used to complete the project. Since it complements the ‘BookingCancellationPredictions’ project, it’s also included there.
4) run_all.py – A script that automatically runs preprocessing.py and dashboard_dataframe.py.
5) preprocessing.py – Handles the transformation of the extracted data.
6) dashboard_dataframe.py – Creates the tabular data structures that are uploaded to LS.
7) cleaning.py – Contains custom functions used in preprocessing.py.
8) testing.py – Contains testing scripts to ensure the proper functioning of some custom functions.
9) dictionaries.py – Helps with manipulating the ‘country’ column.
10) results.py – Includes custom functions for model evaluation and interpretation.
11) run_all.txt – A log file that monitors the successful execution of run_all.py. I added it just to show its format.
12) This file - readme.txt

# HOW TO SET UP THE ENVIRONMENT
Please note that my scripts are designed to retrieve data from my local PostgreSQL database, so they may not work out-of-the-box on your machine. However, if you'd like to discuss alternative setups or solutions, feel free to connect with me on [Linkedin](https://www.linkedin.com/in/kimon-ioannis-lappas).
