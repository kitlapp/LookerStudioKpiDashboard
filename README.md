# LOOKER STUDIO DASHBOARD WITH HOSPITALITY KPIs
It contains all the scripts needed to create a static, yet fully updated Looker Studio (LS) dashboard. It can be shared with stakeholders at specific time intervals, such as monthly. The KPIs are chosen based on both the machine learning outputs from the Booking Cancellations Prediction project and domain research.

As this project is complementary to BookingCancellationsPredictions project, I include both projects' workflow detailly in Full_Project_Explained.pdf. 

Note that all processes before the cleaned data upload onto LS are automated. 

Since my case study is about a static but fully updated KPI dashboard, the calculated fields needed in LS can be prepared outside of it using Python. In this way, the dashboard update times are minimized because LS only needs to reconnect to the updated data sources after each new data upload. Also, the dashboard structure stays stable thanks to proper data source management.

All in all, even if the process is not 100% automated, the only human action needed after the first dashboard creation is to upload the fresh data into LS and quickly manage the reconnections, making sure that the data refreshes correctly. Specifically, the person who works with LS does not need to know low-level dashboard coding. They only need to follow simple, repeated steps in LS data management. After these easy tasks, the static but fully updated KPI dashboard is ready to be shared with stakeholders.

# DATA COLLECTION
https://www.kaggle.com/datasets/mojtaba142/hotel-booking

# FILES INCLUDED
1) Doc_KPIs_Looker.pdf – General documentation for the project.
2) KPIs_Significance.pdf - Explains what is the meaning of the dashboard KPIs and what are the goals.
3) Full_Project_Explained.pdf – Walks through the workflow used to complete the project. Since it complements the ‘BookingCancellationPredictions’ project, it’s also included there.
4) run_all.py – A script that automatically runs preprocessing.py and dashboard_dataframe.py.
5) preprocessing.py – Handles the transformation of the extracted data.
6) dashboard_dataframe.py – This file handles the tabular data structures creation which are uploaded to LS.
7) cleaning.py – Contains custom functions used in preprocessing.py.
8) testing.py – Contains testing scripts to ensure the proper functioning of some custom functions.
9) dictionaries.py – Helps with manipulating the ‘country’ column.
10) results.py – Includes custom functions for model evaluation and interpretation.
11) run_all.txt – A log file that monitors the successful execution of run_all.py. I added it just to show its format.
12) This file - readme.txt

# HOW TO SET UP THE ENVIRONMENT
Please note that my scripts are designed to retrieve data from my local PostgreSQL database, so they may not work out-of-the-box on your machine. However, if you'd like to discuss alternative setups or solutions, feel free to connect with me on [Linkedin](https://www.linkedin.com/in/kimon-ioannis-lappas).
