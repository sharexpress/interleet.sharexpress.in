# Copyright 2026 Sharexpress Contributors
# Module 3: Case Study - Cab Booking App (Joins) (10 Problems)

import json

MODULE3_CHALLENGES = [
    # 24. All Trips and Riders
    {
        "title": "Cab Booking: All Trips and Riders",
        "slug": "sql-cab-all-trips-riders",
        "short_description": "Retrieve completed and scheduled trips matched with rider identity.",
        "description": (
            "### Problem Statement\n\n"
            "The cab dispatch system tracks ride bookings and customer accounts. "
            "Write a SQL query using an `INNER JOIN` between `trips` and `riders` to list each trip's ID, "
            "the rider's name, pickup location, dropoff location, and fare.\n\n"
            "#### Table Schema: `riders`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `rider_id` | INT (PK) | Rider account identifier |\n"
            "| `name` | TEXT | Customer full name |\n"
            "| `phone` | TEXT | Contact number |\n"
            "| `rating` | REAL | Rider star rating |\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip transaction identifier |\n"
            "| `rider_id` | INT | Foreign key to `riders` |\n"
            "| `driver_id` | INT | Foreign key to `drivers` |\n"
            "| `pickup_location` | TEXT | Starting area |\n"
            "| `dropoff_location` | TEXT | Destination area |\n"
            "| `fare` | REAL | Total ride fare in dollars |\n"
            "| `status` | TEXT | Trip status ('Completed', 'Cancelled') |\n\n"
            "#### Output Requirements\n"
            "Return `trip_id`, `rider_name` (aliased from `riders.name`), `pickup_location`, `dropoff_location`, and `fare`.\n"
            "Order by `trip_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "JOIN", "INNER JOIN", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Inner Join", "Foreign Key Matching", "Column Aliasing"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE riders ("
            "  rider_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  phone TEXT NOT NULL,"
            "  rating REAL NOT NULL"
            ");"
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  rider_id INT NOT NULL,"
            "  driver_id INT,"
            "  pickup_location TEXT NOT NULL,"
            "  dropoff_location TEXT NOT NULL,"
            "  fare REAL NOT NULL,"
            "  status TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "riders": [
                {"rider_id": 1, "name": "Alice Johnson", "phone": "555-0101", "rating": 4.9},
                {"rider_id": 2, "name": "Bob Smith", "phone": "555-0102", "rating": 4.7},
                {"rider_id": 3, "name": "Charlie Brown", "phone": "555-0103", "rating": 4.5},
                {"rider_id": 4, "name": "Diana Prince", "phone": "555-0104", "rating": 5.0}
            ],
            "trips": [
                {"trip_id": 101, "rider_id": 1, "driver_id": 11, "pickup_location": "Downtown", "dropoff_location": "Airport", "fare": 35.50, "status": "Completed"},
                {"trip_id": 102, "rider_id": 2, "driver_id": 12, "pickup_location": "Uptown", "dropoff_location": "Midtown", "fare": 18.00, "status": "Completed"},
                {"trip_id": 103, "rider_id": 1, "driver_id": 11, "pickup_location": "Suburbs", "dropoff_location": "Downtown", "fare": 24.75, "status": "Completed"},
                {"trip_id": 104, "rider_id": 3, "driver_id": 13, "pickup_location": "Tech Park", "dropoff_location": "Station", "fare": 12.00, "status": "Cancelled"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Retrieve completed and scheduled trips matched with rider identity.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Retrieve completed and scheduled trips matched with rider identity.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Retrieve completed and scheduled trips matched with rider identity.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Retrieve completed and scheduled trips matched with rider identity.\n\n"
        },
        "canonical_solution": (
            "SELECT t.trip_id, r.name AS rider_name, t.pickup_location, t.dropoff_location, t.fare "
            "FROM trips t "
            "JOIN riders r ON t.rider_id = r.rider_id "
            "ORDER BY t.trip_id ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-trips-riders-tc-1", "name": "Standard Trip Rider Match", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE riders (rider_id INT PRIMARY KEY, name TEXT NOT NULL, phone TEXT NOT NULL, rating REAL NOT NULL);"
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, rider_id INT NOT NULL, driver_id INT, pickup_location TEXT NOT NULL, dropoff_location TEXT NOT NULL, fare REAL NOT NULL, status TEXT NOT NULL);"
                    ),
                    "fixtures": {
                        "riders": [
                            {"rider_id": 1, "name": "Alice Johnson", "phone": "555-0101", "rating": 4.9},
                            {"rider_id": 2, "name": "Bob Smith", "phone": "555-0102", "rating": 4.7},
                            {"rider_id": 3, "name": "Charlie Brown", "phone": "555-0103", "rating": 4.5},
                            {"rider_id": 4, "name": "Diana Prince", "phone": "555-0104", "rating": 5.0}
                        ],
                        "trips": [
                            {"trip_id": 101, "rider_id": 1, "driver_id": 11, "pickup_location": "Downtown", "dropoff_location": "Airport", "fare": 35.50, "status": "Completed"},
                            {"trip_id": 102, "rider_id": 2, "driver_id": 12, "pickup_location": "Uptown", "dropoff_location": "Midtown", "fare": 18.00, "status": "Completed"},
                            {"trip_id": 103, "rider_id": 1, "driver_id": 11, "pickup_location": "Suburbs", "dropoff_location": "Downtown", "fare": 24.75, "status": "Completed"},
                            {"trip_id": 104, "rider_id": 3, "driver_id": 13, "pickup_location": "Tech Park", "dropoff_location": "Station", "fare": 12.00, "status": "Cancelled"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"trip_id": 101, "rider_name": "Alice Johnson", "pickup_location": "Downtown", "dropoff_location": "Airport", "fare": 35.5},
                    {"trip_id": 102, "rider_name": "Bob Smith", "pickup_location": "Uptown", "dropoff_location": "Midtown", "fare": 18.0},
                    {"trip_id": 103, "rider_name": "Alice Johnson", "pickup_location": "Suburbs", "dropoff_location": "Downtown", "fare": 24.75},
                    {"trip_id": 104, "rider_name": "Charlie Brown", "pickup_location": "Tech Park", "dropoff_location": "Station", "fare": 12.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 25. Completed Driver Trips
    {
        "title": "Cab Booking: Completed Driver Trips",
        "slug": "sql-cab-completed-driver-trips",
        "short_description": "Join trips and drivers for fulfilled rides with distance and vehicle type.",
        "description": (
            "### Problem Statement\n\n"
            "The operations team wants a log of all successfully fulfilled rides (`status = 'Completed'`). "
            "Join `trips` with `drivers` on `driver_id` to display the trip ID, driver's name, vehicle type, "
            "trip fare, and distance in kilometers.\n\n"
            "#### Table Schema: `drivers`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `driver_id` | INT (PK) | Driver identification number |\n"
            "| `name` | TEXT | Driver full name |\n"
            "| `vehicle_type` | TEXT | Category ('Sedan', 'SUV', 'Hatchback') |\n"
            "| `rating` | REAL | Driver performance rating |\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip transaction identifier |\n"
            "| `driver_id` | INT | Foreign key to `drivers` |\n"
            "| `distance_km` | REAL | Distance traversed in km |\n"
            "| `fare` | REAL | Trip price |\n"
            "| `status` | TEXT | Trip status |\n\n"
            "#### Output Requirements\n"
            "Return `trip_id`, `driver_name` (aliased from `drivers.name`), `vehicle_type`, `fare`, and `distance_km`.\n"
            "Filter for `status = 'Completed'` and order by `trip_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "JOIN", "INNER JOIN", "Filtering"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Inner Join", "Filter Predicates", "Multi-table Attributes"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 55, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE drivers ("
            "  driver_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  vehicle_type TEXT NOT NULL,"
            "  rating REAL NOT NULL"
            ");"
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  driver_id INT,"
            "  distance_km REAL NOT NULL,"
            "  fare REAL NOT NULL,"
            "  status TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "drivers": [
                {"driver_id": 11, "name": "Marcus Kane", "vehicle_type": "Sedan", "rating": 4.85},
                {"driver_id": 12, "name": "Elena Rostova", "vehicle_type": "SUV", "rating": 4.92},
                {"driver_id": 13, "name": "Devon Miller", "vehicle_type": "Hatchback", "rating": 4.60}
            ],
            "trips": [
                {"trip_id": 201, "driver_id": 11, "distance_km": 18.5, "fare": 32.00, "status": "Completed"},
                {"trip_id": 202, "driver_id": 12, "distance_km": 6.2, "fare": 14.50, "status": "Completed"},
                {"trip_id": 203, "driver_id": 13, "distance_km": 11.0, "fare": 20.00, "status": "Cancelled"},
                {"trip_id": 204, "driver_id": 11, "distance_km": 24.1, "fare": 45.00, "status": "Completed"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Join trips and drivers for fulfilled rides with distance and vehicle type.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Join trips and drivers for fulfilled rides with distance and vehicle type.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Join trips and drivers for fulfilled rides with distance and vehicle type.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Join trips and drivers for fulfilled rides with distance and vehicle type.\n\n"
        },
        "canonical_solution": (
            "SELECT t.trip_id, d.name AS driver_name, d.vehicle_type, t.fare, t.distance_km "
            "FROM trips t "
            "JOIN drivers d ON t.driver_id = d.driver_id "
            "WHERE t.status = 'Completed' "
            "ORDER BY t.trip_id ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-completed-drivers-tc-1", "name": "Completed Trips Driver Join", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE drivers (driver_id INT PRIMARY KEY, name TEXT NOT NULL, vehicle_type TEXT NOT NULL, rating REAL NOT NULL);"
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, driver_id INT, distance_km REAL NOT NULL, fare REAL NOT NULL, status TEXT NOT NULL);"
                    ),
                    "fixtures": {
                        "drivers": [
                            {"driver_id": 11, "name": "Marcus Kane", "vehicle_type": "Sedan", "rating": 4.85},
                            {"driver_id": 12, "name": "Elena Rostova", "vehicle_type": "SUV", "rating": 4.92},
                            {"driver_id": 13, "name": "Devon Miller", "vehicle_type": "Hatchback", "rating": 4.60}
                        ],
                        "trips": [
                            {"trip_id": 201, "driver_id": 11, "distance_km": 18.5, "fare": 32.00, "status": "Completed"},
                            {"trip_id": 202, "driver_id": 12, "distance_km": 6.2, "fare": 14.50, "status": "Completed"},
                            {"trip_id": 203, "driver_id": 13, "distance_km": 11.0, "fare": 20.00, "status": "Cancelled"},
                            {"trip_id": 204, "driver_id": 11, "distance_km": 24.1, "fare": 45.00, "status": "Completed"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"trip_id": 201, "driver_name": "Marcus Kane", "vehicle_type": "Sedan", "fare": 32.0, "distance_km": 18.5},
                    {"trip_id": 202, "driver_name": "Elena Rostova", "vehicle_type": "SUV", "fare": 14.5, "distance_km": 6.2},
                    {"trip_id": 204, "driver_name": "Marcus Kane", "vehicle_type": "Sedan", "fare": 45.0, "distance_km": 24.1}
                ], indent=2) + "\n"
            }
        ]
    },

    # 26. All Riders and Their Trips (Left Join)
    {
        "title": "Cab Booking: All Riders and Trip History",
        "slug": "sql-cab-all-riders-trip-status",
        "short_description": "Produce a comprehensive rider audit including users without any bookings.",
        "description": (
            "### Problem Statement\n\n"
            "Growth marketing wants to audit every rider in the database, including prospective riders "
            "who signed up but haven't booked any trip yet. "
            "Perform a `LEFT JOIN` from `riders` to `trips` to show rider ID, name, trip ID, and fare.\n\n"
            "#### Table Schema: `riders`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `rider_id` | INT (PK) | Rider ID |\n"
            "| `name` | TEXT | Full name |\n"
            "| `signup_date` | TEXT | Registration date |\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip identifier |\n"
            "| `rider_id` | INT | Rider ID foreign key |\n"
            "| `fare` | REAL | Fare amount |\n\n"
            "#### Output Requirements\n"
            "Return `rider_id`, `name`, `trip_id`, and `fare`.\n"
            "Order by `r.rider_id ASC`, `t.trip_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "JOIN", "LEFT JOIN", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Left Outer Join", "Preserving Unmatched Rows", "NULL Handling"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 55, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE riders ("
            "  rider_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  signup_date TEXT NOT NULL"
            ");"
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  rider_id INT NOT NULL,"
            "  fare REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "riders": [
                {"rider_id": 1, "name": "Sarah Connor", "signup_date": "2026-01-10"},
                {"rider_id": 2, "name": "John Connor", "signup_date": "2026-01-12"},
                {"rider_id": 3, "name": "Kyle Reese", "signup_date": "2026-02-01"}
            ],
            "trips": [
                {"trip_id": 301, "rider_id": 1, "fare": 25.00},
                {"trip_id": 302, "rider_id": 1, "fare": 42.50},
                {"trip_id": 303, "rider_id": 2, "fare": 16.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Produce a comprehensive rider audit including users without any bookings.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Produce a comprehensive rider audit including users without any bookings.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Produce a comprehensive rider audit including users without any bookings.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Produce a comprehensive rider audit including users without any bookings.\n\n"
        },
        "canonical_solution": (
            "SELECT r.rider_id, r.name, t.trip_id, t.fare "
            "FROM riders r "
            "LEFT JOIN trips t ON r.rider_id = t.rider_id "
            "ORDER BY r.rider_id ASC, t.trip_id ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-all-riders-tc-1", "name": "Rider Booking History Left Join", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE riders (rider_id INT PRIMARY KEY, name TEXT NOT NULL, signup_date TEXT NOT NULL);"
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, rider_id INT NOT NULL, fare REAL NOT NULL);"
                    ),
                    "fixtures": {
                        "riders": [
                            {"rider_id": 1, "name": "Sarah Connor", "signup_date": "2026-01-10"},
                            {"rider_id": 2, "name": "John Connor", "signup_date": "2026-01-12"},
                            {"rider_id": 3, "name": "Kyle Reese", "signup_date": "2026-02-01"}
                        ],
                        "trips": [
                            {"trip_id": 301, "rider_id": 1, "fare": 25.00},
                            {"trip_id": 302, "rider_id": 1, "fare": 42.50},
                            {"trip_id": 303, "rider_id": 2, "fare": 16.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"rider_id": 1, "name": "Sarah Connor", "trip_id": 301, "fare": 25.0},
                    {"rider_id": 1, "name": "Sarah Connor", "trip_id": 302, "fare": 42.5},
                    {"rider_id": 2, "name": "John Connor", "trip_id": 303, "fare": 16.0},
                    {"rider_id": 3, "name": "Kyle Reese", "trip_id": None, "fare": None}
                ], indent=2) + "\n"
            }
        ]
    },

    # 27. Inactive Drivers (Left Join with IS NULL)
    {
        "title": "Cab Booking: Find Inactive Drivers",
        "slug": "sql-cab-inactive-drivers",
        "short_description": "Isolate registered drivers who have not accepted any rides.",
        "description": (
            "### Problem Statement\n\n"
            "Fleet operations needs to identify drivers who are currently registered in `drivers` "
            "but have zero associated records in the `trips` table. "
            "Write a SQL query using a `LEFT JOIN` and an `IS NULL` check to find all such drivers.\n\n"
            "#### Table Schema: `drivers`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `driver_id` | INT (PK) | Driver identification number |\n"
            "| `name` | TEXT | Driver full name |\n"
            "| `vehicle_plate` | TEXT | License plate number |\n"
            "| `joined_date` | TEXT | Date driver onboarded |\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip transaction identifier |\n"
            "| `driver_id` | INT | Driver identifier |\n\n"
            "#### Output Requirements\n"
            "Return `driver_id`, `name`, and `vehicle_plate` for drivers who have never completed or received a trip.\n"
            "Order by `driver_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "JOIN", "LEFT JOIN", "IS NULL", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Anti-Join Pattern", "LEFT JOIN with IS NULL", "Filtering Nulls"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE drivers ("
            "  driver_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  vehicle_plate TEXT NOT NULL,"
            "  joined_date TEXT NOT NULL"
            ");"
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  driver_id INT"
            ");"
        ),
        "fixtures": {
            "drivers": [
                {"driver_id": 10, "name": "Liam Neeson", "vehicle_plate": "NYC-4921", "joined_date": "2026-01-05"},
                {"driver_id": 20, "name": "Bruce Willis", "vehicle_plate": "LA-8832", "joined_date": "2026-01-15"},
                {"driver_id": 30, "name": "Keanu Reeves", "vehicle_plate": "CHI-1092", "joined_date": "2026-02-01"},
                {"driver_id": 40, "name": "Tom Cruise", "vehicle_plate": "MIA-7711", "joined_date": "2026-02-10"}
            ],
            "trips": [
                {"trip_id": 1, "driver_id": 10},
                {"trip_id": 2, "driver_id": 30},
                {"trip_id": 3, "driver_id": 10}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Isolate registered drivers who have not accepted any rides.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Isolate registered drivers who have not accepted any rides.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Isolate registered drivers who have not accepted any rides.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Isolate registered drivers who have not accepted any rides.\n\n"
        },
        "canonical_solution": (
            "SELECT d.driver_id, d.name, d.vehicle_plate "
            "FROM drivers d "
            "LEFT JOIN trips t ON d.driver_id = t.driver_id "
            "WHERE t.trip_id IS NULL "
            "ORDER BY d.driver_id ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-inactive-drivers-tc-1", "name": "Anti-Join Zero Trips Scan", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE drivers (driver_id INT PRIMARY KEY, name TEXT NOT NULL, vehicle_plate TEXT NOT NULL, joined_date TEXT NOT NULL);"
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, driver_id INT);"
                    ),
                    "fixtures": {
                        "drivers": [
                            {"driver_id": 10, "name": "Liam Neeson", "vehicle_plate": "NYC-4921", "joined_date": "2026-01-05"},
                            {"driver_id": 20, "name": "Bruce Willis", "vehicle_plate": "LA-8832", "joined_date": "2026-01-15"},
                            {"driver_id": 30, "name": "Keanu Reeves", "vehicle_plate": "CHI-1092", "joined_date": "2026-02-01"},
                            {"driver_id": 40, "name": "Tom Cruise", "vehicle_plate": "MIA-7711", "joined_date": "2026-02-10"}
                        ],
                        "trips": [
                            {"trip_id": 1, "driver_id": 10},
                            {"trip_id": 2, "driver_id": 30},
                            {"trip_id": 3, "driver_id": 10}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"driver_id": 20, "name": "Bruce Willis", "vehicle_plate": "LA-8832"},
                    {"driver_id": 40, "name": "Tom Cruise", "vehicle_plate": "MIA-7711"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 28. Unified Trip Dossier (Three-Table Join)
    {
        "title": "Cab Booking: Unified Trip Dossier",
        "slug": "sql-cab-full-trip-dossier",
        "short_description": "Join trips, riders, and drivers to compile complete ride manifest.",
        "description": (
            "### Problem Statement\n\n"
            "The customer care center requires a unified dispatch log combining passenger names, "
            "assigned driver names, vehicle classes, and trip fare amounts. "
            "Perform a 3-table join (`trips`, `riders`, and `drivers`) for all completed trips.\n\n"
            "#### Table Schema: `riders`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `rider_id` | INT (PK) | Rider ID |\n"
            "| `name` | TEXT | Passenger full name |\n\n"
            "#### Table Schema: `drivers`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `driver_id` | INT (PK) | Driver ID |\n"
            "| `name` | TEXT | Driver full name |\n"
            "| `vehicle_type` | TEXT | Vehicle category |\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip transaction identifier |\n"
            "| `rider_id` | INT | Foreign key to `riders` |\n"
            "| `driver_id` | INT | Foreign key to `drivers` |\n"
            "| `fare` | REAL | Total ride charge |\n"
            "| `status` | TEXT | Trip status |\n\n"
            "#### Output Requirements\n"
            "Return `trip_id`, `rider_name` (from `riders.name`), `driver_name` (from `drivers.name`), "
            "`vehicle_type`, and `fare`.\n"
            "Filter for `status = 'Completed'` and order by `trip_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "JOIN", "MULTI-JOIN", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Three-Table Joins", "Foreign Key Chaining", "Status Filtering"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE riders ("
            "  rider_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL"
            ");"
            "CREATE TABLE drivers ("
            "  driver_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  vehicle_type TEXT NOT NULL"
            ");"
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  rider_id INT NOT NULL,"
            "  driver_id INT NOT NULL,"
            "  fare REAL NOT NULL,"
            "  status TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "riders": [
                {"rider_id": 1, "name": "Grace Hopper"},
                {"rider_id": 2, "name": "Alan Turing"},
                {"rider_id": 3, "name": "Ada Lovelace"}
            ],
            "drivers": [
                {"driver_id": 101, "name": "James Watt", "vehicle_type": "Sedan"},
                {"driver_id": 102, "name": "Nikola Tesla", "vehicle_type": "EV"}
            ],
            "trips": [
                {"trip_id": 501, "rider_id": 1, "driver_id": 101, "fare": 28.50, "status": "Completed"},
                {"trip_id": 502, "rider_id": 2, "driver_id": 102, "fare": 45.00, "status": "Completed"},
                {"trip_id": 503, "rider_id": 3, "driver_id": 101, "fare": 15.00, "status": "Cancelled"},
                {"trip_id": 504, "rider_id": 3, "driver_id": 102, "fare": 32.00, "status": "Completed"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Join trips, riders, and drivers to compile complete ride manifest.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Join trips, riders, and drivers to compile complete ride manifest.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Join trips, riders, and drivers to compile complete ride manifest.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Join trips, riders, and drivers to compile complete ride manifest.\n\n"
        },
        "canonical_solution": (
            "SELECT t.trip_id, r.name AS rider_name, d.name AS driver_name, d.vehicle_type, t.fare "
            "FROM trips t "
            "JOIN riders r ON t.rider_id = r.rider_id "
            "JOIN drivers d ON t.driver_id = d.driver_id "
            "WHERE t.status = 'Completed' "
            "ORDER BY t.trip_id ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-dossier-tc-1", "name": "Tri-Table Completed Ride Assembly", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE riders (rider_id INT PRIMARY KEY, name TEXT NOT NULL);"
                        "CREATE TABLE drivers (driver_id INT PRIMARY KEY, name TEXT NOT NULL, vehicle_type TEXT NOT NULL);"
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, rider_id INT NOT NULL, driver_id INT NOT NULL, fare REAL NOT NULL, status TEXT NOT NULL);"
                    ),
                    "fixtures": {
                        "riders": [
                            {"rider_id": 1, "name": "Grace Hopper"},
                            {"rider_id": 2, "name": "Alan Turing"},
                            {"rider_id": 3, "name": "Ada Lovelace"}
                        ],
                        "drivers": [
                            {"driver_id": 101, "name": "James Watt", "vehicle_type": "Sedan"},
                            {"driver_id": 102, "name": "Nikola Tesla", "vehicle_type": "EV"}
                        ],
                        "trips": [
                            {"trip_id": 501, "rider_id": 1, "driver_id": 101, "fare": 28.50, "status": "Completed"},
                            {"trip_id": 502, "rider_id": 2, "driver_id": 102, "fare": 45.00, "status": "Completed"},
                            {"trip_id": 503, "rider_id": 3, "driver_id": 101, "fare": 15.00, "status": "Cancelled"},
                            {"trip_id": 504, "rider_id": 3, "driver_id": 102, "fare": 32.00, "status": "Completed"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"trip_id": 501, "rider_name": "Grace Hopper", "driver_name": "James Watt", "vehicle_type": "Sedan", "fare": 28.5},
                    {"trip_id": 502, "rider_name": "Alan Turing", "driver_name": "Nikola Tesla", "vehicle_type": "EV", "fare": 45.0},
                    {"trip_id": 504, "rider_name": "Ada Lovelace", "driver_name": "Nikola Tesla", "vehicle_type": "EV", "fare": 32.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 29. Trips with Unresolved Complaints
    {
        "title": "Cab Booking: Trips with Unresolved Complaints",
        "slug": "sql-cab-trips-with-complaints",
        "short_description": "Isolate high-friction trips by joining trips with unresolved grievance tickets.",
        "description": (
            "### Problem Statement\n\n"
            "The safety and trust department monitors unresolved rider complaints (`resolved = 0`). "
            "Write a SQL query joining `trips` with `complaints` on `trip_id` to report "
            "the trip ID, trip date, fare, complaint issue category, and severity.\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip transaction identifier |\n"
            "| `trip_date` | TEXT | Date of ride |\n"
            "| `fare` | REAL | Ride fare |\n\n"
            "#### Table Schema: `complaints`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `complaint_id` | INT (PK) | Complaint ticket ID |\n"
            "| `trip_id` | INT | Associated trip ID |\n"
            "| `issue_category` | TEXT | Reason ('Route Deviation', 'Vehicle Cleanliness', 'Rash Driving') |\n"
            "| `severity` | TEXT | Priority level ('Low', 'Medium', 'High') |\n"
            "| `resolved` | INT | Resolution status (1 for resolved, 0 for open) |\n\n"
            "#### Output Requirements\n"
            "Return `trip_id`, `trip_date`, `fare`, `issue_category`, and `severity` for unresolved complaints.\n"
            "Order by `trip_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "JOIN", "INNER JOIN", "Filtering", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Table Joining", "Conditional Filtering", "Audit Queries"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  trip_date TEXT NOT NULL,"
            "  fare REAL NOT NULL"
            ");"
            "CREATE TABLE complaints ("
            "  complaint_id INT PRIMARY KEY,"
            "  trip_id INT NOT NULL,"
            "  issue_category TEXT NOT NULL,"
            "  severity TEXT NOT NULL,"
            "  resolved INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "trips": [
                {"trip_id": 601, "trip_date": "2026-03-01", "fare": 34.00},
                {"trip_id": 602, "trip_date": "2026-03-01", "fare": 18.50},
                {"trip_id": 603, "trip_date": "2026-03-02", "fare": 52.00},
                {"trip_id": 604, "trip_date": "2026-03-02", "fare": 12.00}
            ],
            "complaints": [
                {"complaint_id": 1, "trip_id": 601, "issue_category": "Rash Driving", "severity": "High", "resolved": 0},
                {"complaint_id": 2, "trip_id": 602, "issue_category": "Vehicle Cleanliness", "severity": "Low", "resolved": 1},
                {"complaint_id": 3, "trip_id": 603, "issue_category": "Route Deviation", "severity": "Medium", "resolved": 0}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Isolate high-friction trips by joining trips with unresolved grievance tickets.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Isolate high-friction trips by joining trips with unresolved grievance tickets.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Isolate high-friction trips by joining trips with unresolved grievance tickets.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Isolate high-friction trips by joining trips with unresolved grievance tickets.\n\n"
        },
        "canonical_solution": (
            "SELECT t.trip_id, t.trip_date, t.fare, c.issue_category, c.severity "
            "FROM trips t "
            "JOIN complaints c ON t.trip_id = c.trip_id "
            "WHERE c.resolved = 0 "
            "ORDER BY t.trip_id ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-complaints-tc-1", "name": "Unresolved Complaints Join", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, trip_date TEXT NOT NULL, fare REAL NOT NULL);"
                        "CREATE TABLE complaints (complaint_id INT PRIMARY KEY, trip_id INT NOT NULL, issue_category TEXT NOT NULL, severity TEXT NOT NULL, resolved INT NOT NULL);"
                    ),
                    "fixtures": {
                        "trips": [
                            {"trip_id": 601, "trip_date": "2026-03-01", "fare": 34.00},
                            {"trip_id": 602, "trip_date": "2026-03-01", "fare": 18.50},
                            {"trip_id": 603, "trip_date": "2026-03-02", "fare": 52.00},
                            {"trip_id": 604, "trip_date": "2026-03-02", "fare": 12.00}
                        ],
                        "complaints": [
                            {"complaint_id": 1, "trip_id": 601, "issue_category": "Rash Driving", "severity": "High", "resolved": 0},
                            {"complaint_id": 2, "trip_id": 602, "issue_category": "Vehicle Cleanliness", "severity": "Low", "resolved": 1},
                            {"complaint_id": 3, "trip_id": 603, "issue_category": "Route Deviation", "severity": "Medium", "resolved": 0}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"trip_id": 601, "trip_date": "2026-03-01", "fare": 34.0, "issue_category": "Rash Driving", "severity": "High"},
                    {"trip_id": 603, "trip_date": "2026-03-02", "fare": 52.0, "issue_category": "Route Deviation", "severity": "Medium"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 30. Vehicle Performance Analytics
    {
        "title": "Cab Booking: Vehicle Performance Analytics",
        "slug": "sql-cab-vehicle-performance",
        "short_description": "Aggregate ride counts, total revenue, and average distance by vehicle class.",
        "description": (
            "### Problem Statement\n\n"
            "The fleet economics group wants to compare commercial performance across vehicle categories. "
            "Join `drivers` and `trips` to compute the total completed trips, total fare revenue, "
            "and average distance traveled per vehicle type for completed trips (`status = 'Completed'`).\n\n"
            "#### Table Schema: `drivers`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `driver_id` | INT (PK) | Driver ID |\n"
            "| `vehicle_type` | TEXT | Category ('Sedan', 'SUV', 'Hatchback') |\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip ID |\n"
            "| `driver_id` | INT | Driver ID |\n"
            "| `distance_km` | REAL | Distance in kilometers |\n"
            "| `fare` | REAL | Ride fare |\n"
            "| `status` | TEXT | Ride status |\n\n"
            "#### Output Requirements\n"
            "Return `vehicle_type`, `total_trips`, `total_revenue` (rounded to 2 decimal places), "
            "and `avg_distance` (rounded to 2 decimal places).\n"
            "Order by `total_revenue DESC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "JOIN", "GROUP BY", "AGGREGATION", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Aggregating Joined Tables", "ROUND Function", "GROUP BY Vehicle Type"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE drivers ("
            "  driver_id INT PRIMARY KEY,"
            "  vehicle_type TEXT NOT NULL"
            ");"
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  driver_id INT NOT NULL,"
            "  distance_km REAL NOT NULL,"
            "  fare REAL NOT NULL,"
            "  status TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "drivers": [
                {"driver_id": 1, "vehicle_type": "Sedan"},
                {"driver_id": 2, "vehicle_type": "SUV"},
                {"driver_id": 3, "vehicle_type": "Sedan"},
                {"driver_id": 4, "vehicle_type": "Hatchback"}
            ],
            "trips": [
                {"trip_id": 10, "driver_id": 1, "distance_km": 15.0, "fare": 30.00, "status": "Completed"},
                {"trip_id": 11, "driver_id": 2, "distance_km": 25.0, "fare": 65.50, "status": "Completed"},
                {"trip_id": 12, "driver_id": 3, "distance_km": 10.0, "fare": 22.00, "status": "Completed"},
                {"trip_id": 13, "driver_id": 2, "distance_km": 30.0, "fare": 74.50, "status": "Completed"},
                {"trip_id": 14, "driver_id": 4, "distance_km": 8.0, "fare": 16.00, "status": "Cancelled"},
                {"trip_id": 15, "driver_id": 4, "distance_km": 12.0, "fare": 24.00, "status": "Completed"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Aggregate ride counts, total revenue, and average distance by vehicle class.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Aggregate ride counts, total revenue, and average distance by vehicle class.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Aggregate ride counts, total revenue, and average distance by vehicle class.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Aggregate ride counts, total revenue, and average distance by vehicle class.\n\n"
        },
        "canonical_solution": (
            "SELECT d.vehicle_type, COUNT(t.trip_id) AS total_trips, "
            "ROUND(SUM(t.fare), 2) AS total_revenue, "
            "ROUND(AVG(t.distance_km), 2) AS avg_distance "
            "FROM drivers d "
            "JOIN trips t ON d.driver_id = t.driver_id "
            "WHERE t.status = 'Completed' "
            "GROUP BY d.vehicle_type "
            "ORDER BY total_revenue DESC;"
        ),
        "test_cases": [
            {
                "id": "cab-vehicle-perf-tc-1", "name": "Vehicle Segment Aggregation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE drivers (driver_id INT PRIMARY KEY, vehicle_type TEXT NOT NULL);"
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, driver_id INT NOT NULL, distance_km REAL NOT NULL, fare REAL NOT NULL, status TEXT NOT NULL);"
                    ),
                    "fixtures": {
                        "drivers": [
                            {"driver_id": 1, "vehicle_type": "Sedan"},
                            {"driver_id": 2, "vehicle_type": "SUV"},
                            {"driver_id": 3, "vehicle_type": "Sedan"},
                            {"driver_id": 4, "vehicle_type": "Hatchback"}
                        ],
                        "trips": [
                            {"trip_id": 10, "driver_id": 1, "distance_km": 15.0, "fare": 30.00, "status": "Completed"},
                            {"trip_id": 11, "driver_id": 2, "distance_km": 25.0, "fare": 65.50, "status": "Completed"},
                            {"trip_id": 12, "driver_id": 3, "distance_km": 10.0, "fare": 22.00, "status": "Completed"},
                            {"trip_id": 13, "driver_id": 2, "distance_km": 30.0, "fare": 74.50, "status": "Completed"},
                            {"trip_id": 14, "driver_id": 4, "distance_km": 8.0, "fare": 16.00, "status": "Cancelled"},
                            {"trip_id": 15, "driver_id": 4, "distance_km": 12.0, "fare": 24.00, "status": "Completed"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"vehicle_type": "SUV", "total_trips": 2, "total_revenue": 140.0, "avg_distance": 27.5},
                    {"vehicle_type": "Sedan", "total_trips": 2, "total_revenue": 52.0, "avg_distance": 12.5},
                    {"vehicle_type": "Hatchback", "total_trips": 1, "total_revenue": 24.0, "avg_distance": 12.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 31. Zone and Vehicle Class Matrix (Cross Join)
    {
        "title": "Cab Booking: Zone and Vehicle Pricing Matrix",
        "slug": "sql-cab-cross-city-locations",
        "short_description": "Generate a full pricing matrix pairing all operational zones with vehicle categories.",
        "description": (
            "### Problem Statement\n\n"
            "The pricing team is calibrating base fares for new suburban expansions. "
            "Write a SQL query using a `CROSS JOIN` between `service_zones` and `vehicle_classes` "
            "to generate every possible pairing of service zone and vehicle tier.\n\n"
            "#### Table Schema: `service_zones`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `zone_id` | INT (PK) | Operational zone ID |\n"
            "| `zone_name` | TEXT | Zone name |\n\n"
            "#### Table Schema: `vehicle_classes`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `class_id` | INT (PK) | Vehicle class ID |\n"
            "| `class_name` | TEXT | Tier name ('Economy', 'Comfort', 'Executive') |\n"
            "| `base_fare` | REAL | Starting minimum fare |\n\n"
            "#### Output Requirements\n"
            "Return `zone_name`, `class_name`, and `base_fare`.\n"
            "Order by `zone_name ASC`, `class_name ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "JOIN", "CROSS JOIN", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Cartesian Product", "Cross Join", "Pricing Matrix Creation"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE service_zones ("
            "  zone_id INT PRIMARY KEY,"
            "  zone_name TEXT NOT NULL"
            ");"
            "CREATE TABLE vehicle_classes ("
            "  class_id INT PRIMARY KEY,"
            "  class_name TEXT NOT NULL,"
            "  base_fare REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "service_zones": [
                {"zone_id": 1, "zone_name": "Downtown"},
                {"zone_id": 2, "zone_name": "Metro North"}
            ],
            "vehicle_classes": [
                {"class_id": 10, "class_name": "Comfort", "base_fare": 12.00},
                {"class_id": 20, "class_name": "Economy", "base_fare": 7.50},
                {"class_id": 30, "class_name": "Executive", "base_fare": 25.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Generate a full pricing matrix pairing all operational zones with vehicle categories.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Generate a full pricing matrix pairing all operational zones with vehicle categories.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Generate a full pricing matrix pairing all operational zones with vehicle categories.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Generate a full pricing matrix pairing all operational zones with vehicle categories.\n\n"
        },
        "canonical_solution": (
            "SELECT z.zone_name, v.class_name, v.base_fare "
            "FROM service_zones z "
            "CROSS JOIN vehicle_classes v "
            "ORDER BY z.zone_name ASC, v.class_name ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-pricing-matrix-tc-1", "name": "Cartesian Matrix Generation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE service_zones (zone_id INT PRIMARY KEY, zone_name TEXT NOT NULL);"
                        "CREATE TABLE vehicle_classes (class_id INT PRIMARY KEY, class_name TEXT NOT NULL, base_fare REAL NOT NULL);"
                    ),
                    "fixtures": {
                        "service_zones": [
                            {"zone_id": 1, "zone_name": "Downtown"},
                            {"zone_id": 2, "zone_name": "Metro North"}
                        ],
                        "vehicle_classes": [
                            {"class_id": 10, "class_name": "Comfort", "base_fare": 12.00},
                            {"class_id": 20, "class_name": "Economy", "base_fare": 7.50},
                            {"class_id": 30, "class_name": "Executive", "base_fare": 25.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"zone_name": "Downtown", "class_name": "Comfort", "base_fare": 12.0},
                    {"zone_name": "Downtown", "class_name": "Economy", "base_fare": 7.5},
                    {"zone_name": "Downtown", "class_name": "Executive", "base_fare": 25.0},
                    {"zone_name": "Metro North", "class_name": "Comfort", "base_fare": 12.0},
                    {"zone_name": "Metro North", "class_name": "Economy", "base_fare": 7.5},
                    {"zone_name": "Metro North", "class_name": "Executive", "base_fare": 25.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 32. Frequent Rider-Driver Pairs
    {
        "title": "Cab Booking: Frequent Rider-Driver Pairs",
        "slug": "sql-cab-repeat-riders-drivers",
        "short_description": "Identify loyal rider and driver pairs who have completed 2 or more trips together.",
        "description": (
            "### Problem Statement\n\n"
            "For VIP customer loyalty tracking, the analytics team wants to pinpoint rider and driver pairs "
            "who have completed at least 2 trips together. "
            "Join `trips`, `riders`, and `drivers` where `status = 'Completed'`, group by the pair, "
            "and filter for combinations with `COUNT(*) >= 2`.\n\n"
            "#### Table Schema: `riders`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `rider_id` | INT (PK) | Rider ID |\n"
            "| `name` | TEXT | Rider full name |\n\n"
            "#### Table Schema: `drivers`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `driver_id` | INT (PK) | Driver ID |\n"
            "| `name` | TEXT | Driver full name |\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip transaction identifier |\n"
            "| `rider_id` | INT | Rider ID |\n"
            "| `driver_id` | INT | Driver ID |\n"
            "| `status` | TEXT | Ride status |\n\n"
            "#### Output Requirements\n"
            "Return `rider_name` (from `riders.name`), `driver_name` (from `drivers.name`), and `trip_count`.\n"
            "Order by `trip_count DESC`, `rider_name ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "JOIN", "HAVING", "GROUP BY", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Composite Group By", "HAVING Clause", "Multi-table Aggregation"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 70, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE riders ("
            "  rider_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL"
            ");"
            "CREATE TABLE drivers ("
            "  driver_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL"
            ");"
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  rider_id INT NOT NULL,"
            "  driver_id INT NOT NULL,"
            "  status TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "riders": [
                {"rider_id": 1, "name": "Emily Watson"},
                {"rider_id": 2, "name": "David Kim"}
            ],
            "drivers": [
                {"driver_id": 101, "name": "George Lucas"},
                {"driver_id": 102, "name": "Steven Spielberg"}
            ],
            "trips": [
                {"trip_id": 1, "rider_id": 1, "driver_id": 101, "status": "Completed"},
                {"trip_id": 2, "rider_id": 1, "driver_id": 101, "status": "Completed"},
                {"trip_id": 3, "rider_id": 1, "driver_id": 102, "status": "Completed"},
                {"trip_id": 4, "rider_id": 2, "driver_id": 101, "status": "Completed"},
                {"trip_id": 5, "rider_id": 1, "driver_id": 101, "status": "Completed"},
                {"trip_id": 6, "rider_id": 2, "driver_id": 102, "status": "Cancelled"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Identify loyal rider and driver pairs who have completed 2 or more trips together.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Identify loyal rider and driver pairs who have completed 2 or more trips together.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Identify loyal rider and driver pairs who have completed 2 or more trips together.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Identify loyal rider and driver pairs who have completed 2 or more trips together.\n\n"
        },
        "canonical_solution": (
            "SELECT r.name AS rider_name, d.name AS driver_name, COUNT(t.trip_id) AS trip_count "
            "FROM trips t "
            "JOIN riders r ON t.rider_id = r.rider_id "
            "JOIN drivers d ON t.driver_id = d.driver_id "
            "WHERE t.status = 'Completed' "
            "GROUP BY r.rider_id, r.name, d.driver_id, d.name "
            "HAVING COUNT(t.trip_id) >= 2 "
            "ORDER BY trip_count DESC, rider_name ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-repeat-pairs-tc-1", "name": "Frequent Rider Driver Pairs", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE riders (rider_id INT PRIMARY KEY, name TEXT NOT NULL);"
                        "CREATE TABLE drivers (driver_id INT PRIMARY KEY, name TEXT NOT NULL);"
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, rider_id INT NOT NULL, driver_id INT NOT NULL, status TEXT NOT NULL);"
                    ),
                    "fixtures": {
                        "riders": [
                            {"rider_id": 1, "name": "Emily Watson"},
                            {"rider_id": 2, "name": "David Kim"}
                        ],
                        "drivers": [
                            {"driver_id": 101, "name": "George Lucas"},
                            {"driver_id": 102, "name": "Steven Spielberg"}
                        ],
                        "trips": [
                            {"trip_id": 1, "rider_id": 1, "driver_id": 101, "status": "Completed"},
                            {"trip_id": 2, "rider_id": 1, "driver_id": 101, "status": "Completed"},
                            {"trip_id": 3, "rider_id": 1, "driver_id": 102, "status": "Completed"},
                            {"trip_id": 4, "rider_id": 2, "driver_id": 101, "status": "Completed"},
                            {"trip_id": 5, "rider_id": 1, "driver_id": 101, "status": "Completed"},
                            {"trip_id": 6, "rider_id": 2, "driver_id": 102, "status": "Cancelled"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"rider_name": "Emily Watson", "driver_name": "George Lucas", "trip_count": 3}
                ], indent=2) + "\n"
            }
        ]
    },

    # 33. Trip and Payment Reconciliation (Full Outer Join)
    {
        "title": "Cab Booking: Payment Gateway Reconciliation",
        "slug": "sql-cab-unmatched-records-audit",
        "short_description": "Perform full outer join to reconcile trips against gateway transactions.",
        "description": (
            "### Problem Statement\n\n"
            "Finance is reconciling internal trip bookings with external payment records. "
            "Some trips might be missing a gateway payment record, while some orphan payment transactions "
            "might not match any registered trip. "
            "Perform a `FULL OUTER JOIN` between `trips` and `gateway_payments` on `trip_id`.\n\n"
            "#### Table Schema: `trips`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `trip_id` | INT (PK) | Trip transaction identifier |\n"
            "| `fare` | REAL | Recorded internal fare |\n\n"
            "#### Table Schema: `gateway_payments`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `payment_id` | INT (PK) | External payment transaction ID |\n"
            "| `trip_id` | INT | Matched trip ID |\n"
            "| `amount_paid` | REAL | Settled amount |\n\n"
            "#### Output Requirements\n"
            "Return `t.trip_id`, `t.fare`, `p.payment_id`, and `p.amount_paid`.\n"
            "Order by `COALESCE(t.trip_id, p.trip_id) ASC`, `p.payment_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Hard",
        "tags": ["SQL", "JOIN", "FULL OUTER JOIN", "Financial Reconciliation", "Cab Booking"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Full Outer Join", "Data Reconciliation", "COALESCE Sorting"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 80, "estimated_time_minutes": 18,
        "schema_sql": (
            "CREATE TABLE trips ("
            "  trip_id INT PRIMARY KEY,"
            "  fare REAL NOT NULL"
            ");"
            "CREATE TABLE gateway_payments ("
            "  payment_id INT PRIMARY KEY,"
            "  trip_id INT,"
            "  amount_paid REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "trips": [
                {"trip_id": 1001, "fare": 25.00},
                {"trip_id": 1002, "fare": 40.00},
                {"trip_id": 1003, "fare": 18.50}
            ],
            "gateway_payments": [
                {"payment_id": 901, "trip_id": 1001, "amount_paid": 25.00},
                {"payment_id": 902, "trip_id": 1002, "amount_paid": 40.00},
                {"payment_id": 903, "trip_id": 9999, "amount_paid": 60.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Task: Perform full outer join to reconcile trips against gateway transactions.\n\n",
            "sqlite": "-- Write your SQLite query below\n-- Task: Perform full outer join to reconcile trips against gateway transactions.\n\n",
            "mysql": "-- Write your MySQL query below\n-- Task: Perform full outer join to reconcile trips against gateway transactions.\n\n",
            "postgresql": "-- Write your PostgreSQL query below\n-- Task: Perform full outer join to reconcile trips against gateway transactions.\n\n"
        },
        "canonical_solution": (
            "SELECT t.trip_id, t.fare, p.payment_id, p.amount_paid "
            "FROM trips t "
            "FULL OUTER JOIN gateway_payments p ON t.trip_id = p.trip_id "
            "ORDER BY COALESCE(t.trip_id, p.trip_id) ASC, p.payment_id ASC;"
        ),
        "test_cases": [
            {
                "id": "cab-full-outer-tc-1", "name": "Payment Reconciliation Audit", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE trips (trip_id INT PRIMARY KEY, fare REAL NOT NULL);"
                        "CREATE TABLE gateway_payments (payment_id INT PRIMARY KEY, trip_id INT, amount_paid REAL NOT NULL);"
                    ),
                    "fixtures": {
                        "trips": [
                            {"trip_id": 1001, "fare": 25.00},
                            {"trip_id": 1002, "fare": 40.00},
                            {"trip_id": 1003, "fare": 18.50}
                        ],
                        "gateway_payments": [
                            {"payment_id": 901, "trip_id": 1001, "amount_paid": 25.00},
                            {"payment_id": 902, "trip_id": 1002, "amount_paid": 40.00},
                            {"payment_id": 903, "trip_id": 9999, "amount_paid": 60.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"trip_id": 1001, "fare": 25.0, "payment_id": 901, "amount_paid": 25.0},
                    {"trip_id": 1002, "fare": 40.0, "payment_id": 902, "amount_paid": 40.0},
                    {"trip_id": 1003, "fare": 18.5, "payment_id": None, "amount_paid": None},
                    {"trip_id": None, "fare": None, "payment_id": 903, "amount_paid": 60.0}
                ], indent=2) + "\n"
            }
        ]
    }
]
