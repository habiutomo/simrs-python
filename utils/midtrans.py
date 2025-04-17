"""
Midtrans payment integration utilities for SIMRS
"""
import os
import json
import base64
import requests
from datetime import datetime
from flask import url_for

# Midtrans API Configuration
MIDTRANS_SERVER_KEY = os.environ.get('MIDTRANS_SERVER_KEY')
MIDTRANS_BASE_URL = 'https://api.sandbox.midtrans.com/v2'  # Use 'https://api.midtrans.com/v2' for production

def generate_order_id():
    """Generate a unique order ID based on timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"SIMRS-BILL-{timestamp}"

def create_payment_url(bill_id, patient_name, amount, items=None, description=None):
    """
    Create a Midtrans Snap payment URL
    
    Args:
        bill_id (str): The billing ID
        patient_name (str): Patient's name
        amount (float): Total amount to pay
        items (list): List of items in the bill (optional)
        description (str): Description of the payment (optional)
        
    Returns:
        dict: Response from Midtrans containing payment URL and token
    """
    if not MIDTRANS_SERVER_KEY:
        raise ValueError("MIDTRANS_SERVER_KEY is not set")
    
    # Ensure amount is an integer (Midtrans requires amount in lowest currency unit)
    amount = int(amount)
    
    # Generate order ID if not provided
    order_id = generate_order_id()
    
    # Prepare transaction details
    transaction_details = {
        "order_id": order_id,
        "gross_amount": amount
    }
    
    # Prepare customer details
    customer_details = {
        "first_name": patient_name,
        "email": "patient@example.com",  # In a real app, use the patient's actual email
        "phone": "08111222333"  # In a real app, use the patient's actual phone number
    }
    
    # Prepare item details
    item_details = []
    if items:
        item_details = items
    else:
        item_details = [{
            "id": bill_id,
            "price": amount,
            "quantity": 1,
            "name": description or f"Payment for Bill #{bill_id}"
        }]
    
    # Create the request payload
    payload = {
        "transaction_details": transaction_details,
        "customer_details": customer_details,
        "item_details": item_details,
        "callbacks": {
            "finish": url_for('main_bp.payment_finish', _external=True),
            "error": url_for('main_bp.payment_error', _external=True),
            "cancel": url_for('main_bp.payment_cancel', _external=True)
        }
    }
    
    # Set up the request headers with authentication
    auth_string = base64.b64encode(f"{MIDTRANS_SERVER_KEY}:".encode()).decode()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Basic {auth_string}'
    }
    
    # Make the request to Midtrans Snap API
    response = requests.post(
        f"{MIDTRANS_BASE_URL}/snap/v1/transactions",
        headers=headers,
        data=json.dumps(payload)
    )
    
    # Process the response
    if response.status_code == 201:
        return response.json()
    else:
        # Handle error
        error_message = response.json().get('error_messages', ['Unknown error'])[0]
        raise Exception(f"Failed to create payment: {error_message}")

def check_transaction_status(order_id):
    """
    Check the status of a transaction
    
    Args:
        order_id (str): The order ID to check
        
    Returns:
        dict: Transaction status details
    """
    if not MIDTRANS_SERVER_KEY:
        raise ValueError("MIDTRANS_SERVER_KEY is not set")
    
    # Set up the request headers with authentication
    auth_string = base64.b64encode(f"{MIDTRANS_SERVER_KEY}:".encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {auth_string}'
    }
    
    # Make the request to Midtrans API
    response = requests.get(
        f"{MIDTRANS_BASE_URL}/{order_id}/status",
        headers=headers
    )
    
    # Process the response
    if response.status_code == 200:
        return response.json()
    else:
        # Handle error
        error_message = response.json().get('error_messages', ['Unknown error'])[0]
        raise Exception(f"Failed to check transaction status: {error_message}")

def handle_notification(notification_data):
    """
    Handle Midtrans payment notification webhook
    
    Args:
        notification_data (dict): Notification data from Midtrans
        
    Returns:
        dict: Processed notification data with transaction status
    """
    transaction_status = notification_data.get('transaction_status')
    order_id = notification_data.get('order_id')
    
    # Verify the transaction status with Midtrans
    status_response = check_transaction_status(order_id)
    
    # Make sure the status from notification matches the status from API
    if status_response.get('transaction_status') != transaction_status:
        raise ValueError("Transaction status mismatch between notification and API")
    
    # Process based on transaction status
    if transaction_status == 'capture' or transaction_status == 'settlement':
        # Payment successful
        return {
            'status': 'success',
            'order_id': order_id,
            'transaction_id': notification_data.get('transaction_id'),
            'amount': notification_data.get('gross_amount'),
            'payment_type': notification_data.get('payment_type')
        }
    elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
        # Payment failed
        return {
            'status': 'failed',
            'order_id': order_id,
            'reason': transaction_status
        }
    elif transaction_status == 'pending':
        # Payment pending
        return {
            'status': 'pending',
            'order_id': order_id,
            'transaction_id': notification_data.get('transaction_id')
        }
    else:
        # Unknown status
        return {
            'status': 'unknown',
            'order_id': order_id,
            'transaction_status': transaction_status
        }