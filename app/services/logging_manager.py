"""
Enterprise Logging & Monitoring System
Comprehensive logging, error tracking, and system monitoring
"""
import logging
import time
import json
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from functools import wraps
from collections import defaultdict
import threading

class CustomJSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'execution_time'):
            log_entry['execution_time'] = record.execution_time
        if hasattr(record, 'ip_address'):
            log_entry['ip_address'] = record.ip_address
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_entry, ensure_ascii=False)

class SecurityLogger:
    """Specialized logger for security events"""
    
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.failed_attempts = defaultdict(list)
        self.suspicious_activities = []
    
    def log_failed_login(self, email: str, ip_address: str, user_agent: str = None):
        """Log failed login attempts"""
        self.failed_attempts[ip_address].append({
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'user_agent': user_agent
        })
        
        # Check for brute force attempts
        recent_attempts = [
            attempt for attempt in self.failed_attempts[ip_address]
            if datetime.fromisoformat(attempt['timestamp']) > datetime.now() - timedelta(hours=1)
        ]
        
        if len(recent_attempts) >= 5:
            self.log_suspicious_activity(
                'brute_force_detected',
                f"Multiple failed login attempts from {ip_address}",
                {'ip_address': ip_address, 'attempts': len(recent_attempts)}
            )
        
        self.logger.warning(
            f"Failed login attempt for {email} from {ip_address}",
            extra={'user_id': email, 'ip_address': ip_address, 'event_type': 'failed_login'}
        )
    
    def log_successful_login(self, user_id: str, ip_address: str, user_agent: str = None):
        """Log successful login"""
        self.logger.info(
            f"Successful login for {user_id} from {ip_address}",
            extra={'user_id': user_id, 'ip_address': ip_address, 'event_type': 'successful_login'}
        )
    
    def log_suspicious_activity(self, activity_type: str, description: str, metadata: Dict = None):
        """Log suspicious activities"""
        activity = {
            'type': activity_type,
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.suspicious_activities.append(activity)
        
        self.logger.critical(
            f"Suspicious activity detected: {description}",
            extra={'event_type': 'suspicious_activity', 'activity_type': activity_type}
        )
    
    def log_api_key_usage(self, api_key_id: str, endpoint: str, ip_address: str):
        """Log API key usage"""
        self.logger.info(
            f"API key {api_key_id} used for {endpoint} from {ip_address}",
            extra={'api_key_id': api_key_id, 'endpoint': endpoint, 'ip_address': ip_address}
        )

class PerformanceMonitor:
    """Performance monitoring and profiling"""
    
    def __init__(self):
        self.logger = logging.getLogger('performance')
        self.metrics = defaultdict(list)
        self.slow_queries = []
        self.memory_alerts = []
    
    def timing_decorator(self, operation_name: str = None):
        """Decorator to measure function execution time"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    op_name = operation_name or f"{func.__module__}.{func.__name__}"
                    self.track_performance(op_name, execution_time)
                    
                    # Log slow operations
                    if execution_time > 1.0:  # Operations taking more than 1 second
                        self.logger.warning(
                            f"Slow operation detected: {op_name} took {execution_time:.2f}s",
                            extra={'execution_time': execution_time, 'operation': op_name}
                        )
                    
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self.logger.error(
                        f"Operation failed: {operation_name or func.__name__} in {execution_time:.2f}s",
                        extra={'execution_time': execution_time, 'error': str(e)},
                        exc_info=True
                    )
                    raise
            return wrapper
        return decorator
    
    def track_performance(self, operation: str, execution_time: float):
        """Track performance metrics"""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time
        }
        self.metrics[operation].append(metric)
        
        # Keep only last 100 metrics per operation
        if len(self.metrics[operation]) > 100:
            self.metrics[operation] = self.metrics[operation][-100:]
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        summary = {}
        for operation, metrics in self.metrics.items():
            if metrics:
                times = [m['execution_time'] for m in metrics]
                summary[operation] = {
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'total_calls': len(times),
                    'last_call': metrics[-1]['timestamp']
                }
        return summary

class ErrorTracker:
    """Error tracking and analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger('error_tracker')
        self.errors = []
        self.error_patterns = defaultdict(int)
    
    def track_error(self, error: Exception, context: Dict = None, user_id: str = None):
        """Track application errors"""
        error_info = {
            'id': len(self.errors) + 1,
            'type': type(error).__name__,
            'message': str(error),
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'user_id': user_id
        }
        
        self.errors.append(error_info)
        
        # Track error patterns
        error_key = f"{type(error).__name__}: {str(error)[:100]}"
        self.error_patterns[error_key] += 1
        
        # Log the error
        self.logger.error(
            f"Application error: {error_info['type']} - {error_info['message']}",
            extra={
                'error_id': error_info['id'],
                'user_id': user_id,
                'context': context
            },
            exc_info=True
        )
        
        return error_info['id']
    
    def get_error_analysis(self) -> Dict:
        """Get error analysis and trends"""
        if not self.errors:
            return {'total_errors': 0, 'patterns': {}, 'recent_errors': []}
        
        # Recent errors (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        recent_errors = [
            e for e in self.errors 
            if datetime.fromisoformat(e['timestamp']) > cutoff
        ]
        
        # Top error patterns
        top_patterns = dict(sorted(
            self.error_patterns.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10])
        
        return {
            'total_errors': len(self.errors),
            'recent_errors_24h': len(recent_errors),
            'top_error_patterns': top_patterns,
            'recent_errors': recent_errors[-10:],  # Last 10 errors
            'error_rate': len(recent_errors) / 24  # Errors per hour
        }

