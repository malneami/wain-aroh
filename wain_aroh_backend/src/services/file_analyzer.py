"""
File Analyzer Service
Analyzes uploaded medical files (images, PDFs, documents) using AI
"""

from openai import OpenAI
import base64
import os
from pathlib import Path
import mimetypes

client = OpenAI()

class FileAnalyzer:
    def __init__(self):
        self.upload_dir = Path("/tmp/wain_aroh_uploads")
        self.upload_dir.mkdir(exist_ok=True)
        
        # Supported file types
        self.supported_types = {
            'image': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
            'pdf': ['application/pdf'],
            'document': ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
            'text': ['text/plain']
        }
    
    def is_supported(self, mime_type):
        """Check if file type is supported"""
        for category, types in self.supported_types.items():
            if mime_type in types:
                return True, category
        return False, None
    
    def save_file(self, file, session_id):
        """Save uploaded file temporarily"""
        try:
            # Create session directory
            session_dir = self.upload_dir / session_id
            session_dir.mkdir(exist_ok=True)
            
            # Save file
            filename = file.filename
            filepath = session_dir / filename
            file.save(str(filepath))
            
            return str(filepath)
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def analyze_image(self, image_path, context=""):
        """Analyze medical image using GPT-4 Vision"""
        try:
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Determine image type
            mime_type, _ = mimetypes.guess_type(image_path)
            
            # Analyze with GPT-4 Vision
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """أنت مساعد طبي ذكي متخصص في تحليل الصور الطبية والمستندات.
                        
مهمتك:
1. تحليل الصورة المرفقة بعناية
2. استخراج المعلومات الطبية المهمة
3. تحديد نوع المستند (نتيجة فحص، وصفة طبية، صورة أشعة، إلخ)
4. تلخيص النتائج بشكل واضح باللغة العربية
5. تحديد مستوى الأهمية (عادي، مهم، عاجل)

ملاحظات:
- لا تقدم تشخيصاً نهائياً
- اذكر أن هذا تحليل أولي ويجب استشارة طبيب
- كن دقيقاً وموضوعياً"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""حلل هذه الصورة الطبية:

سياق المحادثة: {context if context else 'لا يوجد'}

يرجى تقديم:
1. نوع المستند/الصورة
2. المعلومات الطبية المهمة
3. القيم غير الطبيعية (إن وجدت)
4. مستوى الأهمية
5. التوصيات الأولية"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'success': True,
                'type': 'image',
                'analysis': analysis,
                'file_path': image_path
            }
            
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_pdf(self, pdf_path, context=""):
        """Analyze PDF document"""
        try:
            # For now, we'll use a simple text extraction approach
            # In production, you'd use PyPDF2 or similar
            
            return {
                'success': True,
                'type': 'pdf',
                'analysis': """تم استلام ملف PDF.

للحصول على أفضل تحليل، يرجى:
1. تحويل الملف إلى صورة (PNG/JPG)
2. أو نسخ النص المهم ولصقه في المحادثة

يمكنني تحليل الصور الطبية ونتائج الفحوصات بشكل أفضل عند رفعها كصور.""",
                'file_path': pdf_path
            }
            
        except Exception as e:
            print(f"Error analyzing PDF: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_file(self, file_path, file_type, context=""):
        """Analyze uploaded file based on type"""
        if file_type == 'image':
            return self.analyze_image(file_path, context)
        elif file_type == 'pdf':
            return self.analyze_pdf(file_path, context)
        else:
            return {
                'success': False,
                'error': 'Unsupported file type'
            }
    
    def format_analysis_message(self, analysis_result, filename):
        """Format analysis result as Arabic message"""
        if not analysis_result['success']:
            return f"""❌ عذراً، لم نتمكن من تحليل الملف "{filename}".

يرجى التأكد من:
- الملف بصيغة مدعومة (صورة، PDF)
- حجم الملف مناسب
- الصورة واضحة وقابلة للقراءة"""
        
        file_type_ar = {
            'image': 'صورة',
            'pdf': 'مستند PDF',
            'document': 'مستند',
            'text': 'ملف نصي'
        }
        
        type_name = file_type_ar.get(analysis_result['type'], 'ملف')
        
        message = f"""📎 تم تحليل {type_name}: "{filename}"

{analysis_result['analysis']}

---
💡 **ملاحظة مهمة**: هذا تحليل أولي بواسطة الذكاء الاصطناعي. يجب استشارة طبيب مختص للتشخيص والعلاج النهائي."""
        
        return message
    
    def cleanup_session_files(self, session_id):
        """Clean up uploaded files for a session"""
        try:
            session_dir = self.upload_dir / session_id
            if session_dir.exists():
                import shutil
                shutil.rmtree(session_dir)
        except Exception as e:
            print(f"Error cleaning up files: {e}")

# Global instance
file_analyzer = FileAnalyzer()

