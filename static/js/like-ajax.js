document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form.like-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const btn = form.querySelector('.like-button');
      const url = form.action;
      const csrf = form.querySelector('[name=csrfmiddlewaretoken]')?.value;
      const formData = new FormData(form);

      try {
        const res = await fetch(url, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf
          },
          body: formData,
          credentials: 'same-origin'
        });
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        if (!data.success) throw new Error('Like failed');

        // UI update
        const card = form.closest(`[class*="review-box-"]`) || document;
        const countEl = card.querySelector('.like-count') || form.querySelector('.like-count');
        const svg = btn.querySelector('svg');

        if (data.liked) {
          btn.classList.remove('bg-gray-100','text-gray-600','hover:bg-gray-200');
          btn.classList.add('bg-red-100','text-red-600','hover:bg-red-200');
          if (svg) svg.setAttribute('fill', 'currentColor');
        } else {
          btn.classList.remove('bg-red-100','text-red-600','hover:bg-red-200');
          btn.classList.add('bg-gray-100','text-gray-600','hover:bg-gray-200');
          if (svg) svg.setAttribute('fill', 'none');
        }
        if (countEl) countEl.textContent = `${data.like_count}`;
      } catch (err) {
        console.error(err);
        alert('Could not toggle like. Please try again.');
      }
    });
  });
});