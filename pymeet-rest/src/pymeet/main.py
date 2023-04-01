"""
Applicant Main File.
"""
import uvicorn

from pymeet.app.asgi import get_application

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app)
