from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
import markdown
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

# Register custom fonts
def register_fonts():
    font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    os.makedirs(font_dir, exist_ok=True)
    
    # Using system fonts as fallback if custom fonts aren't available
    try:
        pdfmetrics.registerFont(TTFont('Garamond', os.path.join(font_dir, 'Garamond.ttf')))
    except:
        pass  # Will use default fonts if Garamond is not available

class CoverLetterCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self._drawPageDecoration()
            Canvas.showPage(self)
        Canvas.save(self)

    def _drawPageDecoration(self):
        width, height = letter
        
        # Draw top accent bar
        self.setFillColor(HexColor('#2c5282'))
        self.rect(0.75*inch, height - 0.75*inch, width - 1.5*inch, 0.05*inch, fill=1)
        
        # Draw borders
        self.setFillColor(HexColor('#2c5282'))
        # Left border
        self.rect(0.75*inch, 0.75*inch, 0.02*inch, height - 1.5*inch, fill=1)
        # Right border
        self.rect(width - 0.77*inch, 0.75*inch, 0.02*inch, height - 1.5*inch, fill=1)
        
        # Add decorative corner elements
        self.setStrokeColor(HexColor('#2c5282'))
        self.setLineWidth(0.5)
        corner_size = 0.25*inch
        
        # Top left corner
        self.line(0.75*inch, height - 0.75*inch, 0.75*inch + corner_size, height - 0.75*inch)
        self.line(0.75*inch, height - 0.75*inch, 0.75*inch, height - (0.75*inch + corner_size))
        
        # Top right corner
        self.line(width - 0.75*inch - corner_size, height - 0.75*inch, width - 0.75*inch, height - 0.75*inch)
        self.line(width - 0.75*inch, height - 0.75*inch, width - 0.75*inch, height - (0.75*inch + corner_size))
        
        # Bottom left corner
        self.line(0.75*inch, 0.75*inch, 0.75*inch + corner_size, 0.75*inch)
        self.line(0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch + corner_size)
        
        # Bottom right corner
        self.line(width - 0.75*inch - corner_size, 0.75*inch, width - 0.75*inch, 0.75*inch)
        self.line(width - 0.75*inch, 0.75*inch, width - 0.75*inch, 0.75*inch + corner_size)
        
        # Draw bottom accent bar
        self.rect(0.75*inch, 0.75*inch, width - 1.5*inch, 0.05*inch, fill=1)

def markdown_to_pdf(markdown_text, output_path, author_name):
    # Register fonts
    register_fonts()
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Create PDF document with professional margins
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=1.25*inch,
        rightMargin=1.25*inch,
        topMargin=1.25*inch,
        bottomMargin=1*inch
    )
    
    # Create custom styles
    styles = getSampleStyleSheet()
    
    # Professional color scheme
    primary_color = HexColor('#1a1a1a')  # Almost black for main text
    secondary_color = HexColor('#2c5282')  # Professional blue for headers
    accent_color = HexColor('#4a5568')    # Subtle gray for dates
    
    # Main text style with more character
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='Garamond' if 'Garamond' in pdfmetrics.getRegisteredFontNames() else 'Times-Roman',
        fontSize=11,
        leading=18,
        spaceBefore=12,
        spaceAfter=12,
        firstLineIndent=0,
        textColor=primary_color,
        alignment=TA_JUSTIFY,
    )
    
    # More prominent header style
    header_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontName='Garamond-Bold' if 'Garamond-Bold' in pdfmetrics.getRegisteredFontNames() else 'Times-Bold',
        fontSize=16,
        leading=24,
        spaceBefore=24,
        spaceAfter=16,
        textColor=secondary_color,
        alignment=TA_LEFT,
    )
    
    # Refined date style
    date_style = ParagraphStyle(
        'DateStyle',
        parent=normal_style,
        fontSize=10,
        textColor=accent_color,
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=6,
    )
    
    # Enhanced signature style
    signature_style = ParagraphStyle(
        'SignatureStyle',
        parent=normal_style,
        fontSize=12,
        textColor=secondary_color,
        spaceBefore=36,
        spaceAfter=0,
        alignment=TA_LEFT,
    )
    
    # Process the HTML content
    story = []
    
    # Add initial spacing for better layout
    story.append(Spacer(1, 12))
    
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'ul']):
        if element.name.startswith('h'):
            style = header_style
        else:
            style = normal_style
            
        # Enhanced list handling with better indentation
        if element.name == 'ul':
            for li in element.find_all('li'):
                bullet_text = f"• {li.get_text()}"
                p = Paragraph(bullet_text, normal_style)
                p.style.leftIndent = 20
                story.append(p)
                story.append(Spacer(1, 8))
            continue
            
        text = element.get_text()
        if text.strip():
            story.append(Paragraph(text, style))
    
    # Add professional signature section with more spacing
    story.append(Spacer(1, 5))
    current_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(current_date, date_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(author_name, signature_style))
    
    # Build PDF with custom canvas
    def create_document(canvas, doc):
        canvas._drawPageDecoration()
    
    doc.build(story, onFirstPage=create_document, onLaterPages=create_document, canvasmaker=CoverLetterCanvas)

def generate_cover_letter_pdf(markdown_text, author_name, output_path="Cover_Letter.pdf"):
    """
    Generate a professional PDF cover letter from markdown text.
    
    Args:
        markdown_text (str): The cover letter content in markdown format
        author_name (str): The name of the author to be used in the signature
        output_path (str): The path where the PDF should be saved
    """
    try:
        markdown_to_pdf(markdown_text, output_path, author_name)
        return True, f"Successfully generated PDF at {output_path}"
    except Exception as e:
        return False, f"Error generating PDF: {str(e)}"

if __name__ == "__main__":
    # Example usage
    sample_markdown = open("../cover_letter.md", "r").read()
    
    success, message = generate_cover_letter_pdf(
        sample_markdown,
        "John Doe",
        "sample_cover_letter.pdf"
    )
    print(message) 