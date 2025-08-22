/**
 * AI Career Success Platform - Advanced JavaScript
 * Comprehensive client-side functionality for enterprise career platform
 */

// Application State Management
class CareerPlatformApp {
    constructor() {
        this.state = {
            currentAnalysis: null,
            currentUser: null,
            isLoading: false,
            errors: [],
            analytics: {
                pageViews: 0,
                analysisCount: 0,
                userEngagement: 0
            }
        };
        
        this.eventListeners = new Map();
        this.apiClient = new APIClient();
        this.uiManager = new UIManager();
        this.analytics = new AnalyticsManager();
        this.storage = new StorageManager();
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.loadUserPreferences();
        this.analytics.trackPageView();
    }
    
    setupEventListeners() {
        // Form submissions
        this.addEventListener('resumeAnalysisForm', 'submit', this.handleResumeAnalysis.bind(this));
        this.addEventListener('coverLetterForm', 'submit', this.handleCoverLetterGeneration.bind(this));
        this.addEventListener('jobSearchForm', 'submit', this.handleJobSearch.bind(this));
        this.addEventListener('interviewPrepForm', 'submit', this.handleInterviewPrep.bind(this));
        
        // File uploads
        this.addEventListener('resumeFile', 'change', this.handleFileUpload.bind(this));
        
        // Real-time features
        this.addEventListener('resumeText', 'input', this.debounce(this.handleRealTimeGrammarCheck.bind(this), 1000));
        this.addEventListener('resumeText', 'blur', this.handleAutosave.bind(this));
        
        // UI interactions
        this.addEventListener('document', 'keydown', this.handleKeyboardShortcuts.bind(this));
        this.addEventListener('window', 'resize', this.debounce(this.handleResize.bind(this), 250));
        this.addEventListener('window', 'beforeunload', this.handleBeforeUnload.bind(this));
        
        // Navigation
        this.addEventListener('document', 'click', this.handleNavigation.bind(this));
    }
    
    addEventListener(elementId, event, handler) {
        const element = elementId === 'document' ? document : 
                       elementId === 'window' ? window : 
                       document.getElementById(elementId);
        
        if (element) {
            element.addEventListener(event, handler);
            this.eventListeners.set(`${elementId}-${event}`, { element, event, handler });
        }
    }
    
    initializeComponents() {
        // Initialize tooltips
        this.initializeTooltips();
        
        // Initialize progress indicators
        this.initializeProgressIndicators();
        
        // Initialize notification system
        this.uiManager.initializeNotifications();
        
        // Initialize keyboard shortcuts
        this.initializeKeyboardShortcuts();
        
        // Initialize performance monitoring
        this.initializePerformanceMonitoring();
    }
    
    // Resume Analysis Handler
    async handleResumeAnalysis(event) {
        event.preventDefault();
        
        const formData = this.extractFormData('resumeAnalysisForm');
        
        if (!this.validateResumeForm(formData)) {
            return;
        }
        
        this.uiManager.showLoading('Analyzing your resume with AI...', 0);
        this.analytics.trackEvent('resume_analysis_started');
        
        try {
            // Progressive loading simulation
            await this.simulateProgressiveAnalysis();
            
            const response = await this.apiClient.analyzeResume(formData);
            
            if (response.success) {
                this.state.currentAnalysis = response.analysis;
                this.uiManager.displayAnalysisResults(response.analysis);
                this.storage.saveAnalysis(response.analysis);
                this.analytics.trackEvent('resume_analysis_completed', { score: response.analysis.overall_score });
                this.uiManager.showNotification('Analysis completed successfully!', 'success');
            } else {
                throw new Error(response.error || 'Analysis failed');
            }
            
        } catch (error) {
            this.handleError(error, 'Resume analysis failed');
            this.analytics.trackEvent('resume_analysis_failed', { error: error.message });
        } finally {
            this.uiManager.hideLoading();
        }
    }
    
