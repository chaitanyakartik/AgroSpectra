"""
Markdown to PDF Converter for Mining Site Inspection Report
Uses markdown2 and weasyprint for high-quality PDF generation
"""

import os
from pathlib import Path

def convert_md_to_pdf(md_file, output_pdf=None, css_file=None):
    """
    Convert markdown file to PDF with custom styling
    
    Args:
        md_file: Path to markdown file
        output_pdf: Output PDF path (optional, defaults to same name as md)
        css_file: Path to custom CSS file (optional)
    """
    try:
        import markdown2
        from weasyprint import HTML, CSS
    except ImportError:
        print("ERROR: Required libraries not installed!")
        print("\nPlease install required packages:")
        print("  pip install markdown2 weasyprint")
        print("\nNote: WeasyPrint also requires system dependencies:")
        print("  macOS: brew install python3 cairo pango gdk-pixbuf libffi")
        print("  Ubuntu: sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0")
        return False
    
    # Set up file paths
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"ERROR: Markdown file not found: {md_file}")
        return False
    
    if output_pdf is None:
        output_pdf = md_path.with_suffix('.pdf')
    
    print("=" * 70)
    print("MARKDOWN TO PDF CONVERTER")
    print("=" * 70)
    print(f"Input:  {md_path}")
    print(f"Output: {output_pdf}")
    print()
    
    # Read markdown content
    print("📄 Reading markdown file...")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    print("🔄 Converting markdown to HTML...")
    html_content = markdown2.markdown(
        md_content,
        extras=[
            'tables',           # Enable table support
            'fenced-code-blocks',  # Code blocks with ```
            'strike',           # Strikethrough text
            'task_list',        # Checkbox lists
            'header-ids',       # Generate IDs for headers
            'toc',              # Table of contents
        ]
    )
    
    # Create custom CSS for professional styling
    default_css = """
        @page {
            size: A4;
            margin: 2cm;
            @top-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }
        }
        
        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 24pt;
            font-weight: bold;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 20px;
            page-break-before: always;
        }
        
        h1:first-of-type {
            page-break-before: avoid;
        }
        
        h2 {
            color: #34495e;
            font-size: 18pt;
            font-weight: bold;
            margin-top: 20px;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 5px;
        }
        
        h3 {
            color: #2c3e50;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 15px;
        }
        
        h4 {
            color: #555;
            font-size: 12pt;
            font-weight: bold;
            margin-top: 10px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }
        
        th {
            background-color: #3498db;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            padding: 8px;
            border: 1px solid #ddd;
        }
        
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        tr:hover {
            background-color: #e8f4f8;
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border: 1px solid #ddd;
            padding: 5px;
            background: white;
        }
        
        em {
            display: block;
            text-align: center;
            font-size: 9pt;
            color: #666;
            margin-top: -15px;
            margin-bottom: 20px;
            font-style: italic;
        }
        
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }
        
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 9pt;
        }
        
        ul, ol {
            margin: 10px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 5px 0;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 15px 0;
            color: #555;
            font-style: italic;
        }
        
        hr {
            border: none;
            border-top: 2px solid #3498db;
            margin: 30px 0;
        }
        
        strong {
            color: #2c3e50;
            font-weight: bold;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Prevent page breaks inside elements */
        table, figure, img {
            page-break-inside: avoid;
        }
        
        h1, h2, h3, h4 {
            page-break-after: avoid;
        }
        
        /* Custom classes for status indicators */
        .status-good { color: #27ae60; font-weight: bold; }
        .status-warning { color: #f39c12; font-weight: bold; }
        .status-critical { color: #e74c3c; font-weight: bold; }
    """
    
    # Wrap HTML content
    html_full = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Mining Site Inspection Report</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert to PDF
    print("📊 Generating PDF...")
    try:
        # Use custom CSS if provided, otherwise use default
        if css_file and Path(css_file).exists():
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            stylesheets = [CSS(string=css_content)]
            print(f"   Using custom CSS: {css_file}")
        else:
            stylesheets = [CSS(string=default_css)]
            print("   Using default styling")
        
        # Generate PDF
        HTML(string=html_full, base_url=str(md_path.parent)).write_pdf(
            output_pdf,
            stylesheets=stylesheets
        )
        
        # Get file size
        file_size = os.path.getsize(output_pdf) / 1024  # KB
        
        print()
        print("=" * 70)
        print("✅ SUCCESS! PDF generated successfully")
        print("=" * 70)
        print(f"📁 Output file: {output_pdf}")
        print(f"📦 File size: {file_size:.1f} KB")
        print(f"📄 Location: {Path(output_pdf).absolute()}")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR during PDF generation: {str(e)}")
        return False


def main():
    """Main function to run the converter"""
    
    # Configuration
    markdown_file = "report.md"  # Change this to your markdown file
    output_file = "Mining_Site_Inspection_Report.pdf"   # Change this to desired output name
    
    # Optional: Use custom CSS file
    custom_css = None  # Set to "custom_style.css" if you have one
    
    # Check if markdown file exists
    if not os.path.exists(markdown_file):
        print(f"❌ ERROR: Markdown file '{markdown_file}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Please update the 'markdown_file' variable in the script.")
        return
    
    # Convert
    success = convert_md_to_pdf(markdown_file, output_file, custom_css)
    
    if success:
        print("\n💡 TIP: Open the PDF to verify all images are displayed correctly.")
        print("   If images are missing, ensure the relative paths are correct.")
    else:
        print("\n💡 TIP: Make sure you have installed all required dependencies.")


if __name__ == "__main__":
    main()