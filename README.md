# AI-Powered Job Application Toolkit

This project is an AI-driven platform designed to help job seekers optimize their job application process. It provides tools for resume analysis, ATS (Applicant Tracking System) compatibility scoring, personalized cover letter generation, interview preparation, and real-time job search integration.

## Features

- **Resume Analysis:** Upload your resume and receive detailed feedback and ATS compatibility scoring.
- **Cover Letter Generator:** Instantly generate personalized cover letters tailored to job descriptions.
- **Interview Preparation:** Get AI-generated interview questions and suggested answers based on your resume and target role.
- **Job Search Integration:** Search for jobs in real-time using LinkedIn and other APIs.
- **User-Friendly Interface:** Simple, intuitive web interface for all features.

## Tech Stack

- **Backend:** Python, Flask
- **AI Integration:** OpenAI GPT-4 API
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **APIs:** LinkedIn API (for job search)
- **Testing:** pytest

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/tarunpinnem/AI-Powered-Job-Application-Toolkit.git
    cd AI-Powered-Job-Application-Toolkit
    ```

2. **Set up your environment:**
    - Create a `.env` file with your OpenAI API key and any other required secrets:
      ```
      OPENAI_API_KEY=your_openai_key_here
      ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    python app.py
    ```

5. **Access the app:**
    - Open your browser and go to `http://localhost:5000`

