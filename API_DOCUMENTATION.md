# Payment Gateway API Documentation

This document provides details for all available API endpoints.

## Table of Contents
1.  [Authentication Flow](#authentication-flow)
2.  [User Account Endpoints](#user-account-endpoints)
    *   [`POST /api/auth/signup`](#post-authsignup)
    *   [`POST /api/auth/signin`](#post-authsignin)
    *   [`POST /api/auth/refresh`](#post-authrefresh)
3.  [OTP Endpoints](#otp-endpoints)
    *   [`POST /api/otp/generate-otp`](#post-otpgenerate-otp)
    *   [`POST /api/otp/verify-otp`](#post-otpverify-otp)
4.  [Payment Endpoints](#payment-endpoints)
    *   [`POST /api/payment/create-order`](#post-paymentcreate-order)
    *   [`POST /api/payment/verify-payment`](#post-paymentverify-payment)

---

## Authentication Flow

This API uses JSON Web Tokens (JWT) for authenticating users.

1.  **Obtain Tokens:**
    *   A new user registers via `POST /api/auth/signup`.
    *   The user signs in via `POST /api/auth/signin` with their credentials (email/phone and password).
    *   Upon successful signin, the API returns an `access_token` and a `refresh_token`.

2.  **Using Access Token:**
    *   For all protected endpoints, the client must include the `access_token` in the `Authorization` header with the `Bearer` scheme.
    *   Example: `Authorization: Bearer <your_access_token>`

3.  **Refreshing Access Token:**
    *   Access tokens have a limited lifetime. When an access token expires, the client should use the `refresh_token` to obtain a new access token.
    *   This is done by making a `POST` request to `/api/auth/refresh` with the `refresh_token` in the `Authorization: Bearer <your_refresh_token>` header.
    *   A new `access_token` will be returned if the refresh token is valid.

4.  **JWT Error Handling:**
    *   If an access token is missing, invalid, or expired, protected endpoints will typically return a `401 Unauthorized` or `422 Unprocessable Entity` error (see specific endpoint documentation for details).
    *   The error response body will usually be JSON with a `msg` field explaining the error, e.g., `{"msg": "Missing Authorization Header"}` or `{"msg": "Token has expired"}`.

---

## User Account Endpoints

### `POST /api/auth/signup`
Registers a new user in the system.

*   **HTTP Method:** `POST`
*   **URL Path:** `/api/auth/signup`
*   **Description:** Creates a new user account with the provided email, phone number, and password.
*   **Request Body (JSON):**
    *   `email` (string, required): User's email address. Must be unique.
    *   `phone_number` (string, required): User's phone number. Must be unique.
    *   `password` (string, required): User's desired password.
*   **Example Request Body:**
    ```json
    {
        "email": "user@example.com",
        "phone_number": "1234567890",
        "password": "securepassword123"
    }
    ```
*   **Success Response:**
    *   **Code:** `201 Created`
    *   **Body:**
        ```json
        {
            "message": "User created successfully",
            "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
        }
        ```
*   **Error Responses:**
    *   **Code:** `400 Bad Request`
        *   **Body (Missing Fields):**
            ```json
            {
                "error": "Missing required fields"
            }
            ```
    *   **Code:** `409 Conflict`
        *   **Body (Email Exists):**
            ```json
            {
                "error": "Email already exists"
            }
            ```
        *   **Body (Phone Number Exists):**
            ```json
            {
                "error": "Phone number already exists"
            }
            ```
    *   **Code:** `500 Internal Server Error`
        *   **Body (Database Error):**
            ```json
            {
                "error": "Database integrity error"
            }
            ```
*   **Authentication:** None required.

---

### `POST /api/auth/signin`
Logs in an existing user.

*   **HTTP Method:** `POST`
*   **URL Path:** `/api/auth/signin`
*   **Description:** Authenticates a user based on their identifier (email or phone number) and password.
*   **Request Body (JSON):**
    *   `identifier` (string, required): User's email address OR phone number.
    *   `password` (string, required): User's password.
*   **Example Request Body:**
    ```json
    {
        "identifier": "user@example.com",
        "password": "securepassword123"
    }
    ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:**
        ```json
        {
            "message": "Login successful",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
        ```
*   **Error Responses:**
    *   **Code:** `400 Bad Request`
        *   **Body (Missing Fields):**
            ```json
            {
                "error": "Missing identifier or password"
            }
            ```
    *   **Code:** `401 Unauthorized`
        *   **Body (Invalid Credentials):**
            ```json
            {
                "error": "Invalid credentials"
            }
            ```
*   **Authentication:** None required.

---

### `POST /api/auth/refresh`
Refreshes an expired access token.

*   **HTTP Method:** `POST`
*   **URL Path:** `/api/auth/refresh`
*   **Description:** Takes a valid refresh token and returns a new access token.
*   **Authentication:** JWT Refresh Token required.
    *   Header: `Authorization: Bearer <refresh_token>`
*   **Request Body:** None.
*   **Example Request (Header):**
    ```
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9... (your refresh token)
    ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:**
        ```json
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
        ```
*   **Error Responses:**
    *   **Code:** `401 Unauthorized` (e.g., if refresh token is missing or invalid)
        *   **Body:** `{"msg": "Missing Authorization Header"}` or `{"msg": "Invalid token"}`
    *   **Code:** `422 Unprocessable Entity` (e.g., if token is not a refresh token)
        *   **Body:** `{"msg": "Only refresh tokens are allowed"}`

---

### `GET /api/auth/dashboard`
Retrieves user details and their payment history.

*   **HTTP Method:** `GET`
*   **URL Path:** `/api/auth/dashboard`
*   **Description:** Fetches the authenticated user's profile information and a list of all their payments. User is identified by the JWT access token.
*   **Authentication:** JWT Access Token required.
    *   Header: `Authorization: Bearer <access_token>`
*   **Request Body:** None.
*   **Example Request (Header):**
    ```
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9... (your access token)
    ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:**
        ```json
        {
            "user_details": {
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "email": "user@example.com",
                "phone_number": "1234567890"
            },
            "payment_history": [
                {
                    "payment_id": "p1a2b3c4-d5e6-f789-0123-456789abcdef",
                    "amount": 150.00,
                    "status": "completed",
                    "razorpay_payment_id": "pay_EKwxwAgItmmXdp",
                    "razorpay_order_id": "order_EKwxwAgItmmXdp",
                    "created_at": "2023-01-15T10:30:00Z",
                    "updated_at": "2023-01-15T10:31:00Z"
                },
                {
                    "payment_id": "q9r8s7t6-u5v4-w3x2-y1z0-fedcba987654",
                    "amount": 75.50,
                    "status": "pending",
                    "razorpay_payment_id": null,
                    "razorpay_order_id": "order_FGhijkLmNopQrs",
                    "created_at": "2023-01-16T12:00:00Z",
                    "updated_at": "2023-01-16T12:00:00Z"
                }
            ]
        }
        ```
*   **Error Responses:**
    *   **Code:** `401 Unauthorized` (e.g., if token is missing, invalid, or expired)
        *   **Body:** `{"msg": "Missing Authorization Header"}` or `{"msg": "Token has expired"}`
    *   **Code:** `404 Not Found`
        *   **Body (User identified by token not found):**
            ```json
            {
                "error": "User not found"
            }
            ```
*   **Authentication:** JWT Access Token required.

---

## OTP Endpoints

### `POST /api/otp/generate-otp`
Generates and sends an OTP to the user.

*   **HTTP Method:** `POST`
*   **URL Path:** `/api/otp/generate-otp`
*   **Description:** Creates a One-Time Password (OTP) for a specified user and purpose, and sends it via the chosen delivery method (email/SMS - currently placeholder).
*   **Request Body (JSON):**
    *   `identifier` (string, required): User's email address OR phone number (E.164 format for SMS).
    *   `type` (string, required): The purpose of the OTP (e.g., "registration", "password_reset", "payment_confirmation"). This is used for namespacing OTPs in Redis.
    *   `delivery_method` (string, required): How to send the OTP. Must be "email" or "sms".
*   **Example Request Body:**
    ```json
    {
        "identifier": "user@example.com",
        "type": "registration",
        "delivery_method": "email"
    }
    ```
    ```json
    {
        "identifier": "+12345678900",
        "type": "password_reset",
        "delivery_method": "sms"
    }
    ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body (Email):**
        ```json
        {
            "message": "OTP sent successfully to your email."
        }
        ```
    *   **Body (SMS):**
        ```json
        {
            "message": "OTP sent successfully to your SMS to phone number."
        }
        ```
        *(Note: OTPs are now actually sent. `otp_id` is not returned as OTPs are managed in Redis.)*
*   **Error Responses:**
    *   **Code:** `400 Bad Request`
        *   **Body (Missing Fields):**
            ```json
            {
                "error": "Missing identifier (email/phone), type, or delivery_method"
            }
            ```
        *   **Body (Invalid Delivery Method):**
            ```json
            {
                "error": "Invalid delivery_method. Must be 'email' or 'sms'."
            }
            ```
        *   **Body (User Missing Email/Phone for chosen method):**
            ```json
            {
                "error": "User does not have an email address on file." // or "User does not have a phone number on file."
            }
            ```
    *   **Code:** `404 Not Found`
        *   **Body (User Not Found):**
            ```json
            {
                "error": "User not found"
            }
            ```
    *   **Code:** `500 Internal Server Error`
        *   **Body (Failed to Send OTP):**
            ```json
            {
                "error": "Failed to send OTP email. Please try again later." // or "Failed to send OTP SMS..."
            }
            ```
        *   **Body (Failed to Store OTP):**
             ```json
            {
                "error": "Failed to store OTP. Please try again."
            }
            ```
*   **Authentication:** Public endpoint. Designed for scenarios like registration or password reset where the user may not be logged in.

---

### `POST /api/otp/verify-otp`
Verifies an OTP provided by the user.

*   **HTTP Method:** `POST`
*   **URL Path:** `/api/otp/verify-otp`
*   **Description:** Checks if the provided OTP code is valid for the given user and type, and has not expired.
*   **Request Body (JSON):**
    *   `user_id` (string, UUID, required): The ID of the user for whom the OTP was generated.
        *(Note: This `user_id` is typically obtained from the response of a preceding step, like user registration, or known if the user is trying to perform a post-login verification.)*
    *   `otp_code` (string, required): The OTP code entered by the user.
    *   `type` (string, required): The purpose of the OTP (must match the type during generation, e.g., "registration", "password_reset").
*   **Example Request Body:**
    ```json
    {
        "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "otp_code": "123456",
        "type": "registration"
    }
    ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body:**
        ```json
        {
            "message": "OTP verified successfully"
        }
        ```
*   **Error Responses:**
    *   **Code:** `400 Bad Request`
        *   **Body (Missing Fields):**
            ```json
            {
                "error": "Missing user_id, otp_code, or type"
            }
            ```
        *   **Body (Invalid or Expired OTP):**
            ```json
            {
                "error": "Invalid or expired OTP"
            }
            ```
            *(Note: This single message now covers cases where the OTP is not found, does not match, or has expired in Redis.)*
*   **Authentication:** Public endpoint.

---

## Payment Endpoints

### `POST /api/payment/create-order`
Creates a payment order with Razorpay for the authenticated user.

*   **HTTP Method:** `POST`
*   **URL Path:** `/api/payment/create-order`
*   **Description:** Initializes a payment by creating an order with Razorpay for a fixed amount (currently 150 INR). The user is identified by their JWT access token.
*   **Authentication:** JWT Access Token required.
    *   Header: `Authorization: Bearer <access_token>`
*   **Request Body:** None. (Amount is fixed on the server-side for this example).
*   **Example Request (Header):**
    ```
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9... (your access token)
    ```
*   **Success Response:**
    *   **Code:** `201 Created`
    *   **Body:**
        ```json
        {
            "message": "Order created successfully",
            "order_id": "order_EKwxwAgItmmXdp", // Razorpay Order ID
            "amount": 15000, // Amount in paise (e.g., 150.00 INR)
            "currency": "INR",
            "key_id": "rzp_test_YOUR_KEY_ID", // Your Razorpay Key ID
            "payment_db_id": "p1a2b3c4-d5e6-f789-0123-456789abcdef" // Internal DB ID for the payment record
        }
        ```
*   **Error Responses:**
    *   **Code:** `401 Unauthorized` (e.g., if token is missing, invalid, or expired)
        *   **Body:** `{"msg": "Missing Authorization Header"}` or `{"msg": "Token has expired"}`
    *   **Code:** `404 Not Found`
        *   **Body (User identified by token not found):**
            ```json
            {
                "error": "User not found"
            }
            ```
    *   **Code:** `500 Internal Server Error`
        *   **Body (Razorpay Client Not Initialized):**
            ```json
            {
                "error": "Razorpay client not initialized or misconfigured. Check server configuration."
            }
            ```
        *   **Body (Razorpay Order Creation Failed):**
            ```json
            {
                "error": "Razorpay order creation failed: <specific error from Razorpay>"
            }
            ```
        *   **Body (Database Error):**
            ```json
            {
                "error": "Database error after creating Razorpay order: <specific db error>"
            }
            ```
*   **Authentication:** JWT Access Token required.

---

### `POST /api/payment/verify-payment`
Verifies a payment with Razorpay for the authenticated user.

*   **HTTP Method:** `POST`
*   **URL Path:** `/api/payment/verify-payment`
*   **Description:** Verifies the signature of a completed Razorpay payment to confirm its authenticity and updates the payment status in the database. The user is identified by their JWT access token, and the payment must belong to this user.
*   **Authentication:** JWT Access Token required.
    *   Header: `Authorization: Bearer <access_token>`
*   **Request Body (JSON):**
    *   `razorpay_payment_id` (string, required): The payment ID from Razorpay.
    *   `razorpay_order_id` (string, required): The order ID from Razorpay (should match the one from `/create-order`).
    *   `razorpay_signature` (string, required): The signature generated by Razorpay on successful payment.
*   **Example Request (Header and Body):**
    *   Header:
        ```
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9... (your access token)
        ```
    *   Body:
        ```json
        {
            "razorpay_payment_id": "pay_EKwxwAgItmmXdp",
            "razorpay_order_id": "order_EKwxwAgItmmXdp",
            "razorpay_signature": "generated_razorpay_signature_string"
        }
        ```
*   **Success Response:**
    *   **Code:** `200 OK`
    *   **Body (Verification Successful):**
        ```json
        {
            "message": "Payment verified successfully",
            "payment_id": "p1a2b3c4-d5e6-f789-0123-456789abcdef" // Internal DB ID
        }
        ```
    *   **Body (Already Verified):**
        ```json
        {
            "message": "Payment already verified and completed"
        }
        ```
*   **Error Responses:**
    *   **Code:** `400 Bad Request`
        *   **Body (Missing Fields):**
            ```json
            {
                "error": "Missing Razorpay payment details for verification"
            }
            ```
        *   **Body (Invalid Signature):**
            ```json
            {
                "error": "Invalid payment signature: <specific error from Razorpay>"
            }
            ```
    *   **Code:** `401 Unauthorized` (e.g., if token is missing, invalid, or expired)
        *   **Body:** `{"msg": "Missing Authorization Header"}` or `{"msg": "Token has expired"}`
    *   **Code:** `403 Forbidden`
        *   **Body (User attempting to verify payment not belonging to them):**
            ```json
            {
                "error": "Unauthorized to verify this payment."
            }
            ```
    *   **Code:** `404 Not Found`
        *   **Body (Payment Record Not Found):**
            ```json
            {
                "error": "Payment record not found for this order_id. Please contact support."
            }
            ```
    *   **Code:** `500 Internal Server Error`
        *   **Body (Razorpay Client Not Initialized):**
            ```json
            {
                "error": "Razorpay client not initialized or misconfigured. Check server configuration."
            }
            ```
        *   **Body (Error during signature verification - other than invalid sig):**
             ```json
            {
                "error": "Error during signature verification: <specific error>"
            }
            ```
        *   **Body (Database Error after Verification):**
            ```json
            {
                "error": "Database error after payment verification: <specific db error>"
            }
            ```
*   **Authentication:** JWT Access Token required.

---
This concludes the API documentation.
