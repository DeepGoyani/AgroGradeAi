#!/usr/bin/env python3
"""
AgroGrade AI - Server Startup Script
Starts both backend and frontend servers simultaneously
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from typing import Optional

class ServerManager:
    def __init__(self):
        self.repo_path = Path.cwd()
        self.backend_process: Optional[subprocess.Popen] = None
        self.frontend_process: Optional[subprocess.Popen] = None
        print("🚀 AgroGrade AI - Server Startup")
        print("=" * 40)
    
    def start_backend(self) -> bool:
        """Start the FastAPI backend server"""
        print("\n🐍 Starting backend server...")
        
        backend_path = self.repo_path / "backend"
        venv_path = backend_path / "venv"
        
        # Check if virtual environment exists
        if not venv_path.exists():
            print("❌ Backend virtual environment not found")
            print("💡 Run 'python init_project.py' first")
            return False
        
        # Determine Python executable
        if os.name == 'nt':  # Windows
            python_executable = venv_path / "Scripts" / "python"
        else:  # Unix
            python_executable = venv_path / "bin" / "python"
        
        # Start backend server
        try:
            self.backend_process = subprocess.Popen(
                [str(python_executable), "main.py"],
                cwd=backend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("✅ Backend server starting...")
            print(f"📍 Backend URL: http://localhost:8000")
            print(f"📖 API Docs: http://localhost:8000/docs")
            
            return True
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self) -> bool:
        """Start the React frontend server"""
        print("\n⚛️ Starting frontend server...")
        
        # Check if node_modules exists
        node_modules = self.repo_path / "node_modules"
        if not node_modules.exists():
            print("❌ Frontend dependencies not installed")
            print("💡 Run 'python init_project.py' first")
            return False
        
        # Start frontend server
        try:
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("✅ Frontend server starting...")
            print(f"📍 Frontend URL: http://localhost:8080")
            print(f"🌾 AI Analysis: http://localhost:8080/ai-analysis")
            
            return True
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def wait_for_servers(self):
        """Wait for servers to be ready"""
        print("\n⏳ Waiting for servers to start...")
        
        # Wait for backend
        backend_ready = False
        frontend_ready = False
        
        for i in range(30):  # Wait up to 30 seconds
            try:
                import requests
                
                # Check backend
                if not backend_ready:
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        backend_ready = True
                        print("✅ Backend server is ready!")
                
                # Check frontend
                if not frontend_ready:
                    response = requests.get("http://localhost:8080", timeout=2)
                    if response.status_code == 200:
                        frontend_ready = True
                        print("✅ Frontend server is ready!")
                
                if backend_ready and frontend_ready:
                    break
                    
            except:
                pass
            
            time.sleep(1)
            print(f"⏳ Waiting... ({i+1}/30)")
        
        if not backend_ready:
            print("⚠️ Backend server may not be ready yet")
        
        if not frontend_ready:
            print("⚠️ Frontend server may not be ready yet")
    
    def show_status(self):
        """Show server status and access information"""
        print("\n" + "="*50)
        print("🎉 AgroGrade AI Servers are Running!")
        print("="*50)
        print("\n📱 Access Points:")
        print("🌐 Frontend: http://localhost:8080")
        print("🤖 AI Analysis: http://localhost:8080/ai-analysis")
        print("🔧 Backend API: http://localhost:8000")
        print("📖 API Documentation: http://localhost:8000/docs")
        print("💚 Health Check: http://localhost:8000/health")
        
        print("\n🚀 Quick Test:")
        print("1. Open http://localhost:8080/ai-analysis")
        print("2. Upload a leaf image")
        print("3. Click 'Analyze Leaf'")
        print("4. Get AI disease detection results!")
        
        print("\n🛑 To stop servers:")
        print("Press Ctrl+C or close this terminal")
    
    def monitor_servers(self):
        """Monitor servers and handle shutdown"""
        print("\n👀 Monitoring servers... (Press Ctrl+C to stop)")
        
        try:
            while True:
                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend server stopped unexpectedly")
                    break
                
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend server stopped unexpectedly")
                    break
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
        finally:
            self.stop_servers()
    
    def stop_servers(self):
        """Stop all running servers"""
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except:
                self.backend_process.kill()
                print("✅ Backend server forced to stop")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except:
                self.frontend_process.kill()
                print("✅ Frontend server forced to stop")
    
    def start_all(self):
        """Start all servers"""
        print(f"📁 Working directory: {self.repo_path}")
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Start frontend
        if not self.start_frontend():
            self.stop_servers()
            return False
        
        # Wait for servers to be ready
        self.wait_for_servers()
        
        # Show status
        self.show_status()
        
        # Monitor servers
        self.monitor_servers()
        
        return True


def main():
    """Main startup function"""
    manager = ServerManager()
    
    # Set up signal handler for graceful shutdown
    def signal_handler(signum, frame):
        print("\n🛑 Shutdown signal received")
        manager.stop_servers()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        success = manager.start_all()
        if not success:
            print("\n❌ Failed to start servers")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Servers stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        manager.stop_servers()
        sys.exit(1)


if __name__ == "__main__":
    main()
