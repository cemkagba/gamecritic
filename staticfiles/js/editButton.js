// Edit Button Functionality for Profile Page
function toggleEditForm(postId) {
    const form = document.getElementById('edit-form-' + postId);

    if (!form) {
        console.error('Edit form not found for post ID:', postId);
        return;
    }

    if (form.classList.contains('hidden')) {
        document.querySelectorAll('[id^="edit-form-"]').forEach(f => {
            f.classList.add('hidden');
        });

        form.classList.remove('hidden');

    } else {
        form.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('click', function(event) {
        const editButton = event.target.closest('.edit-button');
        if (editButton) {
            event.preventDefault();
            const postId = editButton.dataset.postId;
            if (postId) {
                toggleEditForm(parseInt(postId, 10));
            }
        }
    });

    document.body.addEventListener('mouseover', function(event) {
        const editButton = event.target.closest('.edit-button');
        if (editButton) {
            editButton.style.transform = 'scale(1.05)';
        }
    });

    document.body.addEventListener('mouseout', function(event) {
        const editButton = event.target.closest('.edit-button');
        if (editButton) {
            editButton.style.transform = 'scale(1)';
        }
    });
});
