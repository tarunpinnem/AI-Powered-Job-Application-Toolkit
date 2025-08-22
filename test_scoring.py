#!/usr/bin/env python3
"""
Test script to verify that different resumes get different analysis scores
"""

import requests
import json

# Test different resume examples
test_resumes = [
    {
        "name": "Senior Developer Resume",
        "resume_text": """
        John Smith
        Senior Software Engineer
        john.smith@email.com | (555) 123-4567

        PROFESSIONAL SUMMARY
        Experienced senior software engineer with 8+ years developing scalable web applications. 
        Led teams of 5+ developers and improved system performance by 40%.

        EXPERIENCE
        Senior Software Engineer | Tech Corp | 2020-2024
        • Developed 15+ microservices handling 1M+ daily requests
        • Reduced deployment time by 60% through CI/CD optimization
        • Mentored 3 junior developers and improved team productivity by 25%
        • Led migration to AWS cloud, saving $50K annually

        Software Engineer | StartupCo | 2018-2020  
        • Built React applications serving 100K+ users
        • Implemented automated testing reducing bugs by 35%
        • Collaborated with product team on 20+ feature releases

        TECHNICAL SKILLS
        Languages: Python, JavaScript, TypeScript, Java
        Frameworks: React, Node.js, Django, Spring Boot
        Cloud: AWS, Docker, Kubernetes
        Databases: PostgreSQL, MongoDB, Redis

        EDUCATION
        Bachelor of Science in Computer Science | University of Technology | 2018
        """
    },
    {
        "name": "Entry Level Resume",
        "resume_text": """
        Sarah Johnson
        Recent Graduate
        sarah.j@email.com

        OBJECTIVE
        Recent computer science graduate seeking entry-level position in software development.

        EDUCATION
        Bachelor of Science in Computer Science | State University | 2024
        GPA: 3.5/4.0

        EXPERIENCE
        Intern | Local Company | Summer 2023
        • Worked on various projects
        • Helped with coding tasks
        • Learned new technologies

        PROJECTS
        Personal Website
        • Built a website using HTML and CSS
        • Added some JavaScript features

        SKILLS
        Programming languages: Python, Java
        Web technologies: HTML, CSS, JavaScript
        """
    },
    {
        "name": "Marketing Professional Resume",
        "resume_text": """
        Michael Brown
        Marketing Manager
        m.brown@email.com | (555) 987-6543

        PROFESSIONAL SUMMARY
        Results-driven marketing manager with 6 years of experience in digital marketing campaigns.
        Increased brand awareness by 80% and generated $2M+ in revenue through strategic initiatives.

        EXPERIENCE
        Marketing Manager | Growth Agency | 2021-2024
        • Managed $500K annual marketing budget across 10+ channels
        • Launched 25+ successful campaigns with average 15% conversion rate
        • Grew social media following from 10K to 150K followers
        • Implemented marketing automation increasing leads by 45%

        Digital Marketing Specialist | MediaCorp | 2019-2021
        • Created content strategy resulting in 300% increase in engagement
        • Managed Google Ads campaigns with $100K monthly spend
        • Analyzed campaign performance and optimized ROI by 35%

        SKILLS
        Digital Marketing: SEO, SEM, Social Media, Email Marketing
        Analytics: Google Analytics, HubSpot, Salesforce
        Creative: Adobe Creative Suite, Canva, Video Editing
        Project Management: Asana, Trello, Slack

        EDUCATION
        Bachelor of Arts in Marketing | Business School | 2019
        """
    }
]

# Test URL
base_url = "http://127.0.0.1:5001"

def test_resume_analysis(resume_data):
    """Test resume analysis and return scores"""
    url = f"{base_url}/api/analyze-resume"
    
    data = {
        'resume_text': resume_data['resume_text'],
        'job_description': 'Software Engineer position requiring Python, JavaScript, and cloud experience.',
        'industry': 'technology'
    }
    
    try:
        response = requests.post(url, data=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                analysis = result.get('analysis', {})
                return {
                    'name': resume_data['name'],
                    'overall_score': analysis.get('overall_score', 0),
                    'grammar_score': analysis.get('grammar_score', 0),
                    'ats_score': analysis.get('ats_score', 0),
                    'action_verb_score': analysis.get('action_verb_score', 0),
                    'quantified_score': analysis.get('quantified_score', 0),
                    'content_hash': analysis.get('content_hash', 'N/A'),
                    'success': True
                }
            else:
                return {'name': resume_data['name'], 'error': result.get('error', 'Unknown error'), 'success': False}
        else:
            return {'name': resume_data['name'], 'error': f'HTTP {response.status_code}', 'success': False}
    except Exception as e:
        return {'name': resume_data['name'], 'error': str(e), 'success': False}

def main():
    """Run the test and display results"""
    print("🧪 Testing Resume Analysis Score Differentiation")
    print("=" * 60)
    
    results = []
    for resume in test_resumes:
        print(f"\n📄 Testing: {resume['name']}")
        result = test_resume_analysis(resume)
        results.append(result)
        
        if result['success']:
            print(f"✅ Analysis successful")
            print(f"   Overall Score: {result['overall_score']}")
            print(f"   Grammar Score: {result['grammar_score']}")
            print(f"   ATS Score: {result['ats_score']}")
            print(f"   Action Verbs: {result['action_verb_score']}")
            print(f"   Quantified: {result['quantified_score']}")
            print(f"   Content Hash: {result['content_hash']}")
        else:
            print(f"❌ Analysis failed: {result['error']}")
    
    # Compare results
    print("\n" + "=" * 60)
    print("📊 COMPARISON SUMMARY")
    print("=" * 60)
    
    successful_results = [r for r in results if r['success']]
    
    if len(successful_results) >= 2:
        # Check if scores are different
        overall_scores = [r['overall_score'] for r in successful_results]
        unique_scores = set(overall_scores)
        
        print(f"Total resumes tested: {len(results)}")
        print(f"Successful analyses: {len(successful_results)}")
        print(f"Unique overall scores: {len(unique_scores)}")
        
        if len(unique_scores) == len(successful_results):
            print("✅ SUCCESS: All resumes received different scores!")
        elif len(unique_scores) > 1:
            print("⚠️  PARTIAL: Some score variation detected")
        else:
            print("❌ ISSUE: All resumes received identical scores")
        
        print("\nDetailed scores:")
        for result in successful_results:
            print(f"  {result['name']}: {result['overall_score']} (Hash: {result['content_hash']})")
    else:
        print("❌ ISSUE: Insufficient successful analyses to compare")

if __name__ == "__main__":
    main()
