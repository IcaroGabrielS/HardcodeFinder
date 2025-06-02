import re
_JAVA_LITERAL_PATTERN_STR = r"""
    (?:\"(?:\\.|[^\"\\])*\") |        
    (?:\'(?:\\.|[^\'\\])*\') |        
    (?:true|false|null) |             
    (?:-?\b\d+(?:\.\d+)?[LlFfDd]?\b) |
    (?:\[[^\]\n]*\]) |                
    (?:\{[^\}\n]*\})                  
"""
_JAVA_DECLARATION_REGEX = re.compile(
    r"^\s*(?:(?:private|public|protected|static|final|volatile|transient)\s+)*"  
    r"(?:[a-zA-Z][\w.$]*(?:<[^>]+>)?)\s+"                                        
    r"([a-zA-Z_$][\w$]*)\s*=\s*("                                               
    + _JAVA_LITERAL_PATTERN_STR +                                                
    r")\s*;(?:\s*//.*)?$",                                                       
    re.VERBOSE
)
_JAVA_CONSTANT_REGEX = re.compile(
    r"^\s*(?:(?:private|public|protected)\s+)?static\s+final\s+"                
    r"(?:[a-zA-Z][\w.$]*(?:<[^>]+>)?)\s+"                                       
    r"([A-Z][A-Z0-9_]*)\s*=\s*("                                                
    + _JAVA_LITERAL_PATTERN_STR +                                               
    r")\s*;(?:\s*//.*)?$",                                                      
    re.VERBOSE
)
def find_hardcoded_in_java_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            content_no_block_comments = re.sub(r'/\*[\s\S]*?\*/', '', content)
            lines = content_no_block_comments.splitlines()
            for line_number, line_content in enumerate(lines, 1):
                if line_content.strip().startswith("//"):
                    continue
                match = _JAVA_DECLARATION_REGEX.search(line_content)
                if match:
                    variable_name = match.group(1)
                    value_str = match.group(2).strip()
                    findings.append({
                        "line": line_number,
                        "variable": variable_name,
                        "value": value_str
                    })
                    continue
                match = _JAVA_CONSTANT_REGEX.search(line_content)
                if match:
                    constant_name = match.group(1)
                    value_str = match.group(2).strip()
                    findings.append({
                        "line": line_number,
                        "variable": constant_name,
                        "value": value_str
                    })
        return findings
    except FileNotFoundError:
        print(f"Erro [Analisador Java]: Arquivo '{filepath}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro inesperado [Analisador Java] processando '{filepath}': {e}")
        return None
