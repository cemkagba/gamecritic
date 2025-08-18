document.addEventListener('DOMContentLoaded', function() {
    // Only run if the img-upload element exists on this page
    const imgUploadElement = document.getElementById('img-upload');
    
    if (imgUploadElement) {
        imgUploadElement.addEventListener('change', function (event) {
            const [file] = event.target.files;
            if (file) {
                const profileImg = document.getElementById('profile-img');
                if (profileImg) {
                    profileImg.src = URL.createObjectURL(file);
                }
            }
        });
    }
});
