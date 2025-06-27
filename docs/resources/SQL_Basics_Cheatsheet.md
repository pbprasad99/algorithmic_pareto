# SQL Basics Cheatsheet

1.  **Order of execution of SQL:** `FROM` -\> `ON` -\> `JOIN` -\> `WHERE` -\> `GROUP BY` -\> `CUBE`/`ROLLUP` -\> `HAVING` -\> `SELECT` -\> `DISTINCT` -\> `ORDER BY` -\> `TOP`/`LIMIT`.

2.  **Difference between WHERE and HAVING:** `WHERE` filters individual rows *before* grouping, while `HAVING` filters groups *after* grouping.

3.  **Use of GROUP BY:** `GROUP BY` groups rows that have the same values in specified columns into a summary row, often used with aggregate functions.

4.  **Types of joins in SQL:**

      * **INNER JOIN:** Returns rows when there is a match in both tables.
      * **LEFT (OUTER) JOIN:** Returns all rows from the left table, and matching rows from the right table. If no match, NULLs for right table columns.
      * **RIGHT (OUTER) JOIN:** Returns all rows from the right table, and matching rows from the left table. If no match, NULLs for left table columns.
      * **FULL (OUTER) JOIN:** Returns all rows when there is a match in one of the tables. If no match, NULLs for the non-matching side.
      * **CROSS JOIN:** Returns the Cartesian product of the two tables (every row from the first table combined with every row from the second).

5.  **Triggers in SQL:** Special types of stored procedures that automatically execute (fire) when a specific event (INSERT, UPDATE, DELETE) occurs on a table or view.

6.  **Stored procedure in SQL:** A prepared SQL code block that can be saved, reused, and executed multiple times. They can accept parameters and return values.

7.  **Types of window functions (rank, row\_num, dense\_rank, lead & lag):**

      * **`ROW_NUMBER()`:** Assigns a unique, sequential integer to each row within its partition, starting from 1.
      * **`RANK()`:** Assigns a rank to each row within its partition, with gaps in the ranking for ties.
      * **`DENSE_RANK()`:** Assigns a rank to each row within its partition, with no gaps in the ranking for ties.
      * **`LEAD(column, offset, default)`:** Accesses data from a subsequent row in the same result set without using a self-join.
      * **`LAG(column, offset, default)`:** Accesses data from a preceding row in the same result set without using a self-join.

8.  **Difference between DELETE and TRUNCATE:**

      * **`DELETE`:** A DML command, removes rows one by one, logs each row deletion, can be rolled back, and can have a `WHERE` clause.
      * **`TRUNCATE`:** A DDL command, deallocates the data pages, does not log individual row deletions (logs deallocation), cannot be rolled back, and cannot have a `WHERE` clause. It's much faster for large tables.

9.  **Difference between DML, DDL and DCL:**

      * **DML (Data Manipulation Language):** Used for managing data within schema objects (e.g., `SELECT`, `INSERT`, `UPDATE`, `DELETE`).
      * **DDL (Data Definition Language):** Used for defining and modifying the database schema (e.g., `CREATE`, `ALTER`, `DROP`, `TRUNCATE`).
      * **DCL (Data Control Language):** Used for controlling access to data and the database (e.g., `GRANT`, `REVOKE`).

10. **Aggregate functions and when do we use them:** Functions that perform a calculation on a set of values and return a single summary value. We use them to summarize data.

      * **Examples:**
          * `COUNT(*)`: Number of rows.
          * `SUM(column)`: Sum of values in a column.
          * `AVG(column)`: Average of values in a column.
          * `MAX(column)`: Maximum value in a column.
          * `MIN(column)`: Minimum value in a column.

11. **Which is faster between CTE and Subquery?** Generally, there isn't a significant performance difference. The SQL optimizer often treats them similarly. CTEs are often preferred for readability and reusability, especially for complex queries.

12. **What are constraints and types of Constraints?** Rules enforced on data columns in a table to limit the type of data that can go into a table, ensuring data accuracy and integrity.

      * **Types:**
          * `NOT NULL`: Ensures a column cannot have a NULL value.
          * `UNIQUE`: Ensures all values in a column are different.
          * `PRIMARY KEY`: A combination of `NOT NULL` and `UNIQUE`, uniquely identifies each record.
          * `FOREIGN KEY`: Links two tables together, referencing the `PRIMARY KEY` of another table.
          * `CHECK`: Ensures all values in a column satisfy a specific condition.
          * `DEFAULT`: Sets a default value for a column when no value is specified.

