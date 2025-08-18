function TextUpdateByAvg(){
    const ratingElements = document.querySelectorAll('[data-text]');
    ratingElements.forEach(element => {
        const rating = parseFloat(element.dataset.text);
        let colorClass = '';
        let textContent = '';
         if (rating >= 4.5) {
            colorClass = 'text-green-600';
            textContent = 'Fantastic';
        } else if (rating >= 3.5) {
            colorClass = 'text-green-600';
            textContent = 'Great';
        } else if (rating >= 2.5) {
            colorClass = 'text-yellow-600';
            textContent = 'Okay';
        } else if (rating >= 1.5) {
            colorClass = 'text-orange-600';
            textContent = 'Meh';
        } else if (rating >= 1.0) { 
           colorClass = 'text-red-600';
           textContent = 'Awful';
        } else {
            colorClass = 'text-gray-500';
            textContent = 'No Rating';
        }
        
        element.classList.remove('text-green-600', 'text-yellow-600', 'text-orange-600', 'text-red-500', 'text-red-600', 'text-gray-500');

        element.classList.add(colorClass);
        element.textContent = textContent;
    });
}
document.addEventListener('DOMContentLoaded', TextUpdateByAvg);