    // Cover Letter Generation Handler
    async handleCoverLetterGeneration(event) {
        event.preventDefault();
        
        if (!this.state.currentAnalysis) {
            this.uiManager.showNotification('Please analyze your resume first', 'warning');
            return;
        }
        
        const formData = this.extractFormData('coverLetterForm');
        
        this.uiManager.showLoading('Generating personalized cover letter...');
        this.analytics.trackEvent('cover_letter_generation_started');
        
        try {
            const response = await this.apiClient.generateCoverLetter({
                ...formData,
                resume_text: document.getElementById('resumeText').value,
                job_description: document.getElementById('jobDescription').value
            });
            
            if (response.success) {
                this.uiManager.displayCoverLetter(response.cover_letter);
                this.storage.saveCoverLetter(response.cover_letter, formData);
                this.analytics.trackEvent('cover_letter_generated');
                this.uiManager.showNotification('Cover letter generated successfully!', 'success');
            } else {
                throw new Error(response.error || 'Generation failed');
            }
            
        } catch (error) {
            this.handleError(error, 'Cover letter generation failed');
        } finally {
            this.uiManager.hideLoading();
        }
    }
    
    // Job Search Handler
    async handleJobSearch(event) {
        event.preventDefault();
        
        if (!this.state.currentAnalysis) {
            this.uiManager.showNotification('Please analyze your resume first', 'warning');
            return;
        }
        
        const formData = this.extractFormData('jobSearchForm');
        
        this.uiManager.showLoading('Searching for matching jobs...');
        this.analytics.trackEvent('job_search_started');
        
        try {
            const response = await this.apiClient.findJobs({
                ...formData,
                resume_text: document.getElementById('resumeText').value
            });
            
            if (response.success) {
                this.uiManager.displayJobResults(response.jobs);
                this.storage.saveJobSearchResults(response.jobs);
                this.analytics.trackEvent('job_search_completed', { 
                    jobs_found: response.total_found,
                    location: formData.location,
                    industry: formData.industry
                });
                this.uiManager.showNotification(`Found ${response.total_found} matching jobs!`, 'success');
            } else {
                throw new Error(response.error || 'Job search failed');
            }
            
        } catch (error) {
            this.handleError(error, 'Job search failed');
        } finally {
            this.uiManager.hideLoading();
        }
    }
    
    // Interview Preparation Handler
    async handleInterviewPrep(event) {
        event.preventDefault();
        
        if (!this.state.currentAnalysis) {
            this.uiManager.showNotification('Please analyze your resume first', 'warning');
            return;
        }
        
        const formData = this.extractFormData('interviewPrepForm');
        
        this.uiManager.showLoading('Preparing interview questions...');
        this.analytics.trackEvent('interview_prep_started');
        
        try {
            const response = await this.apiClient.prepareInterview({
                ...formData,
                resume_text: document.getElementById('resumeText').value,
                job_description: document.getElementById('jobDescription').value
            });
            
            if (response.success) {
                this.uiManager.displayInterviewPrep(response.interview_prep);
                this.storage.saveInterviewPrep(response.interview_prep);
                this.analytics.trackEvent('interview_prep_generated', { type: formData.type });
                this.uiManager.showNotification('Interview preparation ready!', 'success');
            } else {
                throw new Error(response.error || 'Interview prep failed');
            }
            
        } catch (error) {
            this.handleError(error, 'Interview preparation failed');
        } finally {
            this.uiManager.hideLoading();
        }
    }
    
    // File Upload Handler
    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        // Validate file
        if (!this.validateFile(file)) {
            return;
        }
        
        this.uiManager.showLoading('Processing uploaded file...');
        
