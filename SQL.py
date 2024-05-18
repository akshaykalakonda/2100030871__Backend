import sqlite3

def create_and_populate_tables():
    conn = sqlite3.connect('akki.db') 
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY,
            FirstName TEXT,
            LastName TEXT,
            Email TEXT,
            DateOfBirth DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INTEGER PRIMARY KEY,
            CustomerID INTEGER,
            OrderDate DATE,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderItems (
            OrderItemID INTEGER PRIMARY KEY,
            OrderID INTEGER,
            ProductID INTEGER,
            Quantity INTEGER,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY,
            ProductName TEXT,
            Price REAL
        )
    ''')
    cursor.executemany('''
        INSERT INTO Customers (CustomerID, FirstName, LastName, Email, DateOfBirth) 
        VALUES (?, ?, ?, ?, ?)
    ''', [
        (1, 'John', 'Doe', 'john.doe@example.com', '1985-01-15'),
        (2, 'Jane', 'Smith', 'jane.smith@example.com', '1990-06-20')
    ])

    cursor.executemany('''
        INSERT INTO Orders (OrderID, CustomerID, OrderDate) 
        VALUES (?, ?, ?)
    ''', [
        (1, 1, '2023-01-10'),
        (2, 2, '2023-01-12')
    ])

    cursor.executemany('''
        INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity) 
        VALUES (?, ?, ?, ?)
    ''', [
        (1, 1, 1, 1),
        (2, 1, 3, 2),
        (3, 2, 2, 1),
        (4, 2, 3, 1)
    ])

    cursor.executemany('''
        INSERT INTO Products (ProductID, ProductName, Price) 
        VALUES (?, ?, ?)
    ''', [
        (1, 'Laptop', 1000),
        (2, 'Smartphone', 600),
        (3, 'Headphones', 100)
    ])

    conn.commit()
    conn.close()
    
def customerslist():
    conn = sqlite3.connect('akki.db')  
    cursor = conn.cursor()
    query='''
        SELECT * FROM Customers
        '''
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print("CustomerID:", row[0])
        print("First Name:", row[1])
        print("Last Name:", row[2])
        print("Email:", row[3])
        print("DateOfBirth", row[4])
        print()

    conn.close()
    
def find_orders_in_january_2023():
    conn = sqlite3.connect('akki.db')
    cursor = conn.cursor()

    query = '''
        SELECT * 
        FROM Orders 
        WHERE strftime('%Y-%m', OrderDate) = '2023-01'
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print("OrderID:", row[0])
        print("CustomerID:", row[1])
        print("OrderDate:", row[2])
        print()

    conn.close()

def get_order_details_with_customer_info():
    conn = sqlite3.connect('akki.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            Orders.OrderID,
            Orders.OrderDate,
            Customers.FirstName,
            Customers.LastName,
            Customers.Email
        FROM 
            Orders
        JOIN 
            Customers ON Orders.CustomerID = Customers.CustomerID
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print("OrderID:", row[0])
        print("OrderDate:", row[1])
        print("Customer Name:", row[2], row[3])
        print("Customer Email:", row[4])
        print()

    conn.close()

def list_products_in_order(order_id):
    conn = sqlite3.connect('akki.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            Products.ProductID,
            Products.ProductName,
            OrderItems.Quantity
        FROM 
            OrderItems
        JOIN 
            Products ON OrderItems.ProductID = Products.ProductID
        WHERE 
            OrderItems.OrderID = ?
    '''

    cursor.execute(query, (order_id,))
    results = cursor.fetchall()

    for row in results:
        print("ProductID:", row[0])
        print("Product Name:", row[1])
        print("Quantity:", row[2])
        print()

    conn.close()

def calculate_total_spent_by_customer():
    conn = sqlite3.connect('akki.db')
    cursor = conn.cursor()

    query = '''
        SELECT
            c.CustomerID,
            c.FirstName,
            c.LastName,
            c.Email,
            SUM(p.Price * oi.Quantity) AS TotalSpent
        FROM
            Customers c
        JOIN
            Orders o ON c.CustomerID = o.CustomerID
        JOIN
            OrderItems oi ON o.OrderID = oi.OrderID
        JOIN
            Products p ON oi.ProductID = p.ProductID
        GROUP BY
            c.CustomerID, c.FirstName, c.LastName, c.Email
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print("CustomerID:", row[0])
        print("First Name:", row[1])
        print("Last Name:", row[2])
        print("Email:", row[3])
        print("Total Spent:", row[4])
        print()

    conn.close()

def find_most_popular_product():
    conn = sqlite3.connect('akki.db')
    cursor = conn.cursor()

    query = '''
        SELECT
            p.ProductID,
            p.ProductName,
            COUNT(oi.OrderItemID) AS TotalOrders
        FROM
            Products p
        JOIN
            OrderItems oi ON p.ProductID = oi.ProductID
        GROUP BY
            p.ProductID, p.ProductName
        ORDER BY
            TotalOrders DESC
        LIMIT 1
    '''

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        print("ProductID:", result[0])
        print("Product Name:", result[1])
        print("Total Orders:", result[2])
        print()
    else:
        print("No data found.")

    conn.close()

def get_orders_and_sales_by_month_2023():
    conn = sqlite3.connect('akki.db')
    cursor = conn.cursor()

    query = '''
        SELECT 
            strftime('%Y-%m', o.OrderDate) AS Month,
            COUNT(o.OrderID) AS TotalOrders,
            SUM(p.Price * oi.Quantity) AS TotalSalesAmount
        FROM 
            Orders o
        JOIN 
            OrderItems oi ON o.OrderID = oi.OrderID
        JOIN 
            Products p ON oi.ProductID = p.ProductID
        WHERE 
            strftime('%Y', o.OrderDate) = '2023'
        GROUP BY 
            Month
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print("Month:", row[0])
        print("Total Orders:", row[1])
        print("Total Sales Amount:", row[2])
        print()

    conn.close()

def query_customers_spent_more_than_1000():
    conn = sqlite3.connect('akki.db')  
    cursor = conn.cursor()

    query = '''
        SELECT
            c.CustomerID,
            c.FirstName,
            c.LastName,
            c.Email,
            SUM(p.Price * oi.Quantity) AS TotalSpent
        FROM
            Customers c
        JOIN
            Orders o ON c.CustomerID = o.CustomerID
        JOIN
            OrderItems oi ON o.OrderID = oi.OrderID
        JOIN
            Products p ON oi.ProductID = p.ProductID
        GROUP BY
            c.CustomerID, c.FirstName, c.LastName, c.Email
        HAVING
            TotalSpent > 1000
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print("CustomerID:", row[0])
        print("First Name:", row[1])
        print("Last Name:", row[2])
        print("Email:", row[3])
        print("Total Spent:", row[4])
        print()

    conn.close()


#create_and_populate_tables()

print("Query 1: List all customers")
customerslist()

print("Query 2: Orders placed in January 2023:")
find_orders_in_january_2023()

print("Query 3: Order details with customer information:")
get_order_details_with_customer_info()

print("Query 4: Products purchased in OrderID 1:")
list_products_in_order(1)

print("Query 5: Total amount spent by each customer:")
calculate_total_spent_by_customer()

print("Query 6:Most popular product")
find_most_popular_product()

print("Query 7: Total number of orders and sales amount for each month in 2023:")
get_orders_and_sales_by_month_2023()

print("Query 8: Customers who spent more than $1000:")
query_customers_spent_more_than_1000()
