import os
import subprocess
import json
import yaml
from pathlib import Path

OLLAMA_HOST = "http://localhost:11434"
MODEL = "mistral"

def query_ollama(prompt_yaml, context):
    """Send request to Ollama API"""
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

def main():
    # Create directories
    Path("tests").mkdir(exist_ok=True)
    Path("instructions").mkdir(exist_ok=True)
    
    # Process each C++ file
    for cpp_file in Path("src").glob("*.cpp"):
        with open(cpp_file) as f:
            code = f.read()
        
        # Generate initial tests
        test_code = query_ollama("instructions/generate_tests.yaml", {"code": code})
        
        test_path = Path("tests") / f"test_{cpp_file.name}"
        with open(test_path, "w") as f:
            f.write(test_code)
        
        # Build and refine tests
        for attempt in range(3):  # Max 3 fix attempts
            result = subprocess.run(
                ["./scripts/run_tests.sh", test_path],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                break  # Build succeeded
            
            # Fix tests
            test_code = query_ollama("instructions/fix_tests.yaml", {
                "error_log": result.stderr,
                "test_code": test_code
            })
            with open(test_path, "w") as f:
                f.write(test_code)
        else:
            print(f"Failed to fix tests for {cpp_file} after 3 attempts")

if __name__ == "__main__":
    main()