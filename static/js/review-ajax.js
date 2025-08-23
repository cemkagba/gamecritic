// Review Edit AJAX (single copy)
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[id^="edit-form-"] form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const postId = form.closest('[id^="edit-form-"]').id.replace('edit-form-', '');
      const url = form.action;
      const formData = new FormData(form);

      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData,
        credentials: 'same-origin'
      })
      .then(async (res) => {
        if (!res.ok) {
          const text = await res.text();
          throw new Error(text);
        }
        return res.json();
      })
      .then((data) => {
        if (!data.success) {
          // form hataları
          let errorMsg = '';
          for (let field in data.errors) errorMsg += data.errors[field].join('<br>') + '<br>';
          let errorDiv = form.querySelector('.ajax-error');
          if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'ajax-error text-red-600 text-sm mt-2';
            form.appendChild(errorDiv);
          }
          errorDiv.innerHTML = errorMsg;
          return;
        }

        const reviewBox = form.closest('.bg-gray-50');

        // Başlık (profile’da “Title : …” şeklinde; iki durumu da destekle)
        const titleEl = reviewBox.querySelector('h4');
        if (titleEl) {
          const label = titleEl.textContent.includes(':') ? titleEl.textContent.split(':')[0] + ' : ' : '';
          titleEl.textContent = `${label}${data.review.title}`;
        }

        // Açıklama: sadece bu review’a ait kapsayıcıyı güncelle
        const descEl = reviewBox.querySelector(`.review-description-${postId}`) ||
                       reviewBox.querySelector('p.text-gray-700');
        if (descEl) descEl.innerHTML = data.review.description;

        // Rating: id’li varsa onu, yoksa genel sınıfı güncelle
        const ratingEl = reviewBox.querySelector(`.review-rating-${postId}`) ||
                         reviewBox.querySelector('.review-rating');
        if (ratingEl) ratingEl.textContent = `Rating : ${data.review.rating}/5`;

        // Tarih: extra_details’ta var, profile’da yok → varsa güncelle
        const updatedAtEl = reviewBox.querySelector('.text-xs.text-gray-500,[data-updated-at]');
        if (updatedAtEl) updatedAtEl.textContent = data.review.updated_at;

        // Formu kapat
        form.closest('[id^="edit-form-"]').classList.add('hidden');
      })
      .catch((err) => {
        console.error(err);
        alert('An error occurred. Please try again.');
      });
    });
  });
});
