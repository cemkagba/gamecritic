/**
 * Star Rating Functionality
 * Handles interactive star rating in review forms
 */

document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating .fa-star');
    const ratingInput = document.querySelector('input[name="rating"]');
    const ratingText = document.getElementById('rating-text');
    
    const ratingTexts = {
        1: 'Awful - 1 star',
        2: 'Meh - 2 stars',  
        3: 'Okay - 3 stars',
        4: 'Great - 4 stars',
        5: 'Fantastic - 5 stars'
    };
    
    if (stars.length > 0 && ratingInput) {
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = index + 1;
                ratingInput.value = rating;
                
                // Update visual state
                updateStarDisplay(rating);
                
                // Update text
                if (ratingText) {
                    ratingText.textContent = ratingTexts[rating];
                    ratingText.classList.remove('text-gray-600');
                    ratingText.classList.add('text-yellow-600', 'font-medium');
                }
            });
            
            star.addEventListener('mouseenter', function() {
                const rating = index + 1;
                updateStarDisplay(rating);
            });
        });
        
        // Reset to actual rating on mouse leave
        const starContainer = document.querySelector('.star-rating');
        if (starContainer) {
            starContainer.addEventListener('mouseleave', function() {
                const currentRating = ratingInput.value || 0;
                updateStarDisplay(currentRating);
            });
        }
    }
    
    function updateStarDisplay(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.remove('text-gray-300');
                star.classList.add('text-yellow-400');
            } else {
                star.classList.remove('text-yellow-400');
                star.classList.add('text-gray-300');
            }
        });
    }
});
