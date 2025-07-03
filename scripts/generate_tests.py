import os
import subprocess
import json
import yaml
from pathlib import Path

OLLAMA_HOST = "http://localhost:11434"
MODEL = "mistral"
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

def query_ollama(prompt_yaml, context):
    """Send request to Ollama API"""
    try:
        with open(prompt_yaml) as f:
            prompt_data = yaml.safe_load(f)
        
        messages = [
            {"role": "system", "content": prompt_data["system"]},
            {"role": "user", "content": prompt_data["user"].format(**context)}
        ]
        
        response = subprocess.run(
            ["curl", "-s", f"{OLLAMA_HOST}/api/chat", 
             "-d", json.dumps({
                 "model": MODEL,
                 "messages": messages,
                 "stream": False
             })],
            capture_output=True, text=True
        )
        
        if response.returncode != 0:
            raise RuntimeError(f"Ollama error: {response.stderr}")
        
        return json.loads(response.stdout)["message"]["content"]
    except Exception as e:
        print(f"Error in query_ollama: {str(e)}")
        raise

def run_tests(test_path):
    """Execute test script with proper permissions"""
    test_script = PROJECT_ROOT / "scripts" / "run_tests.sh"
    if not os.access(test_script, os.X_OK):
        os.chmod(test_script, 0o755)
    
    try:
        result = subprocess.run(
            [str(test_script), str(test_path)],
            cwd=PROJECT_ROOT,
            capture_output=True, 
            text=True
        )
        return result
    except PermissionError:
        print("Permission denied - trying to fix...")
        os.chmod(test_script, 0o755)
        return subprocess.run(
            [str(test_script), str(test_path)],
            cwd=PROJECT_ROOT,
            capture_output=True, 
            text=True
        )

def main():
    # Create directories
    (PROJECT_ROOT / "tests").mkdir(exist_ok=True)
    (PROJECT_ROOT / "instructions").mkdir(exist_ok=True)
    
    # Process each C++ file
    for cpp_file in (PROJECT_ROOT / "src").glob("*.cpp"):
        with open(cpp_file) as f:
            code = f.read()
        
        # Generate initial tests
        test_code = query_ollama(
            str(PROJECT_ROOT / "instructions" / "generate_tests.yaml"), 
            {"code": code}
        )
        
        test_path = PROJECT_ROOT / "tests" / f"test_{cpp_file.name}"
        with open(test_path, "w") as f:
            f.write(test_code)
        
        # Build and refine tests
        for attempt in range(3):
            result = run_tests(test_path)
            
            if result.returncode == 0:
                break
            
            # Fix tests
            test_code = query_ollama(
                str(PROJECT_ROOT / "instructions" / "fix_tests.yaml"), 
                {
                    "error_log": result.stderr,
                    "test_code": test_code
                }
            )
            with open(test_path, "w") as f:
                f.write(test_code)
        else:
            print(f"Failed to fix tests for {cpp_file} after 3 attempts")
            continue
        
        # Show coverage if successful
        coverage_file = PROJECT_ROOT / "coverage.txt"
        if coverage_file.exists():
            with open(coverage_file) as f:
                print(f.read())

if __name__ == "__main__":
    main()