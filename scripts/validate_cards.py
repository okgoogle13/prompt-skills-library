import yaml
import sys
import glob
import os

def validate_card(filepath, required_type):
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error parsing YAML in {filepath}: {e}")
        return False
    
    if not data or required_type not in data:
        print(f"Error: {filepath} missing root key '{required_type}'")
        return False
        
    card = data[required_type]
    required_keys = ['id', 'title', 'version', 'status']
    
    missing_keys = [k for k in required_keys if k not in card or not card[k]]
    if missing_keys:
        print(f"Error: {filepath} missing required keys: {missing_keys}")
        return False
        
    print(f"PASS: {filepath}")
    return True

def main():
    success = True
    
    # Check prompt cards
    prompt_files = glob.glob('examples/*prompt-card.yaml')
    for f in prompt_files:
        if not validate_card(f, 'prompt_card'):
            success = False
            
    # Check skill cards
    skill_files = glob.glob('examples/*skill-card.yaml')
    for f in skill_files:
        if not validate_card(f, 'skill_card'):
            success = False
            
    if not success:
        sys.exit(1)
    
    print("All examples passed validation!")
    
if __name__ == '__main__':
    main()
