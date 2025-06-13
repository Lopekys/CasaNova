# CasaNova — Django Furniture Store

**CasaNova** is e-commerce web application for selling furniture, built with Django.  
It features a product catalog, shopping cart, checkout, blog, testimonials, newsletter subscription, and a contact form.

---

## Requirements

- Python 3.10  
- pip

---

## Quickstart (Local Installation)

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Lopekys/CasaNova
    cd CasaNova
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate      # On Linux/Mac: source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **No migrations needed:**  
   The `db.sqlite3` file (database) is already present in the repository.

5. **Superuser is already created:**  
   - **Login:** `admin`  
   - **Password:** `FpBcZg2B.QBZBaR`

6. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Open in your browser:**  
   - Storefront: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Notes

- All products, blog posts, testimonials, etc. can be managed via the Django admin panel.
- The default SQLite database (`db.sqlite3`) is included with the project.
- Uploaded images are stored in the `media/` directory.
