"""
Report Generator Module
Generates PDF reports for mental health assessments
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend

class MentalHealthReportGenerator:
    """
    Generate comprehensive PDF reports for mental health assessments
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Risk level style
        self.styles.add(ParagraphStyle(
            name='RiskLevel',
            parent=self.styles['Normal'],
            fontSize=18,
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Warning style
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
    
    def _create_header(self):
        """Create report header"""
        elements = []
        
        # Title
        title = Paragraph(
            "Mental Health Assessment Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        
        # Subtitle
        subtitle = Paragraph(
            "AI-Powered Student Wellness Screening",
            self.styles['Normal']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))
        
        # Date and confidentiality notice
        date_text = f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        elements.append(Paragraph(date_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        confidential = Paragraph(
            "<b>CONFIDENTIAL</b> - This report contains sensitive health information",
            self.styles['Warning']
        )
        elements.append(confidential)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_risk_summary(self, prediction_result):
        """Create risk level summary section"""
        elements = []
        
        # Section header
        header = Paragraph("Risk Assessment Summary", self.styles['CustomSubtitle'])
        elements.append(header)
        
        # Risk level box
        risk_level = prediction_result['risk_level']
        probability = prediction_result['probability']
        risk_color = prediction_result['risk_color']
        
        # Color mapping
        color_map = {
            'green': colors.HexColor('#2ecc71'),
            'orange': colors.HexColor('#f39c12'),
            'red': colors.HexColor('#e74c3c')
        }
        
        # Create risk level table
        risk_data = [
            ['Risk Level:', risk_level],
            ['Probability:', f'{probability}%'],
            ['Assessment Date:', datetime.now().strftime('%B %d, %Y')]
        ]
        
        risk_table = Table(risk_data, colWidths=[2.5*inch, 3*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('BACKGROUND', (1, 0), (1, 0), color_map.get(risk_color, colors.grey)),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTSIZE', (1, 0), (1, 0), 14),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Interpretation
        interpretation = self._get_risk_interpretation(risk_level)
        elements.append(Paragraph(interpretation, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _get_risk_interpretation(self, risk_level):
        """Get interpretation text based on risk level"""
        interpretations = {
            'Low': """
                <b>Low Risk Interpretation:</b><br/>
                Your assessment indicates low risk for depression based on current lifestyle 
                and academic factors. Your responses suggest healthy patterns in sleep, stress 
                management, and overall wellbeing. Continue maintaining these positive habits 
                and stay connected with your support network.
            """,
            'Moderate': """
                <b>Moderate Risk Interpretation:</b><br/>
                Your assessment indicates moderate risk for depression. Some factors suggest 
                elevated stress levels that may benefit from attention and lifestyle adjustments. 
                Consider reaching out to campus resources for preventive support, improving 
                sleep hygiene, or exploring stress management techniques. Early intervention 
                can prevent escalation.
            """,
            'High': """
                <b>High Risk Interpretation:</b><br/>
                Your assessment indicates high risk for depression. Multiple risk factors have 
                been identified that warrant immediate attention. We strongly recommend 
                scheduling an appointment with a mental health professional for proper evaluation. 
                This screening tool is not a diagnosis but indicates you would benefit from 
                professional support. Help is available, and reaching out is a sign of strength.
            """
        }
        return interpretations.get(risk_level, "")
    
    def _create_input_summary(self, input_data):
        """Create summary of input data"""
        elements = []
        
        header = Paragraph("Your Assessment Inputs", self.styles['CustomSubtitle'])
        elements.append(header)
        
        # Prepare data for table
        table_data = [['Parameter', 'Your Response']]
        
        # Format the input data
        formatted_inputs = {
            'Age': f"{input_data.get('age', 'N/A')} years",
            'Gender': input_data.get('gender', 'N/A'),
            'CGPA': f"{input_data.get('cgpa', 'N/A'):.1f}/10.0",
            'Study Hours per Day': f"{input_data.get('study_hours', 'N/A')} hours",
            'Academic Pressure': f"{input_data.get('academic_pressure', 'N/A')}/5",
            'Study Satisfaction': f"{input_data.get('study_satisfaction', 'N/A')}/5",
            'Sleep Duration': input_data.get('sleep_duration', 'N/A'),
            'Dietary Habits': input_data.get('dietary_habits', 'N/A'),
            'Financial Stress': f"{input_data.get('financial_stress', 'N/A')}/5"
        }
        
        for param, value in formatted_inputs.items():
            table_data.append([param, value])
        
        # Create table
        input_table = Table(table_data, colWidths=[3*inch, 2.5*inch])
        input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(input_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_feature_analysis(self, feature_contributions):
        """Create feature contribution analysis"""
        elements = []
        
        header = Paragraph("Detailed Factor Analysis", self.styles['CustomSubtitle'])
        elements.append(header)
        
        explanation = Paragraph(
            """The following factors contributed to your risk score. Higher values indicate 
            greater contribution to overall risk. This analysis helps identify specific areas 
            that may benefit from attention or intervention.""",
            self.styles['Normal']
        )
        elements.append(explanation)
        elements.append(Spacer(1, 0.15*inch))
        
        # Sort by contribution
        sorted_features = sorted(
            feature_contributions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Create table
        table_data = [['Risk Factor', 'Contribution (%)', 'Impact Level']]
        
        for feature, contribution in sorted_features:
            # Determine impact level
            if contribution >= 15:
                impact = "High"
                impact_color = colors.HexColor('#e74c3c')
            elif contribution >= 8:
                impact = "Moderate"
                impact_color = colors.HexColor('#f39c12')
            else:
                impact = "Low"
                impact_color = colors.HexColor('#2ecc71')
            
            table_data.append([
                feature,
                f"{contribution:.1f}%",
                impact
            ])
        
        feature_table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(feature_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_recommendations(self, risk_level, input_data):
        """Create personalized recommendations"""
        elements = []
        
        header = Paragraph("Personalized Recommendations", self.styles['CustomSubtitle'])
        elements.append(header)
        
        recommendations = []
        
        # Sleep recommendations
        if input_data.get('sleep_duration') in ['Less than 5 hours', '5-6 hours']:
            recommendations.append({
                'title': '😴 Improve Sleep Hygiene',
                'items': [
                    'Aim for 7-8 hours of sleep per night',
                    'Establish a consistent sleep schedule',
                    'Avoid screens 1 hour before bedtime',
                    'Create a relaxing bedtime routine'
                ]
            })
        
        # Academic pressure recommendations
        if input_data.get('academic_pressure', 0) >= 4:
            recommendations.append({
                'title': '📚 Manage Academic Stress',
                'items': [
                    'Break large tasks into smaller, manageable chunks',
                    'Use time management techniques (Pomodoro)',
                    'Seek tutoring or join study groups',
                    'Discuss workload concerns with professors'
                ]
            })
        
        # Financial stress recommendations
        if input_data.get('financial_stress', 0) >= 4:
            recommendations.append({
                'title': '💰 Address Financial Concerns',
                'items': [
                    'Explore scholarship and grant opportunities',
                    'Consult with financial aid office',
                    'Look into part-time campus employment',
                    'Create and stick to a realistic budget'
                ]
            })
        
        # Dietary recommendations
        if input_data.get('dietary_habits') == 'Unhealthy':
            recommendations.append({
                'title': '🥗 Improve Nutrition',
                'items': [
                    'Eat regular, balanced meals',
                    'Stay hydrated throughout the day',
                    'Limit caffeine and sugar intake',
                    'Include fruits and vegetables daily'
                ]
            })
        
        # Study satisfaction recommendations
        if input_data.get('study_satisfaction', 5) <= 2:
            recommendations.append({
                'title': '🎯 Increase Academic Engagement',
                'items': [
                    'Explore connections between coursework and interests',
                    'Join academic clubs or research opportunities',
                    'Seek academic advising for course selection',
                    'Consider talking to a career counselor'
                ]
            })
        
        # General recommendations if low risk
        if risk_level == 'Low' and not recommendations:
            recommendations.append({
                'title': '✅ Maintain Your Wellbeing',
                'items': [
                    'Continue your healthy sleep schedule',
                    'Keep up with balanced nutrition',
                    'Maintain work-life balance',
                    'Stay connected with support networks',
                    'Practice regular self-care activities'
                ]
            })
        
        # Format recommendations
        for rec in recommendations:
            elements.append(Paragraph(f"<b>{rec['title']}</b>", self.styles['SectionHeader']))
            for item in rec['items']:
                bullet = Paragraph(f"• {item}", self.styles['Normal'])
                elements.append(bullet)
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_resources(self, risk_level):
        """Create resource section"""
        elements = []
        
        header = Paragraph("Mental Health Resources", self.styles['CustomSubtitle'])
        elements.append(header)
        
        if risk_level == 'High':
            urgent = Paragraph(
                "<b>⚠️ IMMEDIATE ACTION RECOMMENDED</b>",
                self.styles['Warning']
            )
            elements.append(urgent)
            elements.append(Spacer(1, 0.1*inch))
        
        # Resources table
        resource_data = [
            ['Resource', 'Contact Information', 'Availability']
        ]
        
        resources = [
            ['Campus Counseling Center', 'XXX-XXX-XXXX', 'Mon-Fri, 9 AM - 5 PM'],
            ['National Suicide Prevention Lifeline', '1-800-273-8255', '24/7'],
            ['Crisis Text Line', 'Text HOME to 741741', '24/7'],
            ['Student Health Services', 'Visit Student Center', 'Walk-in Hours Daily'],
            ['Emergency Services', '911', '24/7']
        ]
        
        for resource in resources:
            resource_data.append(resource)
        
        resource_table = Table(resource_data, colWidths=[2.2*inch, 2*inch, 1.3*inch])
        resource_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fef2f2')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        elements.append(resource_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_disclaimer(self):
        """Create disclaimer section"""
        elements = []
        
        header = Paragraph("Important Disclaimer", self.styles['SectionHeader'])
        elements.append(header)
        
        disclaimer_text = """
            <b>This is a screening tool, not a medical diagnosis.</b><br/><br/>
            
            This assessment uses machine learning to identify potential risk factors based on 
            lifestyle and academic patterns. It does not replace professional medical evaluation 
            or diagnosis. The predictions are based on statistical patterns and may not account 
            for all individual circumstances.<br/><br/>
            
            <b>If you are experiencing mental health difficulties, please consult with a qualified 
            healthcare provider.</b> Mental health conditions are complex and require professional 
            assessment and treatment.<br/><br/>
            
            This report is confidential and intended for personal use only. Data privacy is 
            maintained throughout the assessment process, with no information stored in external 
            databases.<br/><br/>
            
            <b>Model Information:</b><br/>
            • Algorithm: Random Forest Classifier<br/>
            • Training Data: 27,900 student records<br/>
            • Overall Accuracy: 84.1%<br/>
            • Recall Rate: 87% (sensitivity to at-risk cases)<br/>
            • Last Updated: January 2025<br/><br/>
            
            For questions about this assessment or tool, please contact your campus counseling 
            center or student health services.
        """
        
        disclaimer = Paragraph(disclaimer_text, self.styles['Normal'])
        elements.append(disclaimer)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_footer(self):
        """Create report footer"""
        elements = []
        
        footer_text = f"""
            Mental Health Prediction Dashboard | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
            Developed by: Divyanshi Sahu, Deeksha Singh, Chhavi Agrahari, Mishika Kulshrestha<br/>
            GL Bajaj Institute of Technology & Management | Department of CSE (Data Science)<br/>
            <b>CONFIDENTIAL - For Personal Use Only</b>
        """
        
        footer = Paragraph(footer_text, self.styles['Footer'])
        elements.append(Spacer(1, 0.3*inch))
        elements.append(footer)
        
        return elements
    
    def generate_report(self, prediction_result, input_data, output_path=None):
        """
        Generate complete PDF report
        
        Args:
            prediction_result: Dictionary with prediction results
            input_data: Dictionary with user input data
            output_path: Path to save PDF (if None, returns BytesIO)
            
        Returns:
            BytesIO object or saves to file
        """
        # Create buffer or file
        if output_path:
            buffer = output_path
        else:
            buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build report content
        story = []
        
        # Add header
        story.extend(self._create_header())
        
        # Add risk summary
        story.extend(self._create_risk_summary(prediction_result))
        
        # Add input summary
        story.extend(self._create_input_summary(input_data))
        
        # Page break
        story.append(PageBreak())
        
        # Add feature analysis
        story.extend(self._create_feature_analysis(
            prediction_result['feature_contributions']
        ))
        
        # Add recommendations
        story.extend(self._create_recommendations(
            prediction_result['risk_level'],
            input_data
        ))
        
        # Page break
        story.append(PageBreak())
        
        # Add resources
        story.extend(self._create_resources(prediction_result['risk_level']))
        
        # Add disclaimer
        story.extend(self._create_disclaimer())
        
        # Add footer
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        # Return buffer or confirm file creation
        if output_path:
            return True
        else:
            buffer.seek(0)
            return buffer


def generate_quick_report(prediction_result, input_data):
    """
    Quick function to generate report and return BytesIO
    
    Args:
        prediction_result: Prediction results dictionary
        input_data: User input data dictionary
        
    Returns:
        BytesIO object containing PDF
    """
    generator = MentalHealthReportGenerator()
    return generator.generate_report(prediction_result, input_data)


if __name__ == "__main__":
    # Example usage
    print("Report Generator Module")
    print("Use generate_quick_report() to create PDF reports")