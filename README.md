Morabe – Real Estate Investment Platform

Morabe is a Django-based backend platform that enables users to invest in construction projects with flexibility. Admins can register projects that need funding, and users can purchase land in any quantity, even less than one square meter, based on their financial capacity. Investments generate digital assets that can later be sold to other users at prices approved by the admin.

Features

User Registration & Authentication
Users must register and complete identity verification by uploading a short video of themselves. The admin approves each user before they can make purchases.

Admin Panel
A fully functional admin panel allows admins to manage projects, verify users, and upload progress updates (photos, area completed, supervisors, etc.).

Flexible Land Investment
Users can invest any amount in available projects, with a minimum purchase price that allows participation even with small budgets.

Digital Asset Management
After investment, users receive digital assets representing their purchased land. They can sell portions of these assets to other users at prices approved by the admin.

Real-Time Updates
Transactions and asset ownership are updated in real-time. Project progress is periodically updated by the admin.

Integrated Wallet & Payment Gateway
Each user has a personal wallet that can be topped up via the ZarinPal payment gateway to facilitate land purchases.

Tech Stack

Backend: Python & Django REST Framework (DRF)

Database: SQLite/PostgreSQL (configurable)

Authentication: JWT / Token-based

Payment Gateway: ZarinPal

Note: Frontend development is planned separately and is not included in this repository yet

Project Status

Currently, the project backend is under development. Only the DRF backend is implemented; frontend development will be completed separately. The features described above represent the planned full functionality.

Contribution

This project is under active development. Contributions are welcome from developers familiar with Django REST Framework.
