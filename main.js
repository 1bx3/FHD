document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
    }
    
    // Newsletter form submission (prevent default for now)
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email) {
                // Show success message
                const successMessage = document.createElement('p');
                successMessage.classList.add('success-message');
                successMessage.textContent = 'شكرًا للاشتراك! سنرسل لك الأخبار قريبًا.';
                
                // Replace form with success message
                this.style.display = 'none';
                this.parentNode.appendChild(successMessage);
            }
        });
    }
    
    // Killer/Survivor search filter
    const searchKiller = document.getElementById('search-killer');
    if (searchKiller) {
        searchKiller.addEventListener('input', function() {
            filterCards('killer-card', this.value);
        });
    }
    
    const searchSurvivor = document.getElementById('search-survivor');
    if (searchSurvivor) {
        searchSurvivor.addEventListener('input', function() {
            filterCards('survivor-card', this.value);
        });
    }
    
    const searchPerk = document.getElementById('search-perk');
    if (searchPerk) {
        searchPerk.addEventListener('input', function() {
            filterCards('perk-card', this.value);
        });
    }
    
    // Difficulty filter for killers
    const difficultyFilterKiller = document.getElementById('difficulty-filter');
    if (difficultyFilterKiller && document.querySelector('.killer-card')) {
        difficultyFilterKiller.addEventListener('change', function() {
            const selectedDifficulty = this.value;
            const killerCards = document.querySelectorAll('.killer-card');
            
            killerCards.forEach(card => {
                if (selectedDifficulty === 'all' || card.dataset.difficulty === selectedDifficulty) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Difficulty filter for survivors
    const difficultyFilterSurvivor = document.getElementById('difficulty-filter');
    if (difficultyFilterSurvivor && document.querySelector('.survivor-card')) {
        difficultyFilterSurvivor.addEventListener('change', function() {
            const selectedDifficulty = this.value;
            const survivorCards = document.querySelectorAll('.survivor-card');
            
            survivorCards.forEach(card => {
                if (selectedDifficulty === 'all' || card.dataset.difficulty === selectedDifficulty) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Function to filter cards based on search input
    function filterCards(cardClass, searchText) {
        const cards = document.querySelectorAll('.' + cardClass);
        const searchLower = searchText.toLowerCase();
        
        cards.forEach(card => {
            const cardText = card.textContent.toLowerCase();
            if (cardText.includes(searchLower)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
});
