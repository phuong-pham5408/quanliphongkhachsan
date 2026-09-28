import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
import pandas as pd
import time

# ============================================================
# CONFIGURATION
# ============================================================

st.image("VT.jpg")
st.set_page_config(
    page_title="AURELIA HOTEL — Room Management",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_FILE = "hotel_management.db"

# ============================================================
# LUXURY CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --navy: #081522;
    --navy2: #0d1e2d;
    --gold: #c8a96b;
    --gold-light: #e6cf9a;
    --cream: #f6f2e9;
    --white: #ffffff;
    --muted: #8d99a6;
    --green: #5ca77a;
    --red: #c96b6b;
    --orange: #c99455;
    --blue: #6095c7;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(200,169,107,.10), transparent 25%),
        linear-gradient(135deg, #f5f2eb 0%, #faf9f6 45%, #f1eee7 100%);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07131f 0%, #0b1b29 100%);
    border-right: 1px solid rgba(200,169,107,.20);
}

section[data-testid="stSidebar"] * {
    color: #e9e4d8 !important;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 8px 12px;
    border-radius: 8px;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #172635;
}

.hero {
    padding: 28px 34px;
    border-radius: 20px;
    margin-bottom: 25px;
    background:
        linear-gradient(115deg, rgba(7,19,31,.98), rgba(15,36,52,.92)),
        radial-gradient(circle at 80% 20%, rgba(200,169,107,.25), transparent 35%);
    box-shadow: 0 20px 45px rgba(13, 30, 45, .16);
    border: 1px solid rgba(200,169,107,.28);
}

.hero h1 {
    color: #f4ead5 !important;
    font-size: 38px;
    margin: 0;
    letter-spacing: 1px;
}

.hero p {
    color: #bfc9d2;
    margin: 8px 0 0;
    font-size: 14px;
    letter-spacing: .5px;
}

.gold-line {
    width: 70px;
    height: 3px;
    background: #c8a96b;
    margin: 14px 0;
    border-radius: 5px;
}

.metric-card {
    background: rgba(255,255,255,.88);
    border: 1px solid rgba(18,39,55,.08);
    border-radius: 16px;
    padding: 19px 20px;
    min-height: 120px;
    box-shadow: 0 8px 28px rgba(17,35,50,.07);
}

.metric-label {
    color: #8b949e;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.3px;
}

.metric-value {
    font-size: 29px;
    font-weight: 700;
    color: #172635;
    margin-top: 7px;
}

.metric-sub {
    font-size: 12px;
    color: #84909a;
    margin-top: 5px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    color: #172635;
    font-size: 25px;
    margin: 28px 0 14px;
}

.room-card {
    border-radius: 14px;
    padding: 17px;
    min-height: 160px;
    margin-bottom: 12px;
    box-shadow: 0 8px 22px rgba(16,34,49,.08);
    border: 1px solid rgba(255,255,255,.75);
    transition: all .2s ease;
}

.room-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(16,34,49,.12);
}

.room-number {
    font-family: 'Playfair Display', serif;
    font-size: 23px;
    font-weight: 700;
}

.room-type {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: .72;
    margin-top: 2px;
}

.status-pill {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 30px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .6px;
    margin-top: 12px;
}

.occupied {
    background: #f6dddd;
    color: #9d4545;
}

.vacant {
    background: #dff1e6;
    color: #367a50;
}

.cleaning {
    background: #fff0d9;
    color: #986523;
}

.maintenance {
    background: #e5e8eb;
    color: #56616c;
}

.reserved {
    background: #dce9f5;
    color: #3d6f9c;
}

