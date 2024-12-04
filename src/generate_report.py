import os
import sys
import subprocess
import json

def generate_report(subjectid):
    try:
        result = subprocess.run([
            'jupyter', 'nbconvert', 
            '--to', 'html', 
            '--execute', 
            f'--ExecutePreprocessor.kernel_name=python{sys.version_info.major}.{sys.version_info.minor}',
            '--output-dir', 'reports',
            f'--env', f'SUBJECTID={subjectid}',
            'TMLDNreport.ipynb'
        ], capture_output=True, text=True)
        
        return result.returncode == 0
    except Exception:
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    
    subjectid = sys.argv[1]
    success = generate_report(subjectid)
    sys.exit(0 if success else 1)
