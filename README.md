# Cryptographic API Implementation

## Introduction

In the modern digital era, data security and integrity are critical concerns for ensuring safe communication and data storage. Cryptographic techniques such as encryption, decryption, and hashing play a vital role in protecting sensitive information from unauthorized access and tampering.

This project presents the design and development of a **Cryptographic API** that performs key generation, encryption, and decryption using **symmetric (AES) and asymmetric (RSA) algorithms**, as well as hashing for data integrity checks. The API is implemented using **Flask** and leverages industry-standard cryptographic libraries such as **Cryptography**.

### Objectives:
1. Develop a secure and efficient key generation mechanism for cryptographic operations.
2. Implement encryption and decryption APIs for secure data transmission.
3. Create a hashing API for data integrity verification.
4. Ensure API accessibility and usability through structured endpoints.

---

## API Design and Functionality

The Cryptographic API provides endpoints for key generation, encryption, decryption, hashing, and hash verification.

### 1️⃣ Key Generation Endpoint
- **Endpoint:** `POST /generate-key`
- **Description:** Generates cryptographic keys based on the specified algorithm.
- **Request Body:**
  ```json
  {
    "key_type": "AES",
    "key_size": 256
  }
  ```
- **Response:**
  ```json
  {
    "key_id": "12345",
    "key_value": "base64-encoded-key"
  }
  ```

### 2️⃣ Encryption Endpoint
- **Endpoint:** `POST /encrypt`
- **Description:** Encrypts plaintext messages using the specified key.
- **Request Body:**
  ```json
  {
    "key_id": "12345",
    "plaintext": "message-to-encrypt",
    "algorithm": "AES"
  }
  ```
- **Response:**
  ```json
  {
    "ciphertext": "base64-encoded-ciphertext"
  }
  ```

### 3️⃣ Decryption Endpoint
- **Endpoint:** `POST /decrypt`
- **Description:** Decrypts encrypted messages back into plaintext.
- **Request Body:**
  ```json
  {
    "key_id": "12345",
    "ciphertext": "base64-encoded-ciphertext",
    "algorithm": "AES"
  }
  ```
- **Response:**
  ```json
  {
    "plaintext": "original-message"
  }
  ```

### 4️⃣ Hash Generation Endpoint
- **Endpoint:** `POST /generate-hash`
- **Description:** Generates a hash for a given data input.
- **Request Body:**
  ```json
  {
    "data": "some-important-data",
    "algorithm": "SHA256"
  }
  ```
- **Response:**
  ```json
  {
    "hash": "generated-hash-value"
  }
  ```

### 5️⃣ Hash Verification Endpoint
- **Endpoint:** `POST /verify-hash`
- **Description:** Verifies if a given hash matches the original data.
- **Request Body:**
  ```json
  {
    "data": "some-important-data",
    "hash": "generated-hash-value",
    "algorithm": "SHA256"
  }
  ```
- **Response:**
  ```json
  {
    "match": true
  }
  ```

---

## Installation and Usage

### Running the API Locally

For development or testing purposes, you can still run the API locally.

1. Clone the repository:
    ```sh
    git clone https://github.com/Team-ByteFort/Cryptographic-API-Implementation.git
    cd Cryptographic-API-Implementation
    ```

2. Set up a virtual environment and install dependencies:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Run the API:
    ```sh
    python main.py
    ```

### Testing with cURL

To test the API locally using cURL, you can send a request like:

```sh
curl -X POST http://127.0.0.1:5000/generate-key -H "Content-Type: application/json" -d '{"key_type": "AES", "key_size": 256}'


