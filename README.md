# Jongu Kids Book Builder

A FastAPI-powered web application for creating interactive children's books with AI-generated content and images.

## Features

- Interactive chat with GPT-4 for story creation
- DALL-E 3 image generation
- Page management and preview
- PDF export functionality
- Modern, responsive UI

## Deployment to Vercel

### Prerequisites

1. OpenAI API key
2. Vercel account
3. Git repository

### Steps

1. **Set Environment Variables in Vercel:**
   - Go to your Vercel project dashboard
   - Navigate to Settings → Environment Variables
   - Add: `OPENAI_API_KEY` with your OpenAI API key

2. **Deploy:**
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push
   ```
   
   Or use Vercel CLI:
   ```bash
   vercel --prod
   ```

### Important Files

- `vercel.json` - Vercel deployment configuration
- `main.py` - FastAPI backend with API endpoints
- `requirements.txt` - Python dependencies
- `config.js` - Frontend API endpoint configuration
- `index.html` - Main application interface
- `app.js` - Frontend JavaScript logic

### API Endpoints

- `GET /` - Health check
- `POST /chat` - Chat with GPT-4
- `POST /generate-image` - Generate images with DALL-E 3

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. Open `index.html` in a browser

## Troubleshooting

- **Environment Variables**: Make sure `OPENAI_API_KEY` is set in Vercel dashboard
- **CORS Issues**: The app allows all origins for development
- **API Calls**: Frontend automatically detects deployment environment
- **File Structure**: Make sure all files are in the root directory
