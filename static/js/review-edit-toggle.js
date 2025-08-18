/**
 * Review Edit Form Toggle Functionality
 * Handles show/hide functionality for review edit forms
 */

function toggleEditForm(postId) {
    const editForm = document.getElementById(`edit-form-${postId}`);
    
    if (editForm) {
        if (editForm.classList.contains('hidden')) {
            editForm.classList.remove('hidden');
            // Scroll to form
            editForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            editForm.classList.add('hidden');
        }
    }
}
