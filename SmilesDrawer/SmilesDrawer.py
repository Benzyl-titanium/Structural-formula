# -*- coding: utf-8 -*-

def read_smiles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def generate_html(smiles_list):
    template = '''
                    <td valign="center"><img data-smiles="{}" data-smiles-options="{{ 'width': 100, 'height': 100 }}" /></td>
    '''
    html_content = ""
    for smiles in smiles_list:
        smiles = smiles.strip()  
        if smiles:
            html_content += template.format(smiles)
    return html_content

def write_html_file(content, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("<table>\n")
        f.write(content)
        f.write("</table>\n")

def main():
    smiles_list = read_smiles('smiles_5.txt')
    html_content = generate_html(smiles_list)
    write_html_file(html_content, 'output_5.html')

if __name__ == "__main__":
    main() 