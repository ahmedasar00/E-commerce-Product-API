# Django E-commerce API

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST-A30000?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![WhiteNoise](https://img.shields.io/badge/WhiteNoise-FFFFFF?style=for-the-badge&logo=python&logoColor=black)

</div>

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
- **Static Files:** WhiteNoise

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

| Method         | Endpoint                  | Description                         | Auth Required      |
| :------------- | :------------------------ | :---------------------------------- | :----------------- |
| **Products**   |                           |                                     |                    |
| `GET`          | `/products/api/`          | Get a list of all products.         | No                 |
| `POST`         | `/products/api/`          | Create a new product.               | Yes (Seller)       |
| `GET`          | `/products/api/{slug}/`   | Get details of a specific product.  | No                 |
| `PUT / PATCH`  | `/products/api/{slug}/`   | Update a product.                   | Yes (Seller)       |
| `DELETE`       | `/products/api/{slug}/`   | Delete a product.                   | Yes (Seller)       |
| **Categories** |                           |                                     |                    |
| `GET`          | `/categories/api/`        | Get a list of all categories.       | No                 |
| `POST`         | `/categories/api/`        | Create a new category.              | Yes (Admin/Seller) |
| `GET`          | `/categories/api/{slug}/` | Get details of a specific category. | No                 |
| `PUT / PATCH`  | `/categories/api/{slug}/` | Update a category.                  | Yes (Admin/Seller) |
| `DELETE`       | `/categories/api/{slug}/` | Delete a category.                  | Yes (Admin/Seller) |
| **Reviews**    |                           |                                     |                    |
| `GET`          | `/reviews/api/`           | Get all reviews for a product.      | No                 |
| `POST`         | `/reviews/api/`           | Create a new review.                | Yes (Customer)     |
| `GET`          | `/reviews/api/{id}/`      | Get details of a specific review.   | No                 |
| `PUT / PATCH`  | `/reviews/api/{id}/`      | Update a review.                    | Yes (Customer)     |
| `DELETE`       | `/reviews/api/{id}/`      | Delete a review.                    | Yes (Customer)     |
| **Orders**     |                           |                                     |                    |
| `GET`          | `/orders/api/`            | Get a list of the user's orders.    | Yes (Customer)     |
| `POST`         | `/orders/api/`            | Create a new order.                 | Yes (Customer)     |
| `GET`          | `/orders/api/{id}/`       | Get details of a specific order.    | Yes (Customer)     |
| `PUT / PATCH`  | `/orders/api/{id}/`       | Update a specific order.            | Yes (Customer)     |
| `DELETE`       | `/orders/api/{id}/`       | Cancel/Delete an order.             | Yes (Customer)     |

_Note: The project also includes several template-based URLs for rendering HTML pages (e.g., `/register/`, `/login/`, `/products/`, `/categories/`, `/my-orders/`). The table above focuses exclusively on the RESTful API endpoints that handle JSON data._

curl -X DELETE http://127.0.0.1:8000/products/api/laptop-pro/ \
-H "Authorization: Token YOUR_SELLER_AUTH_TOKEN"

curl -X DELETE http://127.0.0.1:8000/categories/api/electronics/ \
-H "Authorization: Token YOUR_ADMIN_AUTH_TOKEN"

### ⚠️ Important Notes & Fixes

- **Categories**: The API path is `/categories/api/`. To activate it, you must uncomment the line `path("api/", include(api_router.urls)),` in your `categories/urls.py` file.
- **Orders**: The Orders API endpoints have been removed from this table as they do not exist in your provided `orders/urls.py` file. That file only contains template-based views.
- **Reviews**: The Reviews API endpoints have been added as they exist in your project structure but were missing from the original table. The correct path is `/reviews/api/reviews/`.

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
