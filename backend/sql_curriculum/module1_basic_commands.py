# Copyright 2026 Sharexpress Contributors
# Module 1: SQL Essentials & Basic Commands (13 Problems)

import json

MODULE1_CHALLENGES = [
    # 1. All Products
    {
        "title": "All Products",
        "slug": "sql-all-products",
        "short_description": "Retrieve all rows and columns from the product catalog table.",
        "description": (
            "### Problem Statement\n\n"
            "An e-commerce store needs an audit of its entire inventory catalog. "
            "Write a SQL query to retrieve all product attributes from the `products` table.\n\n"
            "#### Table Schema: `products`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `product_id` | INT (PK) | Unique product identifier |\n"
            "| `product_name` | VARCHAR(100) | Commercial name of the item |\n"
            "| `category` | VARCHAR(50) | Inventory category |\n"
            "| `price` | DECIMAL(10,2) | Retail price in USD |\n"
            "| `stock_quantity` | INT | Units currently in stock |\n\n"
            "#### Output Requirements\n"
            "Select all columns (`*`). Order the result by `product_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "SELECT", "Basics", "Data Retrieval"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Table Projections", "SELECT Asterisk", "Ascending Sorting"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE products ("
            "  product_id INT PRIMARY KEY,"
            "  product_name TEXT NOT NULL,"
            "  category TEXT NOT NULL,"
            "  price DECIMAL(10,2) NOT NULL,"
            "  stock_quantity INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "products": [
                {"product_id": 1, "product_name": "Mechanical Keyboard", "category": "Electronics", "price": 89.99, "stock_quantity": 45},
                {"product_id": 2, "product_name": "Wireless Ergonomic Mouse", "category": "Electronics", "price": 49.50, "stock_quantity": 120},
                {"product_id": 3, "product_name": "Organic Green Tea", "category": "Beverages", "price": 12.00, "stock_quantity": 300},
                {"product_id": 4, "product_name": "Stainless Steel Water Bottle", "category": "Fitness", "price": 24.99, "stock_quantity": 80},
                {"product_id": 5, "product_name": "Noise Cancelling Headphones", "category": "Electronics", "price": 199.99, "stock_quantity": 25}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT * FROM products\nORDER BY product_id ASC;\n",
            "sqlite": "SELECT * FROM products ORDER BY product_id ASC;\n",
            "mysql": "SELECT * FROM products ORDER BY product_id ASC;\n",
            "postgresql": "SELECT * FROM products ORDER BY product_id ASC;\n"
        },
        "canonical_solution": "SELECT * FROM products ORDER BY product_id ASC;",
        "test_cases": [
            {
                "id": "all-prod-tc-1", "name": "Catalog Full Inventory Scan", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, stock_quantity INT NOT NULL);",
                    "fixtures": {
                        "products": [
                            {"product_id": 1, "product_name": "Mechanical Keyboard", "category": "Electronics", "price": 89.99, "stock_quantity": 45},
                            {"product_id": 2, "product_name": "Wireless Ergonomic Mouse", "category": "Electronics", "price": 49.50, "stock_quantity": 120},
                            {"product_id": 3, "product_name": "Organic Green Tea", "category": "Beverages", "price": 12.00, "stock_quantity": 300},
                            {"product_id": 4, "product_name": "Stainless Steel Water Bottle", "category": "Fitness", "price": 24.99, "stock_quantity": 80},
                            {"product_id": 5, "product_name": "Noise Cancelling Headphones", "category": "Electronics", "price": 199.99, "stock_quantity": 25}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"product_id": 1, "product_name": "Mechanical Keyboard", "category": "Electronics", "price": 89.99, "stock_quantity": 45},
                    {"product_id": 2, "product_name": "Wireless Ergonomic Mouse", "category": "Electronics", "price": 49.50, "stock_quantity": 120},
                    {"product_id": 3, "product_name": "Organic Green Tea", "category": "Beverages", "price": 12.00, "stock_quantity": 300},
                    {"product_id": 4, "product_name": "Stainless Steel Water Bottle", "category": "Fitness", "price": 24.99, "stock_quantity": 80},
                    {"product_id": 5, "product_name": "Noise Cancelling Headphones", "category": "Electronics", "price": 199.99, "stock_quantity": 25}
                ], indent=2) + "\n"
            }
        ]
    },

    # 2. High Price of Products
    {
        "title": "High Price of Products",
        "slug": "sql-high-price-of-products",
        "short_description": "Filter premium products priced strictly higher than $100.00.",
        "description": (
            "### Problem Statement\n\n"
            "Identify luxury and high-value catalog items. Write a SQL query to select all products "
            "where `price` is strictly greater than `100.00`.\n\n"
            "#### Table Schema: `products`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `product_id` | INT (PK) | Item identifier |\n"
            "| `product_name` | VARCHAR(100) | Item title |\n"
            "| `category` | VARCHAR(50) | Item category |\n"
            "| `price` | DECIMAL(10,2) | Unit retail price |\n"
            "| `stock_quantity` | INT | Available stock |\n\n"
            "#### Output Requirements\n"
            "Return `product_id`, `product_name`, and `price`. Order results by `price DESC, product_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "WHERE", "Filtering", "Comparison Operators"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["WHERE Clauses", "Numeric Comparison", "Descending Ordering"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE products ("
            "  product_id INT PRIMARY KEY,"
            "  product_name TEXT NOT NULL,"
            "  category TEXT NOT NULL,"
            "  price DECIMAL(10,2) NOT NULL,"
            "  stock_quantity INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "products": [
                {"product_id": 101, "product_name": "Gaming Monitor 4K", "category": "Electronics", "price": 450.00, "stock_quantity": 15},
                {"product_id": 102, "product_name": "USB-C Cable", "category": "Electronics", "price": 14.99, "stock_quantity": 250},
                {"product_id": 103, "product_name": "Standing Desk", "category": "Furniture", "price": 320.00, "stock_quantity": 10},
                {"product_id": 104, "product_name": "Ceramic Mug", "category": "Home", "price": 9.50, "stock_quantity": 100},
                {"product_id": 105, "product_name": "Leather Office Chair", "category": "Furniture", "price": 185.00, "stock_quantity": 20},
                {"product_id": 106, "product_name": "Laptop Stand", "category": "Electronics", "price": 99.99, "stock_quantity": 60}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Select product_id, product_name, price where price > 100.00\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT product_id, product_name, price FROM products WHERE price > 100.00 ORDER BY price DESC, product_id ASC;",
        "test_cases": [
            {
                "id": "high-price-tc-1", "name": "Premium Tier Threshold Filtering", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, stock_quantity INT NOT NULL);",
                    "fixtures": {
                        "products": [
                            {"product_id": 101, "product_name": "Gaming Monitor 4K", "category": "Electronics", "price": 450.00, "stock_quantity": 15},
                            {"product_id": 102, "product_name": "USB-C Cable", "category": "Electronics", "price": 14.99, "stock_quantity": 250},
                            {"product_id": 103, "product_name": "Standing Desk", "category": "Furniture", "price": 320.00, "stock_quantity": 10},
                            {"product_id": 104, "product_name": "Ceramic Mug", "category": "Home", "price": 9.50, "stock_quantity": 100},
                            {"product_id": 105, "product_name": "Leather Office Chair", "category": "Furniture", "price": 185.00, "stock_quantity": 20},
                            {"product_id": 106, "product_name": "Laptop Stand", "category": "Electronics", "price": 99.99, "stock_quantity": 60}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"product_id": 101, "product_name": "Gaming Monitor 4K", "price": 450.0},
                    {"product_id": 103, "product_name": "Standing Desk", "price": 320.0},
                    {"product_id": 105, "product_name": "Leather Office Chair", "price": 185.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 3. Average Salary
    {
        "title": "Average Salary",
        "slug": "sql-average-salary",
        "short_description": "Calculate the average employee salary across all corporate divisions.",
        "description": (
            "### Problem Statement\n\n"
            "The Human Resources department needs a benchmark metric for payroll planning. "
            "Write a SQL query to compute the average base salary across all employees in the company.\n\n"
            "#### Table Schema: `employees`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `employee_id` | INT (PK) | Unique employee ID |\n"
            "| `first_name` | VARCHAR(50) | First name |\n"
            "| `last_name` | VARCHAR(50) | Last name |\n"
            "| `department` | VARCHAR(50) | Department name |\n"
            "| `salary` | DECIMAL(10,2) | Annual base compensation |\n\n"
            "#### Output Requirements\n"
            "Return a single column named `average_salary`, rounded to 2 decimal places using `ROUND()`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "AVG", "Aggregates", "ROUND"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Scalar Aggregations", "AVG Function", "Decimal Rounding"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE employees ("
            "  employee_id INT PRIMARY KEY,"
            "  first_name TEXT NOT NULL,"
            "  last_name TEXT NOT NULL,"
            "  department TEXT NOT NULL,"
            "  salary DECIMAL(10,2) NOT NULL"
            ");"
        ),
        "fixtures": {
            "employees": [
                {"employee_id": 1, "first_name": "Alice", "last_name": "Smith", "department": "Engineering", "salary": 110000.00},
                {"employee_id": 2, "first_name": "Bob", "last_name": "Jones", "department": "Marketing", "salary": 75000.00},
                {"employee_id": 3, "first_name": "Charlie", "last_name": "Brown", "department": "Engineering", "salary": 95000.00},
                {"employee_id": 4, "first_name": "Diana", "last_name": "Prince", "department": "Finance", "salary": 85000.00},
                {"employee_id": 5, "first_name": "Evan", "last_name": "Wright", "department": "Human Resources", "salary": 65000.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Return average_salary rounded to 2 decimal places\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT ROUND(AVG(salary), 2) AS average_salary FROM employees;",
        "test_cases": [
            {
                "id": "avg-sal-tc-1", "name": "Company-wide Payroll Average", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE employees (employee_id INT PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, department TEXT NOT NULL, salary DECIMAL(10,2) NOT NULL);",
                    "fixtures": {
                        "employees": [
                            {"employee_id": 1, "first_name": "Alice", "last_name": "Smith", "department": "Engineering", "salary": 110000.00},
                            {"employee_id": 2, "first_name": "Bob", "last_name": "Jones", "department": "Marketing", "salary": 75000.00},
                            {"employee_id": 3, "first_name": "Charlie", "last_name": "Brown", "department": "Engineering", "salary": 95000.00},
                            {"employee_id": 4, "first_name": "Diana", "last_name": "Prince", "department": "Finance", "salary": 85000.00},
                            {"employee_id": 5, "first_name": "Evan", "last_name": "Wright", "department": "Human Resources", "salary": 65000.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"average_salary": 86000.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 4. Locate People
    {
        "title": "Locate People",
        "slug": "sql-locate-people",
        "short_description": "Locate all citizens residing in the city of Seattle.",
        "description": (
            "### Problem Statement\n\n"
            "A municipal census database holds residential profiles. Write a SQL query to list all citizens "
            "who reside in the city of `'Seattle'`.\n\n"
            "#### Table Schema: `citizens`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `citizen_id` | INT (PK) | Unique citizen identification |\n"
            "| `full_name` | VARCHAR(100) | Legal full name |\n"
            "| `city` | VARCHAR(50) | Resident city |\n"
            "| `state` | VARCHAR(50) | State / Province |\n"
            "| `postal_code` | VARCHAR(20) | Zip / Postal code |\n\n"
            "#### Output Requirements\n"
            "Return `citizen_id`, `full_name`, and `city`. Order alphabetically by `full_name ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "WHERE", "Strings", "Equality"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["String Comparison", "WHERE Filtering", "Lexicographical Sort"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE citizens ("
            "  citizen_id INT PRIMARY KEY,"
            "  full_name TEXT NOT NULL,"
            "  city TEXT NOT NULL,"
            "  state TEXT NOT NULL,"
            "  postal_code TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "citizens": [
                {"citizen_id": 1, "full_name": "Marcus Vance", "city": "Seattle", "state": "WA", "postal_code": "98101"},
                {"citizen_id": 2, "full_name": "Elena Rostova", "city": "Chicago", "state": "IL", "postal_code": "60601"},
                {"citizen_id": 3, "full_name": "David Kim", "city": "Seattle", "state": "WA", "postal_code": "98104"},
                {"citizen_id": 4, "full_name": "Sophia Martinez", "city": "New York", "state": "NY", "postal_code": "10001"},
                {"citizen_id": 5, "full_name": "Aiden Clark", "city": "Seattle", "state": "WA", "postal_code": "98109"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT citizen_id, full_name, city FROM citizens WHERE city = 'Seattle' ORDER BY full_name ASC;",
        "test_cases": [
            {
                "id": "locate-people-tc-1", "name": "Seattle Residents Filter", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE citizens (citizen_id INT PRIMARY KEY, full_name TEXT NOT NULL, city TEXT NOT NULL, state TEXT NOT NULL, postal_code TEXT NOT NULL);",
                    "fixtures": {
                        "citizens": [
                            {"citizen_id": 1, "full_name": "Marcus Vance", "city": "Seattle", "state": "WA", "postal_code": "98101"},
                            {"citizen_id": 2, "full_name": "Elena Rostova", "city": "Chicago", "state": "IL", "postal_code": "60601"},
                            {"citizen_id": 3, "full_name": "David Kim", "city": "Seattle", "state": "WA", "postal_code": "98104"},
                            {"citizen_id": 4, "full_name": "Sophia Martinez", "city": "New York", "state": "NY", "postal_code": "10001"},
                            {"citizen_id": 5, "full_name": "Aiden Clark", "city": "Seattle", "state": "WA", "postal_code": "98109"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"citizen_id": 5, "full_name": "Aiden Clark", "city": "Seattle"},
                    {"citizen_id": 3, "full_name": "David Kim", "city": "Seattle"},
                    {"citizen_id": 1, "full_name": "Marcus Vance", "city": "Seattle"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 5. Distinct Companies
    {
        "title": "Distinct Companies",
        "slug": "sql-distinct-companies",
        "short_description": "List all unique corporate employers currently offering career openings.",
        "description": (
            "### Problem Statement\n\n"
            "A job aggregator portal contains thousands of job openings with repeated hiring companies. "
            "Write a SQL query to return a distinct list of company names actively recruiting.\n\n"
            "#### Table Schema: `job_postings`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `job_id` | INT (PK) | Job listing ID |\n"
            "| `company_name` | VARCHAR(100) | Hiring organization |\n"
            "| `role_title` | VARCHAR(100) | Job title |\n"
            "| `location` | VARCHAR(50) | Office location |\n\n"
            "#### Output Requirements\n"
            "Return a single column named `company_name` containing unique entries, ordered alphabetically (`company_name ASC`)."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "DISTINCT", "Deduplication", "Sorting"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["DISTINCT Keyword", "Duplicate Removal", "Alphabetical Sort"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE job_postings ("
            "  job_id INT PRIMARY KEY,"
            "  company_name TEXT NOT NULL,"
            "  role_title TEXT NOT NULL,"
            "  location TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "job_postings": [
                {"job_id": 1, "company_name": "Google", "role_title": "Software Engineer", "location": "Mountain View"},
                {"job_id": 2, "company_name": "Meta", "role_title": "Product Designer", "location": "Menlo Park"},
                {"job_id": 3, "company_name": "Google", "role_title": "Data Scientist", "location": "New York"},
                {"job_id": 4, "company_name": "Amazon", "role_title": "Cloud Architect", "location": "Seattle"},
                {"job_id": 5, "company_name": "Meta", "role_title": "Systems Engineer", "location": "Remote"},
                {"job_id": 6, "company_name": "Apple", "role_title": "Hardware Lead", "location": "Cupertino"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Return unique company_name in alphabetical order\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT DISTINCT company_name FROM job_postings ORDER BY company_name ASC;",
        "test_cases": [
            {
                "id": "distinct-comp-tc-1", "name": "Company Name De-duplication", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE job_postings (job_id INT PRIMARY KEY, company_name TEXT NOT NULL, role_title TEXT NOT NULL, location TEXT NOT NULL);",
                    "fixtures": {
                        "job_postings": [
                            {"job_id": 1, "company_name": "Google", "role_title": "Software Engineer", "location": "Mountain View"},
                            {"job_id": 2, "company_name": "Meta", "role_title": "Product Designer", "location": "Menlo Park"},
                            {"job_id": 3, "company_name": "Google", "role_title": "Data Scientist", "location": "New York"},
                            {"job_id": 4, "company_name": "Amazon", "role_title": "Cloud Architect", "location": "Seattle"},
                            {"job_id": 5, "company_name": "Meta", "role_title": "Systems Engineer", "location": "Remote"},
                            {"job_id": 6, "company_name": "Apple", "role_title": "Hardware Lead", "location": "Cupertino"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"company_name": "Amazon"},
                    {"company_name": "Apple"},
                    {"company_name": "Google"},
                    {"company_name": "Meta"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 6. Fiction Collection Size
    {
        "title": "Fiction Collection Size",
        "slug": "sql-fiction-collection-size",
        "short_description": "Count the total number of literary titles in the Fiction section.",
        "description": (
            "### Problem Statement\n\n"
            "A public bookstore is tracking genre distribution. Write a SQL query to count how many distinct "
            "book titles belong to the `'Fiction'` genre.\n\n"
            "#### Table Schema: `books`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `book_id` | INT (PK) | Unique book identifier |\n"
            "| `title` | VARCHAR(150) | Book title |\n"
            "| `genre` | VARCHAR(50) | Literary genre |\n"
            "| `publication_year` | INT | Year published |\n"
            "| `copies_available` | INT | Current shelf count |\n\n"
            "#### Output Requirements\n"
            "Return a single column named `fiction_books_count`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "COUNT", "WHERE", "Aggregates"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Conditional Count", "COUNT(*) Aggregate", "Alias Naming"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE books ("
            "  book_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  genre TEXT NOT NULL,"
            "  publication_year INT NOT NULL,"
            "  copies_available INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "books": [
                {"book_id": 1, "title": "The Great Gatsby", "genre": "Fiction", "publication_year": 1925, "copies_available": 4},
                {"book_id": 2, "title": "A Brief History of Time", "genre": "Science", "publication_year": 1988, "copies_available": 2},
                {"book_id": 3, "title": "To Kill a Mockingbird", "genre": "Fiction", "publication_year": 1960, "copies_available": 5},
                {"book_id": 4, "title": "Sapiens", "genre": "History", "publication_year": 2011, "copies_available": 3},
                {"book_id": 5, "title": "1984", "genre": "Fiction", "publication_year": 1949, "copies_available": 6}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT COUNT(*) AS fiction_books_count FROM books WHERE genre = 'Fiction';",
        "test_cases": [
            {
                "id": "fiction-size-tc-1", "name": "Fiction Inventory Count", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE books (book_id INT PRIMARY KEY, title TEXT NOT NULL, genre TEXT NOT NULL, publication_year INT NOT NULL, copies_available INT NOT NULL);",
                    "fixtures": {
                        "books": [
                            {"book_id": 1, "title": "The Great Gatsby", "genre": "Fiction", "publication_year": 1925, "copies_available": 4},
                            {"book_id": 2, "title": "A Brief History of Time", "genre": "Science", "publication_year": 1988, "copies_available": 2},
                            {"book_id": 3, "title": "To Kill a Mockingbird", "genre": "Fiction", "publication_year": 1960, "copies_available": 5},
                            {"book_id": 4, "title": "Sapiens", "genre": "History", "publication_year": 2011, "copies_available": 3},
                            {"book_id": 5, "title": "1984", "genre": "Fiction", "publication_year": 1949, "copies_available": 6}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"fiction_books_count": 3}
                ], indent=2) + "\n"
            }
        ]
    },

    # 7. List of Movies with Ratings
    {
        "title": "List of Movies with Ratings",
        "slug": "sql-list-of-movies-with-ratings",
        "short_description": "Sort cinema catalog by critic ratings in descending order.",
        "description": (
            "### Problem Statement\n\n"
            "A film rating portal displays curated motion pictures. Write a SQL query to list all movies "
            "ordered from highest rating to lowest rating.\n\n"
            "#### Table Schema: `movies`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `movie_id` | INT (PK) | Cinema identifier |\n"
            "| `title` | VARCHAR(120) | Movie title |\n"
            "| `director` | VARCHAR(80) | Director name |\n"
            "| `release_year` | INT | Year of theatrical debut |\n"
            "| `rating` | DECIMAL(3,1) | Critic rating (out of 10.0) |\n\n"
            "#### Output Requirements\n"
            "Return `title`, `release_year`, and `rating`. Order primarily by `rating DESC`, and secondarily by `title ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "ORDER BY", "Sorting", "Multi-column"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Descending Sorting", "Secondary Sort Keys", "Projection"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE movies ("
            "  movie_id INT PRIMARY KEY,"
            "  title TEXT NOT NULL,"
            "  director TEXT NOT NULL,"
            "  release_year INT NOT NULL,"
            "  rating DECIMAL(3,1) NOT NULL"
            ");"
        ),
        "fixtures": {
            "movies": [
                {"movie_id": 1, "title": "Inception", "director": "Christopher Nolan", "release_year": 2010, "rating": 8.8},
                {"movie_id": 2, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "rating": 8.7},
                {"movie_id": 3, "title": "Parasite", "director": "Bong Joon-ho", "release_year": 2019, "rating": 8.5},
                {"movie_id": 4, "title": "Tenet", "director": "Christopher Nolan", "release_year": 2020, "rating": 7.3},
                {"movie_id": 5, "title": "Whiplash", "director": "Damien Chazelle", "release_year": 2014, "rating": 8.5}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT title, release_year, rating FROM movies ORDER BY rating DESC, title ASC;",
        "test_cases": [
            {
                "id": "movies-rating-tc-1", "name": "Critique Leaderboard Sort", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE movies (movie_id INT PRIMARY KEY, title TEXT NOT NULL, director TEXT NOT NULL, release_year INT NOT NULL, rating DECIMAL(3,1) NOT NULL);",
                    "fixtures": {
                        "movies": [
                            {"movie_id": 1, "title": "Inception", "director": "Christopher Nolan", "release_year": 2010, "rating": 8.8},
                            {"movie_id": 2, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "rating": 8.7},
                            {"movie_id": 3, "title": "Parasite", "director": "Bong Joon-ho", "release_year": 2019, "rating": 8.5},
                            {"movie_id": 4, "title": "Tenet", "director": "Christopher Nolan", "release_year": 2020, "rating": 7.3},
                            {"movie_id": 5, "title": "Whiplash", "director": "Damien Chazelle", "release_year": 2014, "rating": 8.5}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"title": "Inception", "release_year": 2010, "rating": 8.8},
                    {"title": "Interstellar", "release_year": 2014, "rating": 8.7},
                    {"title": "Parasite", "release_year": 2019, "rating": 8.5},
                    {"title": "Whiplash", "release_year": 2014, "rating": 8.5},
                    {"title": "Tenet", "release_year": 2020, "rating": 7.3}
                ], indent=2) + "\n"
            }
        ]
    },

    # 8. Handling NULL Values
    {
        "title": "Handling NULL Values",
        "slug": "sql-handling-null-values",
        "short_description": "Sanitize missing shipping tracking identifiers using COALESCE.",
        "description": (
            "### Problem Statement\n\n"
            "Orders that have not yet dispatched from the fulfillment warehouse contain `NULL` in the `tracking_number` field. "
            "Write a SQL query to select all orders that have a valid delivery address, replacing any missing `tracking_number` "
            "with the placeholder string `'Not Assigned'`.\n\n"
            "#### Table Schema: `orders`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `order_id` | INT (PK) | Order transaction number |\n"
            "| `customer_name` | VARCHAR(100) | Customer full name |\n"
            "| `delivery_address` | TEXT | Destination address (can be NULL) |\n"
            "| `tracking_number` | VARCHAR(50) | Logistics tracking code (can be NULL) |\n\n"
            "#### Output Requirements\n"
            "Return `order_id`, `customer_name`, and a column named `shipping_status` containing either the tracking number or `'Not Assigned'`. "
            "Only include rows where `delivery_address IS NOT NULL`. Order by `order_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "COALESCE", "NULL Handling", "Data Cleaning"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["COALESCE Function", "IS NOT NULL Predicate", "Default Fallbacks"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE orders ("
            "  order_id INT PRIMARY KEY,"
            "  customer_name TEXT NOT NULL,"
            "  delivery_address TEXT,"
            "  tracking_number TEXT"
            ");"
        ),
        "fixtures": {
            "orders": [
                {"order_id": 501, "customer_name": "John Doe", "delivery_address": "123 Main St", "tracking_number": "TRK99281"},
                {"order_id": 502, "customer_name": "Jane Smith", "delivery_address": "456 Oak Ave", "tracking_number": None},
                {"order_id": 503, "customer_name": "Sam Taylor", "delivery_address": None, "tracking_number": None},
                {"order_id": 504, "customer_name": "Lucas Grey", "delivery_address": "789 Pine Rd", "tracking_number": "TRK44102"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT order_id, customer_name, COALESCE(tracking_number, 'Not Assigned') AS shipping_status FROM orders WHERE delivery_address IS NOT NULL ORDER BY order_id ASC;",
        "test_cases": [
            {
                "id": "null-handling-tc-1", "name": "Tracking Number Fallback", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE orders (order_id INT PRIMARY KEY, customer_name TEXT NOT NULL, delivery_address TEXT, tracking_number TEXT);",
                    "fixtures": {
                        "orders": [
                            {"order_id": 501, "customer_name": "John Doe", "delivery_address": "123 Main St", "tracking_number": "TRK99281"},
                            {"order_id": 502, "customer_name": "Jane Smith", "delivery_address": "456 Oak Ave", "tracking_number": None},
                            {"order_id": 503, "customer_name": "Sam Taylor", "delivery_address": None, "tracking_number": None},
                            {"order_id": 504, "customer_name": "Lucas Grey", "delivery_address": "789 Pine Rd", "tracking_number": "TRK44102"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"order_id": 501, "customer_name": "John Doe", "shipping_status": "TRK99281"},
                    {"order_id": 502, "customer_name": "Jane Smith", "shipping_status": "Not Assigned"},
                    {"order_id": 504, "customer_name": "Lucas Grey", "shipping_status": "TRK44102"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 9. Salary of Employees
    {
        "title": "Salary of Employees",
        "slug": "sql-salary-of-employees",
        "short_description": "Compound boolean filtering for Engineering and Sales department tiers.",
        "description": (
            "### Problem Statement\n\n"
            "Corporate compensation audits require finding employees meeting specific departmental thresholds. "
            "Write a SQL query to select all staff members who are either:\n"
            "1. In `'Engineering'` with a salary of at least `80000.00`, OR\n"
            "2. In `'Sales'` with a salary of at least `70000.00`.\n\n"
            "#### Table Schema: `staff`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `staff_id` | INT (PK) | Staff member ID |\n"
            "| `name` | VARCHAR(100) | Full name |\n"
            "| `department` | VARCHAR(50) | Operational division |\n"
            "| `salary` | DECIMAL(10,2) | Current annual salary |\n"
            "| `performance_rating` | INT | Rating 1 to 5 |\n\n"
            "#### Output Requirements\n"
            "Return `staff_id`, `name`, `department`, and `salary`. Order results by `salary DESC, staff_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "AND/OR", "Boolean Logic", "Filtering"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Parenthesized Boolean Logic", "Disjunction OR", "Conjunction AND"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 60, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE staff ("
            "  staff_id INT PRIMARY KEY,"
            "  name TEXT NOT NULL,"
            "  department TEXT NOT NULL,"
            "  salary DECIMAL(10,2) NOT NULL,"
            "  performance_rating INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "staff": [
                {"staff_id": 1, "name": "Sarah Connor", "department": "Engineering", "salary": 88000.00, "performance_rating": 5},
                {"staff_id": 2, "name": "Kyle Reese", "department": "Engineering", "salary": 72000.00, "performance_rating": 3},
                {"staff_id": 3, "name": "John Miller", "department": "Sales", "salary": 75000.00, "performance_rating": 4},
                {"staff_id": 4, "name": "Lisa Ray", "department": "Sales", "salary": 65000.00, "performance_rating": 3},
                {"staff_id": 5, "name": "Bruce Wayne", "department": "Executive", "salary": 250000.00, "performance_rating": 5}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT staff_id, name, department, salary FROM staff WHERE (department = 'Engineering' AND salary >= 80000.00) OR (department = 'Sales' AND salary >= 70000.00) ORDER BY salary DESC, staff_id ASC;",
        "test_cases": [
            {
                "id": "salary-emp-tc-1", "name": "Engineering & Sales Threshold Filter", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE staff (staff_id INT PRIMARY KEY, name TEXT NOT NULL, department TEXT NOT NULL, salary DECIMAL(10,2) NOT NULL, performance_rating INT NOT NULL);",
                    "fixtures": {
                        "staff": [
                            {"staff_id": 1, "name": "Sarah Connor", "department": "Engineering", "salary": 88000.00, "performance_rating": 5},
                            {"staff_id": 2, "name": "Kyle Reese", "department": "Engineering", "salary": 72000.00, "performance_rating": 3},
                            {"staff_id": 3, "name": "John Miller", "department": "Sales", "salary": 75000.00, "performance_rating": 4},
                            {"staff_id": 4, "name": "Lisa Ray", "department": "Sales", "salary": 65000.00, "performance_rating": 3},
                            {"staff_id": 5, "name": "Bruce Wayne", "department": "Executive", "salary": 250000.00, "performance_rating": 5}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"staff_id": 1, "name": "Sarah Connor", "department": "Engineering", "salary": 88000.0},
                    {"staff_id": 3, "name": "John Miller", "department": "Sales", "salary": 75000.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 10. Department of Each Employee
    {
        "title": "Department of Each Employee",
        "slug": "sql-department-of-each-employee",
        "short_description": "Concatenate names and format uppercase department codes.",
        "description": (
            "### Problem Statement\n\n"
            "An enterprise directory service requires formatted roster badges. Write a SQL query to create:\n"
            "1. `employee_full_name`: concatenation of `first_name`, a single space `' '`, and `last_name`.\n"
            "2. `assigned_department`: the `department_code` converted to uppercase using `UPPER()`.\n\n"
            "#### Table Schema: `workers`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `worker_id` | INT (PK) | Personnel identifier |\n"
            "| `first_name` | VARCHAR(50) | Worker given name |\n"
            "| `last_name` | VARCHAR(50) | Worker surname |\n"
            "| `department_code` | VARCHAR(10) | Code identifier (e.g. 'eng', 'fin') |\n\n"
            "#### Output Requirements\n"
            "Return `employee_full_name` and `assigned_department`. Order alphabetically by `employee_full_name ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "Concatenation", "UPPER", "String Functions"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["String Concatenation", "Case Transformation", "Column Aliasing"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE workers ("
            "  worker_id INT PRIMARY KEY,"
            "  first_name TEXT NOT NULL,"
            "  last_name TEXT NOT NULL,"
            "  department_code TEXT NOT NULL"
            ");"
        ),
        "fixtures": {
            "workers": [
                {"worker_id": 1, "first_name": "Liam", "last_name": "Neeson", "department_code": "sec"},
                {"worker_id": 2, "first_name": "Emma", "last_name": "Watson", "department_code": "pr"},
                {"worker_id": 3, "first_name": "Chris", "last_name": "Evans", "department_code": "ops"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT (first_name || ' ' || last_name) AS employee_full_name, UPPER(department_code) AS assigned_department FROM workers ORDER BY employee_full_name ASC;",
        "test_cases": [
            {
                "id": "dept-emp-tc-1", "name": "Badge Formatter", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE workers (worker_id INT PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, department_code TEXT NOT NULL);",
                    "fixtures": {
                        "workers": [
                            {"worker_id": 1, "first_name": "Liam", "last_name": "Neeson", "department_code": "sec"},
                            {"worker_id": 2, "first_name": "Emma", "last_name": "Watson", "department_code": "pr"},
                            {"worker_id": 3, "first_name": "Chris", "last_name": "Evans", "department_code": "ops"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"employee_full_name": "Chris Evans", "assigned_department": "OPS"},
                    {"employee_full_name": "Emma Watson", "assigned_department": "PR"},
                    {"employee_full_name": "Liam Neeson", "assigned_department": "SEC"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 11. Article Views
    {
        "title": "Article Views",
        "slug": "sql-article-views",
        "short_description": "Identify content creators who visited their own published articles.",
        "description": (
            "### Problem Statement\n\n"
            "An online publication platform monitors viewership patterns. Write a SQL query to identify "
            "all authors who viewed at least one of their own articles.\n\n"
            "#### Table Schema: `views`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `article_id` | INT | Article ID |\n"
            "| `author_id` | INT | Author ID who wrote the article |\n"
            "| `viewer_id` | INT | User ID who accessed the article |\n"
            "| `view_date` | DATE | Date of the impression |\n\n"
            "#### Output Requirements\n"
            "Return a distinct column named `id` (representing the author ID), ordered by `id ASC`."
        ),
        "domain": "Databases", "difficulty": "Easy",
        "tags": ["SQL", "Self-Comparison", "DISTINCT", "WHERE"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Column-to-Column Equality", "DISTINCT Filter", "Projection Renaming"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 50, "estimated_time_minutes": 10,
        "schema_sql": (
            "CREATE TABLE views ("
            "  article_id INT NOT NULL,"
            "  author_id INT NOT NULL,"
            "  viewer_id INT NOT NULL,"
            "  view_date DATE NOT NULL"
            ");"
        ),
        "fixtures": {
            "views": [
                {"article_id": 1, "author_id": 3, "viewer_id": 5, "view_date": "2026-03-01"},
                {"article_id": 2, "author_id": 7, "viewer_id": 7, "view_date": "2026-03-02"},
                {"article_id": 1, "author_id": 3, "viewer_id": 3, "view_date": "2026-03-03"},
                {"article_id": 4, "author_id": 7, "viewer_id": 1, "view_date": "2026-03-04"},
                {"article_id": 3, "author_id": 4, "viewer_id": 4, "view_date": "2026-03-04"},
                {"article_id": 3, "author_id": 4, "viewer_id": 4, "view_date": "2026-03-05"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT DISTINCT author_id AS id FROM views WHERE author_id = viewer_id ORDER BY id ASC;",
        "test_cases": [
            {
                "id": "article-views-tc-1", "name": "Self-View Author Extraction", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE views (article_id INT NOT NULL, author_id INT NOT NULL, viewer_id INT NOT NULL, view_date DATE NOT NULL);",
                    "fixtures": {
                        "views": [
                            {"article_id": 1, "author_id": 3, "viewer_id": 5, "view_date": "2026-03-01"},
                            {"article_id": 2, "author_id": 7, "viewer_id": 7, "view_date": "2026-03-02"},
                            {"article_id": 1, "author_id": 3, "viewer_id": 3, "view_date": "2026-03-03"},
                            {"article_id": 4, "author_id": 7, "viewer_id": 1, "view_date": "2026-03-04"},
                            {"article_id": 3, "author_id": 4, "viewer_id": 4, "view_date": "2026-03-04"},
                            {"article_id": 3, "author_id": 4, "viewer_id": 4, "view_date": "2026-03-05"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"id": 3},
                    {"id": 4},
                    {"id": 7}
                ], indent=2) + "\n"
            }
        ]
    },

    # 12. Player Performance Insights
    {
        "title": "Player Performance Insights",
        "slug": "sql-player-performance-insights",
        "short_description": "Query games where basketball athletes scored 25+ points and recorded 5+ assists.",
        "description": (
            "### Problem Statement\n\n"
            "An analytics department tracks all-star performances in professional basketball. "
            "Write a SQL query to identify high-impact games where a player recorded at least `25` points "
            "and at least `5` assists.\n\n"
            "#### Table Schema: `match_stats`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `match_id` | INT (PK) | Game fixture number |\n"
            "| `player_id` | INT | Athlete ID |\n"
            "| `match_date` | DATE | Date of match |\n"
            "| `points_scored` | INT | Points made |\n"
            "| `assists` | INT | Decisive passes |\n"
            "| `rebounds` | INT | Rebounds retrieved |\n\n"
            "#### Output Requirements\n"
            "Return `match_id`, `player_id`, and `points_scored`. Order results by `points_scored DESC, match_date ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Analytics", "Multi-criteria", "WHERE"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Compound Numeric Filters", "Compound Sort Ordering", "Sports Metrics"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 80, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE match_stats ("
            "  match_id INT PRIMARY KEY,"
            "  player_id INT NOT NULL,"
            "  match_date DATE NOT NULL,"
            "  points_scored INT NOT NULL,"
            "  assists INT NOT NULL,"
            "  rebounds INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "match_stats": [
                {"match_id": 1, "player_id": 23, "match_date": "2026-01-10", "points_scored": 32, "assists": 8, "rebounds": 7},
                {"match_id": 2, "player_id": 30, "match_date": "2026-01-12", "points_scored": 28, "assists": 4, "rebounds": 5},
                {"match_id": 3, "player_id": 77, "match_date": "2026-01-15", "points_scored": 35, "assists": 11, "rebounds": 10},
                {"match_id": 4, "player_id": 23, "match_date": "2026-01-18", "points_scored": 22, "assists": 9, "rebounds": 6},
                {"match_id": 5, "player_id": 30, "match_date": "2026-01-20", "points_scored": 27, "assists": 6, "rebounds": 3}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT match_id, player_id, points_scored FROM match_stats WHERE points_scored >= 25 AND assists >= 5 ORDER BY points_scored DESC, match_date ASC;",
        "test_cases": [
            {
                "id": "player-perf-tc-1", "name": "All-Star Performance Threshold", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE match_stats (match_id INT PRIMARY KEY, player_id INT NOT NULL, match_date DATE NOT NULL, points_scored INT NOT NULL, assists INT NOT NULL, rebounds INT NOT NULL);",
                    "fixtures": {
                        "match_stats": [
                            {"match_id": 1, "player_id": 23, "match_date": "2026-01-10", "points_scored": 32, "assists": 8, "rebounds": 7},
                            {"match_id": 2, "player_id": 30, "match_date": "2026-01-12", "points_scored": 28, "assists": 4, "rebounds": 5},
                            {"match_id": 3, "player_id": 77, "match_date": "2026-01-15", "points_scored": 35, "assists": 11, "rebounds": 10},
                            {"match_id": 4, "player_id": 23, "match_date": "2026-01-18", "points_scored": 22, "assists": 9, "rebounds": 6},
                            {"match_id": 5, "player_id": 30, "match_date": "2026-01-20", "points_scored": 27, "assists": 6, "rebounds": 3}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"match_id": 3, "player_id": 77, "points_scored": 35},
                    {"match_id": 1, "player_id": 23, "points_scored": 32},
                    {"match_id": 5, "player_id": 30, "points_scored": 27}
                ], indent=2) + "\n"
            }
        ]
    },

    # 13. Player Details
    {
        "title": "Player Details",
        "slug": "sql-player-details",
        "short_description": "Search gaming accounts matching specific handle prefix and keyword patterns.",
        "description": (
            "### Problem Statement\n\n"
            "An e-sports community platform searches accounts by vanity handle patterns. "
            "Write a SQL query to find all gamers whose `username`:\n"
            "1. Begins with `'pro_'`, OR\n"
            "2. Contains the substring `'_ninja'` anywhere in their name.\n\n"
            "#### Table Schema: `gamers`\n"
            "| Column | Type | Description |\n"
            "| :--- | :--- | :--- |\n"
            "| `gamer_id` | INT (PK) | Account ID |\n"
            "| `username` | VARCHAR(50) | Player username |\n"
            "| `email` | VARCHAR(100) | Account email |\n"
            "| `country_code` | VARCHAR(3) | ISO Country |\n"
            "| `level` | INT | In-game tier level |\n\n"
            "#### Output Requirements\n"
            "Return `gamer_id`, `username`, and `level`. Order by `level DESC, username ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "LIKE", "Pattern Matching", "Wildcards"],
        "technologies": ["sql", "sqlite", "mysql", "postgresql"],
        "concepts": ["Wildcard Pattern Matching", "LIKE Keyword", "Escaped Wildcards"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 80, "estimated_time_minutes": 15,
        "schema_sql": (
            "CREATE TABLE gamers ("
            "  gamer_id INT PRIMARY KEY,"
            "  username TEXT NOT NULL,"
            "  email TEXT NOT NULL,"
            "  country_code TEXT NOT NULL,"
            "  level INT NOT NULL"
            ");"
        ),
        "fixtures": {
            "gamers": [
                {"gamer_id": 1, "username": "shadow_ninja", "email": "sn@gg.com", "country_code": "USA", "level": 48},
                {"gamer_id": 2, "username": "pro_gamer_99", "email": "pro99@gg.com", "country_code": "KOR", "level": 85},
                {"gamer_id": 3, "username": "alex_hunter", "email": "ah@gg.com", "country_code": "GBR", "level": 30},
                {"gamer_id": 4, "username": "pro_sniper", "email": "ps@gg.com", "country_code": "CAN", "level": 62},
                {"gamer_id": 5, "username": "cyber_ninja_warrior", "email": "cnw@gg.com", "country_code": "JPN", "level": 74},
                {"gamer_id": 6, "username": "casual_player", "email": "cp@gg.com", "country_code": "DEU", "level": 15}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\nSELECT \n",
            "sqlite": "SELECT \n",
            "mysql": "SELECT \n",
            "postgresql": "SELECT \n"
        },
        "canonical_solution": "SELECT gamer_id, username, level FROM gamers WHERE username LIKE 'pro_%' OR username LIKE '%_ninja%' ORDER BY level DESC, username ASC;",
        "test_cases": [
            {
                "id": "player-details-tc-1", "name": "Handle Pattern Match", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE gamers (gamer_id INT PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL, country_code TEXT NOT NULL, level INT NOT NULL);",
                    "fixtures": {
                        "gamers": [
                            {"gamer_id": 1, "username": "shadow_ninja", "email": "sn@gg.com", "country_code": "USA", "level": 48},
                            {"gamer_id": 2, "username": "pro_gamer_99", "email": "pro99@gg.com", "country_code": "KOR", "level": 85},
                            {"gamer_id": 3, "username": "alex_hunter", "email": "ah@gg.com", "country_code": "GBR", "level": 30},
                            {"gamer_id": 4, "username": "pro_sniper", "email": "ps@gg.com", "country_code": "CAN", "level": 62},
                            {"gamer_id": 5, "username": "cyber_ninja_warrior", "email": "cnw@gg.com", "country_code": "JPN", "level": 74},
                            {"gamer_id": 6, "username": "casual_player", "email": "cp@gg.com", "country_code": "DEU", "level": 15}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"gamer_id": 2, "username": "pro_gamer_99", "level": 85},
                    {"gamer_id": 5, "username": "cyber_ninja_warrior", "level": 74},
                    {"gamer_id": 4, "username": "pro_sniper", "level": 62},
                    {"gamer_id": 1, "username": "shadow_ninja", "level": 48}
                ], indent=2) + "\n"
            }
        ]
    }
]
