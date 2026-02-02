#!/usr/bin/env python3
"""
AgroGrade AI - Project Initialization Script
Automated setup for new developers and deployment
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import List, Dict

class ProjectInitializer:
    def __init__(self):
        self.repo_path = Path.cwd()
        self.steps = []
        print("🌾 AgroGrade AI - Project Initialization")
        print("=" * 50)
    
    def run_command(self, command: List[str], description: str) -> bool:
        """Run command and handle errors"""
        try:
            print(f"\n🔧 {description}...")
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ {description} completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed:")
            print(f"Error: {e.stderr}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Check if prerequisites are installed"""
        print("\n📋 Checking prerequisites...")
        
        # Check Python
        try:
            python_version = subprocess.run(
                [sys.executable, "--version"],
                capture_output=True,
                text=True
            )
            print(f"✅ Python: {python_version.stdout.strip()}")
        except:
            print("❌ Python not found. Please install Python 3.12+")
            return False
        
        # Check Node.js
        try:
            node_result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True
            )
            print(f"✅ Node.js: {node_result.stdout.strip()}")
        except:
            print("❌ Node.js not found. Please install Node.js 18+")
            return False
        
        # Check npm
        try:
            npm_result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True
            )
            print(f"✅ npm: {npm_result.stdout.strip()}")
        except:
            print("❌ npm not found. Please install npm")
            return False
        
        return True
    
    def setup_backend(self) -> bool:
        """Setup backend environment"""
        print("\n🐍 Setting up backend...")
        
        # Navigate to backend
        backend_path = self.repo_path / "backend"
        if not backend_path.exists():
            print("❌ Backend directory not found")
            return False
        
        # Create virtual environment
        venv_path = backend_path / "venv"
        if not venv_path.exists():
            if not self.run_command(
                [sys.executable, "-m", "venv", "venv"],
                "Creating virtual environment"
            ):
                return False
        
        # Activate virtual environment and install dependencies
        if os.name == 'nt':  # Windows
            pip_executable = venv_path / "Scripts" / "pip"
        else:  # Unix
            pip_executable = venv_path / "bin" / "pip"
        
        # Install requirements
        requirements_files = [
            "requirements.txt"
        ]
        
        for req_file in requirements_files:
            req_path = backend_path / req_file
            if req_path.exists():
                if not self.run_command(
                    [str(pip_executable), "install", "-r", req_file],
                    f"Installing {req_file}"
                ):
                    return False
        
        return True
    
    def setup_frontend(self) -> bool:
        """Setup frontend environment"""
        print("\n⚛️ Setting up frontend...")
        
        # Install npm dependencies
        if not self.run_command(
            ["npm", "install"],
            "Installing frontend dependencies"
        ):
            return False
        
        return True
    
    def setup_database(self) -> bool:
        """Setup database"""
        print("\n🗄️ Setting up database...")
        
        # Check if PostgreSQL is available
        try:
            subprocess.run(
                ["psql", "--version"],
                capture_output=True,
                check=True
            )
            print("✅ PostgreSQL found")
        except:
            print("⚠️ PostgreSQL not found. Using SQLite for development")
            return True
        
        return True
    
    def download_models(self) -> bool:
        """Download or create AI models"""
        print("\n🤖 Setting up AI models...")
        
        backend_path = self.repo_path / "backend"
        
        # Run simple training demo to create initial model
        if not self.run_command(
            [sys.executable, "simple_training_demo.py"],
            "Creating initial AI model"
        ):
            print("⚠️ Model creation failed, but continuing...")
        
        return True
    
    def create_env_file(self) -> bool:
        """Create environment configuration"""
        print("\n⚙️ Creating environment configuration...")
        
        env_content = """# AgroGrade AI Environment Configuration

# Database
DATABASE_URL=sqlite:///./agrograde.db

# API Settings
API_HOST=localhost
API_PORT=8000
ENVIRONMENT=development

# AI Model Settings
MODEL_PATH=ai_models/model_weights/
CONFIDENCE_THRESHOLD=0.7
MAX_IMAGE_SIZE=10485760  # 10MB

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000

# Logging
LOG_LEVEL=INFO
"""
        
        env_path = self.repo_path / "backend" / ".env"
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ Environment file created")
        return True
    
    def verify_setup(self) -> bool:
        """Verify that setup was successful"""
        print("\n🔍 Verifying setup...")
        
        # Check backend
        backend_path = self.repo_path / "backend"
        venv_path = backend_path / "venv"
        
        if venv_path.exists():
            print("✅ Backend virtual environment created")
        else:
            print("❌ Backend virtual environment not found")
            return False
        
        # Check frontend
        node_modules = self.repo_path / "node_modules"
        if node_modules.exists():
            print("✅ Frontend dependencies installed")
        else:
            print("❌ Frontend dependencies not found")
            return False
        
        return True
    
    def provide_next_steps(self):
        """Show next steps for the user"""
        print("\n🎉 Initialization completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Start the servers:")
        print("   python start_servers.py")
        print("\n2. Or start manually:")
        print("   Backend: cd backend && venv\\Scripts\\activate && python main.py")
        print("   Frontend: npm run dev")
        print("\n3. Open your browser:")
        print("   Frontend: http://localhost:8080")
        print("   Backend API: http://localhost:8000")
        print("   AI Analysis: http://localhost:8080/ai-analysis")
        print("\n4. Test the AI:")
        print("   Upload a leaf image and get instant disease detection!")
        print("\n📚 For more information, see README.md")
    
    def initialize(self):
        """Run complete initialization"""
        print(f"📁 Repository: {self.repo_path}")
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("\n❌ Prerequisites not met. Please install required software.")
            return False
        
        # Setup components
        steps = [
            ("Backend Setup", self.setup_backend),
            ("Frontend Setup", self.setup_frontend),
            ("Database Setup", self.setup_database),
            ("AI Models Setup", self.download_models),
            ("Environment Setup", self.create_env_file),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            if not step_func():
                print(f"❌ {step_name} failed")
                return False
        
        # Verify setup
        if not self.verify_setup():
            print("\n❌ Setup verification failed")
            return False
        
        # Provide next steps
        self.provide_next_steps()
        
        return True


def main():
    """Main initialization function"""
    initializer = ProjectInitializer()
    
    try:
        success = initializer.initialize()
        if success:
            print("\n🎊 Project initialization completed successfully!")
            print("🚀 AgroGrade AI is ready to use!")
        else:
            print("\n❌ Project initialization failed")
            print("📞 Please check the error messages above and try again")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
