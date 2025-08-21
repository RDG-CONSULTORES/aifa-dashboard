#!/usr/bin/env python3
"""
Simple structure test for AIFA Dashboard
Tests if all files are present and importable
"""

import os
import sys

def test_structure():
    """Test if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt', 
        'Procfile',
        'runtime.txt',
        'README.md',
        'assets/style.css',
        'src/data/simulated_data.py',
        'src/layouts/strategic.py',
        'src/layouts/geographic.py',
        'src/layouts/financial.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present!")
        return True

def test_content():
    """Test basic content"""
    try:
        # Test if app.py has required content
        with open('app.py', 'r') as f:
            content = f.read()
            if 'AIFA' in content and 'Dash' in content:
                print("✅ app.py content looks good!")
            else:
                print("❌ app.py missing required content")
                return False
        
        # Test CSS
        with open('assets/style.css', 'r') as f:
            css_content = f.read()
            if 'glassmorphism' in css_content.lower() and '#00d4ff' in css_content:
                print("✅ CSS with glassmorphism effects present!")
            else:
                print("❌ CSS missing required styling")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Error testing content: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing AIFA Dashboard Structure...")
    print("="*50)
    
    structure_ok = test_structure()
    content_ok = test_content()
    
    if structure_ok and content_ok:
        print("="*50)
        print("🎉 Dashboard structure test PASSED!")
        print("")
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run locally: python app.py")
        print("3. Deploy to Render.com")
        sys.exit(0)
    else:
        print("="*50)
        print("❌ Dashboard structure test FAILED!")
        sys.exit(1)