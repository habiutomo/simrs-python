"""
BPJS Kesehatan API Integration for SIMRS
This module provides integration with BPJS Kesehatan API services.
"""
import os
import base64
import hashlib
import hmac
import json
import time
from datetime import datetime
import requests
from flask import current_app

# BPJS API Configuration
BPJS_CONS_ID = os.environ.get("BPJS_CONS_ID")
BPJS_SECRET_KEY = os.environ.get("BPJS_SECRET_KEY")
BPJS_USER_KEY = os.environ.get("BPJS_USER_KEY")

# BPJS API URLs
BPJS_BASE_URL = "https://apijkn-dev.bpjs-kesehatan.go.id"
VCLAIM_BASE_URL = f"{BPJS_BASE_URL}/vclaim-rest-dev"
PCARE_BASE_URL = f"{BPJS_BASE_URL}/pcare-rest-dev"
APLICARE_BASE_URL = f"{BPJS_BASE_URL}/aplicaresws"

class BPJSIntegration:
    """BPJS Kesehatan Integration class"""
    
    def __init__(self, 
                 cons_id=BPJS_CONS_ID, 
                 secret_key=BPJS_SECRET_KEY, 
                 user_key=BPJS_USER_KEY,
                 service_type="vclaim"):
        """
        Initialize BPJS Integration
        
        Args:
            cons_id (str): BPJS Consumer ID
            secret_key (str): BPJS Secret Key
            user_key (str): BPJS User Key
            service_type (str): Type of BPJS service ('vclaim', 'pcare', 'aplicare')
        """
        self.cons_id = cons_id
        self.secret_key = secret_key
        self.user_key = user_key
        
        # Set appropriate base URL based on service type
        if service_type == "vclaim":
            self.base_url = VCLAIM_BASE_URL
        elif service_type == "pcare":
            self.base_url = PCARE_BASE_URL
        elif service_type == "aplicare":
            self.base_url = APLICARE_BASE_URL
        else:
            raise ValueError(f"Invalid service type: {service_type}")
            
        # Validate credentials
        if not all([self.cons_id, self.secret_key, self.user_key]):
            current_app.logger.warning("BPJS API credentials are not fully configured.")
    
    def _generate_signature(self, timestamp):
        """
        Generate BPJS signature for request authentication
        
        Args:
            timestamp (str): Current timestamp in format yyyyMMddHHmmss
            
        Returns:
            str: Base64 encoded signature
        """
        message = f"{self.cons_id}&{timestamp}"
        hmac_signature = hmac.new(
            bytes(self.secret_key, 'utf-8'),
            bytes(message, 'utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(hmac_signature).decode('utf-8')
    
    def _construct_headers(self):
        """
        Construct headers for BPJS API requests
        
        Returns:
            dict: Headers including timestamp, signature, and user_key
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        signature = self._generate_signature(timestamp)
        
        headers = {
            'X-cons-id': self.cons_id,
            'X-timestamp': timestamp,
            'X-signature': signature,
            'user_key': self.user_key,
            'Content-Type': 'application/json'
        }
        return headers
    
    def _make_request(self, endpoint, method='GET', data=None):
        """
        Make a request to BPJS API endpoint
        
        Args:
            endpoint (str): API endpoint path
            method (str): HTTP method (GET, POST, PUT, DELETE)
            data (dict, optional): Request data for POST/PUT methods
            
        Returns:
            dict: Response data from BPJS API
        """
        url = f"{self.base_url}/{endpoint}"
        headers = self._construct_headers()
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=headers, 
                                        data=json.dumps(data) if data else None, 
                                        timeout=30)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, 
                                       data=json.dumps(data) if data else None, 
                                       timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"Invalid HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            current_app.logger.error(f"BPJS API request error: {str(e)}")
            return {"metaData": {"code": "500", "message": str(e)}}
    
    # VClaim API Implementations
    def check_peserta_by_noka(self, no_kartu, tgl_pelayanan=None):
        """
        Check/verify BPJS patient by card number (Nomor Kartu)
        
        Args:
            no_kartu (str): BPJS card number
            tgl_pelayanan (str, optional): Service date in format YYYY-MM-DD
                                          Default: today's date
                                          
        Returns:
            dict: Patient information from BPJS
        """
        if not tgl_pelayanan:
            tgl_pelayanan = datetime.now().strftime('%Y-%m-%d')
            
        # Format date properly for BPJS API (remove dashes)
        tgl_pelayanan_format = tgl_pelayanan.replace('-', '')
        
        endpoint = f"Peserta/nokartu/{no_kartu}/tglSEP/{tgl_pelayanan_format}"
        return self._make_request(endpoint)
    
    def check_peserta_by_nik(self, nik, tgl_pelayanan=None):
        """
        Check/verify BPJS patient by NIK (ID card number)
        
        Args:
            nik (str): NIK (National ID number)
            tgl_pelayanan (str, optional): Service date in format YYYY-MM-DD
                                          Default: today's date
                                          
        Returns:
            dict: Patient information from BPJS
        """
        if not tgl_pelayanan:
            tgl_pelayanan = datetime.now().strftime('%Y-%m-%d')
            
        # Format date properly for BPJS API (remove dashes)
        tgl_pelayanan_format = tgl_pelayanan.replace('-', '')
        
        endpoint = f"Peserta/nik/{nik}/tglSEP/{tgl_pelayanan_format}"
        return self._make_request(endpoint)
    
    def get_rujukan_by_nomor(self, no_rujukan):
        """
        Get referral (rujukan) information by referral number
        
        Args:
            no_rujukan (str): Referral number
            
        Returns:
            dict: Referral information from BPJS
        """
        endpoint = f"Rujukan/{no_rujukan}"
        return self._make_request(endpoint)
    
    def get_rujukan_by_peserta(self, no_kartu):
        """
        Get active referrals for a patient by BPJS card number
        
        Args:
            no_kartu (str): BPJS card number
            
        Returns:
            dict: List of referrals for the patient
        """
        endpoint = f"Rujukan/Peserta/{no_kartu}"
        return self._make_request(endpoint)
    
    def create_sep(self, sep_data):
        """
        Create a new SEP (Surat Eligibilitas Peserta)
        
        Args:
            sep_data (dict): SEP data according to BPJS API specifications
            
        Returns:
            dict: Response with SEP information
        """
        endpoint = "SEP/2.0/insert"
        return self._make_request(endpoint, method='POST', data=sep_data)
    
    def update_sep(self, sep_data):
        """
        Update an existing SEP
        
        Args:
            sep_data (dict): Updated SEP data
            
        Returns:
            dict: Response with updated SEP information
        """
        endpoint = "SEP/2.0/update"
        return self._make_request(endpoint, method='PUT', data=sep_data)
    
    def delete_sep(self, sep_data):
        """
        Delete an existing SEP
        
        Args:
            sep_data (dict): SEP deletion data with reason
            
        Returns:
            dict: Response with deletion status
        """
        endpoint = "SEP/2.0/delete"
        return self._make_request(endpoint, method='DELETE', data=sep_data)
    
    def get_sep_by_nomor(self, no_sep):
        """
        Get SEP information by SEP number
        
        Args:
            no_sep (str): SEP number
            
        Returns:
            dict: SEP information from BPJS
        """
        endpoint = f"SEP/{no_sep}"
        return self._make_request(endpoint)
    
    def get_claim_status(self, nomor_sep, jenis_rawat):
        """
        Get claim status for a SEP
        
        Args:
            nomor_sep (str): SEP number
            jenis_rawat (str): Type of service (1: inpatient, 2: outpatient)
            
        Returns:
            dict: Claim status information
        """
        endpoint = f"Monitoring/Klaim/Status/{nomor_sep}/{jenis_rawat}"
        return self._make_request(endpoint)
    
    # Aplicare API Implementations (Bed availability)
    def get_bed_availability(self, kode_ppk, kode_kelas):
        """
        Get bed availability information
        
        Args:
            kode_ppk (str): Hospital code
            kode_kelas (str): Room class code
            
        Returns:
            dict: Bed availability information
        """
        endpoint = f"rest/bed/read/{kode_ppk}/{kode_kelas}"
        return self._make_request(endpoint)

    def update_bed_availability(self, bed_data):
        """
        Update bed availability information
        
        Args:
            bed_data (dict): Bed availability data
            
        Returns:
            dict: Response with update status
        """
        endpoint = "rest/bed/update"
        return self._make_request(endpoint, method='POST', data=bed_data)

# Helper functions for common BPJS operations
def verify_bpjs_membership(nomor_kartu, tanggal_pelayanan=None):
    """
    Verify BPJS membership status
    
    Args:
        nomor_kartu (str): BPJS card number
        tanggal_pelayanan (str, optional): Service date in format YYYY-MM-DD
        
    Returns:
        dict: Membership verification result
    """
    try:
        bpjs = BPJSIntegration()
        result = bpjs.check_peserta_by_noka(nomor_kartu, tanggal_pelayanan)
        
        # Process response
        if 'metaData' in result and result['metaData']['code'] == '200':
            if 'response' in result and 'peserta' in result['response']:
                peserta = result['response']['peserta']
                
                verification_result = {
                    'status': 'active' if peserta.get('statusPeserta', {}).get('kode') == '0' else 'inactive',
                    'nama': peserta.get('nama'),
                    'nik': peserta.get('nik'),
                    'no_kartu': peserta.get('noKartu'),
                    'kelas': peserta.get('hakKelas', {}).get('keterangan'),
                    'jenis_peserta': peserta.get('jenisPeserta', {}).get('keterangan'),
                    'tgl_lahir': peserta.get('tglLahir'),
                    'faskes_tingkat1': peserta.get('provUmum', {}).get('nmProvider'),
                    'validity': True,
                    'message': 'Verifikasi berhasil',
                    'raw_response': result
                }
                return verification_result
            else:
                return {
                    'status': 'unknown',
                    'validity': False,
                    'message': 'Data peserta tidak ditemukan',
                    'raw_response': result
                }
        else:
            return {
                'status': 'error',
                'validity': False,
                'message': result.get('metaData', {}).get('message', 'Terjadi kesalahan'),
                'raw_response': result
            }
    except Exception as e:
        current_app.logger.error(f"Error in verify_bpjs_membership: {str(e)}")
        return {
            'status': 'error',
            'validity': False,
            'message': f"Terjadi kesalahan: {str(e)}",
            'raw_response': None
        }

def get_referrals(nomor_kartu):
    """
    Get active referrals for a patient
    
    Args:
        nomor_kartu (str): BPJS card number
        
    Returns:
        dict: Referral information
    """
    try:
        bpjs = BPJSIntegration()
        result = bpjs.get_rujukan_by_peserta(nomor_kartu)
        
        # Process response
        if 'metaData' in result and result['metaData']['code'] == '200':
            if 'response' in result and 'rujukan' in result['response']:
                return {
                    'status': 'success',
                    'referrals': result['response']['rujukan'],
                    'message': 'Data rujukan berhasil diambil',
                    'raw_response': result
                }
            else:
                return {
                    'status': 'no_data',
                    'referrals': [],
                    'message': 'Tidak ada data rujukan',
                    'raw_response': result
                }
        else:
            return {
                'status': 'error',
                'referrals': [],
                'message': result.get('metaData', {}).get('message', 'Terjadi kesalahan'),
                'raw_response': result
            }
    except Exception as e:
        current_app.logger.error(f"Error in get_referrals: {str(e)}")
        return {
            'status': 'error',
            'referrals': [],
            'message': f"Terjadi kesalahan: {str(e)}",
            'raw_response': None
        }