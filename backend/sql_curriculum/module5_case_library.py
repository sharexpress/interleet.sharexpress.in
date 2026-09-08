# Copyright 2026 Sharexpress Contributors
# Module 5: Case Study - Library Management System (CASE Expressions) (10 Problems)

import json

MODULE5_CHALLENGES = [
    # 44. Book Availability Status
    {
        "title": "Library: Book Availability Status",
        "slug": "sql-lib-book-availability-status",
        "short_description": "Use a simple CASE statement to classify inventory as Available or Out of Stock.",
        "description": (
            "### Problem Statement\n\n"
            "The library catalog kiosk helps patrons identify items available on shelves. "
            "Write a SQL query using a `CASE` expression to inspect `available_copies`. "
            "If `available_copies > 0`, display `'Available'`; otherwise, display `'Out of Stock'` "
            "under the alias `status`.\n\n"
            "#### Table Schema: `books`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `book_id` | INT (PK) | Unique book identifier |\n"
            "| `title` | TEXT | Book title |\n"
            "| `available_copies` | INT | Physical copies currently on shelf |\n\n"
            "#### Output Requirements\n"
            "Return `book_id`, `title`, `available_copies`, and `status`.\n"
            "Order by `book_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "CASE", "Conditional Logic", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Searched CASE", "Binary Conditional", "Inventory Status"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE books ("
            "  book_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  available_copies INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "books": [
                {"book_id": 1, "title": "Clean Code", "available_copies": 3},
                {"book_id": 2, "title": "Design Patterns", "available_copies": 0},
                {"book_id": 3, "title": "Introduction to Algorithms", "available_copies": 1},
                {"book_id": 4, "title": "The Pragmatic Programmer", "available_copies": 0}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT book_id, title, available_copies, "
            "CASE WHEN available_copies > 0 THEN 'Available' ELSE 'Out of Stock' END AS status "
            "FROM books "
            "ORDER BY book_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-avail-tc-1", "name": "Binary Availability Flag", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE books (book_id INT PRIMARY KEY, title TEXT NOT NULL, available_copies INT NOT NULL);",
                    "fixtures": {
                        "books": [
                            {"book_id": 1, "title": "Clean Code", "available_copies": 3},
                            {"book_id": 2, "title": "Design Patterns", "available_copies": 0},
                            {"book_id": 3, "title": "Introduction to Algorithms", "available_copies": 1},
                            {"book_id": 4, "title": "The Pragmatic Programmer", "available_copies": 0}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"book_id": 1, "title": "Clean Code", "available_copies": 3, "status": "Available"},
                    {"book_id": 2, "title": "Design Patterns", "available_copies": 0, "status": "Out of Stock"},
                    {"book_id": 3, "title": "Introduction to Algorithms", "available_copies": 1, "status": "Available"},
                    {"book_id": 4, "title": "The Pragmatic Programmer", "available_copies": 0, "status": "Out of Stock"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 45. Member Tier Classification
    {
        "title": "Library: Member Tier Classification",
        "slug": "sql-lib-member-tier-classification",
        "short_description": "Assign membership tiers (Gold, Silver, Bronze) based on completed reading volume.",
        "description": (
            "### Problem Statement\n\n"
            "Patron loyalty rewards depend on reading milestones. "
            "Write a SQL query using a multi-branch `CASE` expression to classify each member's `membership_tier`:\n"
            "- `'Gold'` when `total_books_read >= 50`\n"
            "- `'Silver'` when `total_books_read >= 20`\n"
            "- `'Bronze'` for all others\n\n"
            "#### Table Schema: `members`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `member_id` | INT (PK) | Member identification number |\n"
            "| `name` | TEXT | Member full name |\n"
            "| `total_books_read` | INT | Lifetime books borrowed & completed |\n\n"
            "#### Output Requirements\n"
            "Return `member_id`, `name`, `total_books_read`, and `membership_tier`.\n"
            "Order by `total_books_read DESC`, `member_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "CASE", "Multi-branch", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Tiering Logic", "Ordered Evaluation", "Patron Classification"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 55, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE members ("
            "  member_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  total_books_read INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "members": [
                {"member_id": 10, "name": "Hermione Granger", "total_books_read": 142},
                {"member_id": 20, "name": "Ron Weasley", "total_books_read": 14},
                {"member_id": 30, "name": "Harry Potter", "total_books_read": 38},
                {"member_id": 40, "name": "Neville Longbottom", "total_books_read": 21}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT member_id, name, total_books_read, "
            "CASE "
            "  WHEN total_books_read >= 50 THEN 'Gold' "
            "  WHEN total_books_read >= 20 THEN 'Silver' "
            "  ELSE 'Bronze' "
            "END AS membership_tier "
            "FROM members "
            "ORDER BY total_books_read DESC, member_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-tiers-tc-1", "name": "Multi-Tier Milestone Allocation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE members (member_id INT PRIMARY KEY, name TEXT NOT NULL, total_books_read INT NOT NULL);",
                    "fixtures": {
                        "members": [
                            {"member_id": 10, "name": "Hermione Granger", "total_books_read": 142},
                            {"member_id": 20, "name": "Ron Weasley", "total_books_read": 14},
                            {"member_id": 30, "name": "Harry Potter", "total_books_read": 38},
                            {"member_id": 40, "name": "Neville Longbottom", "total_books_read": 21}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"member_id": 10, "name": "Hermione Granger", "total_books_read": 142, "membership_tier": "Gold"},
                    {"member_id": 30, "name": "Harry Potter", "total_books_read": 38, "membership_tier": "Silver"},
                    {"member_id": 40, "name": "Neville Longbottom", "total_books_read": 21, "membership_tier": "Silver"},
                    {"member_id": 20, "name": "Ron Weasley", "total_books_read": 14, "membership_tier": "Bronze"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 46. Tiered Overdue Penalty Calculation
    {
        "title": "Library: Tiered Overdue Penalty Calculation",
        "slug": "sql-lib-overdue-penalty-calculation",
        "short_description": "Compute progressive fine charges using conditional mathematical formulas in CASE.",
        "description": (
            "### Problem Statement\n\n"
            "The library board assesses overdue book fines progressively:\n"
            "- If `days_overdue <= 0`, fine is `0.0`.\n"
            "- If `days_overdue <= 7`, fine is `$0.50` per overdue day (`ROUND(days_overdue * 0.50, 2)`).\n"
            "- If `days_overdue > 7`, fine is `$0.50` for the first 7 days plus `$1.00` per day for every day beyond 7 (`ROUND(3.50 + (days_overdue - 7) * 1.00, 2)`).\n\n"
            "#### Table Schema: `loans`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `loan_id` | INT (PK) | Loan transaction ID |\n"
            "| `member_id` | INT | Borrower ID |\n"
            "| `days_overdue` | INT | Days past due date (negative or 0 if timely) |\n\n"
            "#### Output Requirements\n"
            "Return `loan_id`, `member_id`, `days_overdue`, and `penalty_fee`.\n"
            "Order by `loan_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CASE", "Progressive Rates", "Arithmetic", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Piecewise Calculation", "Progressive Fines", "Arithmetic CASE"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 14,
        "schema_sql": (
            "CREATE TABLE loans ("
            "  loan_id INT PRIMARY KEY,"
            "  member_id INT NOT NULL,"
            "  days_overdue INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "loans": [
                {"loan_id": 1, "member_id": 101, "days_overdue": 0},
                {"loan_id": 2, "member_id": 102, "days_overdue": 4},
                {"loan_id": 3, "member_id": 103, "days_overdue": 7},
                {"loan_id": 4, "member_id": 104, "days_overdue": 12},
                {"loan_id": 5, "member_id": 105, "days_overdue": -2}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT loan_id, member_id, days_overdue, "
            "CASE "
            "  WHEN days_overdue <= 0 THEN 0.0 "
            "  WHEN days_overdue <= 7 THEN ROUND(days_overdue * 0.50, 2) "
            "  ELSE ROUND(3.50 + (days_overdue - 7) * 1.00, 2) "
            "END AS penalty_fee "
            "FROM loans "
            "ORDER BY loan_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-penalty-tc-1", "name": "Progressive Overdue Fine Ladder", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE loans (loan_id INT PRIMARY KEY, member_id INT NOT NULL, days_overdue INT NOT NULL);",
                    "fixtures": {
                        "loans": [
                            {"loan_id": 1, "member_id": 101, "days_overdue": 0},
                            {"loan_id": 2, "member_id": 102, "days_overdue": 4},
                            {"loan_id": 3, "member_id": 103, "days_overdue": 7},
                            {"loan_id": 4, "member_id": 104, "days_overdue": 12},
                            {"loan_id": 5, "member_id": 105, "days_overdue": -2}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"loan_id": 1, "member_id": 101, "days_overdue": 0, "penalty_fee": 0.0},
                    {"loan_id": 2, "member_id": 102, "days_overdue": 4, "penalty_fee": 2.0},
                    {"loan_id": 3, "member_id": 103, "days_overdue": 7, "penalty_fee": 3.5},
                    {"loan_id": 4, "member_id": 104, "days_overdue": 12, "penalty_fee": 8.5},
                    {"loan_id": 5, "member_id": 105, "days_overdue": -2, "penalty_fee": 0.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 47. Conditional Stock Matrix by Genre (Pivot Aggregation)
    {
        "title": "Library: Stock Matrix by Genre",
        "slug": "sql-lib-conditional-book-inventory-count",
        "short_description": "Use SUM(CASE WHEN ...) to count available and checked-out titles across genres.",
        "description": (
            "### Problem Statement\n\n"
            "Inventory managers want to analyze stocking health per genre. "
            "Write a SQL query using conditional aggregation (`SUM(CASE WHEN ...)`): "
            "For each `genre`, calculate:\n"
            "1. `total_titles`: Total number of distinct book records\n"
            "2. `available_titles`: Number of titles with `available_copies > 0`\n"
            "3. `unavailable_titles`: Number of titles with `available_copies = 0`\n\n"
            "#### Table Schema: `books`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `book_id` | INT (PK) | Book identifier |\n"
            "| `genre` | TEXT | Genre category |\n"
            "| `available_copies` | INT | Copies on shelf |\n\n"
            "#### Output Requirements\n"
            "Return `genre`, `total_titles`, `available_titles`, and `unavailable_titles`.\n"
            "Order by `total_titles DESC`, `genre ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CASE", "Conditional Aggregation", "GROUP BY", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["SUM(CASE WHEN)", "Pivot Aggregates", "Genre Stock Analysis"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 70, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE books ("
            "  book_id INT PRIMARY KEY,"
            "  genre TEXT NOT NULL,"
            "  available_copies INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "books": [
                {"book_id": 1, "genre": "Sci-Fi", "available_copies": 2},
                {"book_id": 2, "genre": "Sci-Fi", "available_copies": 0},
                {"book_id": 3, "genre": "Sci-Fi", "available_copies": 5},
                {"book_id": 4, "genre": "Fantasy", "available_copies": 1},
                {"book_id": 5, "genre": "Fantasy", "available_copies": 0},
                {"book_id": 6, "genre": "History", "available_copies": 0}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT genre, COUNT(*) AS total_titles, "
            "SUM(CASE WHEN available_copies > 0 THEN 1 ELSE 0 END) AS available_titles, "
            "SUM(CASE WHEN available_copies = 0 THEN 1 ELSE 0 END) AS unavailable_titles "
            "FROM books "
            "GROUP BY genre "
            "ORDER BY total_titles DESC, genre ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-genre-stock-tc-1", "name": "Conditional Stock Matrix", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE books (book_id INT PRIMARY KEY, genre TEXT NOT NULL, available_copies INT NOT NULL);",
                    "fixtures": {
                        "books": [
                            {"book_id": 1, "genre": "Sci-Fi", "available_copies": 2},
                            {"book_id": 2, "genre": "Sci-Fi", "available_copies": 0},
                            {"book_id": 3, "genre": "Sci-Fi", "available_copies": 5},
                            {"book_id": 4, "genre": "Fantasy", "available_copies": 1},
                            {"book_id": 5, "genre": "Fantasy", "available_copies": 0},
                            {"book_id": 6, "genre": "History", "available_copies": 0}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"genre": "Sci-Fi", "total_titles": 3, "available_titles": 2, "unavailable_titles": 1},
                    {"genre": "Fantasy", "total_titles": 2, "available_titles": 1, "unavailable_titles": 1},
                    {"genre": "History", "total_titles": 1, "available_titles": 0, "unavailable_titles": 1}
                ], indent=2) + "\n"
            }
        ]
    },

    # 48. Literary Era Classification
    {
        "title": "Library: Literary Era Classification",
        "slug": "sql-lib-publication-era",
        "short_description": "Classify works into Classic, Modern, and Contemporary literary periods.",
        "description": (
            "### Problem Statement\n\n"
            "The archive curators are grouping literature into chronological eras:\n"
            "- `'Classic'`: Books published before 1950 (`published_year < 1950`)\n"
            "- `'Modern'`: Books published between 1950 and 1999 inclusive (`published_year BETWEEN 1950 AND 1999`)\n"
            "- `'Contemporary'`: Books published in 2000 or later\n\n"
            "#### Table Schema: `books`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `book_id` | INT (PK) | Book ID |\n"
            "| `title` | TEXT | Book title |\n"
            "| `published_year` | INT | Original publication year |\n\n"
            "#### Output Requirements\n"
            "Return `book_id`, `title`, `published_year`, and `era`.\n"
            "Order by `published_year ASC`, `book_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "CASE", "Range Conditions", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["BETWEEN in CASE", "Epoch Categorization", "Sort by Epoch"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 55, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE books ("
            "  book_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  published_year INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "books": [
                {"book_id": 1, "title": "Pride and Prejudice", "published_year": 1813},
                {"book_id": 2, "title": "1984", "published_year": 1949},
                {"book_id": 3, "title": "To Kill a Mockingbird", "published_year": 1960},
                {"book_id": 4, "title": "The Road", "published_year": 2006}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT book_id, title, published_year, "
            "CASE "
            "  WHEN published_year < 1950 THEN 'Classic' "
            "  WHEN published_year BETWEEN 1950 AND 1999 THEN 'Modern' "
            "  ELSE 'Contemporary' "
            "END AS era "
            "FROM books "
            "ORDER BY published_year ASC, book_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-era-tc-1", "name": "Literary Era Discretization", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE books (book_id INT PRIMARY KEY, title TEXT NOT NULL, published_year INT NOT NULL);",
                    "fixtures": {
                        "books": [
                            {"book_id": 1, "title": "Pride and Prejudice", "published_year": 1813},
                            {"book_id": 2, "title": "1984", "published_year": 1949},
                            {"book_id": 3, "title": "To Kill a Mockingbird", "published_year": 1960},
                            {"book_id": 4, "title": "The Road", "published_year": 2006}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"book_id": 1, "title": "Pride and Prejudice", "published_year": 1813, "era": "Classic"},
                    {"book_id": 2, "title": "1984", "published_year": 1949, "era": "Classic"},
                    {"book_id": 3, "title": "To Kill a Mockingbird", "published_year": 1960, "era": "Modern"},
                    {"book_id": 4, "title": "The Road", "published_year": 2006, "era": "Contemporary"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 49. Dynamic Loan Lifecycle Status
    {
        "title": "Library: Dynamic Loan Lifecycle Status",
        "slug": "sql-lib-loan-status-report",
        "short_description": "Map checkout status (Returned, Overdue, Active) based on return timestamps and deadlines.",
        "description": (
            "### Problem Statement\n\n"
            "The circulation system tracks whether a loan is concluded or outstanding. "
            "Given the reference audit cutoff date of `'2026-03-01'`, write a SQL query to classify each loan:\n"
            "- If `returned_date IS NOT NULL`, status is `'Returned'`\n"
            "- Else if `due_date < '2026-03-01'`, status is `'Overdue'`\n"
            "- Otherwise, status is `'Active'`\n\n"
            "#### Table Schema: `loans`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `loan_id` | INT (PK) | Loan ID |\n"
            "| `book_id` | INT | Book ID |\n"
            "| `member_id` | INT | Member ID |\n"
            "| `due_date` | TEXT | Due date in 'YYYY-MM-DD' |\n"
            "| `returned_date` | TEXT | Return date or NULL |\n\n"
            "#### Output Requirements\n"
            "Return `loan_id`, `book_id`, `member_id`, and `loan_status`.\n"
            "Order by `loan_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CASE", "NULL Checking", "Date Evaluation", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["IS NOT NULL with CASE", "Date Boundaries", "Status State Machine"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE loans ("
            "  loan_id INT PRIMARY KEY,"
            "  book_id INT NOT NULL,"
            "  member_id INT NOT NULL,"
            "  due_date TEXT NOT NULL,"
            "  returned_date TEXT"
            ");"
        ),
        "fixtures": {
            "loans": [
                {"loan_id": 1, "book_id": 101, "member_id": 5, "due_date": "2026-02-15", "returned_date": "2026-02-14"},
                {"loan_id": 2, "book_id": 102, "member_id": 6, "due_date": "2026-02-20", "returned_date": None},
                {"loan_id": 3, "book_id": 103, "member_id": 7, "due_date": "2026-03-10", "returned_date": None}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT loan_id, book_id, member_id, "
            "CASE "
            "  WHEN returned_date IS NOT NULL THEN 'Returned' "
            "  WHEN due_date < '2026-03-01' THEN 'Overdue' "
            "  ELSE 'Active' "
            "END AS loan_status "
            "FROM loans "
            "ORDER BY loan_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-loan-status-tc-1", "name": "Loan State Machine Evaluation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE loans (loan_id INT PRIMARY KEY, book_id INT NOT NULL, member_id INT NOT NULL, due_date TEXT NOT NULL, returned_date TEXT);",
                    "fixtures": {
                        "loans": [
                            {"loan_id": 1, "book_id": 101, "member_id": 5, "due_date": "2026-02-15", "returned_date": "2026-02-14"},
                            {"loan_id": 2, "book_id": 102, "member_id": 6, "due_date": "2026-02-20", "returned_date": None},
                            {"loan_id": 3, "book_id": 103, "member_id": 7, "due_date": "2026-03-10", "returned_date": None}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"loan_id": 1, "book_id": 101, "member_id": 5, "loan_status": "Returned"},
                    {"loan_id": 2, "book_id": 102, "member_id": 6, "loan_status": "Overdue"},
                    {"loan_id": 3, "book_id": 103, "member_id": 7, "loan_status": "Active"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 50. Borrowing Eligibility Audit
    {
        "title": "Library: Borrowing Eligibility Audit",
        "slug": "sql-lib-member-activity-profile",
        "short_description": "Audit patron circulation standing (Blocked, At Limit, Eligible) using conditional logic.",
        "description": (
            "### Problem Statement\n\n"
            "The front desk circulation system evaluates borrowing permissions based on active policies:\n"
            "1. If `outstanding_fines > 0.0`, eligibility is `'Blocked'` due to overdue arrears.\n"
            "2. Else if `active_loans >= 3`, eligibility is `'At Limit'`.\n"
            "3. Otherwise, eligibility is `'Eligible'`.\n\n"
            "#### Table Schema: `members`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `member_id` | INT (PK) | Member ID |\n"
            "| `name` | TEXT | Member name |\n"
            "| `outstanding_fines` | REAL | Total unpaid fines in USD |\n"
            "| `active_loans` | INT | Number of books currently checked out |\n\n"
            "#### Output Requirements\n"
            "Return `member_id`, `name`, and `borrow_eligibility`.\n"
            "Order by `member_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CASE", "Business Logic", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Policy Rules", "Multi-condition Branches", "Member Rights"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE members ("
            "  member_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  outstanding_fines REAL NOT NULL,"
            "  active_loans INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "members": [
                {"member_id": 1, "name": "Samwell Tarly", "outstanding_fines": 0.00, "active_loans": 2},
                {"member_id": 2, "name": "Arya Stark", "outstanding_fines": 4.50, "active_loans": 1},
                {"member_id": 3, "name": "Bran Stark", "outstanding_fines": 0.00, "active_loans": 3},
                {"member_id": 4, "name": "Jon Snow", "outstanding_fines": 0.00, "active_loans": 0}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT member_id, name, "
            "CASE "
            "  WHEN outstanding_fines > 0.0 THEN 'Blocked' "
            "  WHEN active_loans >= 3 THEN 'At Limit' "
            "  ELSE 'Eligible' "
            "END AS borrow_eligibility "
            "FROM members "
            "ORDER BY member_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-eligibility-tc-1", "name": "Policy Priority Evaluation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE members (member_id INT PRIMARY KEY, name TEXT NOT NULL, outstanding_fines REAL NOT NULL, active_loans INT NOT NULL);",
                    "fixtures": {
                        "members": [
                            {"member_id": 1, "name": "Samwell Tarly", "outstanding_fines": 0.00, "active_loans": 2},
                            {"member_id": 2, "name": "Arya Stark", "outstanding_fines": 4.50, "active_loans": 1},
                            {"member_id": 3, "name": "Bran Stark", "outstanding_fines": 0.00, "active_loans": 3},
                            {"member_id": 4, "name": "Jon Snow", "outstanding_fines": 0.00, "active_loans": 0}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"member_id": 1, "name": "Samwell Tarly", "borrow_eligibility": "Eligible"},
                    {"member_id": 2, "name": "Arya Stark", "borrow_eligibility": "Blocked"},
                    {"member_id": 3, "name": "Bran Stark", "borrow_eligibility": "At Limit"},
                    {"member_id": 4, "name": "Jon Snow", "borrow_eligibility": "Eligible"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 51. High-Rating Ratio by Genre
    {
        "title": "Library: High-Rating Ratio by Genre",
        "slug": "sql-lib-genre-popularity-index",
        "short_description": "Compute the percentage of high-rated books (>= 4.50) across each genre.",
        "description": (
            "### Problem Statement\n\n"
            "Curators want to assess the critical acclaim of different library sections. "
            "Write a SQL query using conditional counting to calculate the percentage of books with "
            "`rating >= 4.50` within each `genre`. "
            "Formula: `ROUND(100.0 * SUM(CASE WHEN rating >= 4.50 THEN 1 ELSE 0 END) / COUNT(*), 1)`.\n\n"
            "#### Table Schema: `books`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `book_id` | INT (PK) | Book ID |\n"
            "| `genre` | TEXT | Category |\n"
            "| `rating` | REAL | Star rating |\n\n"
            "#### Output Requirements\n"
            "Return `genre`, `total_books`, and `high_rated_pct`.\n"
            "Order by `high_rated_pct DESC`, `genre ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CASE", "Ratio", "Percentage", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Conditional Ratio", "ROUND with 1 decimal", "Percentage Aggregation"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 70, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE books ("
            "  book_id INT PRIMARY KEY,"
            "  genre TEXT NOT NULL,"
            "  rating REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "books": [
                {"book_id": 1, "genre": "Philosophy", "rating": 4.80},
                {"book_id": 2, "genre": "Philosophy", "rating": 4.60},
                {"book_id": 3, "genre": "Philosophy", "rating": 4.20},
                {"book_id": 4, "genre": "Thriller", "rating": 4.70},
                {"book_id": 5, "genre": "Thriller", "rating": 3.90},
                {"book_id": 6, "genre": "Cookbook", "rating": 4.10}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT genre, COUNT(*) AS total_books, "
            "ROUND(100.0 * SUM(CASE WHEN rating >= 4.50 THEN 1 ELSE 0 END) / COUNT(*), 1) AS high_rated_pct "
            "FROM books "
            "GROUP BY genre "
            "ORDER BY high_rated_pct DESC, genre ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-high-rated-tc-1", "name": "Quality Ratio Aggregation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE books (book_id INT PRIMARY KEY, genre TEXT NOT NULL, rating REAL NOT NULL);",
                    "fixtures": {
                        "books": [
                            {"book_id": 1, "genre": "Philosophy", "rating": 4.80},
                            {"book_id": 2, "genre": "Philosophy", "rating": 4.60},
                            {"book_id": 3, "genre": "Philosophy", "rating": 4.20},
                            {"book_id": 4, "genre": "Thriller", "rating": 4.70},
                            {"book_id": 5, "genre": "Thriller", "rating": 3.90},
                            {"book_id": 6, "genre": "Cookbook", "rating": 4.10}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"genre": "Philosophy", "total_books": 3, "high_rated_pct": 66.7},
                    {"genre": "Thriller", "total_books": 2, "high_rated_pct": 50.0},
                    {"genre": "Cookbook", "total_books": 1, "high_rated_pct": 0.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 52. Inventory Depletion & Restock Trigger
    {
        "title": "Library: Restock Urgency Tiers",
        "slug": "sql-lib-reorder-urgency-tier",
        "short_description": "Trigger reorder alerts based on remaining shelf copy ratios.",
        "description": (
            "### Problem Statement\n\n"
            "Logistics monitors copy depletion to trigger replacement orders:\n"
            "- If `available_copies = 0`, urgency is `'Urgent Restock'`\n"
            "- Else if `(available_copies * 1.0 / total_copies) < 0.30`, urgency is `'Low Inventory'`\n"
            "- Otherwise, urgency is `'Adequate'`\n\n"
            "#### Table Schema: `books`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `book_id` | INT (PK) | Book identifier |\n"
            "| `title` | TEXT | Book title |\n"
            "| `available_copies` | INT | Copies on shelf |\n"
            "| `total_copies` | INT | Total system copies |\n\n"
            "#### Output Requirements\n"
            "Return `book_id`, `title`, `available_copies`, `total_copies`, and `inventory_alert`.\n"
            "Order by `available_copies ASC`, `book_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CASE", "Ratio Calculations", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Division by Float", "Depletion Monitoring", "Logistics Triggers"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 14,
        "schema_sql": (
            "CREATE TABLE books ("
            "  book_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  available_copies INT NOT NULL,"
            "  total_copies INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "books": [
                {"book_id": 101, "title": "Database System Concepts", "available_copies": 0, "total_copies": 6},
                {"book_id": 102, "title": "Operating Systems Internals", "available_copies": 1, "total_copies": 5},
                {"book_id": 103, "title": "Computer Networks", "available_copies": 4, "total_copies": 5},
                {"book_id": 104, "title": "Artificial Intelligence A Modern Approach", "available_copies": 2, "total_copies": 4}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT book_id, title, available_copies, total_copies, "
            "CASE "
            "  WHEN available_copies = 0 THEN 'Urgent Restock' "
            "  WHEN (available_copies * 1.0 / total_copies) < 0.30 THEN 'Low Inventory' "
            "  ELSE 'Adequate' "
            "END AS inventory_alert "
            "FROM books "
            "ORDER BY available_copies ASC, book_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-reorder-tc-1", "name": "Ratio Depletion Check", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE books (book_id INT PRIMARY KEY, title TEXT NOT NULL, available_copies INT NOT NULL, total_copies INT NOT NULL);",
                    "fixtures": {
                        "books": [
                            {"book_id": 101, "title": "Database System Concepts", "available_copies": 0, "total_copies": 6},
                            {"book_id": 102, "title": "Operating Systems Internals", "available_copies": 1, "total_copies": 5},
                            {"book_id": 103, "title": "Computer Networks", "available_copies": 4, "total_copies": 5},
                            {"book_id": 104, "title": "Artificial Intelligence A Modern Approach", "available_copies": 2, "total_copies": 4}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"book_id": 101, "title": "Database System Concepts", "available_copies": 0, "total_copies": 6, "inventory_alert": "Urgent Restock"},
                    {"book_id": 102, "title": "Operating Systems Internals", "available_copies": 1, "total_copies": 5, "inventory_alert": "Low Inventory"},
                    {"book_id": 104, "title": "Artificial Intelligence A Modern Approach", "available_copies": 2, "total_copies": 4, "inventory_alert": "Adequate"},
                    {"book_id": 103, "title": "Computer Networks", "available_copies": 4, "total_copies": 5, "inventory_alert": "Adequate"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 53. Fine Amnesty & Concessions
    {
        "title": "Library: Fine Amnesty & Concessions",
        "slug": "sql-lib-discounted-fine-waiver",
        "short_description": "Apply conditional member discounts to calculate adjusted amnesty fines.",
        "description": (
            "### Problem Statement\n\n"
            "An annual community library amnesty program offers targeted fine waivers based on patron affiliation:\n"
            "- `'Student'` members receive a 50% waiver: `ROUND(outstanding_fines * 0.50, 2)`\n"
            "- `'Senior'` members receive a 70% waiver: `ROUND(outstanding_fines * 0.30, 2)`\n"
            "- All other members pay full `outstanding_fines`\n\n"
            "#### Table Schema: `members`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `member_id` | INT (PK) | Member account ID |\n"
            "| `name` | TEXT | Member name |\n"
            "| `member_type` | TEXT | Affiliation ('Student', 'Senior', 'Regular') |\n"
            "| `outstanding_fines` | REAL | Recorded fine balance |\n\n"
            "#### Output Requirements\n"
            "Return `member_id`, `name`, `member_type`, `outstanding_fines`, and `discounted_fines`.\n"
            "Order by `member_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "CASE", "Discounts", "Financial Adjustment", "Library System"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Demographic Discretion", "Scalar Multiplication in CASE", "Rounded Currencies"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 65, "estimated_time_minutes": 12,
        "schema_sql": (
            "CREATE TABLE members ("
            "  member_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  member_type TEXT NOT NULL,"
            "  outstanding_fines REAL NOT NULL"
            ");"
        ),
        "fixtures": {
            "members": [
                {"member_id": 1, "name": "Laura Croft", "member_type": "Regular", "outstanding_fines": 25.00},
                {"member_id": 2, "name": "Peter Parker", "member_type": "Student", "outstanding_fines": 18.50},
                {"member_id": 3, "name": "Charles Xavier", "member_type": "Senior", "outstanding_fines": 30.00},
                {"member_id": 4, "name": "Miles Morales", "member_type": "Student", "outstanding_fines": 10.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": (
            "SELECT member_id, name, member_type, outstanding_fines, "
            "CASE "
            "  WHEN member_type = 'Student' THEN ROUND(outstanding_fines * 0.50, 2) "
            "  WHEN member_type = 'Senior' THEN ROUND(outstanding_fines * 0.30, 2) "
            "  ELSE outstanding_fines "
            "END AS discounted_fines "
            "FROM members "
            "ORDER BY member_id ASC;"
        ),
        "test_cases": [
            {
                "id": "lib-amnesty-tc-1", "name": "Demographic Concession Computation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE members (member_id INT PRIMARY KEY, name TEXT NOT NULL, member_type TEXT NOT NULL, outstanding_fines REAL NOT NULL);",
                    "fixtures": {
                        "members": [
                            {"member_id": 1, "name": "Laura Croft", "member_type": "Regular", "outstanding_fines": 25.00},
                            {"member_id": 2, "name": "Peter Parker", "member_type": "Student", "outstanding_fines": 18.50},
                            {"member_id": 3, "name": "Charles Xavier", "member_type": "Senior", "outstanding_fines": 30.00},
                            {"member_id": 4, "name": "Miles Morales", "member_type": "Student", "outstanding_fines": 10.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"member_id": 1, "name": "Laura Croft", "member_type": "Regular", "outstanding_fines": 25.0, "discounted_fines": 25.0},
                    {"member_id": 2, "name": "Peter Parker", "member_type": "Student", "outstanding_fines": 18.5, "discounted_fines": 9.25},
                    {"member_id": 3, "name": "Charles Xavier", "member_type": "Senior", "outstanding_fines": 30.0, "discounted_fines": 9.0},
                    {"member_id": 4, "name": "Miles Morales", "member_type": "Student", "outstanding_fines": 10.0, "discounted_fines": 5.0}
                ], indent=2) + "\n"
            }
        ]
    }
]
