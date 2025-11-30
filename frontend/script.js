document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('urlForm');
  const originalUrlInput = document.getElementById('originalUrl');
  const resultDiv = document.getElementById('result');
  const shortUrlAnchor = document.getElementById('shortUrl');
  const errorDiv = document.getElementById('error');

  // Константы для сообщений
  const ERROR_MESSAGES = {
    EMPTY_URL: 'Пожалуйста, введите URL',
    INVALID_URL: 'Некорректный URL',
    SERVER_ERROR: 'Произошла внутренняя ошибка сервера. Попробуйте ещё раз.',
    NETWORK_ERROR: 'Не удалось отправить запрос. Проверьте соединение.',
  };

  // Константы для API
  const API_BASE_URL = 'http://localhost:8000';

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    resetUI();

    const originalUrl = originalUrlInput.value.trim();
    
    if (!originalUrl) {
      showError(ERROR_MESSAGES.EMPTY_URL);
      return;
    }

    await shortenUrl(originalUrl);
  });

  async function shortenUrl(url) {
    try {
      const response = await fetch(`${API_BASE_URL}/slug`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ original_url: url })
      });

      if (!response.ok) {
        await handleErrorResponse(response);
        return;
      }

      await handleSuccessResponse(response);
    } catch (err) {
      showError(ERROR_MESSAGES.NETWORK_ERROR);
    }
  }

  async function handleErrorResponse(response) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage = errorData.detail || response.statusText;
    
    switch (response.status) {
      case 400:
        showError(`${ERROR_MESSAGES.INVALID_URL}: ${errorMessage}`);
        break;
      case 500:
        showError(ERROR_MESSAGES.SERVER_ERROR);
        break;
      default:
        showError(`Ошибка: ${errorMessage}`);
    }
  }

  async function handleSuccessResponse(response) {
    const data = await response.json();
    const shortUrl = `${API_BASE_URL}/${encodeURIComponent(data.slug)}`;
    
    shortUrlAnchor.textContent = shortUrl;
    shortUrlAnchor.href = shortUrl;
    resultDiv.classList.remove('hidden');
  }

  function resetUI() {
    errorDiv.classList.add('hidden');
    resultDiv.classList.add('hidden');
    shortUrlAnchor.textContent = '';
    shortUrlAnchor.href = '#';
  }

  function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
  }
});