        try {
            const text = await this.extractTextFromFile(file);
            document.getElementById('resumeText').value = text;
            this.uiManager.showNotification('File uploaded successfully!', 'success');
            this.analytics.trackEvent('file_uploaded', { 
                type: file.type,
                size: file.size,
                name: file.name
            });
        } catch (error) {
            this.handleError(error, 'File upload failed');
        } finally {
            this.uiManager.hideLoading();
        }
    }
    
    // Real-time Grammar Checking
    async handleRealTimeGrammarCheck() {
        const text = document.getElementById('resumeText').value;
        if (text.length < 50) return;
        
        try {
            const response = await this.apiClient.checkGrammar({ text });
            if (response.success && response.grammar_result.error_count > 0) {
                this.uiManager.showGrammarIndicator(response.grammar_result.error_count);
            } else {
                this.uiManager.hideGrammarIndicator();
            }
        } catch (error) {
            // Silently fail for real-time checking
            console.debug('Real-time grammar check failed:', error);
        }
    }
    
    // Autosave Handler
    async handleAutosave() {
        const resumeText = document.getElementById('resumeText').value;
        const jobDescription = document.getElementById('jobDescription').value;
        
        if (resumeText || jobDescription) {
            this.storage.autosave({
                resumeText,
                jobDescription,
                timestamp: Date.now()
            });
            
            this.uiManager.showAutosaveIndicator();
        }
    }
    
    // Keyboard Shortcuts Handler
    handleKeyboardShortcuts(event) {
        const shortcuts = {
            'ctrl+s': (e) => {
                e.preventDefault();
                this.handleAutosave();
            },
            'ctrl+enter': (e) => {
                e.preventDefault();
                const activeTab = document.querySelector('.nav-link.active');
                if (activeTab) {
                    const form = document.querySelector('.tab-pane.active form');
                    if (form) {
                        form.dispatchEvent(new Event('submit'));
                    }
                }
            },
            'esc': (e) => {
                this.uiManager.closeModals();
            },
            'ctrl+shift+d': (e) => {
                e.preventDefault();
                this.toggleDemoMode();
            }
        };
        
        const key = `${event.ctrlKey ? 'ctrl+' : ''}${event.shiftKey ? 'shift+' : ''}${event.key.toLowerCase()}`;
        
        if (shortcuts[key]) {
            shortcuts[key](event);
        }
    }
    
    // Utility Methods
    extractFormData(formId) {
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Add non-form elements
        if (formId === 'resumeAnalysisForm') {
            data.resume_text = document.getElementById('resumeText').value;
            data.job_description = document.getElementById('jobDescription').value;
            data.industry = document.getElementById('industry').value;
        }
        
        return data;
    }
    
    validateResumeForm(data) {
        if (!data.resume_text || data.resume_text.trim().length < 50) {
            this.uiManager.showNotification('Please enter at least 50 characters of resume content', 'warning');
            return false;
        }
        
        return true;
    }
    
    validateFile(file) {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const allowedTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ];
        
        if (file.size > maxSize) {
            this.uiManager.showNotification('File size must be less than 10MB', 'warning');
            return false;
        }
        
        if (!allowedTypes.includes(file.type)) {
            this.uiManager.showNotification('Please upload a PDF, DOC, DOCX, or TXT file', 'warning');
            return false;
        }
        
        return true;
    }
    
    async extractTextFromFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (event) => {
                resolve(event.target.result);
            };
            
            reader.onerror = () => {
                reject(new Error('Failed to read file'));
            };
            
            if (file.type === 'text/plain') {
                reader.readAsText(file);
            } else {
                // For PDF and DOC files, we'd need a proper parser
                // For now, we'll just read as text (this is a demo)
                reader.readAsText(file);
            }
        });
    }
    
    async simulateProgressiveAnalysis() {
        const steps = [
            { progress: 20, message: 'Extracting content...' },
            { progress: 40, message: 'Checking grammar and spelling...' },
            { progress: 60, message: 'Analyzing ATS compatibility...' },
            { progress: 80, message: 'Generating recommendations...' }
        ];
        
        for (const step of steps) {
            this.uiManager.updateLoadingProgress(step.progress, step.message);
            await this.sleep(500);
        }
        
        this.uiManager.updateLoadingProgress(100, 'Analysis complete!');
        await this.sleep(500);
    }
    
    handleError(error, context) {
        console.error(`${context}:`, error);
        this.state.errors.push({ error, context, timestamp: Date.now() });
        this.uiManager.showNotification(`${context}: ${error.message}`, 'danger');
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // Initialize methods
    initializeTooltips() {
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipElements.forEach(el => new bootstrap.Tooltip(el));
    }
    
    initializeProgressIndicators() {
        // Intersection Observer for scroll animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-scale');
                }
            });
        }, { threshold: 0.1 });
        
        document.querySelectorAll('.glass-card, .feature-card').forEach(el => {
            observer.observe(el);
        });
    }
    
    initializeKeyboardShortcuts() {
        // Add keyboard shortcut indicators to help text
        const helpText = `
            Keyboard Shortcuts:
            • Ctrl+S: Autosave
            • Ctrl+Enter: Submit active form
            • Esc: Close modals
            • Ctrl+Shift+D: Toggle demo mode
        `;
        
        // Create help tooltip
        const helpButton = document.createElement('button');
        helpButton.className = 'btn btn-outline-light btn-sm position-fixed';
        helpButton.style.cssText = 'bottom: 6rem; right: 2rem; z-index: 1000;';
        helpButton.innerHTML = '<i class="fas fa-keyboard"></i>';
        helpButton.title = helpText;
        helpButton.setAttribute('data-bs-toggle', 'tooltip');
        helpButton.setAttribute('data-bs-placement', 'left');
        
        document.body.appendChild(helpButton);
        new bootstrap.Tooltip(helpButton);
    }
    
    initializePerformanceMonitoring() {
        // Monitor page performance
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    this.analytics.trackPerformance({
                        loadTime: perfData.loadEventEnd - perfData.fetchStart,
                        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.fetchStart,
                        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
                    });
                }, 0);
            });
        }
    }
    
    loadUserPreferences() {
        const preferences = this.storage.getPreferences();
        if (preferences) {
            // Apply saved preferences
            if (preferences.theme) {
                document.body.setAttribute('data-theme', preferences.theme);
            }
            if (preferences.autosave !== undefined) {
                this.autosaveEnabled = preferences.autosave;
            }
        }
    }
    
    handleResize() {
        // Handle responsive layout changes
        this.uiManager.updateLayout();
    }
    
    handleBeforeUnload(event) {
        // Check if there's unsaved work
        const resumeText = document.getElementById('resumeText')?.value;
        const jobDescription = document.getElementById('jobDescription')?.value;
        
        if ((resumeText && resumeText.length > 50) || (jobDescription && jobDescription.length > 50)) {
            const message = 'You have unsaved changes. Are you sure you want to leave?';
            event.returnValue = message;
            return message;
        }
    }
    
    handleNavigation(event) {
        // Smooth scroll for anchor links
        if (event.target.matches('a[href^="#"]')) {
            event.preventDefault();
            const target = document.querySelector(event.target.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    }
    
    toggleDemoMode() {
        const demoData = {
            resumeText: `John Doe
Software Engineer

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020-2023
• Developed scalable web applications using React and Node.js
• Led a team of 5 developers in agile environment
• Improved application performance by 40% through optimization
• Implemented CI/CD pipelines reducing deployment time by 60%

Software Engineer | StartupXYZ | 2018-2020
• Built RESTful APIs using Python and Django
• Collaborated with cross-functional teams to deliver features
• Wrote comprehensive unit tests achieving 90% code coverage

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2018

SKILLS
• Programming: JavaScript, Python, Java, TypeScript
• Frameworks: React, Node.js, Django, Express
• Databases: PostgreSQL, MongoDB, Redis
• Tools: Git, Docker, AWS, Jenkins`,
            
            jobDescription: `Senior Full Stack Developer
We are seeking a talented Senior Full Stack Developer to join our growing engineering team. 

Requirements:
• 5+ years of experience in full-stack development
• Proficiency in JavaScript, React, Node.js
• Experience with cloud platforms (AWS/Azure)
• Strong understanding of database design
• Experience with CI/CD pipelines
• Excellent problem-solving skills
• Bachelor's degree in Computer Science or related field

Responsibilities:
• Design and develop scalable web applications
• Lead technical decisions and mentor junior developers
• Collaborate with product and design teams
• Implement best practices for code quality and testing
• Optimize application performance and security`,
            
            industry: 'technology'
        };
        
        document.getElementById('resumeText').value = demoData.resumeText;
        document.getElementById('jobDescription').value = demoData.jobDescription;
        document.getElementById('industry').value = demoData.industry;
        
        this.uiManager.showNotification('Demo data loaded!', 'info');
    }
    
    // Cleanup method
    destroy() {
        this.eventListeners.forEach(({ element, event, handler }) => {
            element.removeEventListener(event, handler);
        });
        this.eventListeners.clear();
    }
}

// API Client for backend communication
class APIClient {
    constructor() {
        this.baseURL = '';
        this.headers = {
            'Content-Type': 'application/json'
        };
    }
    
    async analyzeResume(data) {
        const formData = new FormData();
        Object.keys(data).forEach(key => {
            formData.append(key, data[key]);
        });
        
        return this.request('/api/analyze-resume', {
            method: 'POST',
            body: formData,
            headers: {} // Let browser set Content-Type for FormData
        });
    }
    
    async generateCoverLetter(data) {
        return this.request('/api/generate-cover-letter', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async findJobs(data) {
        return this.request('/api/find-jobs', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async prepareInterview(data) {
        return this.request('/api/interview-prep', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async checkGrammar(data) {
        return this.request('/api/grammar-check', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.headers,
                ...options.headers
            }
        };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
}

// UI Manager for all interface interactions
class UIManager {
    constructor() {
        this.loadingModal = null;
        this.notifications = [];
    }
    
    initializeNotifications() {
        // Create notification container
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    showLoading(message, progress = 0) {
        if (!this.loadingModal) {
            this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        }
        
        document.getElementById('loadingMessage').textContent = message;
        document.getElementById('loadingProgress').style.width = progress + '%';
        this.loadingModal.show();
    }
    
    updateLoadingProgress(progress, message) {
        document.getElementById('loadingProgress').style.width = progress + '%';
        if (message) {
            document.getElementById('loadingMessage').textContent = message;
        }
    }
    
    hideLoading() {
        if (this.loadingModal) {
            this.loadingModal.hide();
        }
    }
    
    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('notification-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast show bg-${type} text-white`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="toast-body d-flex align-items-center">
                <i class="fas fa-${this.getIconForType(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close btn-close-white ms-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        container.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast, { delay: duration });
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => {
            container.removeChild(toast);
        });
    }
    
    getIconForType(type) {
        const icons = {
            success: 'check-circle',
            danger: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    displayAnalysisResults(analysis) {
        // Implementation moved to template
        // This would contain the complex result display logic
        const container = document.getElementById('analysisResults');
        // ... (implementation details from template)
    }
    
    displayCoverLetter(coverLetter) {
        // Implementation moved to template
    }
    
    displayJobResults(jobs) {
        // Implementation moved to template
    }
    
    displayInterviewPrep(prepData) {
        // Implementation moved to template
    }
    
    showGrammarIndicator(errorCount) {
        const indicator = document.getElementById('grammar-indicator') || this.createGrammarIndicator();
        indicator.textContent = `${errorCount} grammar issues`;
        indicator.className = 'badge bg-warning position-absolute';
        indicator.style.cssText = 'top: 10px; right: 10px; z-index: 10;';
    }
    
    hideGrammarIndicator() {
        const indicator = document.getElementById('grammar-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    createGrammarIndicator() {
        const indicator = document.createElement('span');
        indicator.id = 'grammar-indicator';
        
        const textareaContainer = document.getElementById('resumeText').parentElement;
        textareaContainer.style.position = 'relative';
        textareaContainer.appendChild(indicator);
        
        return indicator;
    }
    
    showAutosaveIndicator() {
        const indicator = document.getElementById('autosave-indicator') || this.createAutosaveIndicator();
        indicator.textContent = 'Saved';
        indicator.className = 'badge bg-success position-fixed';
        indicator.style.cssText = 'bottom: 8rem; left: 2rem; z-index: 1000;';
        
        setTimeout(() => {
            indicator.style.opacity = '0';
            setTimeout(() => indicator.remove(), 300);
        }, 2000);
    }
    
    createAutosaveIndicator() {
        const indicator = document.createElement('span');
        indicator.id = 'autosave-indicator';
        document.body.appendChild(indicator);
        return indicator;
    }
    
    closeModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
    
    updateLayout() {
        // Handle responsive layout updates
        const isMobile = window.innerWidth < 768;
        document.body.classList.toggle('mobile-layout', isMobile);
    }
}

// Analytics Manager for tracking user interactions
class AnalyticsManager {
    constructor() {
        this.events = [];
        this.sessionId = this.generateSessionId();
        this.startTime = Date.now();
    }
    
    trackEvent(event, data = {}) {
        const eventData = {
            event,
            data,
            timestamp: Date.now(),
            sessionId: this.sessionId,
            url: window.location.href,
            userAgent: navigator.userAgent
        };
        
        this.events.push(eventData);
        console.log('Analytics Event:', eventData);
        
        // In a real app, you'd send this to an analytics service
        this.sendToAnalyticsService(eventData);
    }
    
    trackPageView() {
        this.trackEvent('page_view', {
            title: document.title,
            referrer: document.referrer
        });
    }
    
    trackPerformance(perfData) {
        this.trackEvent('performance', perfData);
    }
    
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + Date.now();
    }
    
    sendToAnalyticsService(eventData) {
        // Mock implementation - in real app, send to analytics service
        if (window.gtag) {
            window.gtag('event', eventData.event, eventData.data);
        }
    }
    
    getSessionSummary() {
        return {
            sessionId: this.sessionId,
            duration: Date.now() - this.startTime,
            eventCount: this.events.length,
            events: this.events
        };
    }
}

// Storage Manager for local data persistence
class StorageManager {
    constructor() {
        this.prefix = 'career_platform_';
    }
    
    saveAnalysis(analysis) {
        this.setItem('latest_analysis', analysis);
    }
    
    getAnalysis() {
        return this.getItem('latest_analysis');
    }
    
    saveCoverLetter(coverLetter, metadata) {
        const data = { coverLetter, metadata, timestamp: Date.now() };
        this.setItem('latest_cover_letter', data);
    }
    
    saveJobSearchResults(jobs) {
        this.setItem('latest_job_search', { jobs, timestamp: Date.now() });
    }
    
    saveInterviewPrep(prepData) {
        this.setItem('latest_interview_prep', { prepData, timestamp: Date.now() });
    }
    
    autosave(data) {
        this.setItem('autosave', data);
    }
    
    getAutosave() {
        return this.getItem('autosave');
    }
    
    savePreferences(preferences) {
        this.setItem('preferences', preferences);
    }
    
    getPreferences() {
        return this.getItem('preferences');
    }
    
    setItem(key, value) {
        try {
            localStorage.setItem(this.prefix + key, JSON.stringify(value));
        } catch (error) {
            console.warn('Failed to save to localStorage:', error);
        }
    }
    
    getItem(key) {
        try {
            const item = localStorage.getItem(this.prefix + key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.warn('Failed to read from localStorage:', error);
            return null;
        }
    }
    
    removeItem(key) {
        try {
            localStorage.removeItem(this.prefix + key);
        } catch (error) {
            console.warn('Failed to remove from localStorage:', error);
        }
    }
    
    clear() {
        try {
            Object.keys(localStorage).forEach(key => {
                if (key.startsWith(this.prefix)) {
                    localStorage.removeItem(key);
                }
            });
        } catch (error) {
            console.warn('Failed to clear localStorage:', error);
        }
    }
}

// Global utility functions
window.CareerPlatformUtils = {
    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    
    scrollToAnalyzer() {
        document.getElementById('analyzer').scrollIntoView({ behavior: 'smooth' });
    },
    
    showDemo() {
        if (window.careerApp) {
            window.careerApp.toggleDemoMode();
        }
    },
    
    exportData() {
        if (window.careerApp) {
            const data = {
                analysis: window.careerApp.storage.getAnalysis(),
                preferences: window.careerApp.storage.getPreferences(),
                analytics: window.careerApp.analytics.getSessionSummary()
            };
            
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'career_platform_data.json';
            a.click();
            URL.revokeObjectURL(url);
        }
    }
};

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the main application
    window.careerApp = new CareerPlatformApp();
    
    // Make utility functions globally available
    window.scrollToTop = window.CareerPlatformUtils.scrollToTop;
    window.scrollToAnalyzer = window.CareerPlatformUtils.scrollToAnalyzer;
    window.showDemo = window.CareerPlatformUtils.showDemo;
    
    // Add development helpers
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('🚀 AI Career Platform - Development Mode');
        console.log('Available commands:');
        console.log('• window.careerApp - Main application instance');
        console.log('• window.CareerPlatformUtils.exportData() - Export user data');
        console.log('• window.showDemo() - Load demo data');
        
        // Add debug panel
        const debugPanel = document.createElement('div');
        debugPanel.style.cssText = `
            position: fixed;
            top: 10px;
            left: 10px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            z-index: 10000;
            max-width: 300px;
        `;
        debugPanel.innerHTML = `
            <div>🚀 Career Platform Debug</div>
            <div>Session: ${window.careerApp.analytics.sessionId}</div>
            <div id="debug-events">Events: 0</div>
            <button onclick="window.CareerPlatformUtils.exportData()" style="margin-top: 5px; padding: 2px 5px;">Export Data</button>
        `;
        document.body.appendChild(debugPanel);
        
        // Update event counter
        const originalTrackEvent = window.careerApp.analytics.trackEvent;
        window.careerApp.analytics.trackEvent = function(...args) {
            originalTrackEvent.apply(this, args);
            document.getElementById('debug-events').textContent = `Events: ${this.events.length}`;
        };
    }
});

// Handle service worker registration for PWA capabilities
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}
