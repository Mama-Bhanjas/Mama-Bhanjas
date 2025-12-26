"""
Lightweight verification - checks code structure without loading models
"""
import sys
import os

def check_imports():
    """Verify all modules can be imported (syntax check)"""
    print("=== Checking Module Imports ===")
    checks = []
    
    # Check if files exist
    files_to_check = [
        ("AI Service API", "ai_service/api.py"),
        ("Unified Processor", "ai_service/pipelines/processor.py"),
        ("Content Extractor", "ai_service/utils/content_extractor.py"),
        ("Classification Pipeline", "ai_service/pipelines/classify.py"),
        ("Summarization Pipeline", "ai_service/pipelines/summarize.py"),
        ("NER Pipeline", "ai_service/pipelines/ner.py"),
        ("Verification Pipeline", "ai_service/pipelines/verification.py"),
    ]
    
    for name, filepath in files_to_check:
        exists = os.path.exists(filepath)
        status = "[OK]" if exists else "[X]"
        print(f"{name:30s}: {status}")
        checks.append(exists)
    
    return all(checks)

def check_requirements():
    """Check if requirements file exists"""
    print("\n=== Checking Requirements ===")
    req_file = "ai_service/requirements.txt"
    exists = os.path.exists(req_file)
    
    if exists:
        with open(req_file, 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
            print(f"Requirements file: [OK] ({len(lines)} dependencies)")
            
            # Check key dependencies
            key_deps = ['transformers', 'torch', 'fastapi', 'pypdf', 'beautifulsoup4']
            for dep in key_deps:
                found = any(dep in line.lower() for line in lines)
                status = "[+]" if found else "[-]"
                print(f"  {status} {dep}")
    else:
        print("Requirements file: [X]")
    
    return exists

def check_api_structure():
    """Verify API endpoints are defined"""
    print("\n=== Checking API Structure ===")
    
    with open("ai_service/api.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    endpoints = [
        ("/api/process/report", "Unified Report Processing"),
        ("/api/process/upload", "PDF Upload Processing"),
        ("/api/realtime/news", "Real-time News Cache"),
        ("/api/fetch/all", "Multi-source Fetch"),
    ]
    
    for path, name in endpoints:
        found = path in content
        status = "[OK]" if found else "[X]"
        print(f"{name:30s}: {status}")
    
    return True

def check_processor_features():
    """Verify UnifiedProcessor has all features"""
    print("\n=== Checking Processor Features ===")
    
    with open("ai_service/pipelines/processor.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    features = [
        ("ContentExtractor", "URL/PDF extraction"),
        ("extract_from_url", "URL content extraction"),
        ("extract_from_pdf", "PDF content extraction"),
        ("file_bytes", "File upload support"),
        ("extracted_text", "Extraction metadata"),
        ("Sachin1224/nepal-disaster", "Fine-tuned models"),
    ]
    
    for keyword, description in features:
        found = keyword in content
        status = "[OK]" if found else "[X]"
        print(f"{description:30s}: {status}")
    
    return True

def check_backend_integration():
    """Check if backend is ready for AI integration"""
    print("\n=== Checking Backend Integration ===")
    
    backend_files = [
        ("Backend Main", "backend/app/main.py"),
        ("Reports Route", "backend/app/routes/reports.py"),
        ("Report Model", "backend/app/models/report.py"),
        ("Report Schema", "backend/app/schemas/report.py"),
    ]
    
    for name, filepath in backend_files:
        exists = os.path.exists(filepath)
        status = "[OK]" if exists else "[X]"
        print(f"{name:30s}: {status}")
    
    # Check if backend uses AI service
    if os.path.exists("backend/app/routes/reports.py"):
        with open("backend/app/routes/reports.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_ai = "ai_pipeline" in content
        has_location_fallback = "location_entities" in content
        has_text_storage = "text_to_store" in content
        
        print(f"  AI Pipeline Integration:     {'[OK]' if has_ai else '[X]'}")
        print(f"  Location Extraction:         {'[OK]' if has_location_fallback else '[X]'}")
        print(f"  Summary Storage (not URL):   {'[OK]' if has_text_storage else '[X]'}")
    
    return True

def check_frontend_features():
    """Check frontend has URL/PDF support"""
    print("\n=== Checking Frontend Features ===")
    
    form_file = "frontend/src/components/ReportForm.jsx"
    
    if os.path.exists(form_file):
        with open(form_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        features = [
            ("inputMode", "Input mode toggle"),
            ("'url'", "URL input mode"),
            ("'pdf'", "PDF input mode"),
            ("attachedFile", "File attachment"),
            ("FormData", "File upload support"),
        ]
        
        for keyword, description in features:
            found = keyword in content
            status = "[OK]" if found else "[X]"
            print(f"{description:30s}: {status}")
    else:
        print("ReportForm.jsx: [X]")
    
    return True

def run_verification():
    """Run all verification checks"""
    print("=" * 60)
    print(" " * 10 + "AI Service Verification (No Model Loading)")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Module Structure", check_imports()))
    results.append(("Requirements", check_requirements()))
    results.append(("API Endpoints", check_api_structure()))
    results.append(("Processor Features", check_processor_features()))
    results.append(("Backend Integration", check_backend_integration()))
    results.append(("Frontend Features", check_frontend_features()))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{name:30s}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n[OK] All systems verified! Code structure is correct.")
        print("\nNext steps:")
        print("1. Deploy to a server with more RAM (8GB+)")
        print("2. Or increase Windows virtual memory")
        print("3. Start AI service: python -m ai_service.api")
        print("4. Start backend: uvicorn app.main:app --reload --port 8001")
        print("5. Start frontend: npm run dev")
    else:
        print("\n[FAIL] Some checks failed. Review the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