class SystemMonitor:
    """System resource monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger('system_monitor')
        self.alerts = []
        self.metrics_history = defaultdict(list)
    
    def check_system_health(self) -> Dict:
        """Check overall system health"""
        # Simulate system metrics (in production, use psutil or similar)
        import random
        
        metrics = {
            'cpu_usage': random.uniform(20, 80),
            'memory_usage': random.uniform(30, 90),
            'disk_usage': random.uniform(40, 85),
            'network_io': random.uniform(5, 50),
            'active_connections': random.randint(10, 100),
            'response_time': random.uniform(0.1, 0.8)
        }
        
        # Store metrics
        timestamp = datetime.now().isoformat()
        for metric, value in metrics.items():
            self.metrics_history[metric].append({
                'timestamp': timestamp,
                'value': value
            })
        
        # Check for alerts
        alerts = []
        if metrics['cpu_usage'] > 80:
            alerts.append({
                'type': 'cpu_high',
                'message': f"High CPU usage: {metrics['cpu_usage']:.1f}%",
                'severity': 'warning'
            })
        
        if metrics['memory_usage'] > 85:
            alerts.append({
                'type': 'memory_high',
                'message': f"High memory usage: {metrics['memory_usage']:.1f}%",
                'severity': 'critical'
            })
        
        if metrics['response_time'] > 0.5:
            alerts.append({
                'type': 'response_slow',
                'message': f"Slow response time: {metrics['response_time']:.2f}s",
                'severity': 'warning'
            })
        
        # Log alerts
        for alert in alerts:
            if alert['severity'] == 'critical':
                self.logger.critical(alert['message'])
            else:
                self.logger.warning(alert['message'])
        
        self.alerts.extend(alerts)
        
        return {
            'metrics': metrics,
            'alerts': alerts,
            'status': 'critical' if any(a['severity'] == 'critical' for a in alerts) else 'healthy',
            'timestamp': timestamp
        }

class LoggingManager:
    """Central logging management"""
    
    def __init__(self):
        self.setup_logging()
        self.security_logger = SecurityLogger()
        self.performance_monitor = PerformanceMonitor()
        self.error_tracker = ErrorTracker()
        self.system_monitor = SystemMonitor()
    
    def setup_logging(self):
        """Setup logging configuration"""
        # Root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Console handler with JSON formatter
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomJSONFormatter())
        root_logger.addHandler(console_handler)
        
        # File handler for persistent logging
        try:
            file_handler = logging.FileHandler('app.log')
            file_handler.setFormatter(CustomJSONFormatter())
            root_logger.addHandler(file_handler)
        except Exception:
            pass  # Skip file logging if not possible
        
        # Specific loggers
        loggers = ['security', 'performance', 'error_tracker', 'system_monitor']
        for logger_name in loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
    
    def get_comprehensive_status(self) -> Dict:
        """Get comprehensive system status"""
        system_health = self.system_monitor.check_system_health()
        performance_summary = self.performance_monitor.get_performance_summary()
        error_analysis = self.error_tracker.get_error_analysis()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system_health': system_health,
            'performance': performance_summary,
            'errors': error_analysis,
            'security': {
                'failed_attempts': len(self.security_logger.failed_attempts),
                'suspicious_activities': len(self.security_logger.suspicious_activities)
            },
            'overall_status': self._determine_overall_status(system_health, error_analysis)
        }
    
    def _determine_overall_status(self, system_health: Dict, error_analysis: Dict) -> str:
        """Determine overall system status"""
        if system_health['status'] == 'critical':
            return 'critical'
        elif error_analysis.get('error_rate', 0) > 10:  # More than 10 errors per hour
            return 'degraded'
        elif system_health['alerts']:
            return 'warning'
        else:
            return 'healthy'

# Global logging manager
logging_manager = LoggingManager()

# Convenience functions
def log_performance(operation_name: str = None):
    """Decorator for performance monitoring"""
    return logging_manager.performance_monitor.timing_decorator(operation_name)

def track_error(error: Exception, context: Dict = None, user_id: str = None):
    """Track application errors"""
    return logging_manager.error_tracker.track_error(error, context, user_id)

def log_security_event(event_type: str, **kwargs):
    """Log security events"""
    if event_type == 'failed_login':
        logging_manager.security_logger.log_failed_login(**kwargs)
    elif event_type == 'successful_login':
        logging_manager.security_logger.log_successful_login(**kwargs)
    elif event_type == 'suspicious_activity':
        logging_manager.security_logger.log_suspicious_activity(**kwargs)
