
CREATE DATABASE LibraryDB;
GO

USE LibraryDB;
GO

-- Library Management System Database Schema
-- Created for SQL Server

-- Drop tables in correct order (child tables first)
IF OBJECT_ID('notification', 'U') IS NOT NULL
    DROP TABLE notification;
GO

IF OBJECT_ID('favorite', 'U') IS NOT NULL
    DROP TABLE favorite;
GO

IF OBJECT_ID('review', 'U') IS NOT NULL
    DROP TABLE review;
GO

IF OBJECT_ID('borrow_request', 'U') IS NOT NULL
    DROP TABLE borrow_request;
GO

IF OBJECT_ID('book', 'U') IS NOT NULL
    DROP TABLE book;
GO

IF OBJECT_ID('category', 'U') IS NOT NULL
    DROP TABLE category;
GO

IF OBJECT_ID('users', 'U') IS NOT NULL
    DROP TABLE users;
GO

-- Create Users Table
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_staff BIT DEFAULT 0,
    is_active BIT DEFAULT 1,
    is_superuser BIT DEFAULT 0,
    role VARCHAR(10),
    date_joined DATETIME DEFAULT GETDATE(),
    last_login DATETIME,
    phone_number VARCHAR(20),
    address TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME
);
GO

-- Create Category Table
CREATE TABLE category (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Create Book Table
CREATE TABLE book (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    description TEXT,
    category_id INT FOREIGN KEY REFERENCES category(id),
    cover_image VARCHAR(255),
    pdf_file VARCHAR(255),
    isbn VARCHAR(13),
    publication_date DATE,
    total_copies INT DEFAULT 0,
    available_copies INT DEFAULT 0,
    borrow_price DECIMAL(6,2),
    buy_price DECIMAL(6,2),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME
);
GO

-- Create Borrow Request Table
CREATE TABLE borrow_request (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(id),
    book_id INT FOREIGN KEY REFERENCES book(id),
    status VARCHAR(20),
    request_date DATETIME DEFAULT GETDATE(),
    borrow_date DATETIME,
    return_date DATETIME,
    actual_return_date DATETIME
);
GO

-- Create Review Table
CREATE TABLE review (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(id),
    book_id INT FOREIGN KEY REFERENCES book(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME
);
GO

-- Create Favorite Table
CREATE TABLE favorite (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(id),
    book_id INT FOREIGN KEY REFERENCES book(id),
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Create Notification Table
CREATE TABLE notification (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT FOREIGN KEY REFERENCES users(id),
    notification_type VARCHAR(50),
    message TEXT,
    is_read BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    related_book_id INT FOREIGN KEY REFERENCES book(id)
);
GO

-- Insert Users Data
INSERT INTO users (username, password, email, first_name, last_name, is_staff, is_active, is_superuser, role, date_joined, last_login, phone_number, address, created_at, updated_at) VALUES
('ahmed', 'pbkdf2_sha256$1000000$YYMwircpqt8ugO2ccqZoUP$Ub...', 'ahmed.a.eldkrory@gmail.com', '', '', 1, 1, 1, 'user', '2025-05-05 16:03:13', '2025-05-05 18:42:06', NULL, NULL, '2025-05-05 16:03:14', '2025-05-05 22:29:14'),
('admin', 'pbkdf2_sha256$1000000$YYMwircpqt8ugO2ccqZoUP$Ub...', 'admin@example.com', '', '', 1, 1, 1, 'admin', '2025-05-05 16:46:42', '2025-05-05 22:30:17', NULL, NULL, '2025-05-05 16:46:42', '2025-05-05 22:29:14'),
('Ali', 'pbkdf2_sha256$1000000$YYMwircpqt8ugO2ccqZoUP$Ub...', 'user1@example.com', 'User 1', 'Test', 0, 1, 0, 'user', '2025-05-05 16:46:42', '2025-05-05 22:30:30', NULL, '', '2025-05-05 16:46:42', '2025-05-05 22:29:14'),
('Fady', 'pbkdf2_sha256$1000000$YYMwircpqt8ugO2ccqZoUP$Ub...', 'user2@example.com', 'User 2', 'Test', 0, 1, 0, 'user', '2025-05-05 16:46:42', NULL, NULL, '', '2025-05-05 16:46:42', '2025-05-05 22:29:14'),
('Mohammed', 'pbkdf2_sha256$1000000$YYMwircpqt8ugO2ccqZoUP$Ub...', 'user3@example.com', 'User 3', 'Test', 0, 1, 0, 'user', '2025-05-05 16:46:43', NULL, NULL, '', '2025-05-05 16:46:43', '2025-05-05 22:29:14'),
('Manar', 'pbkdf2_sha256$1000000$YYMwircpqt8ugO2ccqZoUP$Ub...', 'user4@example.com', 'User 4', 'Test', 0, 1, 0, 'user', '2025-05-05 16:46:44', NULL, NULL, '', '2025-05-05 16:46:44', '2025-05-05 22:29:14'),
('Samy', 'pbkdf2_sha256$1000000$YYMwircpqt8ugO2ccqZoUP$Ub...', 'user5@example.com', 'User 5', 'Test', 0, 1, 0, 'user', '2025-05-05 16:46:44', NULL, NULL, '', '2025-05-05 16:46:44', '2025-05-05 22:29:14');
GO

-- Insert Categories
INSERT INTO category (name, description, created_at) VALUES
('Fiction', 'Novels, short stories, and other fictional works', '2025-05-05 16:46:41'),
('Non-Fiction', 'Factual works, biographies, and informational texts', '2025-05-05 16:46:41'),
('Science Fiction', 'Speculative fiction dealing with imaginative concepts', '2025-05-05 16:46:41'),
('Mystery', 'Fiction dealing with the solution of a crime or puzzle', '2025-05-05 16:46:41'),
('Fantasy', 'Fiction featuring magical and supernatural elements', '2025-05-05 16:46:41'),
('Biography', 'Detailed descriptions of a person''s life', '2025-05-05 16:46:41'),
('History', 'Books about historical events and periods', '2025-05-05 16:46:41'),
('Science', 'Books about scientific discoveries and concepts', '2025-05-05 16:46:41'),
('Technology', 'Books about technological advancements and computing', '2025-05-05 16:46:41'),
('Self-Help', 'Books aimed at personal improvement', '2025-05-05 16:46:41');
GO

-- Insert Books
INSERT INTO book (title, author, description, category_id, cover_image, pdf_file, isbn, publication_date, total_copies, available_copies, borrow_price, buy_price, created_at, updated_at) VALUES
('To Kill a Mockingbird', 'Harper Lee', 'The story of young Scout Finch and her father Atticus', 1, '/media/covers/9780061120084.jpg', NULL, '9780061120084', '1960-07-11', 10, 6, 9.99, 29.99, '2025-05-05 16:46:41', '2025-05-05 17:28:45'),
('1984', 'George Orwell', 'A dystopian novel set in a totalitarian society', 1, '/media/covers/9780451524935.jpg', NULL, '9780451524935', '1949-06-08', 15, 12, 9.99, 29.99, '2025-05-05 16:46:41', '2025-05-05 22:18:49'),
('The Great Gatsby', 'F. Scott Fitzgerald', 'The story of eccentric millionaire Jay Gatsby', 1, '/media/covers/9780743273565.jpg', NULL, '9780743273565', '1925-04-10', 8, 5, 9.99, 29.99, '2025-05-05 16:46:41', '2025-05-05 17:28:57'),
('A Brief History of Time', 'Stephen Hawking', 'A landmark volume in science writing', 8, '/media/covers/9780553380163.jpg', NULL, '9780553380163', '1988-09-01', 7, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:00'),
('The Hobbit', 'J.R.R. Tolkien', 'The adventure of Bilbo Baggins, a hobbit who embarks on an epic quest', 5, '/media/covers/9780547928227.jpg', NULL, '9780547928227', '1937-09-21', 20, 15, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:06'),
('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'A survey of the history of humankind', 7, '/media/covers/9780062316097.jpg', NULL, '9780062316097', '2014-02-10', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:12'),
('The Alchemist', 'Paulo Coelho', 'A philosophical novel about a young Andalusian shepherd', 1, '/media/covers/9780061122415.jpg', NULL, '9780061122415', '1988-01-01', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:15'),
('The Da Vinci Code', 'Dan Brown', 'A mystery thriller novel that follows symbologist Robert Langdon', 4, '/media/covers/9780307474278.jpg', NULL, '9780307474278', '2003-03-18', 18, 14, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:20'),
('Dune', 'Frank Herbert', 'A science fiction novel set in the distant future', 3, '/media/covers/9780441172719.jpg', NULL, '9780441172719', '1965-08-01', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:26'),
('Steve Jobs', 'Walter Isaacson', 'The biography of Apple co-founder Steve Jobs', 6, '/media/covers/9781451648539.jpg', NULL, '9781451648539', '2011-10-24', 8, 7, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:31'),
('Thinking, Fast and Slow', 'Daniel Kahneman', 'A book that summarizes research that Kahneman conducted', 2, '/media/covers/9780374533557.jpg', NULL, '9780374533557', '2011-10-25', 9, 7, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:34'),
('The Catcher in the Rye', 'J.D. Salinger', 'A novel about a teenager named Holden Caulfield', 1, '/media/covers/9780316769488.jpg', NULL, '9780316769488', '1951-07-16', 12, 9, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:39'),
('The Lord of the Rings', 'J.R.R. Tolkien', 'An epic high-fantasy novel that follows hobbits', 5, '/media/covers/9780618640157.jpg', NULL, '9780618640157', '1954-07-29', 25, 20, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:45'),
('The Immortal Life of Henrietta Lacks', 'Rebecca Skloot', 'A non-fiction book about Henrietta Lacks', 8, '/media/covers/9781400052189.jpg', NULL, '9781400052189', '2010-02-02', 7, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:51'),
('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'A psychological thriller that follows journalist Mikael Blomkvist', 4, '/media/covers/9780307454546.jpg', NULL, '9780307454546', '2005-08-01', 14, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:29:56'),
('Educated', 'Tara Westover', 'A memoir about a woman who was raised in a survivalist family', 6, '/media/covers/9780399590504.jpg', NULL, '9780399590504', '2018-02-20', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:02'),
('The Martian', 'Andy Weir', 'A science fiction novel about an astronaut who is stranded on Mars', 3, '/media/covers/9780553418026.jpg', NULL, '9780553418026', '2014-02-11', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:08'),
('Atomic Habits', 'James Clear', 'A practical guide to breaking bad habits and building good ones', 10, '/media/covers/9780735211292.jpg', NULL, '9780735211292', '2018-10-16', 20, 15, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:14'),
('The Silent Patient', 'Alex Michaelides', 'A psychological thriller about a woman who shoots her husband', 4, '/media/covers/9781250301697.jpg', NULL, '9781250301697', '2019-02-05', 12, 9, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:20'),
('The Power of Habit', 'Charles Duhigg', 'An examination of the science behind habit creation', 10, '/media/covers/9780812981605.jpg', NULL, '9780812981605', '2012-02-28', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('Pride and Prejudice', 'Jane Austen', 'A romantic novel of manners', 1, '/media/covers/9780141439518.jpg', NULL, '9780141439518', '1813-01-28', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Hitchhiker''s Guide to the Galaxy', 'Douglas Adams', 'A comic science fiction series', 3, '/media/covers/9780345391803.jpg', NULL, '9780345391803', '1979-10-12', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Kite Runner', 'Khaled Hosseini', 'A story of friendship and redemption', 1, '/media/covers/9781594631931.jpg', NULL, '9781594631931', '2003-05-29', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Art of War', 'Sun Tzu', 'An ancient Chinese military treatise', 2, '/media/covers/9780140439199.jpg', NULL, '9780140439199', '1910-01-01', 8, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Little Prince', 'Antoine de Saint-Exupéry', 'A poetic tale about a young prince', 1, '/media/covers/9780156013987.jpg', NULL, '9780156013987', '1943-04-06', 20, 15, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Art of Thinking Clearly', 'Rolf Dobelli', 'A collection of cognitive biases and errors', 2, '/media/covers/9780062219695.jpg', NULL, '9780062219695', '2013-05-14', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Psychology of Money', 'Morgan Housel', 'Timeless lessons on wealth and happiness', 2, '/media/covers/9780857197689.jpg', NULL, '9780857197689', '2020-09-08', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('Project Hail Mary', 'Andy Weir', 'A science fiction novel about an astronaut', 3, '/media/covers/9781524741338.jpg', NULL, '9781524741338', '2021-05-04', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Midnight Library', 'Matt Haig', 'A novel about infinite possibilities', 1, '/media/covers/9780525559474.jpg', NULL, '9780525559474', '2020-08-13', 12, 9, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('Klara and the Sun', 'Kazuo Ishiguro', 'A novel about artificial intelligence', 3, '/media/covers/9780593318171.jpg', NULL, '9780593318171', '2021-03-02', 8, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Code Breaker', 'Walter Isaacson', 'A biography of Jennifer Doudna', 6, '/media/covers/9781982115852.jpg', NULL, '9781982115852', '2021-03-09', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Anthropocene Reviewed', 'John Green', 'Essays on the human-centered planet', 2, '/media/covers/9780525555216.jpg', NULL, '9780525555216', '2021-05-18', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Thursday Murder Club', 'Richard Osman', 'A mystery novel about a group of retirees', 4, '/media/covers/9780241988268.jpg', NULL, '9780241988268', '2020-09-03', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Lincoln Highway', 'Amor Towles', 'A novel about a road trip across America', 1, '/media/covers/9780735222359.jpg', NULL, '9780735222359', '2021-10-05', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Last Thing He Told Me', 'Laura Dave', 'A mystery novel about a woman''s search for truth', 4, '/media/covers/9781501171345.jpg', NULL, '9781501171345', '2021-05-04', 12, 9, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Seven Husbands of Evelyn Hugo', 'Taylor Jenkins Reid', 'A novel about an aging starlet', 1, '/media/covers/9781501161933.jpg', NULL, '9781501161933', '2017-06-13', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Invisible Life of Addie LaRue', 'V.E. Schwab', 'A fantasy novel about a woman who makes a Faustian bargain', 5, '/media/covers/9780765387561.jpg', NULL, '9780765387561', '2020-10-06', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Four Winds', 'Kristin Hannah', 'A novel about the Great Depression', 1, '/media/covers/9781250178602.jpg', NULL, '9781250178602', '2021-02-02', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Push', 'Ashley Audrain', 'A psychological thriller about motherhood', 4, '/media/covers/9780525657606.jpg', NULL, '9780525657606', '2021-01-05', 8, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Sanatorium', 'Sarah Pearse', 'A thriller set in a remote hotel', 4, '/media/covers/9780593296677.jpg', NULL, '9780593296677', '2021-02-02', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Final Girl Support Group', 'Grady Hendrix', 'A horror novel about final girls', 4, '/media/covers/9780593201237.jpg', NULL, '9780593201237', '2021-07-13', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Maidens', 'Alex Michaelides', 'A psychological thriller set at Cambridge', 4, '/media/covers/9781250304452.jpg', NULL, '9781250304452', '2021-06-15', 12, 9, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Paper Palace', 'Miranda Cowley Heller', 'A novel about a woman''s choice between two loves', 1, '/media/covers/9780593329825.jpg', NULL, '9780593329825', '2021-07-06', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Personal Librarian', 'Marie Benedict', 'A historical novel about Belle da Costa Greene', 6, '/media/covers/9780593101537.jpg', NULL, '9780593101537', '2021-06-29', 8, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Reading List', 'Sara Nisha Adams', 'A novel about the power of books', 1, '/media/covers/9780063025288.jpg', NULL, '9780063025288', '2021-08-03', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Guncle', 'Steven Rowley', 'A novel about an uncle caring for his niece and nephew', 1, '/media/covers/9780525542285.jpg', NULL, '9780525542285', '2021-05-25', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Plot', 'Jean Hanff Korelitz', 'A thriller about a stolen story', 4, '/media/covers/9781250790755.jpg', NULL, '9781250790755', '2021-05-11', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Last House on Needless Street', 'Catriona Ward', 'A psychological thriller', 4, '/media/covers/9781250812624.jpg', NULL, '9781250812624', '2021-09-28', 8, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Love Hypothesis', 'Ali Hazelwood', 'A romantic comedy about a scientist', 1, '/media/covers/9780593336823.jpg', NULL, '9780593336823', '2021-09-14', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Heart Principle', 'Helen Hoang', 'A novel about love and self-discovery', 1, '/media/covers/9780451490841.jpg', NULL, '9780451490841', '2021-08-31', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Guide', 'Peter Heller', 'A thriller set in the wilderness', 4, '/media/covers/9780525657743.jpg', NULL, '9780525657743', '2021-08-24', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Man Who Died Twice', 'Richard Osman', 'A mystery novel about the Thursday Murder Club', 4, '/media/covers/9780241988237.jpg', NULL, '9780241988237', '2021-09-16', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Wish', 'Nicholas Sparks', 'A novel about love and second chances', 1, '/media/covers/9781538728526.jpg', NULL, '9781538728526', '2021-09-28', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Christmas Bookshop', 'Jenny Colgan', 'A holiday novel about a bookshop', 1, '/media/covers/9780063141230.jpg', NULL, '9780063141230', '2021-10-26', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Sentence', 'Louise Erdrich', 'A novel about a haunted bookstore', 1, '/media/covers/9780062671127.jpg', NULL, '9780062671127', '2021-11-09', 8, 6, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Ballad of Songbirds and Snakes', 'Suzanne Collins', 'A prequel to The Hunger Games', 3, '/media/covers/9781338635171.jpg', NULL, '9781338635171', '2020-05-19', 20, 15, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Midnight Library', 'Matt Haig', 'A novel about infinite possibilities', 1, '/media/covers/9780525559474.jpg', NULL, '9780525559474', '2020-08-13', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Invisible Life of Addie LaRue', 'V.E. Schwab', 'A fantasy novel about a woman who makes a Faustian bargain', 5, '/media/covers/9780765387561.jpg', NULL, '9780765387561', '2020-10-06', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The House in the Cerulean Sea', 'TJ Klune', 'A fantasy novel about found family', 5, '/media/covers/9781250217288.jpg', NULL, '9781250217288', '2020-03-17', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Vanishing Half', 'Brit Bennett', 'A novel about twin sisters', 1, '/media/covers/9780525536291.jpg', NULL, '9780525536291', '2020-06-02', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Guest List', 'Lucy Foley', 'A thriller set at a wedding', 4, '/media/covers/9780062868930.jpg', NULL, '9780062868930', '2020-02-20', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Thursday Murder Club', 'Richard Osman', 'A mystery novel about a group of retirees', 4, '/media/covers/9780241988268.jpg', NULL, '9780241988268', '2020-09-03', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Midnight Library', 'Matt Haig', 'A novel about infinite possibilities', 1, '/media/covers/9780525559474.jpg', NULL, '9780525559474', '2020-08-13', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Invisible Life of Addie LaRue', 'V.E. Schwab', 'A fantasy novel about a woman who makes a Faustian bargain', 5, '/media/covers/9780765387561.jpg', NULL, '9780765387561', '2020-10-06', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The House in the Cerulean Sea', 'TJ Klune', 'A fantasy novel about found family', 5, '/media/covers/9781250217288.jpg', NULL, '9781250217288', '2020-03-17', 10, 8, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Vanishing Half', 'Brit Bennett', 'A novel about twin sisters', 1, '/media/covers/9780525536291.jpg', NULL, '9780525536291', '2020-06-02', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Guest List', 'Lucy Foley', 'A thriller set at a wedding', 4, '/media/covers/9780062868930.jpg', NULL, '9780062868930', '2020-02-20', 12, 10, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23'),
('The Thursday Murder Club', 'Richard Osman', 'A mystery novel about a group of retirees', 4, '/media/covers/9780241988268.jpg', NULL, '9780241988268', '2020-09-03', 15, 12, 9.99, 29.99, '2025-05-05 16:46:42', '2025-05-05 17:30:23');
GO

-- Insert Borrow Requests
INSERT INTO borrow_request (user_id, book_id, status, request_date, borrow_date, return_date, actual_return_date) VALUES
(1, 1, 'returned', '2025-05-05 16:52:10', '2025-05-05 16:52:10', '2025-05-05 19:53:00', NULL),
(1, 1, 'rejected', '2025-05-05 16:55:38', '2025-05-05 16:55:38', '2025-05-05 19:57:00', NULL),
(1, 2, 'returned', '2025-05-05 17:10:27', '2025-05-05 17:10:27', '2025-05-05 20:11:00', '2025-05-05 17:15:08'),
(1, 1, 'returned', '2025-05-05 17:15:17', '2025-05-05 17:15:17', '2025-05-05 20:15:00', '2025-05-05 17:15:39'),
(1, 2, 'returned', '2025-05-05 17:23:29', '2025-05-05 17:23:29', '2025-05-05 20:25:00', '2025-05-05 17:23:45'),
(1, 14, 'returned', '2025-05-05 17:26:00', '2025-05-05 17:26:00', '2025-05-05 20:27:00', '2025-05-05 17:26:34'),
(1, 13, 'returned', '2025-05-05 18:32:46', '2025-05-05 18:32:46', '2025-05-05 21:32:00', '2025-05-05 18:33:12'),
(1, 2, 'returned', '2025-05-05 22:13:17', '2025-05-05 22:13:17', NULL, '2025-05-05 22:18:49'),
(1, 3, 'pending', '2025-05-05 22:18:45', '2025-05-05 22:18:45', NULL, NULL);
GO

-- Insert Reviews
INSERT INTO review (user_id, book_id, rating, comment, created_at, updated_at) VALUES
(1, 1, 5, 'Absolutely loved this book! Couldn''t put it down.', '2025-05-05 16:46:45', '2025-05-05 16:46:45'),
(1, 2, 4, 'One of the best books I''ve read this year.', '2025-05-05 16:46:45', '2025-05-05 16:46:45'),
(1, 3, 5, 'One of the best books I''ve read this year.', '2025-05-05 16:46:45', '2025-05-05 16:46:45'),
(1, 4, 4, 'Beautifully written with a compelling narrative.', '2025-05-05 16:46:45', '2025-05-05 16:46:45'),
(1, 5, 4, 'Absolutely loved this book! Couldn''t put it down.', '2025-05-05 16:46:45', '2025-05-05 16:46:45'),
(1, 6, 1, 'Too many clichés and predictable twists.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 7, 4, 'A masterpiece that will stand the test of time.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 8, 3, 'Interesting premise but the execution could have been better.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 9, 5, 'The author''s writing style is exceptional.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 10, 1, 'Didn''t live up to my expectations at all.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 11, 1, 'Had trouble connecting with the characters.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 12, 2, 'Had trouble connecting with the characters.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 13, 3, 'Liked the characters but found the plot somewhat predictable.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 14, 3, 'The first half was excellent, but it lost momentum in the second half.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 15, 1, 'The premise was promising but the execution fell flat.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 16, 4, 'I was completely immersed in the story from start to finish.', '2025-05-05 16:46:46', '2025-05-05 17:00:14'),
(1, 17, 4, 'Highly recommend this to anyone who enjoys this genre.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 18, 4, 'A masterpiece that will stand the test of time.', '2025-05-05 16:46:46', '2025-05-05 17:01:03'),
(1, 19, 4, 'The perfect balance of plot, character development, and pacing.', '2025-05-05 16:46:46', '2025-05-05 16:46:46'),
(1, 20, 4, 'The characters were so well developed and the plot was engaging.', '2025-05-05 16:46:46', '2025-05-05 17:00:26');
GO

-- Test Queries
GO

-- Test Books
SELECT * FROM book;
GO

-- Test Users
SELECT * FROM users;
GO

-- Test Categories
SELECT * FROM category;
GO

-- Test Borrow Requests
SELECT * FROM borrow_request;
GO

-- Test Reviews
SELECT * FROM review;
GO

-- Test Favorites
SELECT * FROM favorite;
GO

-- Test Notifications
SELECT * FROM notification;
GO

-- Test Book Details with Category
SELECT b.title, b.author, c.name as category_name, b.total_copies, b.available_copies
FROM book b
JOIN category c ON b.category_id = c.id;
GO

-- Test User Borrow History
SELECT u.username, b.title, br.status, br.request_date, br.return_date
FROM borrow_request br
JOIN users u ON br.user_id = u.id
JOIN book b ON br.book_id = b.id;
GO

-- Test Book Reviews with User
SELECT b.title, u.username, r.rating, r.comment
FROM review r
JOIN book b ON r.book_id = b.id
JOIN users u ON r.user_id = u.id;
GO

-- Test Available Books
SELECT title, author, available_copies
FROM book
WHERE available_copies > 0;
GO

-- Test Books by Category
SELECT c.name as category, COUNT(*) as book_count
FROM book b
JOIN category c ON b.category_id = c.id
GROUP BY c.name;
GO 