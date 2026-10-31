from database import get_connection

LOCATIONS = [
    "Library",
    "Downhill",
    "Agric Faculty",
    "Uphill",
    "Main Gate"
]


def get_demand_summary():
    connection = get_connection()
    cursor = connection.cursor()

    summary = {}

    for location in LOCATIONS:
        cursor.execute("""
            SELECT
                COALESCE(SUM(passengers), 0),
                COALESCE(
                    MAX(
                        (julianday('now') - julianday(created_at)) * 1440
                    ),
                    0
                )
            FROM requests
            WHERE pickup = ?
        """, (location,))

        waiting, longest_wait = cursor.fetchone()

        cursor.execute("""
            SELECT COUNT(*)
            FROM drivers
            WHERE heading_to = ?
        """, (location,))

        drivers = cursor.fetchone()[0]

        summary[location] = {
            "waiting_passengers": waiting,
            "longest_wait": round(longest_wait),
            "drivers_heading_there": drivers
        }

    connection.close()
    return summary


def get_priorities():
    summary = get_demand_summary()

    return sorted(
        summary.items(),
        key=lambda item: (
            item[1]["waiting_passengers"] /
            (item[1]["drivers_heading_there"] + 1),
            item[1]["longest_wait"]
        ),
        reverse=True
    )

def get_ai_context():
    summary = get_demand_summary()
    priorities = get_priorities()

    context = {
        "demand_summary": summary,
        "priority_ranking": [
            {
                "rank": rank,
                "location": location,
                **data
            }
            for rank, (location, data) in enumerate(priorities, start=1)
        ]
    }

    return context