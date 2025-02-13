USE FauxBankingSystemDB

select * from dbo.Account
select * from dbo.Customer
select * from dbo.TransactionLog
-- TRUNCATE TABLE dbo.TransactionLog
select * from dbo.[Log]


--BEGIN TRANSACTION;
--UPDATE Account SET Balance = Balance - 56 WHERE AccountID = 2;
--INSERT INTO TransactionLog (AccountID, TransactionType, Amount)
--VALUES (2, 'Withdrawal', 56);
--COMMIT;

--USE FauxBankingSystemDB;  -- Ensure we're in the correct database
--SELECT * FROM TransactionLog WHERE AccountID = 2;
--SELECT Balance FROM Account WHERE AccountID = 2;

