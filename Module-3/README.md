# Data Warehouse and BigQuery

## Index:
- [OLTP vs OLAP](#oltp-vs-olap)
- [What is Data Warehouse](#what-is-data-warehouse)
- [BigQuery](#big-query)

## OLTP vs OLAP
OLTP and OLAP are two different types of **Database System Design**, each optimized for specific purposes and use cases.

- **OLTP**: Online Transaction Processing.
- **OLAP**: Online Analytical Processing.

| Feature          | OLTP (Online Transaction Processing)                  | OLAP (Online Analytical Processing)                |
|------------------|-------------------------------------------------------|---------------------------------------------------|
| **Purpose**      | Handles day-to-day operations (inserting, updating, and deleting data in real-time). | Analyzes historical data for insights (primarily read-heavy, relies on `SELECT` queries). |
| **Data Updates**      | Short, fast updates. | Data priodically refreshed with scheduled, long running batch jobs. |
| **Database Design**      | Normalized for effeciency. | Denormaized for analysis (Easy to `SELECT`). |
| **Space**      | Generally small. | Large due to aggregating large datasets. |
| **Backup and Recovery** | Regular backups required to ensure business continuity and meet legal and governance requirements.   | Lost data can be reloaded from OLTP database as needed in lieu of regular backups.                  |
| **Productivity**      | Increases productivity of end users.                                                                 | Increases productivity of business managers, data analysts, and executives.                         |
| **Data View**         | Lists day-to-day business transactions.                                                              | Multi-dimensional view of enterprise data.                                                          |
| **User Examples**     | Customer-facing personnel, clerks, online shoppers.                                                  | Knowledge workers such as data analysts, business analysts, and executives.                         |

## What is Data Warehouse
A **Data Warehouse (DWH)** is an **OLAP** solution used for **reporting and data analysis**. 

- DWH consists of raw data, metadata, and summary.
- **Input**: Various data sources like flat files, operational systems (OS), OLTP databases, etc. These inputs are first written into a **staging area**, which is then processed and loaded into the DWH.
- **Output**: The DWH can be transformed into **data marts**, which are specialized subsets of the data warehouse focused on specific areas (e.g., sales, purchasing, etc.).

<img width="483" alt="Screenshot 2025-02-08 at 2 59 02 PM" src="https://github.com/user-attachments/assets/ab0f4f68-cb61-4699-baf6-593cde1f7ad6" />


## Big Query

