import os
import sys
import json
import argparse
import importlib

# ------------------------------------------------------------------------------------------
def load_language_configs(config_file="languages_config.json"):
    """Loads language configurations from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config["languages"]
    except Exception as e:
        print(f"Error loading language configurations: {e}")
        return []

# ------------------------------------------------------------------------------------------
def load_analyzer_function(module_path, function_name):
    """Dynamically imports the language analyzer function"""
    try:
        module = importlib.import_module(module_path)
        return getattr(module, function_name)
    except ImportError as e:
        print(f"Error importing module '{module_path}': {e}")
        return None
    except AttributeError as e:
        print(f"Function '{function_name}' not found in module '{module_path}': {e}")
        return None

# ------------------------------------------------------------------------------------------
def scan_directory_and_analyze(directory_path, file_extension, analysis_function, language_name):
    """Recursively scans a directory for files with specified extension and analyzes them"""
    all_found_vars = []
    print(f"\nScanning directory for {language_name} files ({file_extension}): {directory_path}")
    files_scanned_count = 0
    files_with_findings_count = 0
    
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.lower().endswith(file_extension):
                files_scanned_count += 1
                filepath = os.path.join(root, filename)
                file_findings = analysis_function(filepath)
                
                if file_findings is None:  
                    continue
                if file_findings: 
                    files_with_findings_count += 1
                    for var_info in file_findings:
                        var_info_with_context = {
                            "file": filepath,
                            "line": var_info.get("line"),
                            "variable": var_info.get("variable"),
                            "value": var_info.get("value"),
                            "language": language_name
                        }
                        all_found_vars.append(var_info_with_context)
    
    if files_scanned_count == 0:
        print(f"No {language_name} ({file_extension}) files found in directory '{directory_path}'.")
    else:
        print(f"Scanned {files_scanned_count} {language_name} file(s). Hardcoded values found in {files_with_findings_count} file(s).")
        
    return all_found_vars

# ------------------------------------------------------------------------------------------
def print_results(hardcoded_vars_list, language_name):
    """Displays analysis results"""
    if hardcoded_vars_list:
        print(f"\n--- Potentially Hardcoded Literal Values Found ({language_name}) ---")
        current_file = None
        for var_info in sorted(hardcoded_vars_list, key=lambda x: x['file']):
            if var_info['file'] != current_file:
                current_file = var_info['file']
                print(f"\n  In File: {var_info['file']}")
            line = var_info.get('line', 'N/A')
            variable = var_info.get('variable', 'N/A')
            value = var_info.get('value', 'N/A')
            print(f"    L{line:<4} | Var: {variable:<25} | Value: {value}")
        print("-----------------------------------------------------------------")

# ------------------------------------------------------------------------------------------
def save_to_json(results, filename):
    """Saves results to a JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=2, ensure_ascii=False)
        print(f"\nResults successfully saved to file: {filename}")
    except Exception as e:
        print(f"\nError saving results to JSON: {e}")

# ------------------------------------------------------------------------------------------
def main():
    """Main program function"""
    # Load configurations
    languages_config = load_language_configs()
    if not languages_config:
        print("No language configurations found. Check the languages_config.json file.")
        sys.exit(1)
    
    # Configure command line arguments
    parser = argparse.ArgumentParser(
        description="HardcodeFinder - Tool to detect hardcoded values in source code"
    )
    parser.add_argument("directory", help="Directory path to scan")
    parser.add_argument("--output", "-o", help="Save results to JSON file")
    
    # Language options
    lang_group = parser.add_mutually_exclusive_group(required=True)
    lang_group.add_argument("--all", action="store_true", help="Analyze all supported languages")
    
    for lang in languages_config:
        lang_id = lang["id"]
        lang_group.add_argument(
            f"--{lang_id}", 
            action="store_true", 
            help=f"Analyze {lang['name']} files ({lang['extension']})"
        )
    
    # Process arguments
    args = parser.parse_args()
    
    # Validate directory
    directory_path = args.directory
    if not os.path.exists(directory_path):
        print(f"Error: Path '{directory_path}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(directory_path):
        print(f"Error: Path '{directory_path}' is not a directory.")
        sys.exit(1)
    
    # Determine which languages to analyze
    langs_to_analyze = []
    
    if args.all:
        langs_to_analyze = languages_config
    else:
        for lang in languages_config:
            if getattr(args, lang["id"], False):
                langs_to_analyze.append(lang)
    
    # Store all results
    all_results = {}
    
    # Execute analysis for each selected language
    for lang in langs_to_analyze:
        analyzer_function = load_analyzer_function(lang["module_path"], lang["function_name"])
        if analyzer_function is None:
            print(f"Skipping {lang['name']} analysis: analyzer could not be loaded.")
            continue
            
        if lang["disclaimer"]:
            print(f"\nNote for {lang['name']} analysis: {lang['disclaimer']}")
            
        results = scan_directory_and_analyze(
            directory_path,
            lang["extension"],
            analyzer_function,
            lang["name"]
        )
        
        print_results(results, lang["name"])
        
        # Add to results dictionary
        all_results[lang["name"]] = results
    
    # Save to JSON if output argument was provided
    if args.output:
        save_to_json(all_results, args.output)

# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("Welcome to Hardcode Finder!")
    print("This tool helps identify hardcoded literal values in your source code.")
    print("=" * 70)
    main()