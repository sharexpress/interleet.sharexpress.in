# Copyright 2026 Sharexpress Contributors
# Module 4: Case Study - House Rental App (Sub-queries & CTEs) (10 Problems)

import json

MODULE4_CHALLENGES = [
    # 34. Properties Above Average Daily Rate
    {
        "title": "House Rental: Above-Average Daily Rate",
        "slug": "sql-rental-above-avg-price",
        "short_description": "Use a scalar subquery in the WHERE clause to isolate luxury rentals.",
        "description": (
            "### Problem Statement\n\n"
            "The marketplace inventory team wants to identify premium listings priced above the platform's "
            "overall average daily price. Write a SQL query using a scalar subquery to find all properties "
            "where `price_per_night` exceeds the catalog average.\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Unique listing identifier |\n"
            "| `title` | TEXT | Listing headline |\n"
            "| `city` | TEXT | City location |\n"
            "| `price_per_night` | REAL | Daily rental rate in USD |\n\n"
            "#### Output Requirements\n"
            "Return `property_id`, `title`, `city`, and `price_per_night`.\n"
            "Order by `price_per_night DESC`, `property_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Subquery", "Scalar Subquery", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Scalar Subquery", "WHERE Clause Subquery", "Average Comparison"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  city TEXT NOT NULL,"
            "  price_per_night REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "properties": [
                {"property_id": 1, "title": "Cozy Downtown Studio", "city": "Seattle", "price_per_night": 110.00},
                {"property_id": 2, "title": "Luxury Waterfront Villa", "city": "Miami", "price_per_night": 450.00},
                {"property_id": 3, "title": "Historic Brownstone", "city": "Boston", "price_per_night": 220.00},
                {"property_id": 4, "title": "Modern Loft", "city": "Chicago", "price_per_night": 160.00},
                {"property_id": 5, "title": "Suburban Family Home", "city": "Austin", "price_per_night": 140.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT property_id, title, city, price_per_night "
            "FROM properties "
            "WHERE price_per_night > (SELECT AVG(price_per_night) FROM properties) "
            "ORDER BY price_per_night DESC, property_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-above-avg-tc-1", "name": "Scalar Average Comparison", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE properties (property_id INT PRIMARY KEY, title TEXT NOT NULL, city TEXT NOT NULL, price_per_night REAL NOT NULL);",
                    "fixtures": {
                        "properties": [
                            {"property_id": 1, "title": "Cozy Downtown Studio", "city": "Seattle", "price_per_night": 110.00},
                            {"property_id": 2, "title": "Luxury Waterfront Villa", "city": "Miami", "price_per_night": 450.00},
                            {"property_id": 3, "title": "Historic Brownstone", "city": "Boston", "price_per_night": 220.00},
                            {"property_id": 4, "title": "Modern Loft", "city": "Chicago", "price_per_night": 160.00},
                            {"property_id": 5, "title": "Suburban Family Home", "city": "Austin", "price_per_night": 140.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"property_id": 2, "title": "Luxury Waterfront Villa", "city": "Miami", "price_per_night": 450.0},
                    {"property_id": 3, "title": "Historic Brownstone", "city": "Boston", "price_per_night": 220.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 35. Unbooked Properties (Subquery with NOT IN)
    {
        "title": "House Rental: Properties with Zero Bookings",
        "slug": "sql-rental-never-booked-properties",
        "short_description": "Locate idle inventory using a NOT IN subquery against the bookings table.",
        "description": (
            "### Problem Statement\n\n"
            "Supply growth needs a list of all active listings that have never recorded a reservation. "
            "Write a SQL query using `NOT IN` with a subquery on `bookings` to extract properties "
            "that have zero entries in the reservation logs.\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Listing ID |\n"
            "| `title` | TEXT | Listing title |\n"
            "| `city` | TEXT | City name |\n"
            "| `price_per_night` | REAL | Price per night |\n\n"
            "#### Table Schema: `bookings`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `booking_id` | INT (PK) | Reservation ID |\n"
            "| `property_id` | INT | Foreign key to `properties` |\n\n"
            "#### Output Requirements\n"
            "Return `property_id`, `title`, `city`, and `price_per_night`.\n"
            "Order by `property_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Subquery", "NOT IN", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["NOT IN Predicate", "Subquery Anti-pattern", "Unbooked Analysis"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  city TEXT NOT NULL,"
            "  price_per_night REAL NOT NULL"
            ");"
            "CREATE TABLE bookings ("
            "  booking_id INT PRIMARY KEY,"
            "  property_id INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "properties": [
                {"property_id": 101, "title": "Alpine Ski Chalet", "city": "Denver", "price_per_night": 290.00},
                {"property_id": 102, "title": "Beachside Bungalow", "city": "San Diego", "price_per_night": 320.00},
                {"property_id": 103, "title": "Desert Oasis", "city": "Phoenix", "price_per_night": 180.00},
                {"property_id": 104, "title": "City Center Condo", "city": "Seattle", "price_per_night": 150.00}
            ],
            "bookings": [
                {"booking_id": 1, "property_id": 101},
                {"booking_id": 2, "property_id": 104},
                {"booking_id": 3, "property_id": 101}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT property_id, title, city, price_per_night "
            "FROM properties "
            "WHERE property_id NOT IN (SELECT property_id FROM bookings) "
            "ORDER BY property_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-unbooked-tc-1", "name": "NOT IN Idle Listings", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE properties (property_id INT PRIMARY KEY, title TEXT NOT NULL, city TEXT NOT NULL, price_per_night REAL NOT NULL);"
                        "CREATE TABLE bookings (booking_id INT PRIMARY KEY, property_id INT NOT NULL);"
                    ),
                    "fixtures": {
                        "properties": [
                            {"property_id": 101, "title": "Alpine Ski Chalet", "city": "Denver", "price_per_night": 290.00},
                            {"property_id": 102, "title": "Beachside Bungalow", "city": "San Diego", "price_per_night": 320.00},
                            {"property_id": 103, "title": "Desert Oasis", "city": "Phoenix", "price_per_night": 180.00},
                            {"property_id": 104, "title": "City Center Condo", "city": "Seattle", "price_per_night": 150.00}
                        ],
                        "bookings": [
                            {"booking_id": 1, "property_id": 101},
                            {"booking_id": 2, "property_id": 104},
                            {"booking_id": 3, "property_id": 101}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"property_id": 102, "title": "Beachside Bungalow", "city": "San Diego", "price_per_night": 320.0},
                    {"property_id": 103, "title": "Desert Oasis", "city": "Phoenix", "price_per_night": 180.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 36. Listings in High-Density Markets (Subquery with IN and HAVING)
    {
        "title": "House Rental: Listings in High-Density Markets",
        "slug": "sql-rental-popular-city-listings",
        "short_description": "Filter listings located in cities having 2 or more registered properties.",
        "description": (
            "### Problem Statement\n\n"
            "Regional directors are organizing regional host summits for key cluster markets. "
            "Write a SQL query using an `IN` subquery with `GROUP BY` and `HAVING COUNT(*) >= 2` "
            "to extract all properties situated in cities with 2 or more listings.\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Property ID |\n"
            "| `title` | TEXT | Title |\n"
            "| `city` | TEXT | City |\n"
            "| `price_per_night` | REAL | Nightly rate |\n\n"
            "#### Output Requirements\n"
            "Return `property_id`, `title`, `city`, and `price_per_night`.\n"
            "Order by `city ASC`, `price_per_night DESC`, `property_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Subquery", "IN", "HAVING", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Multi-row Subqueries", "HAVING Filter in Subquery", "Cluster Analysis"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 14,
        "schema_sql": (
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  city TEXT NOT NULL,"
            "  price_per_night REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "properties": [
                {"property_id": 1, "title": "Austin Downtown Loft", "city": "Austin", "price_per_night": 175.00},
                {"property_id": 2, "title": "South Congress Studio", "city": "Austin", "price_per_night": 130.00},
                {"property_id": 3, "title": "Rainey St Suite", "city": "Austin", "price_per_night": 210.00},
                {"property_id": 4, "title": "Barton Springs Retreat", "city": "Dallas", "price_per_night": 190.00},
                {"property_id": 5, "title": "Mile High Penthouse", "city": "Denver", "price_per_night": 310.00},
                {"property_id": 6, "title": "RiNo Art District Flat", "city": "Denver", "price_per_night": 145.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT property_id, title, city, price_per_night "
            "FROM properties "
            "WHERE city IN (SELECT city FROM properties GROUP BY city HAVING COUNT(*) >= 2) "
            "ORDER BY city ASC, price_per_night DESC, property_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-density-tc-1", "name": "Multi-property Market Filter", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE properties (property_id INT PRIMARY KEY, title TEXT NOT NULL, city TEXT NOT NULL, price_per_night REAL NOT NULL);",
                    "fixtures": {
                        "properties": [
                            {"property_id": 1, "title": "Austin Downtown Loft", "city": "Austin", "price_per_night": 175.00},
                            {"property_id": 2, "title": "South Congress Studio", "city": "Austin", "price_per_night": 130.00},
                            {"property_id": 3, "title": "Rainey St Suite", "city": "Austin", "price_per_night": 210.00},
                            {"property_id": 4, "title": "Barton Springs Retreat", "city": "Dallas", "price_per_night": 190.00},
                            {"property_id": 5, "title": "Mile High Penthouse", "city": "Denver", "price_per_night": 310.00},
                            {"property_id": 6, "title": "RiNo Art District Flat", "city": "Denver", "price_per_night": 145.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"property_id": 3, "title": "Rainey St Suite", "city": "Austin", "price_per_night": 210.0},
                    {"property_id": 1, "title": "Austin Downtown Loft", "city": "Austin", "price_per_night": 175.0},
                    {"property_id": 2, "title": "South Congress Studio", "city": "Austin", "price_per_night": 130.0},
                    {"property_id": 5, "title": "Mile High Penthouse", "city": "Denver", "price_per_night": 310.0},
                    {"property_id": 6, "title": "RiNo Art District Flat", "city": "Denver", "price_per_night": 145.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 37. Cheapest Listing per City (Correlated Subquery)
    {
        "title": "House Rental: Cheapest Listing per City",
        "slug": "sql-rental-cheapest-per-city",
        "short_description": "Implement a correlated subquery to find minimum price listings by city.",
        "description": (
            "### Problem Statement\n\n"
            "Budget travelers frequently look for bargain accommodations in each destination city. "
            "Write a SQL query using a correlated subquery to retrieve the listing with the lowest "
            "`price_per_night` in each respective city.\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Listing identifier |\n"
            "| `title` | TEXT | Headline |\n"
            "| `city` | TEXT | City |\n"
            "| `price_per_night` | REAL | Daily rate |\n\n"
            "#### Output Requirements\n"
            "Return `property_id`, `title`, `city`, and `price_per_night`.\n"
            "Order by `city ASC`, `property_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Subquery", "Correlated Subquery", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Correlated Subquery", "Per-Group Minimum", "Row-Level Binding"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 70, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  city TEXT NOT NULL,"
            "  price_per_night REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "properties": [
                {"property_id": 1, "title": "Bayfront Condo", "city": "San Francisco", "price_per_night": 280.00},
                {"property_id": 2, "title": "Mission District Room", "city": "San Francisco", "price_per_night": 120.00},
                {"property_id": 3, "title": "Broadway Penthouse", "city": "New York", "price_per_night": 450.00},
                {"property_id": 4, "title": "Brooklyn Cozy Suite", "city": "New York", "price_per_night": 160.00},
                {"property_id": 5, "title": "Queens Studio", "city": "New York", "price_per_night": 135.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT p.property_id, p.title, p.city, p.price_per_night "
            "FROM properties p "
            "WHERE p.price_per_night = ("
            "  SELECT MIN(p2.price_per_night) "
            "  FROM properties p2 "
            "  WHERE p2.city = p.city"
            ") "
            "ORDER BY p.city ASC, p.property_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-cheapest-tc-1", "name": "City Group Minimum Resolution", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE properties (property_id INT PRIMARY KEY, title TEXT NOT NULL, city TEXT NOT NULL, price_per_night REAL NOT NULL);",
                    "fixtures": {
                        "properties": [
                            {"property_id": 1, "title": "Bayfront Condo", "city": "San Francisco", "price_per_night": 280.00},
                            {"property_id": 2, "title": "Mission District Room", "city": "San Francisco", "price_per_night": 120.00},
                            {"property_id": 3, "title": "Broadway Penthouse", "city": "New York", "price_per_night": 450.00},
                            {"property_id": 4, "title": "Brooklyn Cozy Suite", "city": "New York", "price_per_night": 160.00},
                            {"property_id": 5, "title": "Queens Studio", "city": "New York", "price_per_night": 135.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"property_id": 5, "title": "Queens Studio", "city": "New York", "price_per_night": 135.0},
                    {"property_id": 2, "title": "Mission District Room", "city": "San Francisco", "price_per_night": 120.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 38. Premier Host Ratings (Derived Table in FROM)
    {
        "title": "House Rental: Premier Host Ratings",
        "slug": "sql-rental-top-owner-rating",
        "short_description": "Use a derived table subquery in the FROM clause to filter premier hosts.",
        "description": (
            "### Problem Statement\n\n"
            "Hosts with an average property rating of 4.80 or higher qualify for Superhost status. "
            "Write a SQL query using a derived table in the `FROM` clause that first aggregates the "
            "average rating per `owner_id` (rounded to 2 decimal places), and then filters for hosts "
            "with `avg_rating >= 4.80`.\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Property ID |\n"
            "| `owner_id` | INT | Property owner ID |\n"
            "| `rating` | REAL | Customer review score |\n\n"
            "#### Output Requirements\n"
            "Return `owner_id` and `avg_rating`.\n"
            "Order by `avg_rating DESC`, `owner_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Subquery", "Derived Table", "FROM Subquery", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Derived Table", "FROM Clause Subquery", "ROUND Aggregation"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 14,
        "schema_sql": (
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  owner_id INT NOT NULL,"
            "  rating REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "properties": [
                {"property_id": 1, "owner_id": 501, "rating": 4.90},
                {"property_id": 2, "owner_id": 501, "rating": 4.80},
                {"property_id": 3, "owner_id": 502, "rating": 4.30},
                {"property_id": 4, "owner_id": 502, "rating": 4.50},
                {"property_id": 5, "owner_id": 503, "rating": 4.95}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT owner_id, avg_rating "
            "FROM ("
            "  SELECT owner_id, ROUND(AVG(rating), 2) AS avg_rating "
            "  FROM properties "
            "  GROUP BY owner_id"
            ") AS host_metrics "
            "WHERE avg_rating >= 4.80 "
            "ORDER BY avg_rating DESC, owner_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-host-ratings-tc-1", "name": "Derived Table Host Aggregation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE properties (property_id INT PRIMARY KEY, owner_id INT NOT NULL, rating REAL NOT NULL);",
                    "fixtures": {
                        "properties": [
                            {"property_id": 1, "owner_id": 501, "rating": 4.90},
                            {"property_id": 2, "owner_id": 501, "rating": 4.80},
                            {"property_id": 3, "owner_id": 502, "rating": 4.30},
                            {"property_id": 4, "owner_id": 502, "rating": 4.50},
                            {"property_id": 5, "owner_id": 503, "rating": 4.95}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"owner_id": 503, "avg_rating": 4.95},
                    {"owner_id": 501, "avg_rating": 4.85}
                ], indent=2) + "\n"
            }
        ]
    },

    # 39. Guests with Luxury Stays (Subquery with EXISTS)
    {
        "title": "House Rental: Guests with Luxury Stays",
        "slug": "sql-rental-users-with-luxury-bookings",
        "short_description": "Locate high-net-worth guests using an EXISTS subquery on luxury bookings.",
        "description": (
            "### Problem Statement\n\n"
            "VIP concierge services wants to target guests who have booked at least one premium property "
            "costing $250 or more per night. "
            "Write a SQL query using `EXISTS` to find all registered `users` who have booked a property "
            "with `price_per_night >= 250`.\n\n"
            "#### Table Schema: `users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `name` | TEXT | Guest full name |\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Property ID |\n"
            "| `price_per_night` | REAL | Nightly rate |\n\n"
            "#### Table Schema: `bookings`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `booking_id` | INT (PK) | Booking ID |\n"
            "| `property_id` | INT | Property ID |\n"
            "| `user_id` | INT | Guest user ID |\n\n"
            "#### Output Requirements\n"
            "Return `user_id` and `name`.\n"
            "Order by `user_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Subquery", "EXISTS", "Correlated Subquery", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["EXISTS Clause", "Boolean Semi-Join", "Customer Segmentation"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 70, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE users ("
            "  user_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL"
            ");"
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  price_per_night REAL NOT NULL"
            ");"
            "CREATE TABLE bookings ("
            "  booking_id INT PRIMARY KEY,"
            "  property_id INT NOT NULL,"
            "  user_id INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "users": [
                {"user_id": 1, "name": "Arthur Dent"},
                {"user_id": 2, "name": "Ford Prefect"},
                {"user_id": 3, "name": "Trillian Astra"},
                {"user_id": 4, "name": "Zaphod Beeblebrox"}
            ],
            "properties": [
                {"property_id": 10, "price_per_night": 120.00},
                {"property_id": 20, "price_per_night": 350.00},
                {"property_id": 30, "price_per_night": 400.00}
            ],
            "bookings": [
                {"booking_id": 100, "property_id": 10, "user_id": 1},
                {"booking_id": 101, "property_id": 20, "user_id": 2},
                {"booking_id": 102, "property_id": 10, "user_id": 3},
                {"booking_id": 103, "property_id": 30, "user_id": 4}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT u.user_id, u.name "
            "FROM users u "
            "WHERE EXISTS ("
            "  SELECT 1 "
            "  FROM bookings b "
            "  JOIN properties p ON b.property_id = p.property_id "
            "  WHERE b.user_id = u.user_id AND p.price_per_night >= 250"
            ") "
            "ORDER BY u.user_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-luxury-guests-tc-1", "name": "EXISTS Semi-Join High Value Stays", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE users (user_id INT PRIMARY KEY, name TEXT NOT NULL);"
                        "CREATE TABLE properties (property_id INT PRIMARY KEY, price_per_night REAL NOT NULL);"
                        "CREATE TABLE bookings (booking_id INT PRIMARY KEY, property_id INT NOT NULL, user_id INT NOT NULL);"
                    ),
                    "fixtures": {
                        "users": [
                            {"user_id": 1, "name": "Arthur Dent"},
                            {"user_id": 2, "name": "Ford Prefect"},
                            {"user_id": 3, "name": "Trillian Astra"},
                            {"user_id": 4, "name": "Zaphod Beeblebrox"}
                        ],
                        "properties": [
                            {"property_id": 10, "price_per_night": 120.00},
                            {"property_id": 20, "price_per_night": 350.00},
                            {"property_id": 30, "price_per_night": 400.00}
                        ],
                        "bookings": [
                            {"booking_id": 100, "property_id": 10, "user_id": 1},
                            {"booking_id": 101, "property_id": 20, "user_id": 2},
                            {"booking_id": 102, "property_id": 10, "user_id": 3},
                            {"booking_id": 103, "property_id": 30, "user_id": 4}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"user_id": 2, "name": "Ford Prefect"},
                    {"user_id": 4, "name": "Zaphod Beeblebrox"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 40. High-Yield Months (Common Table Expression - CTE)
    {
        "title": "House Rental: High-Yield Booking Months",
        "slug": "sql-rental-monthly-booking-revenue",
        "short_description": "Build a CTE to summarize monthly revenue and filter for months generating >= $1000.",
        "description": (
            "### Problem Statement\n\n"
            "Financial accounting monitors monthly gross booking turnover. "
            "Write a SQL query using a Common Table Expression (`WITH` clause) named `monthly_rev` "
            "that sums `total_amount` grouped by `booking_month` (formatted as `YYYY-MM` via `substr(check_in, 1, 7)`). "
            "Filter the final CTE query for months where `revenue >= 1000.0`.\n\n"
            "#### Table Schema: `bookings`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `booking_id` | INT (PK) | Booking identifier |\n"
            "| `check_in` | TEXT | Check-in date in 'YYYY-MM-DD' format |\n"
            "| `total_amount` | REAL | Total booking charge in USD |\n\n"
            "#### Output Requirements\n"
            "Return `booking_month` and `revenue`.\n"
            "Order by `booking_month ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CTE", "WITH Clause", "Aggregation", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Common Table Expression", "Date Substring", "Gross Revenue Filter"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 70, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE bookings ("
            "  booking_id INT PRIMARY KEY,"
            "  check_in TEXT NOT NULL,"
            "  total_amount REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "bookings": [
                {"booking_id": 1, "check_in": "2026-01-05", "total_amount": 450.00},
                {"booking_id": 2, "check_in": "2026-01-18", "total_amount": 620.00},
                {"booking_id": 3, "check_in": "2026-02-10", "total_amount": 350.00},
                {"booking_id": 4, "check_in": "2026-02-22", "total_amount": 250.00},
                {"booking_id": 5, "check_in": "2026-03-01", "total_amount": 1250.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nWITH monthly_rev AS (\n  SELECT \n)\nSELECT \n",
            "sqlite": "WITH monthly_rev AS (\n  SELECT \n)\nSELECT \n",
            "mysql": "WITH monthly_rev AS (\n  SELECT \n)\nSELECT \n",
            "postgresql": "WITH monthly_rev AS (\n  SELECT \n)\nSELECT \n"
        },
        "canonical_solution": (
            "WITH monthly_rev AS ("
            "  SELECT substr(check_in, 1, 7) AS booking_month, SUM(total_amount) AS revenue "
            "  FROM bookings "
            "  GROUP BY substr(check_in, 1, 7)"
            ") "
            "SELECT booking_month, revenue "
            "FROM monthly_rev "
            "WHERE revenue >= 1000.0 "
            "ORDER BY booking_month ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-monthly-rev-tc-1", "name": "CTE Monthly Revenue Aggregation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE bookings (booking_id INT PRIMARY KEY, check_in TEXT NOT NULL, total_amount REAL NOT NULL);",
                    "fixtures": {
                        "bookings": [
                            {"booking_id": 1, "check_in": "2026-01-05", "total_amount": 450.00},
                            {"booking_id": 2, "check_in": "2026-01-18", "total_amount": 620.00},
                            {"booking_id": 3, "check_in": "2026-02-10", "total_amount": 350.00},
                            {"booking_id": 4, "check_in": "2026-02-22", "total_amount": 250.00},
                            {"booking_id": 5, "check_in": "2026-03-01", "total_amount": 1250.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"booking_month": "2026-01", "revenue": 1070.0},
                    {"booking_month": "2026-03", "revenue": 1250.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 41. Multi-City Nomads (CTE with Join and Count Distinct)
    {
        "title": "House Rental: Multi-City Nomads",
        "slug": "sql-rental-multi-city-travelers",
        "short_description": "Leverage a CTE to find adventurous travelers with bookings across 2 or more cities.",
        "description": (
            "### Problem Statement\n\n"
            "Marketing wants to reward multi-city travelers ('digital nomads'). "
            "Create a CTE named `user_cities` that counts distinct cities each user has booked properties in. "
            "Then join this CTE with `users` to list travelers with `distinct_cities > 1`.\n\n"
            "#### Table Schema: `users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `name` | TEXT | User name |\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Property ID |\n"
            "| `city` | TEXT | City location |\n\n"
            "#### Table Schema: `bookings`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `booking_id` | INT (PK) | Booking ID |\n"
            "| `user_id` | INT | User ID |\n"
            "| `property_id` | INT | Property ID |\n\n"
            "#### Output Requirements\n"
            "Return `user_id`, `name`, and `distinct_cities`.\n"
            "Order by `distinct_cities DESC`, `user_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CTE", "COUNT DISTINCT", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["CTE Join", "Distinct City Count", "Traveler Behavior Analysis"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 75, "estimated_time_minutes": 16,
        "schema_sql": (
            "CREATE TABLE users ("
            "  user_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL"
            ");"
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  city TEXT NOT NULL"
            ");"
            "CREATE TABLE bookings ("
            "  booking_id INT PRIMARY KEY,"
            "  user_id INT NOT NULL,"
            "  property_id INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "users": [
                {"user_id": 10, "name": "Jessica Day"},
                {"user_id": 20, "name": "Nick Miller"},
                {"user_id": 30, "name": "Schmidt"}
            ],
            "properties": [
                {"property_id": 1, "city": "Los Angeles"},
                {"property_id": 2, "city": "Los Angeles"},
                {"property_id": 3, "city": "Portland"},
                {"property_id": 4, "city": "Chicago"}
            ],
            "bookings": [
                {"booking_id": 101, "user_id": 10, "property_id": 1},
                {"booking_id": 102, "user_id": 10, "property_id": 3},
                {"booking_id": 103, "user_id": 10, "property_id": 4},
                {"booking_id": 104, "user_id": 20, "property_id": 1},
                {"booking_id": 105, "user_id": 20, "property_id": 2},
                {"booking_id": 106, "user_id": 30, "property_id": 3},
                {"booking_id": 107, "user_id": 30, "property_id": 1}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nWITH user_cities AS (\n  SELECT \n)\nSELECT \n",
            "sqlite": "WITH user_cities AS (\n  SELECT \n)\nSELECT \n",
            "mysql": "WITH user_cities AS (\n  SELECT \n)\nSELECT \n",
            "postgresql": "WITH user_cities AS (\n  SELECT \n)\nSELECT \n"
        },
        "canonical_solution": (
            "WITH user_cities AS ("
            "  SELECT b.user_id, COUNT(DISTINCT p.city) AS distinct_cities "
            "  FROM bookings b "
            "  JOIN properties p ON b.property_id = p.property_id "
            "  GROUP BY b.user_id"
            ") "
            "SELECT u.user_id, u.name, uc.distinct_cities "
            "FROM user_cities uc "
            "JOIN users u ON uc.user_id = u.user_id "
            "WHERE uc.distinct_cities > 1 "
            "ORDER BY uc.distinct_cities DESC, u.user_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-nomads-tc-1", "name": "CTE Multi-City Count", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE users (user_id INT PRIMARY KEY, name TEXT NOT NULL);"
                        "CREATE TABLE properties (property_id INT PRIMARY KEY, city TEXT NOT NULL);"
                        "CREATE TABLE bookings (booking_id INT PRIMARY KEY, user_id INT NOT NULL, property_id INT NOT NULL);"
                    ),
                    "fixtures": {
                        "users": [
                            {"user_id": 10, "name": "Jessica Day"},
                            {"user_id": 20, "name": "Nick Miller"},
                            {"user_id": 30, "name": "Schmidt"}
                        ],
                        "properties": [
                            {"property_id": 1, "city": "Los Angeles"},
                            {"property_id": 2, "city": "Los Angeles"},
                            {"property_id": 3, "city": "Portland"},
                            {"property_id": 4, "city": "Chicago"}
                        ],
                        "bookings": [
                            {"booking_id": 101, "user_id": 10, "property_id": 1},
                            {"booking_id": 102, "user_id": 10, "property_id": 3},
                            {"booking_id": 103, "user_id": 10, "property_id": 4},
                            {"booking_id": 104, "user_id": 20, "property_id": 1},
                            {"booking_id": 105, "user_id": 20, "property_id": 2},
                            {"booking_id": 106, "user_id": 30, "property_id": 3},
                            {"booking_id": 107, "user_id": 30, "property_id": 1}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"user_id": 10, "name": "Jessica Day", "distinct_cities": 3},
                    {"user_id": 30, "name": "Schmidt", "distinct_cities": 2}
                ], indent=2) + "\n"
            }
        ]
    },

    # 42. Complete Property Occupancy Manifest (CTE with Outer Join)
    {
        "title": "House Rental: Complete Occupancy Manifest",
        "slug": "sql-rental-property-occupancy-summary",
        "short_description": "Combine CTE and LEFT JOIN with COALESCE to compile occupancy metrics for every listing.",
        "description": (
            "### Problem Statement\n\n"
            "The marketplace auditing desk requires a complete inventory report detailing total booked nights "
            "and gross revenues across all listings. Unbooked listings must still be included with `0` total nights "
            "and `0.0` gross revenue.\n\n"
            "Construct a CTE named `booking_stats` aggregating `SUM(nights)` and `SUM(total_amount)` per `property_id`. "
            "Then `LEFT JOIN` `properties` with `booking_stats`, wrapping null aggregates with `COALESCE`.\n\n"
            "#### Table Schema: `properties`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `property_id` | INT (PK) | Listing ID |\n"
            "| `title` | TEXT | Property headline |\n\n"
            "#### Table Schema: `bookings`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `booking_id` | INT (PK) | Booking ID |\n"
            "| `property_id` | INT | Property ID |\n"
            "| `nights` | INT | Number of nights reserved |\n"
            "| `total_amount` | REAL | Total booking amount |\n\n"
            "#### Output Requirements\n"
            "Return `property_id`, `title`, `total_nights`, and `gross_revenue`.\n"
            "Order by `gross_revenue DESC`, `property_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Hard",
        "tags": ["SQL", "CTE", "COALESCE", "LEFT JOIN", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["CTE with Left Join", "COALESCE Null Substitution", "Inventory Audit"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 80, "estimated_time_minutes": 18,
        "schema_sql": (
            "CREATE TABLE properties ("
            "  property_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL"
            ");"
            "CREATE TABLE bookings ("
            "  booking_id INT PRIMARY KEY,"
            "  property_id INT NOT NULL,"
            "  nights INT NOT NULL,"
            "  total_amount REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "properties": [
                {"property_id": 1, "title": "Lake Tahoe Cabin"},
                {"property_id": 2, "title": "Aspen Luxury Manor"},
                {"property_id": 3, "title": "Napa Valley Vineyard Estate"}
            ],
            "bookings": [
                {"booking_id": 10, "property_id": 1, "nights": 3, "total_amount": 600.00},
                {"booking_id": 11, "property_id": 1, "nights": 4, "total_amount": 800.00},
                {"booking_id": 12, "property_id": 2, "nights": 5, "total_amount": 2500.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nWITH booking_stats AS (\n  SELECT \n)\nSELECT \n",
            "sqlite": "WITH booking_stats AS (\n  SELECT \n)\nSELECT \n",
            "mysql": "WITH booking_stats AS (\n  SELECT \n)\nSELECT \n",
            "postgresql": "WITH booking_stats AS (\n  SELECT \n)\nSELECT \n"
        },
        "canonical_solution": (
            "WITH booking_stats AS ("
            "  SELECT property_id, SUM(nights) AS total_nights, SUM(total_amount) AS gross_revenue "
            "  FROM bookings "
            "  GROUP BY property_id"
            ") "
            "SELECT p.property_id, p.title, "
            "COALESCE(bs.total_nights, 0) AS total_nights, "
            "COALESCE(bs.gross_revenue, 0.0) AS gross_revenue "
            "FROM properties p "
            "LEFT JOIN booking_stats bs ON p.property_id = bs.property_id "
            "ORDER BY gross_revenue DESC, p.property_id ASC;"
        ),
        "test_cases": [
            {
                "id": "rental-occupancy-tc-1", "name": "CTE Manifest Zero Fill", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": (
                        "CREATE TABLE properties (property_id INT PRIMARY KEY, title TEXT NOT NULL);"
                        "CREATE TABLE bookings (booking_id INT PRIMARY KEY, property_id INT NOT NULL, nights INT NOT NULL, total_amount REAL NOT NULL);"
                    ),
                    "fixtures": {
                        "properties": [
                            {"property_id": 1, "title": "Lake Tahoe Cabin"},
                            {"property_id": 2, "title": "Aspen Luxury Manor"},
                            {"property_id": 3, "title": "Napa Valley Vineyard Estate"}
                        ],
                        "bookings": [
                            {"booking_id": 10, "property_id": 1, "nights": 3, "total_amount": 600.00},
                            {"booking_id": 11, "property_id": 1, "nights": 4, "total_amount": 800.00},
                            {"booking_id": 12, "property_id": 2, "nights": 5, "total_amount": 2500.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"property_id": 2, "title": "Aspen Luxury Manor", "total_nights": 5, "gross_revenue": 2500.0},
                    {"property_id": 1, "title": "Lake Tahoe Cabin", "total_nights": 7, "gross_revenue": 1400.0},
                    {"property_id": 3, "title": "Napa Valley Vineyard Estate", "total_nights": 0, "gross_revenue": 0.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 43. Second Highest Booking Transaction
    {
        "title": "House Rental: Second Highest Booking Transaction",
        "slug": "sql-rental-second-highest-booking",
        "short_description": "Retrieve the 2nd highest booking value strictly using subqueries without LIMIT/OFFSET.",
        "description": (
            "### Problem Statement\n\n"
            "Financial fraud detection compares top outlier expenditures against second-tier benchmarks. "
            "Write a SQL query using a scalar subquery to find the second highest `total_amount` in the `bookings` table "
            "without using `LIMIT` or `OFFSET`.\n\n"
            "#### Table Schema: `bookings`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `booking_id` | INT (PK) | Transaction ID |\n"
            "| `total_amount` | REAL | Total booking charge |\n\n"
            "#### Output Requirements\n"
            "Return a single column named `second_highest_amount`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Subquery", "MAX", "N-th Highest", "House Rental"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["N-th Highest Value", "MAX with Subquery", "Limit-less Ranking"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 70, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE bookings ("
            "  booking_id INT PRIMARY KEY,"
            "  total_amount REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "bookings": [
                {"booking_id": 1, "total_amount": 1200.00},
                {"booking_id": 2, "total_amount": 3400.00},
                {"booking_id": 3, "total_amount": 2100.00},
                {"booking_id": 4, "total_amount": 950.00},
                {"booking_id": 5, "total_amount": 3400.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT MAX(total_amount) AS second_highest_amount "
            "FROM bookings "
            "WHERE total_amount < (SELECT MAX(total_amount) FROM bookings);"
        ),
        "test_cases": [
            {
                "id": "rental-second-max-tc-1", "name": "Scalar Subquery Second Highest", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE bookings (booking_id INT PRIMARY KEY, total_amount REAL NOT NULL);",
                    "fixtures": {
                        "bookings": [
                            {"booking_id": 1, "total_amount": 1200.00},
                            {"booking_id": 2, "total_amount": 3400.00},
                            {"booking_id": 3, "total_amount": 2100.00},
                            {"booking_id": 4, "total_amount": 950.00},
                            {"booking_id": 5, "total_amount": 3400.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"second_highest_amount": 2100.0}
                ], indent=2) + "\n"
            }
        ]
    }
]