.vip {
    background: linear-gradient(135deg, #fff9e9, #f3e3b6);
    color: #85672c;
}

div[data-testid="stButton"] > button {
    border-radius: 9px;
    border: 1px solid #d6c29a;
    background: #fffdf8;
    color: #263746;
    font-weight: 600;
    transition: all .2s ease;
}

div[data-testid="stButton"] > button:hover {
    border-color: #b99859;
    color: #8d6b2e;
    background: #fff9eb;
}

.primary-btn button {
    background: #122638 !important;
    color: #f4ead5 !important;
    border: 1px solid #c8a96b !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 600;
}

hr {
    border-color: rgba(20,40,55,.10);
}

.small-muted {
    color: #8b959e;
    font-size: 12px;
}

.luxury-footer {
    text-align:center;
    padding: 35px 0 10px;
    color:#8d969e;
    font-size:11px;
    letter-spacing:1px;
}

[data-testid="stMetricValue"] {
    color: #172635;
}

.stAlert {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            floor INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Vacant',
            guest_name TEXT,
            guest_phone TEXT,
            check_in TEXT,
            check_out TEXT,
            vip INTEGER DEFAULT 0,
            notes TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            confirmation_no TEXT UNIQUE NOT NULL,
            guest_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            room_number TEXT,
            room_type TEXT,
            check_in TEXT,
            check_out TEXT,
            adults INTEGER DEFAULT 1,
            children INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Confirmed',
            special_request TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS housekeeping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL,
            task TEXT NOT NULL,
            priority TEXT DEFAULT 'Normal',
            assigned_to TEXT,
            status TEXT DEFAULT 'Pending',
            updated_at TEXT
        )
    """)

    # Seed rooms only when database is empty
    count = cur.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]

    if count == 0:
        room_types = [
            ("Deluxe King", 4500000),
            ("Deluxe Twin", 4800000),
            ("Premier King", 6200000),
            ("Premier Ocean View", 7500000),
            ("Executive Suite", 10500000),
            ("Luxury Suite", 15000000),
            ("Presidential Villa", 28000000),
        ]

        rooms = []
        for floor in range(1, 6):
            for number in range(1, 9):
                room_no = f"{floor}{number:02d}"

                if floor == 5:
                    rtype, price = room_types[6]
                elif floor == 4:
                    rtype, price = room_types[5]
                elif floor == 3:
                    rtype, price = room_types[4]
                elif floor == 2:
                    rtype, price = room_types[3]
                else:
                    rtype, price = room_types[(number - 1) % 2]

                rooms.append((
                    room_no,
                    rtype,
                    floor,
                    price,
                    "Vacant",
                    None,
                    None,
                    None,
                    None,
                    0,
                    ""
                ))

        cur.executemany("""
            INSERT INTO rooms
            (room_number, room_type, floor, price, status,
             guest_name, guest_phone, check_in, check_out, vip, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rooms)

    conn.commit()
    conn.close()


init_database()


# ============================================================
# DATABASE HELPERS
# ============================================================

def query_df(sql, params=()):
    conn = get_connection()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df


def execute(sql, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def get_rooms():
    return query_df("SELECT * FROM rooms ORDER BY CAST(room_number AS INTEGER)")


def update_room_status(room_number, status):
    execute(
        "UPDATE rooms SET status=? WHERE room_number=?",
        (status, room_number)
    )


def create_reservation(data):
    execute("""
        INSERT INTO reservations
        (confirmation_no, guest_name, phone, email, room_number,
         room_type, check_in, check_out, adults, children,
         status, special_request, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div style="padding:12px 5px 22px;">
        <div style="font-family:'Playfair Display'; font-size:26px;
                    color:#e6cf9a; letter-spacing:2px;">
            AURELIA
        </div>
        <div style="font-size:9px; letter-spacing:3px;
                    color:#8998a5; margin-top:3px;">
            HOTEL MANAGEMENT SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "MAIN MENU",
        [
            "✦  Executive Dashboard",
            "▦  Room Management",
            "♢  Reservations",
            "✧  Housekeeping",
            "◈  Guest Directory",
            "⚙  System Settings",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div style="padding:10px 4px;">
        <div style="font-size:10px;color:#758694;letter-spacing:1px;">
            PROPERTY
        </div>
        <div style="font-family:'Playfair Display';font-size:17px;
                    color:#e6cf9a;margin-top:5px;">
            AURELIA GRAND HOTEL
        </div>
        <div style="font-size:11px;color:#82909c;margin-top:3px;">
            Luxury Hospitality Collection
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# COMMON HEADER
# ============================================================

def page_header(title, subtitle):
    st.markdown(f"""
    <div class="hero">
        <h1>{title}</h1>
        <div class="gold-line"></div>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label, value, subtitle=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():
    page_header(
        "Executive Dashboard",
        f"Property overview · {datetime.now().strftime('%A, %d %B %Y')}"
    )

    rooms = get_rooms()

    total = len(rooms)
    occupied = len(rooms[rooms.status == "Occupied"])
    vacant = len(rooms[rooms.status == "Vacant"])
    cleaning = len(rooms[rooms.status == "Cleaning"])
    maintenance = len(rooms[rooms.status == "Maintenance"])
    reserved = len(rooms[rooms.status == "Reserved"])

    occupancy = (occupied / total * 100) if total else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        metric_card("Total Inventory", total, "Rooms & villas")

    with c2:
        metric_card("Occupied", occupied, f"{occupancy:.1f}% occupancy")

    with c3:
        metric_card("Available", vacant, "Ready for arrival")

    with c4:
        metric_card("Housekeeping", cleaning, "Rooms being serviced")

    with c5:
        metric_card("Reserved", reserved, "Upcoming arrivals")

    st.markdown('<div class="section-title">Property Pulse</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([1.35, 1])

    with col1:
        status_data = pd.DataFrame({
            "Status": [
                "Occupied",
                "Vacant",
                "Reserved",
                "Cleaning",
                "Maintenance"
            ],
            "Rooms": [
                occupied,
                vacant,
                reserved,
                cleaning,
                maintenance
            ]
        })

        st.bar_chart(
            status_data.set_index("Status"),
            height=300
        )

    with col2:
        st.markdown("""
        <div class="metric-card" style="height:260px;">
            <div class="metric-label">Today's Operations</div>
            <div style="margin-top:18px;">
        """, unsafe_allow_html=True)

        operations = [
            ("Check-in", len(query_df(
                "SELECT * FROM reservations WHERE check_in=?",
                (date.today().isoformat(),)
            )), "Arrivals today"),
            ("Check-out", len(rooms[
                rooms.check_out == date.today().isoformat()
            ]), "Departures today"),
            ("VIP Rooms", int(rooms.vip.sum()), "VIP / special handling"),
            ("Maintenance", maintenance, "Out of service"),
        ]

        for title, value, sub in operations:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        padding:9px 0;border-bottom:1px solid #eee;">
                <div>
                    <b style="color:#273846;">{title}</b>
                    <div class="small-muted">{sub}</div>
                </div>
                <div style="font-size:20px;font-weight:700;
                            color:#b08b4c;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Live Room Status</div>',
                unsafe_allow_html=True)

    floors = sorted(rooms.floor.unique())

    for floor in floors:
        floor_rooms = rooms[rooms.floor == floor]

        st.markdown(
            f"**Floor {floor}**  "
            f"<span class='small-muted'>· {len(floor_rooms)} keys</span>",
            unsafe_allow_html=True
        )

        cols = st.columns(4)

        for i, (_, room) in enumerate(floor_rooms.iterrows()):
            status_class = {
                "Occupied": "occupied",
                "Vacant": "vacant",
                "Cleaning": "cleaning",
                "Maintenance": "maintenance",
                "Reserved": "reserved"
            }.get(room.status, "vacant")

            guest = room.guest_name or "No guest"

            with cols[i % 4]:
                st.markdown(f"""
                <div class="room-card">
                    <div class="room-number">Room {room.room_number}</div>
                    <div class="room-type">{room.room_type}</div>
                    <span class="status-pill {status_class}">
                        {room.status.upper()}
                    </span>
                    <div style="font-size:12px;color:#697580;margin-top:10px;">
                        {guest}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown(
        '<div class="luxury-footer">AURELIA GRAND HOTEL · PRIVATE & CONFIDENTIAL</div>',
        unsafe_allow_html=True
    )


# ============================================================
# ROOM MANAGEMENT
# ============================================================

def room_management():
    page_header(
        "Room Management",
        "Real-time room inventory, room status and guest allocation"
    )

    rooms = get_rooms()

    c1, c2, c3 = st.columns([1.5, 1, 1])

    with c1:
        search = st.text_input(
            "Search room",
            placeholder="Room number, room type or guest..."
        )

    with c2:
        status_filter = st.selectbox(
            "Status",
            ["All", "Vacant", "Occupied", "Reserved", "Cleaning", "Maintenance"]
        )

    with c3:
        floor_filter = st.selectbox(
            "Floor",
            ["All"] + [str(x) for x in sorted(rooms.floor.unique())]
        )

    filtered = rooms.copy()

    if search:
        mask = (
            filtered.room_number.astype(str).str.contains(search, case=False) |
            filtered.room_type.astype(str).str.contains(search, case=False) |
            filtered.guest_name.fillna("").astype(str).str.contains(search, case=False)
        )
        filtered = filtered[mask]

    if status_filter != "All":
        filtered = filtered[filtered.status == status_filter]

    if floor_filter != "All":
        filtered = filtered[filtered.floor == int(floor_filter)]

    st.markdown(
        f"<div class='small-muted' style='margin:15px 0;'>"
        f"Showing <b>{len(filtered)}</b> rooms"
        f"</div>",
        unsafe_allow_html=True
    )

    for floor in sorted(filtered.floor.unique()):
        floor_rooms = filtered[filtered.floor == floor]

        st.markdown(
            f'<div class="section-title" style="font-size:21px;">Floor {floor}</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(4)

        for i, (_, room) in enumerate(floor_rooms.iterrows()):
            status_class = {
                "Occupied": "occupied",
                "Vacant": "vacant",
                "Cleaning": "cleaning",
                "Maintenance": "maintenance",
                "Reserved": "reserved"
            }.get(room.status, "vacant")

            with cols[i % 4]:
                vip_badge = " ✦ VIP" if room.vip else ""

                st.markdown(f"""
                <div class="room-card">
                    <div class="room-number">{room.room_number}{vip_badge}</div>
                    <div class="room-type">{room.room_type}</div>
                    <span class="status-pill {status_class}">
                        {room.status.upper()}
                    </span>
                    <div style="font-size:12px;margin-top:10px;color:#697580;">
                        {room.guest_name or "Available"}
                    </div>
                    <div style="font-size:11px;margin-top:5px;color:#a08a64;">
                        {room.price:,.0f} VND / night
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("Manage"):
                    new_status = st.selectbox(
                        "Change status",
                        [
                            "Vacant",
                            "Occupied",
                            "Reserved",
                            "Cleaning",
                            "Maintenance"
                        ],
                        index=[
                            "Vacant",
                            "Occupied",
                            "Reserved",
                            "Cleaning",
                            "Maintenance"
                        ].index(room.status),
                        key=f"status_{room.room_number}"
                    )

                    guest = st.text_input(
                        "Guest",
                        value=room.guest_name or "",
                        key=f"guest_{room.room_number}"
                    )

                    if st.button(
                        "Save Changes",
                        key=f"save_{room.room_number}"
                    ):
                        execute("""
                            UPDATE rooms
                            SET status=?, guest_name=?
                            WHERE room_number=?
                        """, (new_status, guest or None, room.room_number))

                        st.success(f"Room {room.room_number} updated.")
                        time.sleep(.5)
                        st.rerun()


# ============================================================
# RESERVATIONS
# ============================================================

def reservations():
    page_header(
        "Reservations",
        "Manage arrivals, departures and luxury guest stays"
    )

    tab1, tab2 = st.tabs(["Reservation Book", "New Reservation"])

    with tab1:
        reservations_df = query_df("""
            SELECT confirmation_no AS "Confirmation",
                   guest_name AS "Guest",
                   phone AS "Phone",
                   room_number AS "Room",
                   room_type AS "Room Type",
                   check_in AS "Check-in",
                   check_out AS "Check-out",
                   adults AS "Adults",
                   children AS "Children",
                   status AS "Status"
            FROM reservations
            ORDER BY check_in DESC
        """)

        if reservations_df.empty:
            st.info("No reservations have been created yet.")
        else:
            st.dataframe(
                reservations_df,
                use_container_width=True,
                hide_index=True,
                height=450
            )

    with tab2:
        st.markdown(
            '<div class="section-title">Create New Reservation</div>',
            unsafe_allow_html=True
        )

        rooms = get_rooms()
        available_rooms = rooms[
            rooms.status.isin(["Vacant", "Reserved"])
        ]

        with st.form("new_reservation"):
            c1, c2 = st.columns(2)

            with c1:
                guest_name = st.text_input("Guest full name *")
                phone = st.text_input("Phone")
                email = st.text_input("Email")

                room_options = available_rooms.room_number.tolist()

                room_number = st.selectbox(
                    "Room *",
                    room_options if room_options else ["No room available"]
                )

                adults = st.number_input(
                    "Adults",
                    min_value=1,
                    max_value=10,
                    value=2
                )

            with c2:
                check_in = st.date_input(
                    "Check-in",
                    value=date.today()
                )

                check_out = st.date_input(
                    "Check-out",
                    value=date.today() + timedelta(days=1)
                )

                children = st.number_input(
                    "Children",
                    min_value=0,
                    max_value=10,
                    value=0
                )

                status = st.selectbox(
                    "Reservation status",
                    ["Confirmed", "Tentative", "Checked-in", "Cancelled"]
                )

            special_request = st.text_area(
                "Special requests / VIP notes",
                placeholder="Airport transfer, honeymoon setup, dietary request..."
            )

            submitted = st.form_submit_button(
                "✦  Create Reservation",
                use_container_width=True
            )

            if submitted:
                if not guest_name.strip():
                    st.error("Guest name is required.")
                elif check_out <= check_in:
                    st.error("Check-out must be after check-in.")
                elif not room_options:
                    st.error("There are no available rooms.")
                else:
                    selected_room = available_rooms[
                        available_rooms.room_number == room_number
                    ].iloc[0]

                    confirmation = (
                        "AUR-" +
                        datetime.now().strftime("%y%m%d") +
                        "-" +
                        str(int(time.time()))[-4:]
                    )

                    create_reservation((
                        confirmation,
                        guest_name,
                        phone,
                        email,
                        room_number,
                        selected_room.room_type,
                        check_in.isoformat(),
                        check_out.isoformat(),
                        adults,
                        children,
                        status,
                        special_request,
                        datetime.now().isoformat()
                    ))

                    if status in ["Confirmed", "Tentative"]:
                        update_room_status(room_number, "Reserved")

                    st.success(
                        f"Reservation {confirmation} created successfully."
                    )


# ============================================================
# HOUSEKEEPING
# ============================================================

def housekeeping():
    page_header(
        "Housekeeping Control",
        "Operational control center for room cleanliness and service"
    )

    rooms = get_rooms()

    c1, c2, c3, c4 = st.columns(4)

    pending = len(query_df(
        "SELECT * FROM housekeeping WHERE status='Pending'"
    ))

    in_progress = len(query_df(
        "SELECT * FROM housekeeping WHERE status='In Progress'"
    ))

    completed = len(query_df(
        "SELECT * FROM housekeeping WHERE status='Completed'"
    ))

    with c1:
        metric_card("Pending Tasks", pending, "Awaiting assignment")

    with c2:
        metric_card("In Progress", in_progress, "Team currently working")

    with c3:
        metric_card("Completed", completed, "Today's productivity")

    with c4:
        metric_card(
            "Cleaning Rooms",
            len(rooms[rooms.status == "Cleaning"]),
            "Rooms in service"
        )

    st.markdown(
        '<div class="section-title">Create Housekeeping Task</div>',
        unsafe_allow_html=True
    )

    with st.form("hk_task"):
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            room_number = st.selectbox(
                "Room",
                rooms.room_number.tolist()
            )

        with c2:
            task = st.selectbox(
                "Task",
                [
                    "Full Room Cleaning",
                    "Turn Down Service",
                    "Deep Cleaning",
                    "Inspection",
                    "Amenity Refill",
                    "Maintenance Follow-up"
                ]
            )

        with c3:
            priority = st.selectbox(
                "Priority",
                ["Normal", "High", "VIP", "Urgent"]
            )

        with c4:
            assigned = st.text_input(
                "Assigned to",
                placeholder="Staff name"
            )

        submitted = st.form_submit_button(
            "Assign Task",
            use_container_width=True
        )

        if submitted:
            execute("""
                INSERT INTO housekeeping
                (room_number, task, priority, assigned_to, status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                room_number,
                task,
                priority,
                assigned,
                "Pending",
                datetime.now().isoformat()
            ))

            update_room_status(room_number, "Cleaning")
            st.success("Housekeeping task assigned.")
            time.sleep(.5)
            st.rerun()

    st.markdown(
        '<div class="section-title">Task Board</div>',
        unsafe_allow_html=True
    )

    tasks = query_df("""
        SELECT
            id AS ID,
            room_number AS Room,
            task AS Task,
            priority AS Priority,
            assigned_to AS "Assigned To",
            status AS Status,
            updated_at AS "Updated"
        FROM housekeeping
        ORDER BY
            CASE priority
                WHEN 'Urgent' THEN 1
                WHEN 'VIP' THEN 2
                WHEN 'High' THEN 3
                ELSE 4
            END,
            id DESC
    """)

    if tasks.empty:
        st.info("No housekeeping tasks.")
    else:
        st.dataframe(
            tasks,
            use_container_width=True,
            hide_index=True,
            height=420
        )

        st.markdown(
            '<div class="section-title" style="font-size:20px;">Update Task</div>',
            unsafe_allow_html=True
        )

        task_ids = tasks.ID.tolist()

        c1, c2, c3 = st.columns([1, 1, 2])

        with c1:
            task_id = st.selectbox("Task ID", task_ids)

        with c2:
            new_status = st.selectbox(
                "New status",
                ["Pending", "In Progress", "Completed", "Cancelled"]
            )

        with c3:
            if st.button("Update Task", use_container_width=True):
                task_row = tasks[tasks.ID == task_id].iloc[0]

                execute("""
                    UPDATE housekeeping
                    SET status=?, updated_at=?
                    WHERE id=?
                """, (
                    new_status,
                    datetime.now().isoformat(),
                    task_id
                ))

                if new_status == "Completed":
                    update_room_status(
                        task_row.Room,
                        "Vacant"
                    )

                st.success("Task updated.")
                time.sleep(.5)
                st.rerun()


# ============================================================
# GUEST DIRECTORY
# ============================================================

def guest_directory():
    page_header(
        "Guest Directory",
        "Guest profiles and current in-house information"
    )

    rooms = get_rooms()

    guests = rooms[
        rooms.guest_name.notna() &
        (rooms.guest_name.astype(str).str.strip() != "")
    ].copy()

    if guests.empty:
        st.info("There are currently no in-house guests.")
        return

    search = st.text_input(
        "Search guest",
        placeholder="Guest name or phone number..."
    )

    if search:
        guests = guests[
            guests.guest_name.astype(str).str.contains(
                search, case=False
            ) |
            guests.guest_phone.fillna("").astype(str).str.contains(
                search, case=False
            )
        ]

    st.markdown(
        f"<div class='small-muted'>{len(guests)} guest records</div>",
        unsafe_allow_html=True
    )

    for _, guest in guests.iterrows():
        vip = " ✦ VIP" if guest.vip else ""

        st.markdown(f"""
        <div class="metric-card" style="margin-top:12px;">
            <div style="display:flex;justify-content:space-between;">
                <div>
                    <div style="font-family:'Playfair Display';
                                font-size:21px;color:#1a2b39;">
                        {guest.guest_name}{vip}
                    </div>
                    <div class="small-muted">
                        Room {guest.room_number} · {guest.room_type}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="status-pill occupied">IN HOUSE</div>
                    <div class="small-muted" style="margin-top:7px;">
                        {guest.guest_phone or "No phone"}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# SETTINGS
# ============================================================

def settings():
    page_header(
        "System Settings",
        "Property configuration and database utilities"
    )

    st.markdown(
        '<div class="section-title">Property Profile</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.text_input(
            "Hotel name",
            value="Aurelia Grand Hotel"
        )

        st.text_input(
            "Property type",
            value="Luxury 5-Star Hotel & Resort"
        )

    with c2:
        st.text_input(
            "Currency",
            value="VND"
        )

        st.text_input(
            "Timezone",
            value="Asia/Ho_Chi_Minh"
        )

    st.markdown(
        '<div class="section-title">Database</div>',
        unsafe_allow_html=True
    )

    rooms = get_rooms()
    reservations_df = query_df("SELECT * FROM reservations")
    hk_df = query_df("SELECT * FROM housekeeping")

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "Rooms",
            len(rooms),
            "Records in database"
        )

    with c2:
        metric_card(
            "Reservations",
            len(reservations_df),
            "Reservation records"
        )

    with c3:
        metric_card(
            "HK Tasks",
            len(hk_df),
            "Operational records"
        )

    st.warning(
        "Resetting the database will permanently delete all current "
        "reservations, housekeeping tasks and room guest information."
    )

    if st.button(
        "Reset Demo Database",
        type="secondary"
    ):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS rooms")
        cur.execute("DROP TABLE IF EXISTS reservations")
        cur.execute("DROP TABLE IF EXISTS housekeeping")

        conn.commit()
        conn.close()

        init_database()

        st.success("Demo database has been reset.")
        time.sleep(.8)
        st.rerun()


# ============================================================
# ROUTER
# ============================================================

if page == "✦  Executive Dashboard":
    dashboard()

elif page == "▦  Room Management":
    room_management()

elif page == "♢  Reservations":
    reservations()

elif page == "✧  Housekeeping":
    housekeeping()

elif page == "◈  Guest Directory":
    guest_directory()

elif page == "⚙  System Settings":
    settings()
