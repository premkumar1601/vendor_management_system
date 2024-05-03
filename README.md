# **Vendor Management System with Performance Metrics**

The Vendor Management System is a Django application designed to manage vendor information, track purchase orders, and evaluate vendor performance over time.

### Features

* **Vendor Profile Management** : Create, update, and delete vendor profiles.
* **Purchase Order Tracking** : Capture details of each purchase order and calculate various performance metrics.
* **Historical Performance Tracking** : Optionally store historical data on vendor performance for trend analysis.
* **API Endpoints** : Expose RESTful APIs for interacting with vendor profiles, purchase orders, and performance metrics.

### Project Setup

* Ensure you have Python 3.11 installed on your system.
* Clone the Repository
* #Navigate to project directory

  ```
  cd vendor_management_system
  ```
* #create a virtual environment

  ```
  python3 -m venv myvenv
  ```
* #activate the virtual environment

  ```
  source myvenv/bin/activate
  ```
* #Install required python packages mention in requirements file

  ```
  pip install -r requirements.txt
  ```
* #Create a superuser account with administrative privileges.

  ```
  python manage.py createsuperuser
  ```
* #Create database migration files based on changes made to the models.

  ```
  python manage.py makemigrations
  ```
* #Apply database migrations to update the database schema.

  ```
  python manage.py migrate
  ```
* #Start the Django development server to run the application locally.

  ```
  python manage.py runserver
  ```

### API Endpoints

Here's the published Postman collection containing the API endpoints for our Vendor Management System. You can import this collection into your Postman workspace to access and test the API endpoints easily. In order to test the API endpoints authentication token has to be generated.

The below command sends a POST request to the token endpoint (`/api/token/`) of your local development server (`http://localhost:8000`). It includes the username and password in the request body as JSON data. If the credentials are correct, the server will respond with a JSON object containing the authentication token.

```
curl -X POST http://localhost:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{"username": "your_username", "password": "your_password"}'

```

Replace your_authentication_token with the actual token value obtained, then execute the command to include the authentication token in the headers of your API request.

* [Vendor Profile API](https://documenter.getpostman.com/view/34696503/2sA3JGdiAz)
* [Purchase Orders API](https://documenter.getpostman.com/view/34696503/2sA3JGdiAy)

###### Vendor Profile Management :

* POST /api/vendors/: Create a new vendor.
* GET /api/vendors/: List all vendors.
* GET /api/vendors/{vendor_id}/: Retrieve details of a specific vendor.
* PUT /api/vendors/{vendor_id}/: Update a vendor's details.
* DELETE /api/vendors/{vendor_id}/: Delete a vendor.
* GET /api/vendors/{vendor_id}/performance/: Retrieve performance metrics for a vendor.

###### Purchase Order Management :

* POST /api/purchase_orders/: Create a new purchase order.
* GET /api/purchase_orders/: List all purchase orders.
* GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
* PUT /api/purchase_orders/{po_id}/: Update a purchase order.
* DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
* POST /api/purchase_orders/{po_id}/acknowledge/: Acknowledge a purchase order.

### Django Admin Features

Navigate to the Django admin interface at `http://localhost:8000/admin/` and Log in with the superuser account created earlier.

###### Vendors

* Access the "Vendors" section to view and manage vendor details.
* Metrics such as on-time delivery rate, quality rating average, response time, and fulfilment are displayed for each vendors and additional fields are accessed through related models.

###### Purchase Orders

* In the Django admin interface, navigate to the "Purchase Orders" section.
* Here, you can view a list of purchase orders, vendor, issue date, acknowledgement date and status of each purchase orders.
* Utilize the built-in filtering capabilities to filter purchase orders based on various criteria such as vendor and status.
* Clicking on a specific purchase order will display its detailed information.
