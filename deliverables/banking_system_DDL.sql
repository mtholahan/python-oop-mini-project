/*
* Date: 2-Feb-2025
* Author: Mark Holahan
* Purpose: python-oop-mini-project DDL
* RDBMS: Stood up a SQL Server instance on Azure
*/

USE [FauxBankingSystemDB]
GO

-- Drop Foreign Key from Account Table if it exists
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_Account_Customer' AND parent_object_id = OBJECT_ID('dbo.Account'))
    ALTER TABLE dbo.Account DROP CONSTRAINT FK_Account_Customer;
GO

-- Drop Foreign Key from TransactionLog Table if it exists
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_TransactionLog_Account' AND parent_object_id = OBJECT_ID('dbo.TransactionLog'))
    ALTER TABLE dbo.TransactionLog DROP CONSTRAINT FK_TransactionLog_Account;
GO

-- Drop Tables if they exist
IF OBJECT_ID('dbo.TransactionLog', 'U') IS NOT NULL DROP TABLE dbo.TransactionLog;
IF OBJECT_ID('dbo.Account', 'U') IS NOT NULL DROP TABLE dbo.Account;
IF OBJECT_ID('dbo.Customer', 'U') IS NOT NULL DROP TABLE dbo.Customer;
IF OBJECT_ID('dbo.[Log]', 'U') IS NOT NULL DROP TABLE dbo.[Log];
GO

-- Customer Table
CREATE TABLE dbo.Customer (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    PhoneNumber NVARCHAR(20) NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);
GO

-- Account Table
CREATE TABLE dbo.Account (
    AccountID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT NOT NULL,
    AccountType NVARCHAR(20) CHECK (AccountType IN ('Checking', 'Savings')),
    Balance DECIMAL(18,2) CHECK (Balance >= 0) DEFAULT 0,
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (CustomerID) REFERENCES dbo.Customer(CustomerID) ON DELETE CASCADE
);
GO

CREATE TABLE dbo.TransactionLog (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    AccountID INT NOT NULL,
    RelatedAccountID INT NULL, -- For transfers
    TransactionType NVARCHAR(20) CHECK (TransactionType IN ('Deposit', 'Withdrawal', 'Transfer')),
    Amount DECIMAL(18,2) CHECK (Amount > 0) NOT NULL,
    TransactionTimestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (AccountID) REFERENCES dbo.Account(AccountID) ON DELETE CASCADE,
    FOREIGN KEY (RelatedAccountID) REFERENCES dbo.Account(AccountID) ON DELETE NO ACTION
);
GO

-- Log Table
CREATE TABLE dbo.Log (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    LogLevel NVARCHAR(20) CHECK (LogLevel IN ('INFO', 'WARNING', 'ERROR')),
    Message NVARCHAR(MAX) NOT NULL,
    LogTimestamp DATETIME DEFAULT GETDATE()
);
GO
