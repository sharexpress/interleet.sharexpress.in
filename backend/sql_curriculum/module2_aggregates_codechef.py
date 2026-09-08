# Copyright 2026 Sharexpress Contributors
# Module 2: Case Study - Platform Database (Aggregates & Group By) (10 Problems)

import json

MODULE2_CHALLENGES = [
    # 14. Output All Rows from a Table
    {
        "title": "Output All Rows from a Table",
        "slug": "sql-codechef-output-all-rows",
        "short_description": "Extract coder profiles with rating and country affiliations.",
        "description": (
            "### Problem Statement\n\n"
            "The competitive programming platform analytics team is building an international coder index. "
            "Write a SQL query to select all users with their ID, username, rating, and country.\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | Platform account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Contest performance rating |\n"
            "| `country` | VARCHAR(50) | Home country |\n"
            "| `college_id` | INT | Affiliated institution ID |\n"
            "| `is_pro` | INT | Pro subscriber flag (1 or 0) |\n"
            "| `team_id` | INT | Team roster ID |\n\n"
            "#### Output Requirements\n"
            "Return `user_id`, `username`, `rating`, and `country`. Order by `user_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "SELECT", "Platform", "Basics"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Column Projection", "Table Scanning", "Primary Key Sort"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "tourist_fan", "rating": 2340, "country": "India", "college_id": 101, "is_pro": 1, "team_id": 12},
                {"user_id": 2, "username": "byte_wizard", "rating": 1780, "country": "USA", "college_id": 102, "is_pro": 0, "team_id": 12},
                {"user_id": 3, "username": "algo_queen", "rating": 2210, "country": "Canada", "college_id": 101, "is_pro": 1, "team_id": 14},
                {"user_id": 4, "username": "code_master", "rating": 1540, "country": "Germany", "college_id": 103, "is_pro": 0, "team_id": None},
                {"user_id": 5, "username": "syntax_ninja", "rating": 2450, "country": "Japan", "college_id": 102, "is_pro": 1, "team_id": 14}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT user_id, username, rating, country FROM platform_users ORDER BY user_id ASC;",
        "test_cases": [
            {
                "id": "cc-out-all-tc-1", "name": "Coder Roster Extraction", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "tourist_fan", "rating": 2340, "country": "India", "college_id": 101, "is_pro": 1, "team_id": 12},
                            {"user_id": 2, "username": "byte_wizard", "rating": 1780, "country": "USA", "college_id": 102, "is_pro": 0, "team_id": 12},
                            {"user_id": 3, "username": "algo_queen", "rating": 2210, "country": "Canada", "college_id": 101, "is_pro": 1, "team_id": 14},
                            {"user_id": 4, "username": "code_master", "rating": 1540, "country": "Germany", "college_id": 103, "is_pro": 0, "team_id": None},
                            {"user_id": 5, "username": "syntax_ninja", "rating": 2450, "country": "Japan", "college_id": 102, "is_pro": 1, "team_id": 14}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"user_id": 1, "username": "tourist_fan", "rating": 2340, "country": "India"},
                    {"user_id": 2, "username": "byte_wizard", "rating": 1780, "country": "USA"},
                    {"user_id": 3, "username": "algo_queen", "rating": 2210, "country": "Canada"},
                    {"user_id": 4, "username": "code_master", "rating": 1540, "country": "Germany"},
                    {"user_id": 5, "username": "syntax_ninja", "rating": 2450, "country": "Japan"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 15. Find Average Rating Among Users
    {
        "title": "Find Average Rating Among Users",
        "slug": "sql-codechef-average-rating",
        "short_description": "Calculate the mean contest rating across all registered competitors.",
        "description": (
            "### Problem Statement\n\n"
            "Platform rating normalization requires calculating the global average performance score. "
            "Write a SQL query to compute the average rating across all users in the `platform_users` table.\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Contest performance rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return a single column named `avg_user_rating`, rounded to 2 decimal places using `ROUND()`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "AVG", "ROUND", "Aggregates"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Average Function", "Precision Rounding", "Platform Metrics"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "user1", "rating": 1600, "country": "IND", "college_id": 1, "is_pro": 0, "team_id": 1},
                {"user_id": 2, "username": "user2", "rating": 1850, "country": "USA", "college_id": 2, "is_pro": 1, "team_id": 1},
                {"user_id": 3, "username": "user3", "rating": 2100, "country": "GBR", "college_id": 1, "is_pro": 1, "team_id": 2},
                {"user_id": 4, "username": "user4", "rating": 1450, "country": "CAN", "college_id": 3, "is_pro": 0, "team_id": 2}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT ROUND(AVG(rating), 2) AS avg_user_rating FROM platform_users;",
        "test_cases": [
            {
                "id": "cc-avg-rat-tc-1", "name": "Mean Rating Calculation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "user1", "rating": 1600, "country": "IND", "college_id": 1, "is_pro": 0, "team_id": 1},
                            {"user_id": 2, "username": "user2", "rating": 1850, "country": "USA", "college_id": 2, "is_pro": 1, "team_id": 1},
                            {"user_id": 3, "username": "user3", "rating": 2100, "country": "GBR", "college_id": 1, "is_pro": 1, "team_id": 2},
                            {"user_id": 4, "username": "user4", "rating": 1450, "country": "CAN", "college_id": 3, "is_pro": 0, "team_id": 2}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"avg_user_rating": 1750.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 16. Count of Users in a Range
    {
        "title": "Count of Users in a Range",
        "slug": "sql-codechef-users-in-range",
        "short_description": "Count competitors in the Candidate Master rating bracket (1600 to 1999).",
        "description": (
            "### Problem Statement\n\n"
            "Find how many active coders fall into the intermediate tier. Write a SQL query to count "
            "all users with a `rating` between `1600` and `1999` (inclusive).\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Contest rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return a single column named `candidate_master_count`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "BETWEEN", "COUNT", "Range Filter"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["BETWEEN Operator", "Inclusive Ranges", "COUNT Aggregation"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "c1", "rating": 1599, "country": "USA", "college_id": 1, "is_pro": 0, "team_id": 1},
                {"user_id": 2, "username": "c2", "rating": 1600, "country": "IND", "college_id": 1, "is_pro": 0, "team_id": 1},
                {"user_id": 3, "username": "c3", "rating": 1750, "country": "GER", "college_id": 2, "is_pro": 1, "team_id": 2},
                {"user_id": 4, "username": "c4", "rating": 1999, "country": "JPN", "college_id": 2, "is_pro": 0, "team_id": 2},
                {"user_id": 5, "username": "c5", "rating": 2000, "country": "CAN", "college_id": 3, "is_pro": 1, "team_id": 3}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT COUNT(*) AS candidate_master_count FROM platform_users WHERE rating BETWEEN 1600 AND 1999;",
        "test_cases": [
            {
                "id": "cc-range-tc-1", "name": "Candidate Master Bracket Count", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "c1", "rating": 1599, "country": "USA", "college_id": 1, "is_pro": 0, "team_id": 1},
                            {"user_id": 2, "username": "c2", "rating": 1600, "country": "IND", "college_id": 1, "is_pro": 0, "team_id": 1},
                            {"user_id": 3, "username": "c3", "rating": 1750, "country": "GER", "college_id": 2, "is_pro": 1, "team_id": 2},
                            {"user_id": 4, "username": "c4", "rating": 1999, "country": "JPN", "college_id": 2, "is_pro": 0, "team_id": 2},
                            {"user_id": 5, "username": "c5", "rating": 2000, "country": "CAN", "college_id": 3, "is_pro": 1, "team_id": 3}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"candidate_master_count": 3}
                ], indent=2) + "\n"
            }
        ]
    },

    # 17. Find Users with Maximum Rating
    {
        "title": "Find Users with Maximum Rating",
        "slug": "sql-codechef-users-max-rating",
        "short_description": "Retrieve the top-ranked user(s) holding the global peak contest rating.",
        "description": (
            "### Problem Statement\n\n"
            "Display the platform's number one ranked competitor(s). Write a SQL query using a subquery "
            "to find all users whose rating equals the maximum rating in `platform_users`.\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Current rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return `user_id`, `username`, and `rating`. Order by `user_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "MAX", "Subquery", "Leaderboard"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Scalar Subquery", "MAX Function", "Tie Handling"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "tourist", "rating": 3800, "country": "BLR", "college_id": 1, "is_pro": 1, "team_id": 1},
                {"user_id": 2, "username": "benq", "rating": 3600, "country": "USA", "college_id": 2, "is_pro": 1, "team_id": 1},
                {"user_id": 3, "username": "ecnerwala", "rating": 3800, "country": "USA", "college_id": 2, "is_pro": 1, "team_id": 2},
                {"user_id": 4, "username": "maroonrk", "rating": 3500, "country": "JPN", "college_id": 3, "is_pro": 1, "team_id": 2}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT user_id, username, rating FROM platform_users WHERE rating = (SELECT MAX(rating) FROM platform_users) ORDER BY user_id ASC;",
        "test_cases": [
            {
                "id": "cc-max-rat-tc-1", "name": "Global Highest Rating Users", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "tourist", "rating": 3800, "country": "BLR", "college_id": 1, "is_pro": 1, "team_id": 1},
                            {"user_id": 2, "username": "benq", "rating": 3600, "country": "USA", "college_id": 2, "is_pro": 1, "team_id": 1},
                            {"user_id": 3, "username": "ecnerwala", "rating": 3800, "country": "USA", "college_id": 2, "is_pro": 1, "team_id": 2},
                            {"user_id": 4, "username": "maroonrk", "rating": 3500, "country": "JPN", "college_id": 3, "is_pro": 1, "team_id": 2}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"user_id": 1, "username": "tourist", "rating": 3800},
                    {"user_id": 3, "username": "ecnerwala", "rating": 3800}
                ], indent=2) + "\n"
            }
        ]
    },

    # 18. Users with Rating Greater Than 2199
    {
        "title": "Users with Rating Greater Than 2199",
        "slug": "sql-codechef-rating-greater-than-2199",
        "short_description": "List Grandmaster coders rated above 2199 with country details.",
        "description": (
            "### Problem Statement\n\n"
            "Identify Grandmaster-tier contestants. Write a SQL query to list all coders whose rating is strictly greater than `2199`.\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | Account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return `user_id`, `username`, `rating`, and `country`. Order results by `rating DESC, username ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "WHERE", "Grandmaster", "Sorting"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Tier Cutoffs", "Compound Sort Ordering", "Numeric Filters"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 80, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "red_coder_1", "rating": 2450, "country": "JPN", "college_id": 1, "is_pro": 1, "team_id": 1},
                {"user_id": 2, "username": "yellow_coder", "rating": 2199, "country": "USA", "college_id": 2, "is_pro": 0, "team_id": 1},
                {"user_id": 3, "username": "red_coder_2", "rating": 2600, "country": "IND", "college_id": 1, "is_pro": 1, "team_id": 2},
                {"user_id": 4, "username": "purple_coder", "rating": 1950, "country": "GER", "college_id": 3, "is_pro": 0, "team_id": 2}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT user_id, username, rating, country FROM platform_users WHERE rating > 2199 ORDER BY rating DESC, username ASC;",
        "test_cases": [
            {
                "id": "cc-gt-2199-tc-1", "name": "Grandmaster Roster Filter", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "red_coder_1", "rating": 2450, "country": "JPN", "college_id": 1, "is_pro": 1, "team_id": 1},
                            {"user_id": 2, "username": "yellow_coder", "rating": 2199, "country": "USA", "college_id": 2, "is_pro": 0, "team_id": 1},
                            {"user_id": 3, "username": "red_coder_2", "rating": 2600, "country": "IND", "college_id": 1, "is_pro": 1, "team_id": 2},
                            {"user_id": 4, "username": "purple_coder", "rating": 1950, "country": "GER", "college_id": 3, "is_pro": 0, "team_id": 2}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"user_id": 3, "username": "red_coder_2", "rating": 2600, "country": "IND"},
                    {"user_id": 1, "username": "red_coder_1", "rating": 2450, "country": "JPN"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 19. Sum of Rating with Pro Subscription
    {
        "title": "Sum of Rating with Pro Subscription",
        "slug": "sql-codechef-sum-rating-pro",
        "short_description": "Calculate aggregate rating points generated by Pro premium members.",
        "description": (
            "### Problem Statement\n\n"
            "Analyze subscription value by calculating the total sum of ratings accumulated by all users "
            "holding an active Pro membership (`is_pro = 1`).\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Contest rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag (1 = Pro, 0 = Free) |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return a single column named `total_pro_rating`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "SUM", "WHERE", "Aggregates"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["SUM Function", "Flag Filtering", "Aggregate Scalar"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "pro_alpha", "rating": 2100, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 1},
                {"user_id": 2, "username": "free_beta", "rating": 1600, "country": "IND", "college_id": 2, "is_pro": 0, "team_id": 1},
                {"user_id": 3, "username": "pro_gamma", "rating": 2400, "country": "GBR", "college_id": 1, "is_pro": 1, "team_id": 2},
                {"user_id": 4, "username": "pro_delta", "rating": 1800, "country": "CAN", "college_id": 3, "is_pro": 1, "team_id": 2}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT SUM(rating) AS total_pro_rating FROM platform_users WHERE is_pro = 1;",
        "test_cases": [
            {
                "id": "cc-sum-pro-tc-1", "name": "Pro Member Total Points", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "pro_alpha", "rating": 2100, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 1},
                            {"user_id": 2, "username": "free_beta", "rating": 1600, "country": "IND", "college_id": 2, "is_pro": 0, "team_id": 1},
                            {"user_id": 3, "username": "pro_gamma", "rating": 2400, "country": "GBR", "college_id": 1, "is_pro": 1, "team_id": 2},
                            {"user_id": 4, "username": "pro_delta", "rating": 1800, "country": "CAN", "college_id": 3, "is_pro": 1, "team_id": 2}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"total_pro_rating": 6300}
                ], indent=2) + "\n"
            }
        ]
    },

    # 20. Count of Users in Each Team
    {
        "title": "Count of Users in Each Team",
        "slug": "sql-codechef-users-each-team",
        "short_description": "Group active users by team to compute squad member counts.",
        "description": (
            "### Problem Statement\n\n"
            "Organize tournament brackets by team sizes. Write a SQL query to group users by `team_id` "
            "and compute how many registered members each team possesses. Exclude unassigned users (`team_id IS NULL`).\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Current rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team roster ID |\n\n"
            "#### Output Requirements\n"
            "Return `team_id` and `member_count`. Order by `member_count DESC, team_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "GROUP BY", "COUNT", "Teams"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["GROUP BY Clause", "Count Aggregation", "Multi-column Sort"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 80, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "u1", "rating": 1700, "country": "IND", "college_id": 1, "is_pro": 0, "team_id": 10},
                {"user_id": 2, "username": "u2", "rating": 1900, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 20},
                {"user_id": 3, "username": "u3", "rating": 2100, "country": "CAN", "college_id": 2, "is_pro": 1, "team_id": 10},
                {"user_id": 4, "username": "u4", "rating": 1500, "country": "GER", "college_id": 2, "is_pro": 0, "team_id": 10},
                {"user_id": 5, "username": "u5", "rating": 1800, "country": "JPN", "college_id": 3, "is_pro": 1, "team_id": 20},
                {"user_id": 6, "username": "u6", "rating": 1650, "country": "FRA", "college_id": 3, "is_pro": 0, "team_id": None}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT team_id, COUNT(*) AS member_count FROM platform_users WHERE team_id IS NOT NULL GROUP BY team_id ORDER BY member_count DESC, team_id ASC;",
        "test_cases": [
            {
                "id": "cc-team-count-tc-1", "name": "Team Roster Sizes", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "u1", "rating": 1700, "country": "IND", "college_id": 1, "is_pro": 0, "team_id": 10},
                            {"user_id": 2, "username": "u2", "rating": 1900, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 20},
                            {"user_id": 3, "username": "u3", "rating": 2100, "country": "CAN", "college_id": 2, "is_pro": 1, "team_id": 10},
                            {"user_id": 4, "username": "u4", "rating": 1500, "country": "GER", "college_id": 2, "is_pro": 0, "team_id": 10},
                            {"user_id": 5, "username": "u5", "rating": 1800, "country": "JPN", "college_id": 3, "is_pro": 1, "team_id": 20},
                            {"user_id": 6, "username": "u6", "rating": 1650, "country": "FRA", "college_id": 3, "is_pro": 0, "team_id": None}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"team_id": 10, "member_count": 3},
                    {"team_id": 20, "member_count": 2}
                ], indent=2) + "\n"
            }
        ]
    },

    # 21. User with Highest Rating in Each College
    {
        "title": "User with Highest Rating in Each College",
        "slug": "sql-codechef-highest-rating-college",
        "short_description": "Determine the highest contest rating achieved in each participating institution.",
        "description": (
            "### Problem Statement\n\n"
            "Inter-collegiate championships require tracking top performances. Write a SQL query to find "
            "the maximum rating recorded for each college. Exclude students without an assigned college (`college_id IS NULL`).\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Current rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return `college_id` and `highest_rating`. Order by `highest_rating DESC, college_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "GROUP BY", "MAX", "Collegiate"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Grouped Maximum", "MAX Function", "College Benchmarking"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 90, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "mit_1", "rating": 2600, "country": "USA", "college_id": 501, "is_pro": 1, "team_id": 1},
                {"user_id": 2, "username": "mit_2", "rating": 2400, "country": "USA", "college_id": 501, "is_pro": 1, "team_id": 1},
                {"user_id": 3, "username": "ox_1", "rating": 2800, "country": "GBR", "college_id": 502, "is_pro": 1, "team_id": 2},
                {"user_id": 4, "username": "ox_2", "rating": 2200, "country": "GBR", "college_id": 502, "is_pro": 0, "team_id": 2},
                {"user_id": 5, "username": "iit_1", "rating": 2750, "country": "IND", "college_id": 503, "is_pro": 1, "team_id": 3}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT college_id, MAX(rating) AS highest_rating FROM platform_users WHERE college_id IS NOT NULL GROUP BY college_id ORDER BY highest_rating DESC, college_id ASC;",
        "test_cases": [
            {
                "id": "cc-col-max-tc-1", "name": "Institutional Peak Ratings", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "mit_1", "rating": 2600, "country": "USA", "college_id": 501, "is_pro": 1, "team_id": 1},
                            {"user_id": 2, "username": "mit_2", "rating": 2400, "country": "USA", "college_id": 501, "is_pro": 1, "team_id": 1},
                            {"user_id": 3, "username": "ox_1", "rating": 2800, "country": "GBR", "college_id": 502, "is_pro": 1, "team_id": 2},
                            {"user_id": 4, "username": "ox_2", "rating": 2200, "country": "GBR", "college_id": 502, "is_pro": 0, "team_id": 2},
                            {"user_id": 5, "username": "iit_1", "rating": 2750, "country": "IND", "college_id": 503, "is_pro": 1, "team_id": 3}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"college_id": 502, "highest_rating": 2800},
                    {"college_id": 503, "highest_rating": 2750},
                    {"college_id": 501, "highest_rating": 2600}
                ], indent=2) + "\n"
            }
        ]
    },

    # 22. Ordered List of Students in Each College
    {
        "title": "Ordered List of Students in Each College",
        "slug": "sql-codechef-ordered-students-college",
        "short_description": "Multi-tier hierarchical ordering of institutional students.",
        "description": (
            "### Problem Statement\n\n"
            "Generate an official campus leaderboard. Write a SQL query to list all students associated with an educational institute, "
            "sorted systematically so that colleges are listed in ascending order, and within each college, students appear from highest rating to lowest.\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Contest rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return `college_id`, `username`, and `rating`. Exclude rows where `college_id IS NULL`. "
            "Order by `college_id ASC, rating DESC, username ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "ORDER BY", "Hierarchical Sort", "Leaderboard"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Hierarchical Sorting", "Tie Breaking", "Multi-column Order"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 80, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "alice", "rating": 1900, "country": "USA", "college_id": 10, "is_pro": 1, "team_id": 1},
                {"user_id": 2, "username": "bob", "rating": 2100, "country": "USA", "college_id": 10, "is_pro": 0, "team_id": 1},
                {"user_id": 3, "username": "charlie", "rating": 1800, "country": "CAN", "college_id": 20, "is_pro": 1, "team_id": 2},
                {"user_id": 4, "username": "david", "rating": 2200, "country": "CAN", "college_id": 20, "is_pro": 1, "team_id": 2},
                {"user_id": 5, "username": "anna", "rating": 2100, "country": "USA", "college_id": 10, "is_pro": 1, "team_id": 3}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT college_id, username, rating FROM platform_users WHERE college_id IS NOT NULL ORDER BY college_id ASC, rating DESC, username ASC;",
        "test_cases": [
            {
                "id": "cc-col-ord-tc-1", "name": "Institutional Hierarchy Sort", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "alice", "rating": 1900, "country": "USA", "college_id": 10, "is_pro": 1, "team_id": 1},
                            {"user_id": 2, "username": "bob", "rating": 2100, "country": "USA", "college_id": 10, "is_pro": 0, "team_id": 1},
                            {"user_id": 3, "username": "charlie", "rating": 1800, "country": "CAN", "college_id": 20, "is_pro": 1, "team_id": 2},
                            {"user_id": 4, "username": "david", "rating": 2200, "country": "CAN", "college_id": 20, "is_pro": 1, "team_id": 2},
                            {"user_id": 5, "username": "anna", "rating": 2100, "country": "USA", "college_id": 10, "is_pro": 1, "team_id": 3}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"college_id": 10, "username": "anna", "rating": 2100},
                    {"college_id": 10, "username": "bob", "rating": 2100},
                    {"college_id": 10, "username": "alice", "rating": 1900},
                    {"college_id": 20, "username": "david", "rating": 2200},
                    {"college_id": 20, "username": "charlie", "rating": 1800}
                ], indent=2) + "\n"
            }
        ]
    },

    # 23. Find Team with Highest Average Rating
    {
        "title": "Find Team with Highest Average Rating",
        "slug": "sql-codechef-team-highest-avg-rating",
        "short_description": "Locate the top-performing squad with minimum roster requirements.",
        "description": (
            "### Problem Statement\n\n"
            "Award the champion team accolade for the season. Write a SQL query to identify the team (`team_id`) "
            "with the highest average rating among teams that have at least `2` active members.\n\n"
            "#### Table Schema: `platform_users`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `user_id` | INT (PK) | User account ID |\n"
            "| `username` | VARCHAR(50) | Coder handle |\n"
            "| `rating` | INT | Contest rating |\n"
            "| `country` | VARCHAR(50) | Country |\n"
            "| `college_id` | INT | College ID |\n"
            "| `is_pro` | INT | Pro subscriber flag |\n"
            "| `team_id` | INT | Team ID |\n\n"
            "#### Output Requirements\n"
            "Return `team_id` and `team_avg_rating` (rounded to 2 decimal places). Exclude null teams. "
            "Order by `team_avg_rating DESC, team_id ASC` and retrieve only the single top team (`LIMIT 1`)."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "GROUP BY", "HAVING", "LIMIT"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["HAVING Clause", "Grouped Filtering", "Top K Selection"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE platform_users ("
            "  user_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  rating INT NOT NULL,"
            "  country TEXT NOT NULL,"
            "  college_id INT,"
            "  is_pro INT NOT NULL,"
            "  team_id INT"
            ");"
        ),
        "fixtures": {
            "platform_users": [
                {"user_id": 1, "username": "squadA_1", "rating": 2400, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 100},
                {"user_id": 2, "username": "squadA_2", "rating": 2600, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 100},
                {"user_id": 3, "username": "solo_star", "rating": 3000, "country": "IND", "college_id": 2, "is_pro": 1, "team_id": 200},
                {"user_id": 4, "username": "squadB_1", "rating": 2200, "country": "CAN", "college_id": 3, "is_pro": 1, "team_id": 300},
                {"user_id": 5, "username": "squadB_2", "rating": 2100, "country": "CAN", "college_id": 3, "is_pro": 0, "team_id": 300}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT team_id, ROUND(AVG(rating), 2) AS team_avg_rating FROM platform_users WHERE team_id IS NOT NULL GROUP BY team_id HAVING COUNT(*) >= 2 ORDER BY team_avg_rating DESC, team_id ASC LIMIT 1;",
        "test_cases": [
            {
                "id": "cc-champ-team-tc-1", "name": "Championship Team Calculation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE platform_users (user_id INT PRIMARY KEY, username TEXT NOT NULL, rating INT NOT NULL, country TEXT NOT NULL, college_id INT, is_pro INT NOT NULL, team_id INT);",
                    "fixtures": {
                        "platform_users": [
                            {"user_id": 1, "username": "squadA_1", "rating": 2400, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 100},
                            {"user_id": 2, "username": "squadA_2", "rating": 2600, "country": "USA", "college_id": 1, "is_pro": 1, "team_id": 100},
                            {"user_id": 3, "username": "solo_star", "rating": 3000, "country": "IND", "college_id": 2, "is_pro": 1, "team_id": 200},
                            {"user_id": 4, "username": "squadB_1", "rating": 2200, "country": "CAN", "college_id": 3, "is_pro": 1, "team_id": 300},
                            {"user_id": 5, "username": "squadB_2", "rating": 2100, "country": "CAN", "college_id": 3, "is_pro": 0, "team_id": 300}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"team_id": 100, "team_avg_rating": 2500.0}
                ], indent=2) + "\n"
            }
        ]
    }
]
