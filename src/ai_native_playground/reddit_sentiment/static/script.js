// JavaScript for Reddit Sentiment Analyzer

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzeForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    
    // Form submission handler
    if (form) {
        form.addEventListener('submit', function(e) {
            // Show loading modal
            loadingModal.show();
            
            // Disable the submit button
            if (analyzeBtn) {
                analyzeBtn.disabled = true;
                analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
            }
        });
    }
    
    // URL validation
    const urlInput = document.getElementById('reddit_url');
    if (urlInput) {
        urlInput.addEventListener('blur', function() {
            const url = this.value.trim();
            if (url && !isValidRedditUrl(url)) {
                this.setCustomValidity('Please enter a valid Reddit post URL');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                if (url) {
                    this.classList.add('is-valid');
                }
            }
        });
        
        // Clear validation on input
        urlInput.addEventListener('input', function() {
            this.classList.remove('is-invalid', 'is-valid');
            this.setCustomValidity('');
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            const text = document.querySelector(target).textContent;
            
            navigator.clipboard.writeText(text).then(() => {
                // Show success feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            }).catch(() => {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
            });
        });
    });
});

// Utility function to validate Reddit URLs
function isValidRedditUrl(url) {
    const patterns = [
        /^https?:\/\/(?:www\.)?reddit\.com\/r\/\w+\/comments\/\w+/,
        /^https?:\/\/redd\.it\/\w+/
    ];
    
    return patterns.some(pattern => pattern.test(url));
}

// Function to format numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Function to get mood color class
function getMoodColorClass(mood) {
    const moodMap = {
        'very positive': 'text-success',
        'positive': 'text-info',
        'slightly positive': 'text-primary',
        'neutral': 'text-secondary',
        'slightly negative': 'text-warning',
        'negative': 'text-danger',
        'very negative': 'text-dark'
    };
    
    return moodMap[mood] || 'text-secondary';
}

// Function to animate progress bars
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = width;
        }, 100);
    });
}

// Initialize progress bar animation when page loads
window.addEventListener('load', function() {
    if (document.querySelector('.progress-bar')) {
        animateProgressBars();
    }
});

// Add tooltips to elements with title attribute
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});