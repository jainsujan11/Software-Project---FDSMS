# FOOD Delivery Software Management System

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [API Documentation](#api-documentation)
6. [Contributing](#contributing)

## Introduction
The FOOD Delivery Software Management System is a comprehensive solution designed to streamline the process of managing food delivery services. This system helps restaurants, delivery personnel, and customers by providing an efficient and user-friendly platform to handle orders, track deliveries, and manage customer feedback.

## Features
- **Order Management**: Efficiently manage incoming orders from customers.
- **Delivery Tracking**: Real-time tracking of delivery personnel and orders.
- **Customer Management**: Store and manage customer details and order history.
- **Feedback System**: Collect and manage customer feedback to improve services.

## Installation
### Prerequisites
- MongoDB

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Software-Project---FDSMS
    ```
2. Navigate to the project directory:
    ```bash
    cd Software-Project---FDSMS
    ```
3. Set up the database:
    - Ensure you have a MongoDB account.
    - Create a new database for the project in the following structure.
    - After creating database connect to it by changing line 19 of app.py with the line associated with your mongoDB account.

4. Install dependencies:
    ```bash
    pip install flask
    pip install pymongo
    pip install datetime
    pip install bson
    ```

5. Start the server:
    - Install the extension Live Server in vs code(Ritwick Dey) and the use Go Live button to start the server and then run the code

## Usage
### Admin
- Log in to the admin panel.
- Manage restaurants, delivery personnel, and orders.

### Delivery Personnel
- Log in to the delivery app.
- View assigned orders and delivery details.
- Update delivery status in real-time.

### Customers
- Browse the restaurant menu and place orders.
- Track order status and delivery in real-time.
- Provide feedback and rate the service.

### Restaurants
- Browse current orders and accept/reject them.
- Add items to menu.
- Mark order as out for delivery.
For more detailed usage refer to the [UML Use Case Diagram](https://github.com/jainsujan11/Software-Project---FDSMS/blob/main/UML_Use_Case_Diagram.pdf)

## Software Documentation
For detailed API documentation, refer to the [SRS Document](https://github.com/jainsujan11/Software-Project---FDSMS/blob/main/SRS_Document.pdf).

## Contributing
We welcome contributions to the FOOD Delivery Software Management System. Please follow these steps:
1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Create a pull request.
