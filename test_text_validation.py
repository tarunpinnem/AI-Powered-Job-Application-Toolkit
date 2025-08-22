#!/usr/bin/env python3
"""
Test script to validate text processing and binary detection
"""

import re

def test_text_validation():
    """Test the text validation logic"""
    
    # Test case 1: Valid resume text
    valid_resume = """
John Doe
Software Engineer
john.doe@email.com

EXPERIENCE
Senior Software Engineer, Tech Corp (2020-2024)
- Developed web applications using Python and React
- Managed a team of 5 engineers
- Increased system performance by 40%

EDUCATION
Bachelor of Science in Computer Science
University of Technology (2016-2020)

SKILLS
- Python, JavaScript, React, Node.js
- AWS, Docker, Kubernetes
- Project Management
"""
    
    # Test case 2: PDF header content (should be rejected)
    pdf_content = "%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj"
    
    # Test case 3: Random binary content
    binary_content = "PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00"
    
    def validate_text(text):
        """Simulate the validation logic from the app"""
        binary_indicators = 0
        
        # Check for PDF content
        if text.startswith('%PDF-') or '%PDF-' in text[:100]:
            print("PDF header detected")
            binary_indicators += 2
            
        if text.startswith('PK\x03\x04') or 'PK\x03\x04' in text[:100]:
            print("ZIP/DOCX signature detected")
            binary_indicators += 2
            
        # Count null bytes
        null_count = text.count('\x00')
        if null_count > 5:
            print(f"Null bytes detected: {null_count}")
            binary_indicators += 1
            
        # Check non-printable characters
        non_printable = [c for c in text[:1000] if not c.isprintable() and c not in '\n\r\t\f\v']
        non_printable_ratio = len(non_printable) / len(text[:1000]) if text else 0
        if non_printable_ratio > 0.15:
            print(f"High non-printable ratio: {non_printable_ratio:.2%}")
            binary_indicators += 1
        
        print(f"Binary indicators: {binary_indicators}")
        
        # Check resume content
        resume_indicators = 0
        common_resume_words = ['experience', 'education', 'skills', 'work', 'job', 'degree', 'university', 'company', 'project', 'responsibility']
        for word in common_resume_words:
            if word.lower() in text.lower():
                resume_indicators += 1
        
        # Check for email
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            resume_indicators += 2
        
        # Check for dates
        if re.search(r'\b\d{4}\b', text):
            resume_indicators += 1
        
        print(f"Resume indicators: {resume_indicators}")
        
        # Validation results
        is_binary = binary_indicators >= 2
        is_resume = resume_indicators >= 2
        
        return {
            'is_binary': is_binary,
            'is_resume': is_resume,
            'valid': not is_binary and is_resume,
            'binary_indicators': binary_indicators,
            'resume_indicators': resume_indicators
        }
    
    print("=== Testing Valid Resume ===")
    result1 = validate_text(valid_resume)
    print(f"Result: {result1}")
    print()
    
    print("=== Testing PDF Content ===")
    result2 = validate_text(pdf_content)
    print(f"Result: {result2}")
    print()
    
    print("=== Testing Binary Content ===")
    result3 = validate_text(binary_content)
    print(f"Result: {result3}")
    print()
    
    # Summary
    print("=== SUMMARY ===")
    print(f"Valid resume passes: {result1['valid']}")
    print(f"PDF content rejected: {not result2['valid']}")
    print(f"Binary content rejected: {not result3['valid']}")

if __name__ == "__main__":
    test_text_validation()
