import os
import re

TARGET_ROOT = """        :root {
            /* Padrão visual do curso - Rede Daora Aula 02 */
            --pico-background-color: #1A0B21;
            --pico-secondary-background: #110716;
            --pico-card-background-color: #2D1B36;
            --pico-form-element-background-color: #2D1B36;
            --pico-card-sectioning-background-color: #2D1B36;
            --pico-muted-border-color: #3D264A;
            --pico-border-color: #3D264A;

            --pico-color: #E0E0E0;
            --pico-h1-color: #FFFFFF;
            --pico-h2-color: #FFFFFF;
            --pico-h3-color: #FFFFFF;
            --pico-h4-color: #FFFFFF;
            --pico-h5-color: #FFFFFF;
            --pico-h6-color: #FFFFFF;
            --pico-muted-color: #E0E0E0;

            --pico-primary: #59D2FE;
            --pico-primary-background: #59D2FE;
            --pico-primary-hover: #008CA4;
            --pico-primary-hover-background: #008CA4;
            --pico-primary-focus: rgba(89, 210, 254, 0.25);

            --pico-secondary: #008CA4;
            --pico-secondary-background: #008CA4;
            --pico-secondary-hover: #006b7d;
            --pico-secondary-hover-background: #006b7d;

            /* Adicionais para garantir que elementos estruturais e formulários não fiquem claros */
            --pico-table-row-stripped-background-color: rgba(45, 27, 54, 0.5);
            --pico-code-background-color: #0d0611;
            --pico-mark-background-color: rgba(89, 210, 254, 0.2);
            --pico-mark-color: #59D2FE;
            --pico-form-element-active-background-color: #2D1B36;
            --pico-switch-background-color: #3D264A;
            --pico-switch-checked-background-color: #59D2FE;
            --pico-accordion-active-summary-color: #59D2FE;
            --pico-accordion-close-summary-color: #E0E0E0;
            --pico-accordion-open-summary-color: #E0E0E0;
        }"""

FOOTER = """
    <footer class="container">
        <hr>
        <div class="grid">

            <div style="text-align: right;">
                <small>2026 • Polo Audiovisual - Casa de Cultura do Butantã</small>
            </div>
        </div>
    </footer>
"""

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace html tag
    content = re.sub(r'<html lang="pt-[bB][rR]"(?! data-theme="dark")>', '<html lang="pt-br" data-theme="dark">', content)

    # Replace :root
    content = re.sub(r'[ \t]*:root\s*\{[^}]+\}', TARGET_ROOT, content, flags=re.MULTILINE)

    # Insert footer if missing
    if '<footer class="container">' not in content:
        # Avoid inserting before nested `<main>` or something weird by replacing the last `</main>` 
        # Actually, let's just insert after the unique `</main>` or the last `</main>`
        last_main_idx = content.rfind('</main>')
        if last_main_idx != -1:
            content = content[:last_main_idx + 7] + FOOTER + content[last_main_idx + 7:]

    # Add missing waves CSS to footer.container::before ? Wait, did all files have footer.container CSS?
    # Let's verify by regex...
    if 'footer.container::before' not in content:
        WAVES_CSS = """        /* Ondas de rodapé e grafismos */
        footer.container {
            position: relative;
            margin-top: 4rem;
        }

        footer.container::before {
            content: '';
            position: absolute;
            top: -50px;
            left: 0;
            width: 100%;
            height: 30px;
            background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1200 120" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" fill="%23008CA4" /><path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-23.84V0Z" opacity=".5" fill="%23008CA4" /><path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" fill="%23008CA4" /></svg>') no-repeat center bottom;
            background-size: 100% 30px;
        }

"""
        # Insert WAVES_CSS before </style>
        style_end_idx = content.find('</style>')
        if style_end_idx != -1:
            content = content[:style_end_idx] + WAVES_CSS + content[style_end_idx:]

    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")
    else:
        print(f"No changes for {path}")

for filename in os.listdir('src/apoio/'):
    if filename.endswith('.html') and filename.startswith('0'):
        process_file(os.path.join('src/apoio', filename))
