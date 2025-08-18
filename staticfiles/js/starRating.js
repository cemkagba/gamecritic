// Simple Star Rating System for Beginners
// Wait for the page to fully load before running our code
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating .fa-star');
    const ratingInput = document.getElementById('id_rating');
    const ratingText = document.getElementById('rating-text');
    const starContainer = document.querySelector('.star-rating');
    const reviewForm = document.getElementById('reviewForm');
    
    // Exit early if star rating elements don't exist on this page
    if (!stars.length || !starContainer) {
        console.log('Star rating elements not found, skipping star rating functionality');
        return;
    }
    
    let selectedRating = 0;
    const ratingMessages = {
        1: 'Awful',
        2: 'Meh',   
        3: 'Okay',
        4: 'Great',
        5: 'Fantastic'
    };

    function lightUpStars(numberOfStars) {
        stars.forEach(function(star, index) {
            if (index < numberOfStars) {
                star.classList.remove('text-gray-300');
                star.classList.add('text-yellow-400');
            } else {
                star.classList.remove('text-yellow-400');
                star.classList.add('text-gray-300');
            }
        });
    }

    function showRatingMessage(rating) {
        if (ratingText && rating > 0) {
            ratingText.textContent = ratingMessages[rating];
            ratingText.classList.remove('text-gray-600');
            ratingText.classList.add('text-green-600');
        }
    }

    stars.forEach(function(star, index) {
        const starNumber = index + 1;

        star.addEventListener('mouseenter', function() {
            lightUpStars(starNumber);
            showRatingMessage(starNumber);
        });

        star.addEventListener('click', function() {
            selectedRating = starNumber;
            lightUpStars(starNumber);
            showRatingMessage(starNumber);
            
            if (ratingInput) {
                ratingInput.value = starNumber;
            }
            
            if (ratingText) {
                ratingText.textContent = ratingMessages[starNumber] + ' (Selected)';
            }
        });
    });

    if (starContainer) {
        starContainer.addEventListener('mouseleave', function() {
            if (selectedRating > 0) {
                lightUpStars(selectedRating);
                if (ratingText) {
                    ratingText.textContent = ratingMessages[selectedRating] + ' (Selected)';
                }
            } else {
                lightUpStars(0);
                if (ratingText) {
                    ratingText.textContent = 'Click a star to rate';
                }
            }
        });
    }

    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            if (selectedRating === 0 && ratingInput) {
                e.preventDefault();
                alert('Please select a rating before submitting your review.');
                return false;
            }
        });
    }
});