13. **Types of Keys?**

      * **Primary Key:** Uniquely identifies each record in a table.
      * **Candidate Key:** A super key without any redundant attributes.
      * **Super Key:** A set of attributes that can uniquely identify a tuple in a relation.
      * **Foreign Key:** A field(s) in one table that refers to the primary key of another table.
      * **Alternate Key:** Candidate keys that are not chosen as the primary key.
      * **Composite Key:** A primary key consisting of two or more attributes.

14. **Different types of Operators?**

      * **Arithmetic Operators:** `+`, `-`, `*`, `/`, `%`
      * **Comparison Operators:** `=`, `!=` (or `<>`), `>`, `<`, `>=`, `<=`, `BETWEEN`, `LIKE`, `IN`, `IS NULL`
      * **Logical Operators:** `AND`, `OR`, `NOT`
      * **Bitwise Operators:** `&`, `|`, `^`, `~` (less common in typical SQL usage)
      * **Set Operators:** `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT` (or `MINUS`)

15. **Difference between GROUP BY and WHERE?** `WHERE` filters individual rows *before* grouping, while `GROUP BY` groups rows based on specified columns. `WHERE` cannot use aggregate functions directly unless they are in a subquery or a CTE, whereas `GROUP BY` is used in conjunction with aggregate functions.

16. **What are Views?** A virtual table based on the result-set of a SQL query. A view contains rows and columns, just like a real table, but it does not store data itself. The data is stored in the underlying tables.

