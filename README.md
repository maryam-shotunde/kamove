KAMOVE 

See the demand, Move the supply...

KAMOVE is an AI powered campus mobility coordination system primarily designed to help coordinate student transport demand and driver availability around Lagos State University, Epe Campus.

Problem

Students may experience delays finding available transport, while drivers may not have clear information about where passengers are waiting.

KAMOVE aims to make transport coordination more informed by showing passenger demand across verified campus locations and recommending where drivers should go.

Core Features

- Student View: Students select their pickup location, destination and passenger count, then submit a transport request.
- Operations Dashboard: Displays waiting passengers, longest waiting time and drivers heading to each location.
- Driver View: Displays prioritised locations and allows drivers to indicate where they are heading.
- AI Mobility Analyst: Uses Gemma to explain current transport demand and location priorities.

Campus Locations

1. Library
2. Downhill
3. Agric Faculty
4. Uphill
5. Main Gate

Technology Stack

1 Python
2 Streamlit
3 SQLite
4 Gemma (open-weight AI model)

Installation and Setup

1. Clone the repository:

git clone https://github.com/maryam-shotunde/KAMOVE.git

2. Enter the project folder:

cd KAMOVE

3. Create and activate a virtual environment.
4. Install dependencies:

pip install -r requirements.txt

5. Run the application:

streamlit run app.py

Demo Data

The MVP uses simulated demo drivers and test requests. These are not live campus transport statistics.

Future Improvements

1. Live GPS tracking
2. Student and driver accounts
3. Notifications
4. Live transport operator integration
5. Demand forecasting
6. Route optimisation
7. Chat box

