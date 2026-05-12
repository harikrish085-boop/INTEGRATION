# MES Integration API Clients

A collection of Python scripts for integrating with Manufacturing Execution System (MES) APIs. These clients fetch real-time data from MES endpoints via HTTP and HTTPS protocols with optional API key authentication.

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Scripts](#scripts)
* [Installation](#installation)
* [Usage](#usage)
* [Requirements](#requirements)
* [Configuration](#configuration)
* [Troubleshooting](#troubleshooting)

## Introduction

This project provides lightweight Python clients to connect to MES APIs and retrieve manufacturing data in real-time. The scripts support both secure (HTTPS) and non-secure (HTTP) connections, with configurable polling intervals.

## Features

* **HTTP and HTTPS Support**: Connect to MES endpoints using either protocol
* **API Key Authentication**: Secure connections with API key headers
* **Real-time Data Polling**: Continuous data retrieval with configurable intervals
* **JSON Response Handling**: Automatic parsing and display of API responses
* **Dynamic Folder Parameters**: Support for dynamic folder/tag-based queries

## Scripts

### 1. mesget.py
**Purpose**: Basic HTTP client for local MES API endpoints

**Description**: Connects to a local HTTP endpoint and polls for MES data every 5 seconds. Ideal for development and testing environments.

**Endpoint**: `http://localhost:8088/system/webdev/samplequickstart/MESIntegration/mesapi`

**Features**:
- Simple HTTP GET requests
- Local endpoint access
- 5-second polling interval
- JSON response output

### 2. mesgethttps_api.py
**Purpose**: Secure HTTPS client with API key authentication

**Description**: Connects to a secure HTTPS endpoint with API key authentication. Disables SSL certificate warnings for self-signed certificates. Suitable for production environments with security requirements.

**Endpoint**: `https://localhost:8043/system/webdev/samplequickstart/MESIntegration/mesapikey`

**Features**:
- HTTPS encrypted connection
- API key authentication via headers
- SSL warning suppression for self-signed certs
- 5-second polling interval
- HTTP status code display

### 3. mesgethttps_api_DynamicFolder.py
**Purpose**: Secure HTTPS client with dynamic folder parameter support

**Description**: Connects to a secure HTTPS endpoint with dynamic folder/tag parameters. Allows querying specific data sets or tags within the MES system.

**Endpoint**: `https://localhost:8043/system/webdev/samplequickstart/MESIntegration/mesapikey?folder=[Sample_Tags]Random`

**Features**:
- HTTPS encrypted connection
- API key authentication via headers
- Dynamic folder parameter support
- SSL warning suppression
- 5-second polling interval

## Installation

### Prerequisites
- Python 3.6+
- pip (Python package installer)

### Steps

1. Clone or download this repository:
```bash
git clone https://github.com/username/MESINTEGRATION.git
cd MESINTEGRATION
```

2. Install required dependencies:
```bash
pip install requests urllib3
```

## Usage

### Run Basic HTTP Client
```bash
python mesget.py
```

### Run Secure HTTPS Client
```bash
python mesgethttps_api.py
```

### Run Dynamic Folder Query
```bash
python mesgethttps_api_DynamicFolder.py
```

Each script will continuously poll the MES endpoint every 5 seconds and display responses in the console.

## Requirements

- **Python 3.6+**
- **requests**: HTTP library for making API calls
- **urllib3**: HTTP client library (for SSL handling)

## Configuration

### Updating Endpoints
Edit the `url` variable in each script to point to your MES server:
```python
url = "https://your-mes-server:8043/system/webdev/samplequickstart/MESIntegration/mesapikey"
```

### Updating API Key
Modify the `x-api-key` header value:
```python
headers = {
    "x-api-key": "YOUR_API_KEY_HERE"
}
```

### Adjusting Polling Interval
Change the `time.sleep()` value (in seconds):
```python
time.sleep(5)  # Change 5 to your desired interval
```
llll
### Dynamic Folder Parameters
Modify the folder parameter in the URL:
```python
url = "https://localhost:8043/system/webdev/samplequickstart/MESIntegration/mesapikey?folder=[YOUR_TAG]YOUR_FOLDER"
```

## Troubleshooting

### SSL Certificate Errors
If you encounter SSL errors with HTTPS endpoints using self-signed certificates, the scripts automatically disable SSL warnings. If issues persist, ensure `verify=False` is set in the requests call.

### Connection Refused
- Verify the MES server is running
- Check the endpoint URL and port are correct
- Ensure firewall rules allow connections to the MES port

### Authentication Errors (401/403)
- Verify the API key is correct
- Check that the `x-api-key` header is properly formatted
- Ensure the API key has appropriate permissions

### No Response or Timeout
- Check network connectivity to the MES server
- Verify the endpoint is accessible from your machine
- Increase the timeout if dealing with slow networks