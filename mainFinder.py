import os
import sys
try:
    import logicForLanguages.python_analyzer as python_analyzer
    import logicForLanguages.javascript_analyzer as javascript_analyzer
except ImportError as e:
    print(f"Error importing analyzer modules: {e}")
    print("Please ensure 'python_analyzer.py' and 'javascript_analyzer.py' ""are in the same directory as this script.")
    sys.exit(1)
def scan_directory_and_analyze(directory_path, file_extension, analysis_function, language_name):
    """
    Scans a directory recursively for files with a given extension and analyzes them
    using the provided analysis_function.
    """
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
                    files_with_findings_count +=1
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
        print(f"No {language_name} files ({file_extension}) found in the directory '{directory_path}'.")
    else:
        print(f"Scanned {files_scanned_count} {language_name} file(s). Found potential hardcoded values in {files_with_findings_count} file(s).")
    return all_found_vars
def display_menu():
    print("\n--- Hardcode Finder ---")
    print("1. Analyze Python (.py) files (AST-based)")
    print("2. Analyze JavaScript (.js) files (Regex-based)")
    print("3. Exit")
    print("-----------------------")
def print_results(hardcoded_vars_list, language_name):
    if hardcoded_vars_list:
        print(f"\n--- Potentially Hardcoded Literal Values Found ({language_name}) ---")
        current_file = None
        for var_info in hardcoded_vars_list:
            if var_info['file'] != current_file:
                current_file = var_info['file']
                print(f"\n  In File: {var_info['file']}")
            line = var_info.get('line', 'N/A')
            variable = var_info.get('variable', 'N/A')
            value = var_info.get('value', 'N/A')
            print(f"    L{line:<4} | Var: {variable:<25} | Value: {value}")
        print("-----------------------------------------------------------------")
def main():
    analyzer_map = {
        "1": {
            "name": "Python",
            "extension": ".py",
            "function": python_analyzer.find_hardcoded_in_python_file, 
            "disclaimer": None
        },
        "2": {
            "name": "JavaScript",
            "extension": ".js",
            "function": javascript_analyzer.find_hardcoded_in_js_file, 
            "disclaimer": ("Note: JavaScript analysis uses Regular Expressions. It aims to find simple, "
                           "single-line literal assignments. It may not catch all cases and might have "
                           "false positives/negatives with complex code or multi-line literals.")
        }
    }
    while True:
        display_menu()
        choice = input("Choose an option: ").strip()
        if choice == '3':
            print("Exiting Hardcode Finder...")
            break
        if choice in analyzer_map:
            selected_analyzer = analyzer_map[choice]
            language_name = selected_analyzer["name"]
            print(f"\nSelected: Analyze {language_name} files.")
            if selected_analyzer["disclaimer"]:
                print(selected_analyzer["disclaimer"])
            directory_path = input(f"Enter the full path to the directory for {language_name} analysis: ").strip()
            if not directory_path:
                print("No directory path provided. Please try again.")
                continue
            if not os.path.exists(directory_path):
                print(f"Error: The path '{directory_path}' does not exist.")
                continue
            if not os.path.isdir(directory_path):
                print(f"Error: The path '{directory_path}' is not a directory.")
                continue
            all_hardcoded_vars = scan_directory_and_analyze(
                directory_path,
                selected_analyzer["extension"],
                selected_analyzer["function"],
                language_name
            )
            print_results(all_hardcoded_vars, language_name)
        else:
            print("Invalid option. Please try again.")
if __name__ == "__main__":
    print("=" * 70)
    print("Welcome to Hardcode Finder!")
    print("This tool helps identify hardcoded literal values in your source code.")
    print("=" * 70)
    main()
