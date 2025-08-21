/**
 * Video Modal Functionality
 * Handles YouTube video modal opening/closing
 */

function openVideoModal(videoId, title) {
    const modal = document.getElementById('videoModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalVideo = document.getElementById('modalVideo');
    
    modalTitle.textContent = title;
    modalVideo.src = "https://www.youtube.com/embed/${videoId}";
    modal.classList.remove('hidden');
    
}

function closeVideoModal() {
    const modal = document.getElementById('videoModal');
    const modalVideo = document.getElementById('modalVideo');
    
    modalVideo.src = '';
    modal.classList.add('hidden');
}

// Close with ESC key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeVideoModal();
    }
});
