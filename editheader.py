import os
import re

# Root folder containing all years
root_folder = 'dellater'  # <-- change this to your "work" folder path

# Desired order of links
link_order = ['Works', 'Bio', 'Contact', 'Instagram']

# Href mapping for the links (with relative paths)
href_mapping = {
    'Works': '../../index.html',
    'Bio': '../../bio.html',
    'Contact': '../../contact.html',
    'Instagram': 'https://www.instagram.com/yaffa16/'  # external link
}

# Extra attributes for Instagram
extra_attrs = {
    'Instagram': ' target="_blank" rel="noopener noreferrer"'
}

# Regex to match the <div> that contains the header links
div_pattern = re.compile(
    r'(<div>\s*(?:<a href=".*?">.*?</a>\s*)+</div>)',
    re.DOTALL
)

# Regex to match individual <a> tags
link_pattern = re.compile(r'(<a href=".*?">.*?</a>)')

for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith('.html'):
            file_path = os.path.join(dirpath, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            match = div_pattern.search(content)
            if match:
                original_div = match.group(1)

                # Extract all <a> tags
                links = link_pattern.findall(original_div)

                # Map link text to the original <a> tag
                link_dict = {}
                for link in links:
                    text_match = re.search(r'>(.*?)<', link)
                    if text_match:
                        text = text_match.group(1).strip()
                        link_dict[text] = link

                # Determine indentation from the first <a> tag
                indent_match = re.search(r'(\s*)<a href="', original_div)
                indent = indent_match.group(1) if indent_match else '      '

                # Build reordered links with updated hrefs
                new_links = []
                for text in link_order:
                    if text in link_dict:
                        if text == 'Instagram':
                            # Replace with external link and extra attributes
                            new_link = f'<a href="{href_mapping[text]}"{extra_attrs[text]}>\n  {text}</a>'
                        else:
                            # Replace href for other links, preserve original text
                            new_link = re.sub(r'href=".*?"', f'href="{href_mapping[text]}"', link_dict[text])
                        new_links.append(f'{indent}{new_link}')

                # Join links preserving line breaks
                new_div_content = '\n'.join(new_links)

                # Preserve opening and closing <div> tags
                new_div_html = re.sub(r'(<div>).*?(</div>)', r'\1\n' + new_div_content + r'\n\2', original_div,
                                      flags=re.DOTALL)

                # Replace the old div with new div in content
                content = content.replace(original_div, new_div_html)

                # Write back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f'Updated: {file_path}')
            else:
                print(f'No header links found in: {file_path}')
