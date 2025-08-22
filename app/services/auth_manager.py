"""
Enterprise Authentication & Authorization System
JWT-based authentication with role-based access control
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, Any
import uuid
import logging

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Production authentication and authorization manager"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = 'HS256'
        self.access_token_expire = timedelta(hours=24)
        self.refresh_token_expire = timedelta(days=30)
        
        # In-memory user store (in production, this would be a database)
        self.users = {
            "demo@atsscanner.com": {
                "id": 1,
                "email": "demo@atsscanner.com",
                "password_hash": self._hash_password("demo123"),
                "role": "premium_user",
                "is_active": True,
                "is_verified": True,
                "subscription": "premium",
                "credits": 500,
                "api_calls_today": 45,
                "api_limit": 1000,
                "created_at": datetime.now()
            },
            "admin@atsscanner.com": {
                "id": 2,
                "email": "admin@atsscanner.com",
                "password_hash": self._hash_password("admin123"),
                "role": "admin",
                "is_active": True,
                "is_verified": True,
                "subscription": "enterprise",
                "credits": 10000,
                "api_calls_today": 12,
                "api_limit": 10000,
                "created_at": datetime.now()
            }
        }
        
        # API Keys for external access
        self.api_keys = {
            "ats_sk_test_1234567890abcdef": {
                "user_id": 1,
                "name": "Production API Key",
                "permissions": ["read", "write", "analyze"],
                "rate_limit": 1000,
                "calls_today": 45,
                "is_active": True,
                "created_at": datetime.now(),
                "last_used": datetime.now()
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with email and password"""
        user = self.users.get(email)
        if not user:
            return None
        
        if not self._verify_password(password, user['password_hash']):
            return None
        
        if not user['is_active']:
            return None
        
        # Update last login
        user['last_login'] = datetime.now()
        
        return {
            "id": user['id'],
            "email": user['email'],
            "role": user['role'],
            "subscription": user['subscription'],
            "credits": user['credits']
        }
    
    def generate_tokens(self, user: Dict) -> Dict[str, str]:
        """Generate access and refresh tokens"""
        now = datetime.utcnow()
        
        # Access token payload
        access_payload = {
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'subscription': user['subscription'],
            'iat': now,
            'exp': now + self.access_token_expire,
            'type': 'access'
        }
        
        # Refresh token payload
        refresh_payload = {
            'user_id': user['id'],
            'iat': now,
            'exp': now + self.refresh_token_expire,
            'type': 'refresh'
        }
        
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(self.access_token_expire.total_seconds())
        }
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return None
            
            return payload
        except jwt.InvalidTokenError:
            return None
    
    def verify_api_key(self, api_key: str) -> Optional[Dict]:
        """Verify API key and return associated user info"""
        key_info = self.api_keys.get(api_key)
        if not key_info or not key_info['is_active']:
            return None
        
        # Check rate limits
        if key_info['calls_today'] >= key_info['rate_limit']:
            return None
        
        # Update usage
        key_info['calls_today'] += 1
        key_info['last_used'] = datetime.now()
        
        # Get user info
        user_id = key_info['user_id']
        user = next((u for u in self.users.values() if u['id'] == user_id), None)
        
        if not user:
            return None
        
        return {
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'subscription': user['subscription'],
            'api_key_permissions': key_info['permissions']
        }
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """Generate new access token using refresh token"""
        payload = self.verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return None
        
        # Get user info
        user_id = payload['user_id']
        user = next((u for u in self.users.values() if u['id'] == user_id), None)
        
        if not user:
            return None
        
        # Generate new access token
        user_info = {
            'id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'subscription': user['subscription']
        }
        
        return self.generate_tokens(user_info)
    
    def create_api_key(self, user_id: int, name: str, permissions: list) -> str:
        """Create new API key for user"""
        api_key = f"ats_sk_{'test' if permissions else 'live'}_{uuid.uuid4().hex}"
        
        self.api_keys[api_key] = {
            'user_id': user_id,
            'name': name,
            'permissions': permissions,
            'rate_limit': 1000,
            'calls_today': 0,
            'is_active': True,
            'created_at': datetime.now(),
            'last_used': None
        }
        
        return api_key
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke API key"""
        if api_key in self.api_keys:
            self.api_keys[api_key]['is_active'] = False
            return True
        return False
    
    def check_rate_limit(self, user_id: int) -> Dict:
        """Check rate limits for user"""
        user = next((u for u in self.users.values() if u['id'] == user_id), None)
        if not user:
            return {'allowed': False, 'reason': 'User not found'}
        
        if user['api_calls_today'] >= user['api_limit']:
            return {
                'allowed': False,
                'reason': 'Rate limit exceeded',
                'limit': user['api_limit'],
                'used': user['api_calls_today'],
                'reset_at': 'midnight'
            }
        
        return {
            'allowed': True,
            'limit': user['api_limit'],
            'used': user['api_calls_today'],
            'remaining': user['api_limit'] - user['api_calls_today']
        }
    
    def increment_api_usage(self, user_id: int):
        """Increment API usage counter"""
        user = next((u for u in self.users.values() if u['id'] == user_id), None)
        if user:
            user['api_calls_today'] += 1

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify, current_app
        
        # Get auth manager from app
        auth_manager = getattr(current_app, 'auth_manager', None)
        if not auth_manager:
            return jsonify({'error': 'Authentication not configured'}), 500
        
        # Check for Authorization header
        auth_header = request.headers.get('Authorization')
        api_key = request.headers.get('X-API-Key')
        
        user_info = None
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            payload = auth_manager.verify_token(token)
            if payload:
                user_info = payload
        elif api_key:
            user_info = auth_manager.verify_api_key(api_key)
        
        if not user_info:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Check rate limits
        rate_limit = auth_manager.check_rate_limit(user_info['user_id'])
        if not rate_limit['allowed']:
            return jsonify({'error': 'Rate limit exceeded', 'details': rate_limit}), 429
        
        # Increment usage
        auth_manager.increment_api_usage(user_info['user_id'])
        
        # Add user info to request context
        request.current_user = user_info
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_role(required_roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            
            user_info = getattr(request, 'current_user', None)
            if not user_info:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_role = user_info.get('role')
            if user_role not in required_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

# Global auth manager (will be initialized in app)
auth_manager = None
