import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# Load environment variables (this is safe to do at module level)
load_dotenv()

# Get the API key but don't fail if it's not available yet
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Lazy initialization of OpenAI client
def get_openai_client():
    global OPENAI_API_KEY
    if not OPENAI_API_KEY:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    return openai.OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = '''You are a helpful, creative book assistant for families and educators. When asked to generate a story page, always reply in this format:

Story Text:
<the text that should appear in the book, for children to read>

Image Prompt:
<a vivid, visual description for DALL·E, including any text to overlay, e.g. 'A little girl in a lavender dress, running through a field at sunset, with the words: "You are brave."'>

Do not include any other commentary or instructions. Only output these two sections, clearly labeled. The image prompt should be suitable for DALL·E 3 and include overlay text if appropriate.'''

app = FastAPI()

# Add startup event to check configuration
@app.on_event("startup")
async def startup_event():
    try:
        # Try to get the API key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print(f"✅ OpenAI API key configured (length: {len(api_key)})")
        else:
            print("⚠️ OpenAI API key not found in environment variables")
    except Exception as e:
        print(f"❌ Startup error: {e}")

# Allow CORS for local dev and your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: list

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        # Get OpenAI client (lazy initialization)
        client = get_openai_client()
        
        # Prepend system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + req.messages
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=512,
            temperature=0.8,
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        # Return detailed error for debugging
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate-image")
async def generate_image(req: ImageRequest):
    try:
        # Get OpenAI client (lazy initialization)
        client = get_openai_client()
            
        response = client.images.generate(
            model="dall-e-3",
            prompt=req.prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation error: {str(e)}")

# Add a simple health check and serve the main page
@app.get("/")
async def serve_index():
    return FileResponse("index.html")

# Serve static files
@app.get("/app.js")
async def serve_app_js():
    return FileResponse("app.js")

@app.get("/config.js")
async def serve_config_js():
    return FileResponse("config.js")

# API endpoint for health check
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Jongu Kids Book Builder API is running"}

# Debug endpoint to check environment
@app.get("/api/debug")
async def debug_info():
    current_key = os.getenv("OPENAI_API_KEY")
    return {
        "status": "ok",
        "openai_key_configured": bool(current_key),
        "openai_key_length": len(current_key) if current_key else 0,
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# For Vercel deployment - keep this at the end
handler = app