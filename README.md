# FastAPI RBAC System (Role-Based Access Control)

## Overview
This project is a **Role-Based Access Control (RBAC)** system built using **FastAPI** and **SQLAlchemy**.  
It supports **Superadmin, Admin, and User** roles, with dynamic **resource-level permissions** (CRUD).  

### Features:
- Superadmin can:
  - Approve/Activate users
  - Assign roles
  - Assign resources and CRUD permissions
- Admins and Users can:
  - Perform actions based on assigned resources (e.g., create post, comment post, manage post, create event, create poll, react to post)
- JWT Authentication (Bearer Token)
- PostgreSQL Database (SQLAlchemy ORM)
- `.env` file for secret credentials"# FastAPI-RBAC-System-Role-Based-Access-Control-" 
