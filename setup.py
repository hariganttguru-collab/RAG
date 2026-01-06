<<<<<<< HEAD
#!/usr/bin/env python
"""
Setup script to initialize the project
Run: python setup.py
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*50)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("Project Management Learning Portal - Setup")
    print("="*50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\nCreating .env file from .env.example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✓ .env file created. Please update it with your settings.")
        else:
            print("⚠ .env.example not found. Creating basic .env file...")
            with open('.env', 'w') as f:
                f.write("SECRET_KEY=django-insecure-change-this-in-production\n")
                f.write("OPENAI_API_KEY=your-openai-api-key-here\n")
                f.write("DEBUG=True\n")
            print("✓ Basic .env file created. Please update it with your settings.")
    else:
        print("✓ .env file already exists")
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        print("\n❌ Migration failed. Please check the error above.")
        sys.exit(1)
    
    # Initialize stakeholders
    if not run_command("python manage.py init_stakeholders", "Initializing stakeholders"):
        print("\n⚠ Stakeholder initialization had issues, but continuing...")
    
    print("\n" + "="*50)
    print("Setup complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Update .env file with your OpenAI API key")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the server: python manage.py runserver")
    print("   Or with WebSocket support: daphne -b 0.0.0.0 -p 8000 config.asgi:application")
    print("\nTo create a sample project for a user:")
    print("   python manage.py create_sample_project <username>")

if __name__ == '__main__':
    main()

=======
#!/usr/bin/env python
"""
Setup script to initialize the project
Run: python setup.py
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*50)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("Project Management Learning Portal - Setup")
    print("="*50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\nCreating .env file from .env.example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✓ .env file created. Please update it with your settings.")
        else:
            print("⚠ .env.example not found. Creating basic .env file...")
            with open('.env', 'w') as f:
                f.write("SECRET_KEY=django-insecure-change-this-in-production\n")
                f.write("OPENAI_API_KEY=your-openai-api-key-here\n")
                f.write("DEBUG=True\n")
            print("✓ Basic .env file created. Please update it with your settings.")
    else:
        print("✓ .env file already exists")
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        print("\n❌ Migration failed. Please check the error above.")
        sys.exit(1)
    
    # Initialize stakeholders
    if not run_command("python manage.py init_stakeholders", "Initializing stakeholders"):
        print("\n⚠ Stakeholder initialization had issues, but continuing...")
    
    print("\n" + "="*50)
    print("Setup complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Update .env file with your OpenAI API key")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the server: python manage.py runserver")
    print("   Or with WebSocket support: daphne -b 0.0.0.0 -p 8000 config.asgi:application")
    print("\nTo create a sample project for a user:")
    print("   python manage.py create_sample_project <username>")

if __name__ == '__main__':
    main()

>>>>>>> 58d64fddec4673e0a29d46ffd423ba18536a63a1
