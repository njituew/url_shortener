# URL Shortener

A web service for shortening long URLs, built with FastAPI backend and a simple HTML/CSS/JavaScript frontend. The service uses PostgreSQL as the database and is containerized with Docker for easy deployment.

## Features

- Shorten long URLs into compact slugs
- Redirect to original URLs using the generated slugs
- RESTful API for URL shortening
- Web interface for easy URL shortening
- Docker containerization for seamless deployment
- Comprehensive test suite

## Prerequisites

- Docker
- Docker Compose

## Installation and Launch

1. Clone the repository:
   ```bash
   git clone https://github.com/njituew/url_shortener.git
   cd url_shortener
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL database on port 6432
   - Backend API on port 8000
   - Frontend on port 3000

3. Open your browser and navigate to `http://localhost:3000` to access the web interface.

## Usage

### Web Interface

1. Open `http://localhost:3000` in your browser
2. Enter a long URL in the input field
3. Click "Сократить" (Shorten)
4. Copy the generated short URL

### API Usage

The API provides endpoints for programmatic access:

#### Shorten a URL

```bash
curl -X POST "http://localhost:8000/slug" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://example.com"}'
```

Response:
```json
{
  "slug": "abc123",
  "original_url": "https://example.com"
}
```

#### Redirect to Original URL

```bash
curl -L "http://localhost:8000/abc123"
```

This will redirect to the original URL.

#### Clear All URLs (Admin)

```bash
curl -X DELETE "http://localhost:8000/clear_urls"
```

## API Endpoints

- `POST /slug` - Create a short URL
  - Body: `{"original_url": "string"}`
  - Response: `{"slug": "string", "original_url": "string"}`

- `GET /{slug}` - Redirect to original URL
  - Response: 302 redirect to original URL

- `DELETE /clear_urls` - Clear all URL pairs (admin endpoint)

## Testing

Run the test suite:

```bash
docker-compose exec backend pytest
```

Or run tests locally (requires Python and dependencies):

```bash
cd backend
pip install -r ../requirements.txt
pytest
```

## Project Structure

```
url_shortener/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── db/
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── database.py      # Database configuration
│   │   └── crud.py          # Database operations
│   └── src/
│       ├── service.py       # Business logic
│       ├── short_url.py     # Slug generation
│       ├── url_validator.py # URL validation
│       ├── exception.py     # Custom exceptions
│       ├── dependencies.py  # FastAPI dependencies
│       └── lifespan.py      # Application lifespan events
├── frontend/
│   ├── index.html           # Main page
│   ├── style.css            # Styles
│   └── script.js            # Frontend logic
├── tests/                   # Test files
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile.backend       # Backend container
├── Dockerfile.frontend      # Frontend container
├── requirements.txt         # Python dependencies
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