17. **What are different types of constraints?** (Already answered in question 12). `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `DEFAULT`.

18. **Difference between VARCHAR and NVARCHAR?**

      * **`VARCHAR`:** Stores variable-length non-Unicode string data. Uses 1 byte per character.
      * **`NVARCHAR`:** Stores variable-length Unicode string data. Uses 2 bytes per character, allowing it to store characters from different languages.

19. **Similar for CHAR and NCHAR?**

      * **`CHAR`:** Stores fixed-length non-Unicode string data. Pads with spaces to the defined length.
      * **`NCHAR`:** Stores fixed-length Unicode string data. Pads with spaces to the defined length.

20. **What are index and their types?** An index is a database object that improves the speed of data retrieval operations on a database table. It's like an index in a book.

      * **Types:**
          * **Clustered Index:** Determines the physical order of data in the table. A table can have only one clustered index.
          * **Non-Clustered Index:** Does not alter the physical order of the table. It stores the data separately from the data rows and contains pointers to the actual data. A table can have multiple non-clustered indexes.

21. **What is an index? Explain its different types.** (Already answered in question 20).

22. **List the different types of relationships in SQL.**

      * **One-to-One (1:1):** Each record in table A is linked to at most one record in table B, and vice versa.
      * **One-to-Many (1:M):** One record in table A can be linked to many records in table B, but one record in table B is linked to only one record in table A. (Most common)
      * **Many-to-Many (M:N):** Many records in table A can be linked to many records in table B, and vice versa. This typically requires an intermediary "junction" or "linking" table.

23. **Differentiate between UNION and UNION ALL.**

      * **`UNION`:** Combines the result sets of two or more `SELECT` statements and *removes duplicate rows*.
      * **`UNION ALL`:** Combines the result sets of two or more `SELECT` statements and *includes all duplicate rows*.

24. **How many types of clauses in SQL?** There's no fixed "number of types" of clauses, as they serve different purposes. Some common and distinct clauses include: `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`/`TOP`, `JOIN` (and its variations), `ON`.

25. **What is the difference between UNION and UNION ALL in SQL?** (Already answered in question 23).

26. **What are the various types of relationships in SQL?** (Already answered in question 22).

27. **Difference between Primary Key and Secondary Key?**

      * **Primary Key:** Uniquely identifies each record in a table. Must be unique and `NOT NULL`. There can be only one primary key per table.
      * **Secondary Key (or Alternate Key):** A candidate key that is not chosen as the primary key. It can also uniquely identify records, but it's not the designated primary identifier.

28. **What is the difference between where and having?** (Already answered in question 2).

29. **Find the second highest salary of an employee?**

    ```sql
    SELECT MAX(Salary)
    FROM Employees
    WHERE Salary < (SELECT MAX(Salary) FROM Employees);
    ```

    OR using `DENSE_RANK`:

    ```sql
    SELECT Salary
    FROM (
        SELECT Salary, DENSE_RANK() OVER (ORDER BY Salary DESC) as rnk
        FROM Employees
    ) AS RankedSalaries
    WHERE rnk = 2;
    ```

30. **Write retention query in SQL?** (This is a broad topic and depends on how "retention" is defined, e.g., monthly cohort retention). Here's a basic example for month-over-month retention for users who joined in a specific month:

    Assume `Users` table with `user_id` and `join_date`.
    Assume `Activities` table with `user_id` and `activity_date`.

    ```sql
    WITH UserCohorts AS (
        SELECT
            user_id,
            DATE_TRUNC('month', join_date) AS cohort_month
        FROM Users
    ),
    MonthlyActivity AS (
        SELECT
            user_id,
            DATE_TRUNC('month', activity_date) AS activity_month
        FROM Activities
        GROUP BY user_id, DATE_TRUNC('month', activity_date)
    )
    SELECT
        uc.cohort_month,
        COUNT(DISTINCT uc.user_id) AS total_cohort_users,
        DATE_TRUNC('month', ma.activity_month) AS retention_month,
        COUNT(DISTINCT ma.user_id) AS retained_users,
        (COUNT(DISTINCT ma.user_id) * 100.0) / COUNT(DISTINCT uc.user_id) AS retention_rate
    FROM UserCohorts uc
    INNER JOIN MonthlyActivity ma ON uc.user_id = ma.user_id
    WHERE ma.activity_month >= uc.cohort_month -- Ensure activity is on or after join month
    GROUP BY uc.cohort_month, DATE_TRUNC('month', ma.activity_month)
    ORDER BY uc.cohort_month, retention_month;
    ```

    *Note: `DATE_TRUNC` syntax might vary based on SQL dialect (e.g., `DATE_TRUNC('month', date_column)` in PostgreSQL/Redshift, `FORMAT(date_column, 'yyyy-MM-01')` in SQL Server, `STRFTIME('%Y-%m-01', date_column)` in SQLite).*

31. **Write year-on-year growth in SQL?**
    Assuming a table `Sales` with `sale_date` and `amount`.

    ```sql
    WITH YearlySales AS (
        SELECT
            EXTRACT(YEAR FROM sale_date) AS sales_year,
            SUM(amount) AS total_sales
        FROM Sales
        GROUP BY EXTRACT(YEAR FROM sale_date)
    )
    SELECT
        ys.sales_year,
        ys.total_sales,
        LAG(ys.total_sales, 1, 0) OVER (ORDER BY ys.sales_year) AS previous_year_sales,
        (ys.total_sales - LAG(ys.total_sales, 1, 0) OVER (ORDER BY ys.sales_year)) * 100.0 / LAG(ys.total_sales, 1, NULL) OVER (ORDER BY ys.sales_year) AS yoy_growth_percentage
    FROM YearlySales ys
    ORDER BY ys.sales_year;
    ```

    *Note: `EXTRACT(YEAR FROM date_column)` is common; other functions like `YEAR(date_column)` or `DATEPART(year, date_column)` might be used depending on the SQL dialect.*

32. **Write a query for cumulative sum in SQL?**
    Assuming a table `Orders` with `order_date` and `order_amount`.

    ```sql
    SELECT
        order_date,
        order_amount,
        SUM(order_amount) OVER (ORDER BY order_date ASC) AS cumulative_sum
    FROM Orders
    ORDER BY order_date;
    ```

33. **Difference between Function and Stored Procedure?**

      * **Functions:**
          * Must return a value.
          * Can be called in `SELECT`, `WHERE`, `HAVING` clauses.
          * Cannot perform DML operations (e.g., `INSERT`, `UPDATE`, `DELETE`) directly on tables.
          * Can only have input parameters.
      * **Stored Procedures:**
          * Can return 0 or N values.
          * Cannot be called in `SELECT`, `WHERE`, `HAVING` clauses directly.
          * Can perform DML and DDL operations.
          * Can have input, output, and input/output parameters.

34. **Do we use variables in views?** No, you cannot directly use user-defined variables (like `@variable` in SQL Server or `SET @variable` in MySQL) within a standard SQL view definition. Views are essentially stored queries. To achieve dynamic behavior, you might pass parameters to a stored procedure that then queries the view, or use table-valued functions.

35. **What are the limitations of views?**

      * **Updatability:** Not all views are updatable. Views involving joins, aggregate functions, `GROUP BY`, `DISTINCT`, or certain other complex operations are generally not updatable.
      * **Performance:** A view itself doesn't improve performance. The underlying query is executed every time the view is accessed. Complex views can sometimes be slower than direct queries.
      * **Indexing:** You cannot directly create indexes on a standard view (though some systems support "indexed views" or "materialized views" which are different).
      * **Complexity:** Overly complex views can be hard to understand, debug, and maintain.
      * **Security:** While views can simplify security by showing only specific columns/rows, misconfigured views can inadvertently expose sensitive data.
      * **No Parameters:** Standard views do not accept parameters, limiting their dynamic use cases.