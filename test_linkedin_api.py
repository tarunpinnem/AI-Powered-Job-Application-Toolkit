#!/usr/bin/env python3
"""
LinkedIn Job Search API Test Script
Test different endpoints to find what's available in the subscription
"""

import requests
import json
import os

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def test_linkedin_endpoints():
    """Test various LinkedIn API endpoints to find what's available"""
    
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("❌ No RAPIDAPI_KEY found in environment")
        return
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "linkedin-job-search-api.p.rapidapi.com"
    }
    
    # Test different endpoints that might be available in free tier
    endpoints = [
        ("", "Base endpoint"),
        ("jobs", "Jobs endpoint"),
        ("search", "Search jobs"),
        ("latest", "Latest jobs"),
        ("recent", "Recent jobs"),
        ("active", "Active jobs"),
        ("all", "All jobs"),
        ("list", "List jobs"),
        ("feed", "Job feed"),
        ("api/jobs", "API jobs endpoint"),
        ("v1/jobs", "V1 jobs endpoint"),
    ]
    
    print("🔍 Testing LinkedIn Job Search API endpoints...\n")
    print(f"🔑 Using API Key: {api_key[:10]}...{api_key[-5:]}\n")
    
    for endpoint, description in endpoints:
        print(f"📍 Testing: /{endpoint} ({description})")
        
        try:
            base_url = "https://linkedin-job-search-api.p.rapidapi.com"
            url = f"{base_url}/{endpoint}" if endpoint else base_url
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"   ✅ Success: {len(data)} items found")
                        if data:
                            sample = data[0]
                            print(f"   📋 Sample fields: {list(sample.keys())[:5]}...")
                    elif isinstance(data, dict):
                        print(f"   ✅ Success: Response dict with keys: {list(data.keys())}")
                        # Check if it contains job data
                        if 'jobs' in data:
                            jobs = data['jobs']
                            print(f"   📊 Contains {len(jobs) if isinstance(jobs, list) else 'some'} jobs")
                    else:
                        print(f"   ✅ Success: {type(data)} response")
                except json.JSONDecodeError:
                    print(f"   ✅ Success: Non-JSON response (length: {len(response.text)})")
                    
            elif response.status_code == 401:
                try:
                    error_data = response.json()
                    message = error_data.get('message', 'Unauthorized')
                    if 'disabled' in message.lower():
                        print(f"   🚫 Disabled: {message}")
                    elif 'subscription' in message.lower():
                        print(f"   💰 Subscription: {message}")
                    else:
                        print(f"   🔐 Auth Error: {message}")
                except:
                    print(f"   🔐 Auth Error: {response.text[:100]}...")
                    
            elif response.status_code == 404:
                print(f"   ❌ Not Found: Endpoint doesn't exist")
                
            elif response.status_code == 403:
                print(f"   🚫 Forbidden: Access denied")
                
            else:
                try:
                    error_data = response.json()
                    print(f"   ❌ Error: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"   ❌ Error: {response.text[:100]}...")
                    
        except requests.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        print()
    
    # Test with some common parameters
    print("🔍 Testing with parameters...\n")
    
    test_params = [
        ("", {"limit": 10}),
        ("jobs", {"limit": 5}),
        ("", {"page": 1}),
        ("search", {"q": "software engineer"}),
    ]
    
    for endpoint, params in test_params:
        print(f"📍 Testing: /{endpoint} with params {params}")
        
        try:
            base_url = "https://linkedin-job-search-api.p.rapidapi.com"
            url = f"{base_url}/{endpoint}" if endpoint else base_url
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Success with parameters!")
                try:
                    data = response.json()
                    print(f"   📊 Response type: {type(data)}")
                    if isinstance(data, dict) and 'jobs' in data:
                        print(f"   🎯 Found jobs key!")
                except:
                    pass
            else:
                try:
                    error_data = response.json()
                    print(f"   ❌ {error_data.get('message', 'Error')}")
                except:
                    print(f"   ❌ Status {response.status_code}")
                    
        except requests.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        print()

if __name__ == "__main__":
    test_linkedin_endpoints()
