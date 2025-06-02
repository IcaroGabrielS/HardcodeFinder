import os
import sys
import json
import importlib

# ------------------------------------------------------------------------------------------
def load_language_configs(config_file="languages_config.json"):
    """Carrega as configurações de linguagem do arquivo JSON"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config["languages"]
    except Exception as e:
        print(f"Erro ao carregar configurações de linguagem: {e}")
        return []

# ------------------------------------------------------------------------------------------
def load_analyzer_function(module_path, function_name):
    """Importa dinamicamente a função analisadora da linguagem"""
    try:
        module = importlib.import_module(module_path)
        return getattr(module, function_name)
    except ImportError as e:
        print(f"Erro ao importar módulo '{module_path}': {e}")
        return None
    except AttributeError as e:
        print(f"Função '{function_name}' não encontrada no módulo '{module_path}': {e}")
        return None

# ------------------------------------------------------------------------------------------
def scan_directory_and_analyze(directory_path, file_extension, analysis_function, language_name):
    """Escaneia um diretório recursivamente para arquivos com determinada extensão e os analisa"""
    all_found_vars = []
    print(f"\nEscaneando diretório para arquivos {language_name} ({file_extension}): {directory_path}")
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
        print(f"Nenhum arquivo {language_name} ({file_extension}) encontrado no diretório '{directory_path}'.")
    else:
        print(f"Escaneados {files_scanned_count} arquivo(s) {language_name}. Valores hardcoded encontrados em {files_with_findings_count} arquivo(s).")
        
    return all_found_vars

# ------------------------------------------------------------------------------------------
def display_menu(languages_config):
    """Exibe o menu de opções para o usuário"""
    print("\n--- Hardcode Finder ---")
    for i, lang in enumerate(languages_config, 1):
        print(f"{i}. Analisar arquivos {lang['name']} ({lang['extension']})")
    print(f"{len(languages_config) + 1}. Sair")
    print("-----------------------")

# ------------------------------------------------------------------------------------------
def print_results(hardcoded_vars_list, language_name):
    """Exibe os resultados da análise"""
    if hardcoded_vars_list:
        print(f"\n--- Valores Literais Potencialmente Hardcoded Encontrados ({language_name}) ---")
        current_file = None
        for var_info in hardcoded_vars_list:
            if var_info['file'] != current_file:
                current_file = var_info['file']
                print(f"\n  No Arquivo: {var_info['file']}")
            line = var_info.get('line', 'N/A')
            variable = var_info.get('variable', 'N/A')
            value = var_info.get('value', 'N/A')
            print(f"    L{line:<4} | Var: {variable:<25} | Valor: {value}")
        print("-----------------------------------------------------------------")

# ------------------------------------------------------------------------------------------
def main():
    """Função principal do programa"""
    languages_config = load_language_configs()
    if not languages_config:
        print("Nenhuma configuração de linguagem encontrada. Verifique o arquivo languages_config.json.")
        sys.exit(1)
    
    # Pré-carrega os analisadores
    for lang in languages_config:
        lang["function"] = load_analyzer_function(lang["module_path"], lang["function_name"])
        if lang["function"] is None:
            print(f"Não foi possível carregar o analisador para {lang['name']}. Esta opção não estará disponível.")
    
    # Filtra apenas linguagens com analisadores válidos
    valid_languages = [lang for lang in languages_config if lang["function"] is not None]
    
    while True:
        display_menu(valid_languages)
        try:
            choice = int(input("Escolha uma opção: ").strip())
            if choice == len(valid_languages) + 1:
                print("Saindo do Hardcode Finder...")
                break
                
            if 1 <= choice <= len(valid_languages):
                selected_lang = valid_languages[choice - 1]
                
                print(f"\nSelecionado: Analisar arquivos {selected_lang['name']}.")
                if selected_lang["disclaimer"]:
                    print(selected_lang["disclaimer"])
                    
                directory_path = input(f"Digite o caminho completo do diretório para análise de {selected_lang['name']}: ").strip()
                if not directory_path:
                    print("Nenhum caminho de diretório fornecido. Tente novamente.")
                    continue
                    
                if not os.path.exists(directory_path):
                    print(f"Erro: O caminho '{directory_path}' não existe.")
                    continue
                    
                if not os.path.isdir(directory_path):
                    print(f"Erro: O caminho '{directory_path}' não é um diretório.")
                    continue
                    
                all_hardcoded_vars = scan_directory_and_analyze(
                    directory_path,
                    selected_lang["extension"],
                    selected_lang["function"],
                    selected_lang["name"]
                )
                
                print_results(all_hardcoded_vars, selected_lang["name"])
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")

# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("Bem-vindo ao Hardcode Finder!")
    print("Esta ferramenta ajuda a identificar valores literais hardcoded em seu código fonte.")
    print("=" * 70)
    main()