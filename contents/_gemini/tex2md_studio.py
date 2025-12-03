#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
from pathlib import Path
import argparse
import sys

class TexToPlainMD:
    def __init__(self, tex_file):
        self.tex_file = Path(tex_file).resolve()
        self.work_dir = self.tex_file.parent
        self.figures_dir = self.work_dir / "figures"
        self.figures_dir.mkdir(exist_ok=True)
        
        self.temp_tex_file = self.work_dir / f"{self.tex_file.stem}_extract.tex"
        
        self.math_store = {}
        self.math_counter = 0

    def check_dependencies(self):
        if not shutil.which('pdflatex'):
            print("❌ Error: pdflatex가 필요합니다.")
            sys.exit(1)
        if not (shutil.which('pdf2svg') or shutil.which('inkscape')):
            print("❌ Error: pdf2svg 또는 inkscape가 필요합니다.")
            sys.exit(1)

    # -------------------------------------------------------------------------
    # 1. 그림 추출
    # -------------------------------------------------------------------------
    def extract_figures(self):
        print("📊 Step 1: TikZ 그림 추출 중...")
        
        with open(self.tex_file, 'r', encoding='utf-8') as f:
            content = f.read()

        with open(self.temp_tex_file, 'w', encoding='utf-8') as f:
            f.write(content)

        cmd = [
            'pdflatex', '-shell-escape', '-interaction=nonstopmode',
            '-output-directory', str(self.work_dir),
            self.temp_tex_file.name
        ]
        
        try:
            subprocess.run(cmd, cwd=str(self.work_dir), capture_output=True, timeout=300, check=False)
        except subprocess.TimeoutExpired:
            print("⚠️  pdflatex 시간 초과")

        pdf_pattern = f"{self.temp_tex_file.stem}-figure*.pdf"
        pdf_figures = list(self.figures_dir.glob(pdf_pattern))
        
        if not pdf_figures:
            root_pdfs = list(self.work_dir.glob(pdf_pattern))
            for pdf in root_pdfs:
                shutil.move(str(pdf), str(self.figures_dir / pdf.name))
                pdf_figures.append(self.figures_dir / pdf.name)
        
        pdf_figures.sort(key=lambda f: int(re.search(r'figure(\d+)', f.name).group(1)) if re.search(r'figure(\d+)', f.name) else 0)
        
        return pdf_figures

    def convert_to_svg(self, pdf_files):
        print("🎨 Step 2: SVG로 변환 중...")
        svg_files = []
        converter = 'pdf2svg' if shutil.which('pdf2svg') else 'inkscape'
        
        for pdf_file in pdf_files:
            svg_file = pdf_file.with_suffix('.svg')
            try:
                if converter == 'pdf2svg':
                    subprocess.run(['pdf2svg', str(pdf_file), str(svg_file)], check=True, capture_output=True)
                else:
                    subprocess.run(['inkscape', str(pdf_file), '--export-filename', str(svg_file)], check=True, capture_output=True)
                svg_files.append(svg_file)
            except:
                pass
        return svg_files

    # -------------------------------------------------------------------------
    # 2. 텍스트 처리
    # -------------------------------------------------------------------------
    def protect_math(self, text):
        def replace(match):
            token = f"__MATH_BLOCK_{self.math_counter}__"
            self.math_store[token] = match.group(0)
            self.math_counter += 1
            return token

        # Display Math
        text = re.sub(r'\$\$.*?\$\$', replace, text, flags=re.DOTALL)
        text = re.sub(r'\\\[.*?\\\]', replace, text, flags=re.DOTALL)
        text = re.sub(r'\\begin\{(equation|align|gather)\*?\}.*?\\end\{(equation|align|gather)\*?\}', replace, text, flags=re.DOTALL)
        # Inline Math
        text = re.sub(r'(?<!\\)\$.*?(?<!\\)\$', replace, text, flags=re.DOTALL)
        return text

    def clean_commands_iteratively(self, text):
        # 껍데기만 벗길 명령어들
        wrapper_cmds = ['fbox', 'textbf', 'textit', 'underline', 'text'
                        , 'emph', 'item', 'label', 'ref', 'caption', 'endnote']
        cmd_pattern = r'\\(' + '|'.join(wrapper_cmds) + r')\s*\{([^{}]*)\}'
        
        while True:
            new_text = re.sub(cmd_pattern, r'\2', text)
            if new_text == text:
                break
            text = new_text
            
        # 아예 삭제할 명령어들
        delete_cmds = ['setlength', 'stepcounter', 'numbering', 'newpage', 'clearpage', 
                       'usepackage', 'documentclass', 'pagestyle', 'centering']
        for cmd in delete_cmds:
            text = re.sub(r'\\' + cmd + r'.*$', '', text, flags=re.MULTILINE)
            
        return text

    def restore_math_safe(self, text):
        """수식을 복원하되, \\[...\\] 는 $$...$$ 로 변환"""
        for token, math_code in self.math_store.items():
            # \[ ... \] 패턴을 $$ ... $$ 로 변환
            if math_code.startswith(r'\[') and math_code.endswith(r'\]'):
                # 앞뒤 \[ \] 제거하고 $$ 씌우기
                inner_math = math_code[2:-2]
                math_code = f"$${inner_math}$$"
            
            text = text.replace(token, math_code)
        return text

    def process_text(self, svg_files):
        print("\n🧹 Step 3: 텍스트 정제 및 Markdown 생성 중...")
        
        with open(self.tex_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if r'\begin{document}' in content:
            content = content.split(r'\begin{document}')[1]
        if r'\end{document}' in content:
            content = content.split(r'\end{document}')[0]

        # 1. 수식 보호
        content = self.protect_math(content)
        
        # 2. TikZ -> Image
        tikz_pattern = re.compile(r'\\begin\{tikzpicture\}([\s\S]*?)\\end\{tikzpicture\}')
        matches = list(tikz_pattern.finditer(content))
        
        new_content = content
        for i in range(len(matches) - 1, -1, -1):
            if i < len(svg_files):
                match = matches[i]
                svg_name = svg_files[i].name
                # 앞뒤 공백 확보하여 이미지 블록 분리
                img_tag = f'\n\n![Figure](figures/{svg_name})\n\n'
                new_content = new_content[:match.start()] + img_tag + new_content[match.end():]
        content = new_content

        # 3. 명령어 청소 (Iterative Unwrap)
        content = self.clean_commands_iteratively(content)
        
        # 4. 구조적 변환
        content = re.sub(r'\\section\*?\{(.*?)\}', r'\n## \1\n', content)
        content = re.sub(r'\\subsection\*?\{(.*?)\}', r'\n### \1\n', content)
        content = re.sub(r'\\item\s+', r'* ', content)
        # 환경 제거 (\begin{enumerate} 등 삭제)
        content = re.sub(r'\\begin\{(enumerate|itemize|description|center)\}', '', content)
        content = re.sub(r'\\end\{(enumerate|itemize|description|center)\}', '', content)
        content = re.sub(r'::: center', '', content)
        content = re.sub(r':::', '', content)
        
        # 5. [중요] 들여쓰기 강제 제거 (코드 블록 방지)
        content = re.sub(r'^[ \t]+', '', content, flags=re.MULTILINE)
        
        # 6. 남은 백슬래시 제거
        content = content.replace('\\', '')
        
        # 7. 수식 복원 (+ \[ \] 변환)
        content = self.restore_math_safe(content)
        
        # 8. 빈 줄 정리
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content

    def run(self):
        self.check_dependencies()
        print(f"🚀 LaTeX to Plain Markdown 변환 시작: {self.tex_file.name}")
        
        pdf_figures = self.extract_figures()
        svg_files = self.convert_to_svg(pdf_figures)
        md_content = self.process_text(svg_files)
        
        output_md = self.work_dir / f"{self.tex_file.stem}.md"
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        # 정리
        if self.temp_tex_file.exists():
            try:
                os.remove(self.temp_tex_file)
                for ext in ['.aux', '.log', '.out']:
                    f = self.work_dir / f"{self.temp_tex_file.stem}{ext}"
                    if f.exists(): os.remove(f)
            except: pass

        print("\n" + "="*60)
        print("✨ 변환 완료!")
        print(f"📄 결과: {output_md.name}")
        print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tex_file')
    args = parser.parse_args()
    
    if Path(args.tex_file).exists():
        converter = TexToPlainMD(args.tex_file)
        converter.run()
    else:
        print("파일을 찾을 수 없습니다.")