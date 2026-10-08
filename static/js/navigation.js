// Navbar Dropdown Toggle
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const hamburgerBtn = document.querySelector('.hamburger-btn');
    const mobileNav = document.getElementById('mobileNav');
    const mobileNavClose = document.getElementById('mobileNavClose');
    const mobileNavLinks = mobileNav?.querySelectorAll('.mobile-nav-link');

    function toggleMobileMenu(open = null) {
        const isOpen = mobileNav.classList.contains('active');
        if (open !== null) {
            if (open && !isOpen || !open && isOpen) return;
        }

        mobileNav.classList.toggle('active');
        hamburgerBtn.classList.toggle('active');
        hamburgerBtn.setAttribute('aria-expanded', hamburgerBtn.classList.contains('active'));
        document.body.classList.toggle('menu-open');
    }

    if (hamburgerBtn) {
        hamburgerBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleMobileMenu();
        });
    }

    if (mobileNavClose) {
        mobileNavClose.addEventListener('click', toggleMobileMenu);
    }

    if (mobileNavLinks) {
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => toggleMobileMenu(false));
        });
    }

    // Close on overlay/escape/outside
    document.addEventListener('click', (e) => {
        if (mobileNav.classList.contains('active') && !e.target.closest('.navbar') && !e.target.closest('.mobile-nav')) {
            toggleMobileMenu(false);
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
            toggleMobileMenu(false);
        }
    });

    // Close on window resize >768px
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && mobileNav.classList.contains('active')) {
            toggleMobileMenu(false);
        }
    });

    const userBtn = document.querySelector('.user-btn');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (userBtn && dropdownMenu) {
        userBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('show');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                dropdownMenu.classList.remove('show');
            }
        });

        // Close menu when clicking on a link
        const dropdownLinks = dropdownMenu.querySelectorAll('a');
        dropdownLinks.forEach(link => {
            link.addEventListener('click', function() {
                dropdownMenu.classList.remove('show');
            });
        });
    }

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Logout button handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to log out?')) {
                location.href = this.dataset.logoutUrl;
            }
        });
    }
});

// Cart item update confirmation
function confirmDelete(event) {
    if (!confirm('Are you sure you want to remove this item from cart?')) {
        event.preventDefault();
    }
}
// Logout confirmation
function confirmLogout() {
    if (confirm('Are you sure you want to log out?')) {
        location.href = document.querySelector('[data-logout-url]')?.dataset.logoutUrl || '/logout/';
    }
}