"""
TDOS Entry Point
"""

import uvicorn

from database.database import initialize_database


if __name__ == "__main__":

    initialize_database()

    uvicorn.run(

        "api:app",

        host="127.0.0.1",

        port=8000,

        reload=True,

    )