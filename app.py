
import streamlit as st

from database import create_tables, add_request, get_connection, reset_demo_data
from demand import LOCATIONS, get_demand_summary, get_priorities


# PAGE SETUP
st.set_page_config(
    page_title="KAMOVE",
    page_icon="🚌",
    layout="wide"
)

create_tables()

st.title("KAMOVE")
st.caption("See the demand. Move the supply.")


# CREATE SIX SIMULATED DRIVERS IF THEY DON'T EXIST
connection = get_connection()
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM drivers")
existing_drivers = cursor.fetchone()[0]

demo_locations = [
    ("Main Gate",),
    ("Downhill",),
    ("Library",),
    ("Agric Faculty",),
    ("Uphill",),
    ("Downhill",)
]

if existing_drivers < 6:
    missing_drivers = 6 - existing_drivers

    cursor.executemany(
        "INSERT INTO drivers (current_location) VALUES (?)",
        demo_locations[existing_drivers:existing_drivers + missing_drivers]
    )

connection.commit()
connection.close()


# CREATE THE THREE VIEWS
student_tab, operations_tab, driver_tab = st.tabs(
    ["Student", "Operations", "Driver"]
)


# --------------------------------
# STUDENT VIEW
# --------------------------------

with student_tab:
    st.header("Request a Ride")

    with st.form("student_request"):

        pickup = st.selectbox(
            "Where are you waiting?",
            LOCATIONS
        )

        destination = st.selectbox(
            "Where are you going?",
            LOCATIONS
        )

        passengers = st.number_input(
            "Number of passengers",
            min_value=1,
            max_value=4,
            value=1
        )

        ready = st.checkbox(
            "I'm ready for pickup at this location"
        )

        submitted = st.form_submit_button("Request a Ride")

        if submitted:

            if pickup == destination:
                st.error("Pickup and destination cannot be the same.")

            elif not ready:
                st.warning("Please confirm that you're ready for pickup.")

            else:
                try:
                    add_request(pickup, destination, passengers)

                    st.success(
                        f"Your request has been recorded! "
                        f"{passengers} passenger(s) waiting at {pickup}."
                    )

                except ValueError as error:
                    st.error(str(error))


# --------------------------------
# OPERATIONS DASHBOARD
# --------------------------------

with operations_tab:
    st.header("Operations Dashboard")
    if st.button("Reset demo data"):
        reset_demo_data()
        st.success('Demo data has been reset')
        st.rerun()

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button(" Refresh Dashboard"):
            st.rerun()

    with col2:
        st.caption(
            "Refresh to see the latest passenger demand and driver responses."
        )

    summary = get_demand_summary()
    priorities = get_priorities()

    st.subheader("Demand by Location")

    for location, data in summary.items():

        st.markdown(f"### {location}")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Waiting passengers",
            data["waiting_passengers"]
        )

        col2.metric(
            "Longest wait (minutes)",
            data["longest_wait"]
        )

        col3.metric(
            "Drivers heading here",
            data["drivers_heading_there"]
        )

        st.divider()

    st.subheader("Priority Ranking")

    for rank, (location, data) in enumerate(priorities, start=1):

        st.write(
            f"**{rank}. {location}** | "
            f"Waiting: {data['waiting_passengers']} | "
            f"Drivers heading there: {data['drivers_heading_there']} | "
            f"Longest wait: {data['longest_wait']} minutes"
        )


# --------------------------------
# DRIVER VIEW
# --------------------------------

with driver_tab:
    st.header("Driver Dashboard")
    st.caption("These are simulated demo drivers.")

    col1, col2 = st.columns([1, 5])

    with col1:
        if st.button("🔄 Refresh Locations"):
            st.rerun()

    with col2:
        st.caption("Refresh to see the latest demand and driver assignments.")

    priorities = get_priorities()

    st.subheader("Locations needing attention")

    for rank, (location, data) in enumerate(priorities, start=1):

        st.write(
            f"**{rank}. {location}** - "
            f"{data['waiting_passengers']} waiting passengers"
        )

    st.divider()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, current_location, heading_to FROM drivers ORDER BY id"
    )

    drivers = cursor.fetchall()
    connection.close()

    if drivers:

        driver_options = {
            f"Demo Driver {driver_id} ({current_location})": driver_id
            for driver_id, current_location, heading_to in drivers
        }

        selected_driver = st.selectbox(
            "Select a demo driver",
            list(driver_options.keys())
        )

        selected_driver_id = driver_options[selected_driver]

        destination = st.selectbox(
            "Choose a location to head to",
            LOCATIONS,
            key="driver_destination"
        )

        if st.button("I'm Heading There"):

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE drivers
                SET heading_to = ?
                WHERE id = ?
                """,
                (destination, selected_driver_id)
            )

            connection.commit()
            connection.close()

            st.success(f"Driver is now heading to {destination}.")

            st.rerun()

    else:
        st.warning("No drivers are currently available.")
