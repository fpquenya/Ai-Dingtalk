# AI-Dingtalk News Management System

A web-based news management system integrated with DingTalk AI assistant.

## Features

- **AI Assistant Integration**: Embedded DingTalk AI assistant for intelligent interactions
- **News Management**: Add, edit, delete, and organize news articles
- **Search & Filter**: Real-time search functionality for news articles
- **Responsive Design**: Mobile-friendly interface
- **Data Persistence**: JSON-based data storage with automatic backup
- **Statistics**: View news statistics and analytics

## Project Structure

```
AI-Dingtalk/
├── index.html          # Main page with AI assistant and news display
├── news_page.html      # News management interface
├── news_server.py      # Python HTTP server backend
├── news_manager.py     # News management utilities
├── news.json          # News data storage
└── README.md          # Project documentation
```

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fpquenya/Ai-Dingtalk.git
   cd Ai-Dingtalk
   ```

2. **Start the server**:
   ```bash
   python news_server.py
   ```

3. **Access the application**:
   - Main page: http://localhost:8000
   - News management: http://localhost:8000/news_page.html

## Usage

### Main Interface
- Access the DingTalk AI assistant through the embedded iframe
- View latest news updates in the bottom section

### News Management
- Add new news articles with title and URL
- Search through existing news articles
- Sort news by date (newest/oldest first)
- Edit or delete existing news entries
- Export/import news data

## API Endpoints

- `GET /news.json` - Retrieve all news data
- `POST /api/news` - Save news data
- `GET /api/stats` - Get news statistics

## Technical Details

- **Backend**: Python HTTP server with custom request handlers
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Data Storage**: JSON files with automatic backup
- **CORS**: Enabled for cross-origin requests

## Requirements

- Python 3.6+
- Modern web browser
- Internet connection (for DingTalk AI assistant)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.