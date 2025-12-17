// ALMG Site - Main JavaScript
// Bradley Shields Research Platform

// Desktop Overlay Control
function toggleDesktop() {
    const overlay = document.getElementById('desktopOverlay');
    overlay.classList.toggle('hidden');
    
    // Prevent body scroll when overlay is open
    if (!overlay.classList.contains('hidden')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
}

function closeDesktop() {
    const overlay = document.getElementById('desktopOverlay');
    overlay.classList.add('hidden');
    document.body.style.overflow = '';
}

// Close overlay on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDesktop();
    }
});

// Close overlay when clicking outside the window
document.getElementById('desktopOverlay')?.addEventListener('click', (e) => {
    if (e.target.id === 'desktopOverlay') {
        closeDesktop();
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Add loading animation to navigation cards
document.querySelectorAll('.nav-card').forEach(card => {
    card.addEventListener('click', function(e) {
        // Add a subtle loading indicator
        this.style.opacity = '0.7';
        setTimeout(() => {
            this.style.opacity = '1';
        }, 200);
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('ALMG Research Platform loaded');
    
    // Add intersection observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe navigation cards
    document.querySelectorAll('.nav-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Utility function for dynamic content loading
async function loadContent(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Content not found');
        return await response.text();
    } catch (error) {
        console.error('Error loading content:', error);
        return '<p>Content could not be loaded.</p>';
    }
}

// Export for use in other pages
window.ALMGSite = {
    toggleDesktop,
    closeDesktop,
    loadContent
};
