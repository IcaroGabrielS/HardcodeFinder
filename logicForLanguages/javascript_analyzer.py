import re
_JS_LITERAL_PATTERN_STR = r"""
    (?:\"(?:\\.|[^\"\\])*\") |    
    (?:\'(?:\\.|[^\'\\])*\') |    
    (?:`(?:\\.|[^`\n\\])*`) |    
    (?:true|false|null) |         
    (?:-?\b\d+(?:\.\d+(?:[eE][+-]?\d+)?)?\b) | 
    (?:\[[^\]\n]*\]) |            
    (?:\{[^\}\n]*\})              
"""
_JS_ASSIGNMENT_REGEX = re.compile(
    r"^\s*(?:var|let|const)\s+([a-zA-Z_$][\w$]*)\s*=\s*(" + _JS_LITERAL_PATTERN_STR + r")\s*;?\s*(?:\/\/.*)?$",
    re.VERBOSE  
)

def find_hardcoded_in_js_file(filepath):
    """
    Analyzes a single JavaScript file for hardcoded variable assignments using regex.
    Returns a list of dictionaries with found variables, or an empty list if none found.
    Returns None if a file processing error occurs.
    """
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_number, line_content in enumerate(file, 1):
                line_content_no_block_comments = re.sub(r'/\*.*?\*/', '', line_content)
                match = _JS_ASSIGNMENT_REGEX.search(line_content_no_block_comments)
                if match:
                    variable_name = match.group(1)
                    value_str = match.group(2).strip() 
                    findings.append({
                        "line": line_number,
                        "variable": variable_name,
                        "value": value_str
                    })
        return findings
    except FileNotFoundError:
        print(f"Error [JS Analyzer]: File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"Unexpected error [JS Analyzer] processing '{filepath}': {e}")
        return None
