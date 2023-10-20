import os
import shutil
import re
from bs4 import BeautifulSoup

def replace_inner_html_in_html(html, replacements):
    soup = BeautifulSoup(html, 'html.parser')

    for old_class, new_inner_html in replacements.items():
        elements = soup.find_all(class_=old_class)
        for element in elements:
            element.string = new_inner_html

    return str(soup)

def create_and_copy_files(output_dir, input_html, text_wrapper_2, text_wrapper_3):
    with open(input_html, 'r', encoding='utf-8') as file:
        html = file.read()

    replacements = {
        'text-wrapper-2': text_wrapper_2,
        'text-wrapper-3': text_wrapper_3
    }

    modified_html = replace_inner_html_in_html(html, replacements)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_html = os.path.join(output_dir, 'output.html')

    with open(output_html, 'w', encoding='utf-8') as file:
        file.write(modified_html)

    for item in ["img", "globals.css", "style.css"]:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(output_dir, item))
            else:
                shutil.copy(item, os.path.join(output_dir, item))

def main():
    input_txt = 'input.txt'
    with open(input_txt, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            match = re.findall(r'"(.*?)"', line)
            if len(match) == 2:
                text_wrapper_2, text_wrapper_3 = match
                output_dir = f'output_{i}'
                create_and_copy_files(output_dir, 'index.html', text_wrapper_2, text_wrapper_3)
                print(f'HTML {i} processado e arquivos copiados para {output_dir}')
            else:
                print(f'Linha {i} do arquivo não está no formato esperado.')

if __name__ == '__main__':
    main()