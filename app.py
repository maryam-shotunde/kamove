import streamlit as st

from database import (create_tables,
    create_tables,
    add_request,
    get_connection
)

from demand import (
    LOCATIONS,
    get_demand_summary,
    get_priorities
)


st.set_page_config(
    page_title="KAMOVE",
    page_icon="bus",
    layout="wide"
)

create_tables()

st.title("KAMOVE")
st.subheader("See the demand. Move the supply.")
st.caption("AI-powered campus mobility coordination")


# Create simulated demo drivers once
connection = get_connection()
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM drivers")

if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO drivers (current_location) VALUES (?)",
        [("Main Gate",), ("Downhill",)]
    )

connection.commit()
connection.close()


student_tab, operations_tab, driver_tab = st.tabs(
    ["Student", " Operations", "Driver"]
)


# STUDENT VIEW
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
                add_request(pickup, destination, passengers)

                st.success(
                    f"Your request has been recorded! "
                    f"{passengers} passenger(s) waiting at {pickup}."
                )


# OPERATIONS VIEW
with operations_tab:
    st.header("Operations Dashboard")

    if st.button("Refresh Dashboard"):
        st.rerun()

    summary = get_demand_summary()
    priorities = get_priorities()

    for location, data in summary.items():
        with st.container(border=True):
            st.subheader(location)

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Waiting Passengers",
                data["waiting_passengers"]
            )

            col2.metric(
                "Longest Wait",
                f'{data["longest_wait"]} min'
            )

            col3.metric(
                "Drivers Heading There",
                data["drivers_heading_there"]
            )

    st.subheader("Locations Needing Attention")

    for rank, (location, data) in enumerate(priorities, start=1):
        st.write(
            f"**{rank}. {location}** — "
            f'{data["waiting_passengers"]} waiting passengers'
        )


# DRIVER VIEW
with driver_tab:
    st.header("Driver Dashboard")

    priorities = get_priorities()

    st.subheader("Prioritised Locations")

    for rank, (location, data) in enumerate(priorities, start=1):
        st.write(
            f"**{rank}. {location}** | "
            f'{data["waiting_passengers"]} waiting | '
            f'{data["longest_wait"]} min longest wait | '
            f'{data["drivers_heading_there"]} drivers heading there'
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, current_location FROM drivers"
    )

    drivers = cursor.fetchall()
    connection.close()

    if drivers:
        driver_options = {
            f"Demo Driver {driver_id} ({location})": driver_id
            for driver_id, location in drivers
        }

        selected_driver = st.selectbox(
            "Select demo driver",
            list(driver_options.keys())
        )

        selected_location = st.selectbox(
            "Where are you heading?",
            LOCATIONS
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
                (
                    selected_location,
                    driver_options[selected_driver]
                )
            )

            connection.commit()
            connection.close()

            st.success(
                f"Driver response recorded for {selected_location}!"
            )

            st.rerun()


