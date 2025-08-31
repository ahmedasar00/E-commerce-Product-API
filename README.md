# Django E-commerce API

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [✨ Core Features](#-core-features)
- [🛠️ Technology Stack](#-technology-stack)
- [🗂️ Project Structure](#-project-structure)
- [📊 Database Schema (ERD)](#-database-schema-erd)
- [🚀 API Endpoints](#-api-endpoints)
- [🔧 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [⚙️ Environment Variables](#-environment-variables)
- [▶️ Running the Application](#️-running-the-application)

## 📝 About the Project

This project is a full-featured, multi-vendor e-commerce RESTful API built with Django and Django REST Framework. It provides a robust backend system that allows registered users to become sellers, manage their products (which require admin approval), while buyers can browse products, manage a shopping cart, place orders, and provide reviews.

The architecture is designed to be scalable, secure, and maintainable, following best practices for modern web API development.

---

## ✨ Core Features

- **User Management & Authentication:** Secure user registration and login.
- **Multi-Vendor System:** Users can register as sellers and manage their own product listings.
- **Product Management:** Complete CRUD operations for products, including image uploads.
- **Admin Approval System:** Products submitted by sellers must be approved by an admin before they become visible to buyers.
- **Category & Filtering:** Products are organized by categories, with advanced filtering options.
- **Shopping Cart:** Persistent shopping cart for each authenticated user.
- **Order Management:** A complete system for placing and tracking orders.
- **Reviews & Ratings:** Users can leave reviews and ratings for products they have purchased.
- **Search Functionality:** Flexible product search by name or category.
- **Pagination:** Efficiently handles large datasets for product listings and search results.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.12
- **Framework:** Django
- **API:** Django REST Framework (DRF)
- **Authentication:** DRF Token Authentication (built-in).
- **Database:** PostgreSQL / MySQL / SQLite 3 (Configurable)

---

## 🗂️ Project Structure

The project is organized into modular Django apps for better separation of concerns:

- `ecommerce_api/`: Main project configuration directory.
- `users/`: Handles user registration, authentication, and profiles (template-based).
- `products/`: Manages product details, listings, and seller associations.
- `categories/`: Manages product categories.
- `orders/`: Handles order creation, status tracking, and order items.
- `payments/`: Handles payment processing integrations.
- `reviews/`: Manages user reviews and ratings for products.
- `media/`: Stores user-uploaded files like product images.

---

## 📊 Database Schema (ERD)

The database is designed to support the complex relationships in an e-commerce platform. The key entities include Users, Products, Categories, Orders, OrderItems, and Reviews.

![Entity Relationship Diagram](./docs/ERD/U_ERD.png)

---

## 🚀 API Endpoints

Here is a summary of the available API endpoints based on the current project structure.

| Method         | Endpoint                   | Description                         | Auth Required |
| :------------- | :------------------------- | :---------------------------------- | :------------ |
| **Products**   |                            |                                     |               |
| `GET`          | `/products/api/`           | Get a list of all products.         | No            |
| `POST`         | `/products/api/`           | Create a new product.               | Yes (Seller)  |
| `GET`          | `/products/api/{id}/`      | Get details of a specific product.  | No            |
| `PUT`/`PATCH`  | `/products/api/{id}/`      | Update a product.                   | Yes (Seller)  |
| `DELETE`       | `/products/api/{id}/`      | Delete a product.                   | Yes (Seller)  |
| **Categories** |                            |                                     |               |
| `GET`          | `/api/v1/categories/`      | Get a list of all categories.       | No            |
| `POST`         | `/api/v1/categories/`      | Create a new category.              | Yes (Admin)   |
| `GET`          | `/api/v1/categories/{id}/` | Get details of a specific category. | No            |
| `PUT`/`PATCH`  | `/api/v1/categories/{id}/` | Update a category.                  | Yes (Admin)   |
| `DELETE`       | `/api/v1/categories/{id}/` | Delete a category.                  | Yes (Admin)   |
| **Orders**     |                            |                                     |               |
| `GET`          | `/api/orders/`             | List all orders for the user.       | Yes           |
| `POST`         | `/api/orders/`             | Create a new order.                 | Yes           |
| `GET`          | `/api/orders/{id}/`        | Get details of a specific order.    | Yes           |

_Note: The project also includes several template-based URLs for rendering HTML pages (e.g., `/register/`, `/login/`, `/products/`, `/categories/`, `/my-orders/`). The table above focuses exclusively on the RESTful API endpoints that handle JSON data._

---

## 🔧 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python (3.10 or higher)
- pip (Python package installer)
- Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory. It is recommended to copy from a `.env.example` file if one exists. See the [Environment Variables](#-environment-variables) section below for required keys.

5.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser to access the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```

---

## ⚙️ Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

```ini
# .env file

# Django Settings
SECRET_KEY='your-secret-key'
DEBUG=True

# Database Settings (Example for MySQL/PostgreSQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
```
