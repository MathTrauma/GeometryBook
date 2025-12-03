#!/usr/bin/env python3
"""
LaTeX to HTML Converter for Jupyter Book
Extracts TikZ figures as SVG and converts LaTeX to simple HTML
Preserves math equations (MathJax compatible) and figures
"""

import re
import subprocess
import shutil
from pathlib import Path
import argparse


class TexToHTML:
    def __init__(self, tex_file):
        self.tex_file = Path(tex_file).resolve()
        self.work_dir = self.tex_file.parent
        self.figures_dir = self.work_dir / "figures"
        self.figures_dir.mkdir(exist_ok=True)
        
    def extract_tikz_figures(self):
        """1단계: external 패키지를 사용하여 TikZ 그림 추출"""
        print("📊 Step 1: TikZ 그림 추출 중...")
        
        try:
            subprocess.run(
                ['pdflatex', '-shell-escape', '-interaction=nonstopmode', self.tex_file.name],
                cwd=str(self.work_dir),
                capture_output=True,
                timeout=120,
                check=False
            )
        except subprocess.TimeoutExpired:
            print("⚠️  pdflatex 실행 시간 초과")
        except FileNotFoundError:
            print("❌ pdflatex를 찾을 수 없습니다.")
            return []
        
        if not self.figures_dir.exists():
            print(f"⚠️  {self.figures_dir} 폴더를 찾을 수 없습니다.")
            return []
        
        pdf_pattern = f"{self.tex_file.stem}-figure*.pdf"
        pdf_figures = sorted(self.figures_dir.glob(pdf_pattern))
        print(f"✅ {len(pdf_figures)}개의 그림 추출 완료")
        return pdf_figures
    
    def convert_to_svg(self, pdf_files):
        """2단계: PDF를 SVG로 변환"""
        print("\n🎨 Step 2: SVG로 변환 중...")
        svg_files = []
        
        for pdf_file in pdf_files:
            svg_file = self.figures_dir / f"{pdf_file.stem}.svg"
            
            try:
                if shutil.which('pdf2svg'):
                    subprocess.run(['pdf2svg', str(pdf_file), str(svg_file)], check=True, capture_output=True)
                elif shutil.which('inkscape'):
                    subprocess.run(['inkscape', str(pdf_file), '--export-filename', str(svg_file)], check=True, capture_output=True)
                else:
                    print("❌ pdf2svg 또는 inkscape를 찾을 수 없습니다.")
                    return []
                
                svg_files.append(svg_file)
                print(f"  ✓ {pdf_file.name} -> {svg_file.name}")
            except subprocess.CalledProcessError:
                print(f"  ✗ {pdf_file.name} 변환 실패")
        
        print(f"✅ {len(svg_files)}개의 SVG 파일 생성 완료")
        return svg_files
    
    def protect_math(self, content):
        """수식을 플레이스홀더로 보호"""
        math_blocks = []
        
        def save_math(match):
            math_blocks.append(match.group(0))
            return f"<<<MATH{len(math_blocks)-1}>>>"
        
        # \[...\] 형식
        content = re.sub(r'\\\[.*?\\\]', save_math, content, flags=re.DOTALL)
        
        # $$ ... $$ 형식 (먼저 처리)
        pattern1 = r'\$\$[^\$]+\$\$'
        content = re.sub(pattern1, save_math, content, flags=re.DOTALL)
        
        # $ ... $ 형식
        pattern2 = r'\$[^\$]+\$'
        content = re.sub(pattern2, save_math, content)
        
        # equation 등의 환경
        for env in ['equation', 'align', 'gather', 'multline', 'eqnarray']:
            pat = r'\\begin\{' + env + r'\*?\}.*?\\end\{' + env + r'\*?\}'
            content = re.sub(pat, save_math, content, flags=re.DOTALL)
        
        return content, math_blocks
    
    def restore_math(self, content, math_blocks):
        """플레이스홀더를 원래 수식으로 복원"""
        for idx, math in enumerate(math_blocks):
            content = content.replace(f"<<<MATH{idx}>>>", math)
        return content
    
    def tex_to_html(self, svg_files):
        """3단계: LaTeX를 HTML로 변환"""
        print("\n📝 Step 3: HTML로 변환 중...")
        
        with open(self.tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        svg_list = sorted([svg.name for svg in svg_files])
        
        # 1. 수식 보호
        content, math_blocks = self.protect_math(content)
        
        # 2. TikZ를 SVG로 교체
        tikz_pattern = r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}'
        tikz_blocks = re.findall(tikz_pattern, content, re.DOTALL)
        
        for idx, tikz_block in enumerate(tikz_blocks):
            if idx < len(svg_list):
                img_tag = f'<img src="figures/{svg_list[idx]}" alt="Figure {idx}" style="max-width:100%;" />'
                content = content.replace(tikz_block, img_tag, 1)
        
        # 3. document 환경 추출
        doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', content, re.DOTALL)
        if doc_match:
            content = doc_match.group(1)
        
        # 4. LaTeX 명령어를 HTML로 변환
        content = re.sub(r'\\section\{([^}]+)\}', r'<h2>\1</h2>', content)
        content = re.sub(r'\\subsection\{([^}]+)\}', r'<h3>\1</h3>', content)
        content = re.sub(r'\\subsubsection\{([^}]+)\}', r'<h4>\1</h4>', content)
        content = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', content)
        content = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', content)
        content = re.sub(r'\\emph\{([^}]+)\}', r'<em>\1</em>', content)
        
        # 5. 환경 변환
        content = re.sub(r'\\begin\{itemize\}', r'<ul>', content)
        content = re.sub(r'\\end\{itemize\}', r'</ul>', content)
        content = re.sub(r'\\begin\{enumerate\}', r'<ol>', content)
        content = re.sub(r'\\end\{enumerate\}', r'</ol>', content)
        content = re.sub(r'\\item', r'<li>', content)
        content = re.sub(r'\\begin\{center\}', r'<div style="text-align:center;">', content)
        content = re.sub(r'\\end\{center\}', r'</div>', content)
        
        # 6. 기타 명령어
        content = re.sub(r'\\maketitle', '', content)
        content = re.sub(r'\\tableofcontents', '', content)
        content = re.sub(r'\\newpage', '<hr />', content)
        content = re.sub(r'\\\\', '<br />', content)
        content = re.sub(r'\\noindent\s*', '', content)
        
        # 7. 수식 복원
        content = self.restore_math(content, math_blocks)
        
        # 8. 단락 처리
        paragraphs = content.split('\n\n')
        paragraphs = [f'<p>{p.strip()}</p>' if p.strip() and not p.strip().startswith('<') else p.strip() 
                     for p in paragraphs if p.strip()]
        content = '\n\n'.join(paragraphs)
        
        # 9. HTML 생성
        html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITLE_HERE</title>
    <script>
        MathJax = {
            tex: {
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
                processEscapes: true
            }
        };
    </script>"""
    html_content = html_template.replace('TITLE_HERE', self.tex_file.stem).replace('CONTENT_HERE', content)
    
    output_html = self.work_dir / f"{self.tex_file.stem}.html"
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML 파일 생성: {output_html}")
    return output_html
    
    def cleanup(self):
        """임시 파일 정리"""
        for ext in ['.aux', '.log', '.out']:
            temp_file = self.work_dir / f"{self.tex_file.stem}{ext}"
            if temp_file.exists():
                temp_file.unlink()
    
    def run(self):
        """전체 변환 프로세스 실행"""
        print(f"🚀 LaTeX to HTML 변환 시작: {self.tex_file.name}\n")
        
        pdf_figures = self.extract_tikz_figures()
        svg_files = []
        if pdf_figures:
            svg_files = self.convert_to_svg(pdf_figures)
        
        html_file = self.tex_to_html(svg_files)
        self.cleanup()
        
        print("\n" + "="*60)
        print("✨ 변환 완료!")
        print("="*60)
        print(f"📄 HTML 파일: {html_file}")
        print(f"📁 그림 폴더: {self.figures_dir}")
        print(f"\n브라우저에서 열기: file://{html_file}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='LaTeX 파일을 HTML로 변환')
    parser.add_argument('tex_file', help='변환할 .tex 파일')
    args = parser.parse_args()
    
    converter = TexToHTML(args.tex_file)
    converter.run()


if __name__ == "__main__":
    main()
, '
        
        html_content = html_template.replace('TITLE_HERE', self.tex_file.stem).replace('CONTENT_HERE', content)
        
        output_html = self.work_dir / f"{self.tex_file.stem}.html"
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML 파일 생성: {output_html}")
        return output_html
    
    def cleanup(self):
        """임시 파일 정리"""
        for ext in ['.aux', '.log', '.out']:
            temp_file = self.work_dir / f"{self.tex_file.stem}{ext}"
            if temp_file.exists():
                temp_file.unlink()
    
    def run(self):
        """전체 변환 프로세스 실행"""
        print(f"🚀 LaTeX to HTML 변환 시작: {self.tex_file.name}\n")
        
        pdf_figures = self.extract_tikz_figures()
        svg_files = []
        if pdf_figures:
            svg_files = self.convert_to_svg(pdf_figures)
        
        html_file = self.tex_to_html(svg_files)
        self.cleanup()
        
        print("\n" + "="*60)
        print("✨ 변환 완료!")
        print("="*60)
        print(f"📄 HTML 파일: {html_file}")
        print(f"📁 그림 폴더: {self.figures_dir}")
        print(f"\n브라우저에서 열기: file://{html_file}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='LaTeX 파일을 HTML로 변환')
    parser.add_argument('tex_file', help='변환할 .tex 파일')
    args = parser.parse_args()
    
    converter = TexToHTML(args.tex_file)
    converter.run()


if __name__ == "__main__":
    main()
], ['\\(', '\\)']],
                displayMath: [['$', '$'], ['\\[', '\\]']],
                processEscapes: true,
                processEnvironments: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }
        };
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js"></script>
    <style>
        body {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
        }
        img {
            display: block;
            margin: 20px auto;
            max-width: 100%;
        }
        h2 { margin-top: 2em; }
        h3 { margin-top: 1.5em; }
    </style>
</head>
<body>
CONTENT_HERE
</body>
</html>"""
        
        html_content = html_template.replace('TITLE_HERE', self.tex_file.stem).replace('CONTENT_HERE', content)
        
        output_html = self.work_dir / f"{self.tex_file.stem}.html"
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML 파일 생성: {output_html}")
        return output_html
    
    def cleanup(self):
        """임시 파일 정리"""
        for ext in ['.aux', '.log', '.out']:
            temp_file = self.work_dir / f"{self.tex_file.stem}{ext}"
            if temp_file.exists():
                temp_file.unlink()
    
    def run(self):
        """전체 변환 프로세스 실행"""
        print(f"🚀 LaTeX to HTML 변환 시작: {self.tex_file.name}\n")
        
        pdf_figures = self.extract_tikz_figures()
        svg_files = []
        if pdf_figures:
            svg_files = self.convert_to_svg(pdf_figures)
        
        html_file = self.tex_to_html(svg_files)
        self.cleanup()
        
        print("\n" + "="*60)
        print("✨ 변환 완료!")
        print("="*60)
        print(f"📄 HTML 파일: {html_file}")
        print(f"📁 그림 폴더: {self.figures_dir}")
        print(f"\n브라우저에서 열기: file://{html_file}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='LaTeX 파일을 HTML로 변환')
    parser.add_argument('tex_file', help='변환할 .tex 파일')
    args = parser.parse_args()
    
    converter = TexToHTML(args.tex_file)
    converter.run()


if __name__ == "__main__":
    main()