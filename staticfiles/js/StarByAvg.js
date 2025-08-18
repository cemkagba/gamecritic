function updateRatingColors(){
    const ratingElements = document.querySelectorAll('[data-rating]');
    ratingElements.forEach(element => {
        const rating = parseFloat(element.dataset.rating);
        let colorClass = '';

         if (rating >= 4.0) {
            colorClass = 'text-green-600';
        } else if (rating >= 3.0) {
            colorClass = 'text-yellow-600';
        } else if (rating >= 2.0) {
            colorClass = 'text-orange-600';
        } else if (rating >= 1.0) {
           colorClass = 'text-orange-600';
        } else {
            colorClass = 'text-gray-500';
        }
        
        element.classList.remove('text-green-600', 'text-yellow-600', 'text-orange-600', 'text-red-500', 'text-red-600', 'text-gray-500');

        element.classList.add(colorClass);
    });
}
document.addEventListener('DOMContentLoaded', updateRatingColors);