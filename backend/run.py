#!/usr/bin/env python
"""
Entry point for running the Hogwarts House Points System backend.
This script provides a convenient way to start the application
with different configurations.
"""

import os
import argparse
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Hogwarts API")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload on code changes")
    parser.add_argument("--env", type=str, default="dev", choices=["dev", "test", "prod"], 
                        help="Environment to run the application in")
    
    args = parser.parse_args()
    
    # Set environment based on args
    os.environ["APP_ENV"] = args.env
    
    print(f"Starting Hogwarts API in {args.env} mode on {args.host}:{args.port}")
    
    uvicorn.run(
        "app.main:app", 
        host=args.host, 
        port=args.port, 
        reload=args.reload,
        log_level="info"
    ) 