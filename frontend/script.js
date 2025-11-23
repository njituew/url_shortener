document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('urlForm');
  const originalUrlInput = document.getElementById('originalUrl');
  const resultDiv = document.getElementById('result');
  const shortUrlAnchor = document.getElementById('shortUrl');
  const errorDiv = document.getElementById('error');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorDiv.classList.add('hidden');
    resultDiv.classList.add('hidden');
    shortUrlAnchor.textContent = '';
    shortUrlAnchor.href = '#';

    const originalUrl = originalUrlInput.value.trim();
    if (!originalUrl) {
      showError('Пожалуйста, введите URL');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/slug', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ original_url: originalUrl })
      });

      if (!response.ok) {
        if (response.status === 400) {
          showError('Введён некорректный URL.');
        } else if (response.status === 500) {
          showError('Произошла внутренняя ошибка сервера. Попробуйте ещё раз.');
        } else {
          showError(`Ошибка: ${response.statusText}`);
        }
        return;
      }

      const data = await response.json();
      // Construct the full shortened URL using backend server + /:slug
      const shortUrl = `http://localhost:8000/${encodeURIComponent(data.slug)}`;
      shortUrlAnchor.textContent = shortUrl;
      shortUrlAnchor.href = shortUrl;
      resultDiv.classList.remove('hidden');
    } catch (err) {
      showError('Не удалось отправить запрос. Проверьте соединение.');
    }
  });

  function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
  }
});
