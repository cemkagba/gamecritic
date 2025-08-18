/**
 * Description Toggle Functionality
 * Handles show more/less functionality for game descriptions
 */
document.addEventListener('DOMContentLoaded', function() {
    const descriptionContainer = document.getElementById('descriptionContent');
    const toggleButton = document.getElementById('toggleDescription');
    const toggleText = document.getElementById('toggleText');
    const toggleIcon = document.getElementById('toggleIcon');
    const fadeOverlay = document.getElementById('fadeOverlay');
    
    // Check if description is long enough to need toggle
    if (descriptionContainer && descriptionContainer.scrollHeight > 150) {
        // Show toggle button
        toggleButton.classList.remove('hidden');
        
        // Set initial collapsed state
        descriptionContainer.style.maxHeight = '150px';
        descriptionContainer.style.overflow = 'hidden';
        fadeOverlay.classList.remove('hidden');
        
        let isExpanded = false;
        
        toggleButton.addEventListener('click', function() {
            if (!isExpanded) {
                // Expand
                descriptionContainer.style.maxHeight = descriptionContainer.scrollHeight + 'px';
                setTimeout(() => {
                    descriptionContainer.style.maxHeight = 'none';
                    descriptionContainer.style.overflow = 'visible';
                }, 300);
                toggleText.textContent = 'Show Less';
                toggleIcon.style.transform = 'rotate(180deg)';
                fadeOverlay.classList.add('hidden');
                isExpanded = true;
            } else {
                // Collapse
                descriptionContainer.style.maxHeight = descriptionContainer.scrollHeight + 'px';
                setTimeout(() => {
                    descriptionContainer.style.maxHeight = '150px';
                    descriptionContainer.style.overflow = 'hidden';
                }, 10);
                toggleText.textContent = 'Show More';
                toggleIcon.style.transform = 'rotate(0deg)';
                fadeOverlay.classList.remove('hidden');
                isExpanded = false;
            }
        });
    }
});
