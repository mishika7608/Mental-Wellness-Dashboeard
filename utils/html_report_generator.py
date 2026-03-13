"""
HTML Report Generator Module
NO EXTERNAL DEPENDENCIES - Uses only Python standard library
Generates beautiful HTML reports that can be saved or printed to PDF
"""

from datetime import datetime
import base64


class HTMLReportGenerator:
    """
    Generate comprehensive HTML reports for mental health assessments
    No external dependencies required!
    """
    
    def __init__(self):
        self.report_style = """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
                padding: 20px;
            }
            
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 32px;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 16px;
                opacity: 0.9;
            }
            
            .confidential {
                background: #dc2626;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: bold;
            }
            
            .section {
                padding: 30px 40px;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .section:last-child {
                border-bottom: none;
            }
            
            .section-title {
                color: #1e3a8a;
                font-size: 24px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #3b82f6;
            }
            
            .risk-box {
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: center;
            }
            
            .risk-low {
                background: #d4edda;
                border: 2px solid #2ecc71;
                color: #155724;
            }
            
            .risk-moderate {
                background: #fff3cd;
                border: 2px solid #f39c12;
                color: #856404;
            }
            
            .risk-high {
                background: #f8d7da;
                border: 2px solid #e74c3c;
                color: #721c24;
            }
            
            .risk-level {
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0;
            }
            
            .risk-probability {
                font-size: 48px;
                font-weight: bold;
                margin: 10px 0;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            
            th {
                background: #3b82f6;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }
            
            td {
                padding: 12px;
                border-bottom: 1px solid #e5e7eb;
            }
            
            tr:nth-child(even) {
                background: #f8f9fa;
            }
            
            .factor-high {
                background: #fee2e2;
                font-weight: bold;
            }
            
            .factor-moderate {
                background: #fef3c7;
            }
            
            .factor-low {
                background: #d1fae5;
            }
            
            .recommendation {
                background: #eff6ff;
                border-left: 4px solid #3b82f6;
                padding: 15px;
                margin: 15px 0;
            }
            
            .recommendation h4 {
                color: #1e3a8a;
                margin-bottom: 10px;
            }
            
            .recommendation ul {
                margin-left: 20px;
            }
            
            .recommendation li {
                margin: 5px 0;
            }
            
            .emergency-box {
                background: #fee2e2;
                border: 2px solid #dc2626;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }
            
            .emergency-box h3 {
                color: #dc2626;
                margin-bottom: 15px;
            }
            
            .resource-table {
                margin: 20px 0;
            }
            
            .disclaimer {
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 20px;
                margin: 20px 0;
            }
            
            .footer {
                background: #f3f4f6;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #6b7280;
            }
            
            @media print {
                body {
                    background: white;
                    padding: 0;
                }
                
                .container {
                    box-shadow: none;
                }
                
                .section {
                    page-break-inside: avoid;
                }
            }
        </style>
        """
    
    def _create_header(self):
        """Create report header"""
        date_str = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        return f"""
        <div class="header">
            <h1>🧠 Mental Health Assessment Report</h1>
            <p>AI-Powered Student Wellness Screening</p>
            <p style="margin-top: 10px; font-size: 14px;">Generated: {date_str}</p>
        </div>
        <div class="confidential">
            CONFIDENTIAL - This report contains sensitive health information
        </div>
        """
    
    def _create_risk_summary(self, prediction_result):
        """Create risk level summary section"""
        risk_level = prediction_result['risk_level']
        probability = prediction_result['probability']
        risk_color = prediction_result['risk_color']
        
        risk_class = f"risk-{risk_color}"
        
        interpretation = {
            'Low': """Your assessment indicates low risk for depression based on current lifestyle 
                     and academic factors. Your responses suggest healthy patterns in sleep, stress 
                     management, and overall wellbeing. Continue maintaining these positive habits.""",
            'Moderate': """Your assessment indicates moderate risk for depression. Some factors suggest 
                          elevated stress levels that may benefit from attention and lifestyle adjustments. 
                          Consider reaching out to campus resources for preventive support.""",
            'High': """Your assessment indicates high risk for depression. Multiple risk factors have 
                      been identified that warrant immediate attention. We strongly recommend scheduling 
                      an appointment with a mental health professional for proper evaluation."""
        }
        
        return f"""
        <div class="section">
            <h2 class="section-title">Risk Assessment Summary</h2>
            
            <div class="risk-box {risk_class}">
                <div class="risk-level">{risk_level} Risk</div>
                <div class="risk-probability">{probability}%</div>
                <p>Depression Risk Probability</p>
            </div>
            
            <p style="margin-top: 20px;">{interpretation.get(risk_level, '')}</p>
            
            <table style="margin-top: 20px;">
                <tr>
                    <td><strong>Assessment Date:</strong></td>
                    <td>{datetime.now().strftime('%B %d, %Y')}</td>
                </tr>
                <tr>
                    <td><strong>Risk Level:</strong></td>
                    <td>{risk_level}</td>
                </tr>
                <tr>
                    <td><strong>Probability Score:</strong></td>
                    <td>{probability}%</td>
                </tr>
            </table>
        </div>
        """
    
    def _create_input_summary(self, input_data):
        """Create summary of input data"""
        
        rows = ""
        formatted_data = {
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
        
        for param, value in formatted_data.items():
            rows += f"<tr><td><strong>{param}</strong></td><td>{value}</td></tr>"
        
        return f"""
        <div class="section">
            <h2 class="section-title">Your Assessment Inputs</h2>
            <table>
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Your Response</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def _create_feature_analysis(self, feature_contributions):
        """Create feature contribution analysis"""
        
        sorted_features = sorted(
            feature_contributions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        rows = ""
        for feature, contribution in sorted_features:
            if contribution >= 15:
                impact = "High"
                row_class = "factor-high"
            elif contribution >= 8:
                impact = "Moderate"
                row_class = "factor-moderate"
            else:
                impact = "Low"
                row_class = "factor-low"
            
            rows += f"""
            <tr class="{row_class}">
                <td><strong>{feature}</strong></td>
                <td>{contribution:.1f}%</td>
                <td>{impact}</td>
            </tr>
            """
        
        return f"""
        <div class="section">
            <h2 class="section-title">Detailed Factor Analysis</h2>
            <p>The following factors contributed to your risk score. Higher values indicate 
            greater contribution to overall risk.</p>
            
            <table style="margin-top: 20px;">
                <thead>
                    <tr>
                        <th>Risk Factor</th>
                        <th>Contribution</th>
                        <th>Impact Level</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def _create_recommendations(self, risk_level, input_data):
        """Create personalized recommendations"""
        
        recommendations_html = ""
        
        # Sleep recommendations
        if input_data.get('sleep_duration') in ['Less than 5 hours', '5-6 hours']:
            recommendations_html += """
            <div class="recommendation">
                <h4>😴 Improve Sleep Hygiene</h4>
                <ul>
                    <li>Aim for 7-8 hours of sleep per night</li>
                    <li>Establish a consistent sleep schedule</li>
                    <li>Avoid screens 1 hour before bedtime</li>
                    <li>Create a relaxing bedtime routine</li>
                </ul>
            </div>
            """
        
        # Academic pressure recommendations
        if input_data.get('academic_pressure', 0) >= 4:
            recommendations_html += """
            <div class="recommendation">
                <h4>📚 Manage Academic Stress</h4>
                <ul>
                    <li>Break large tasks into smaller, manageable chunks</li>
                    <li>Use time management techniques (Pomodoro)</li>
                    <li>Seek tutoring or join study groups</li>
                    <li>Discuss workload concerns with professors</li>
                </ul>
            </div>
            """
        
        # Financial stress recommendations
        if input_data.get('financial_stress', 0) >= 4:
            recommendations_html += """
            <div class="recommendation">
                <h4>💰 Address Financial Concerns</h4>
                <ul>
                    <li>Explore scholarship and grant opportunities</li>
                    <li>Consult with financial aid office</li>
                    <li>Look into part-time campus employment</li>
                    <li>Create and stick to a realistic budget</li>
                </ul>
            </div>
            """
        
        # Dietary recommendations
        if input_data.get('dietary_habits') == 'Unhealthy':
            recommendations_html += """
            <div class="recommendation">
                <h4>🥗 Improve Nutrition</h4>
                <ul>
                    <li>Eat regular, balanced meals</li>
                    <li>Stay hydrated throughout the day</li>
                    <li>Limit caffeine and sugar intake</li>
                    <li>Include fruits and vegetables daily</li>
                </ul>
            </div>
            """
        
        # General recommendations if low risk
        if risk_level == 'Low' and not recommendations_html:
            recommendations_html = """
            <div class="recommendation">
                <h4>✅ Maintain Your Wellbeing</h4>
                <ul>
                    <li>Continue your healthy sleep schedule</li>
                    <li>Keep up with balanced nutrition</li>
                    <li>Maintain work-life balance</li>
                    <li>Stay connected with support networks</li>
                    <li>Practice regular self-care activities</li>
                </ul>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2 class="section-title">Personalized Recommendations</h2>
            {recommendations_html}
        </div>
        """
    
    def _create_resources(self, risk_level):
        """Create resource section"""
        
        emergency_html = ""
        if risk_level == 'High':
            emergency_html = """
            <div class="emergency-box">
                <h3>⚠️ IMMEDIATE ACTION RECOMMENDED</h3>
                <p>Based on your assessment, we strongly recommend seeking professional support.</p>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2 class="section-title">Mental Health Resources</h2>
            
            {emergency_html}
            
            <table class="resource-table">
                <thead>
                    <tr>
                        <th>Resource</th>
                        <th>Contact</th>
                        <th>Availability</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Campus Counseling Center</strong></td>
                        <td>XXX-XXX-XXXX</td>
                        <td>Mon-Fri, 9 AM - 5 PM</td>
                    </tr>
                    <tr>
                        <td><strong>National Suicide Prevention Lifeline</strong></td>
                        <td>1-800-273-8255</td>
                        <td>24/7</td>
                    </tr>
                    <tr>
                        <td><strong>Crisis Text Line</strong></td>
                        <td>Text HOME to 741741</td>
                        <td>24/7</td>
                    </tr>
                    <tr>
                        <td><strong>Student Health Services</strong></td>
                        <td>Visit Student Center</td>
                        <td>Walk-in Hours Daily</td>
                    </tr>
                    <tr>
                        <td><strong>Emergency Services</strong></td>
                        <td>911</td>
                        <td>24/7</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    
    def _create_disclaimer(self):
        """Create disclaimer section"""
        return """
        <div class="section">
            <h2 class="section-title">Important Disclaimer</h2>
            
            <div class="disclaimer">
                <h3>This is a screening tool, not a medical diagnosis.</h3>
                <p style="margin-top: 10px;">
                This assessment uses machine learning to identify potential risk factors based on 
                lifestyle and academic patterns. It does not replace professional medical evaluation 
                or diagnosis. The predictions are based on statistical patterns and may not account 
                for all individual circumstances.
                </p>
            </div>
            
            <p style="margin-top: 20px;">
                <strong>If you are experiencing mental health difficulties, please consult with a 
                qualified healthcare provider.</strong> Mental health conditions are complex and 
                require professional assessment and treatment.
            </p>
            
            <h4 style="margin-top: 20px; color: #1e3a8a;">Model Information:</h4>
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li>Algorithm: Random Forest Classifier</li>
                <li>Training Data: 27,900 student records</li>
                <li>Overall Accuracy: 84.1%</li>
                <li>Recall Rate: 87% (sensitivity to at-risk cases)</li>
                <li>Last Updated: January 2025</li>
            </ul>
            
            <p style="margin-top: 20px;">
                This report is confidential and intended for personal use only. Data privacy is 
                maintained throughout the assessment process, with no information stored in external 
                databases.
            </p>
        </div>
        """
    
    def _create_footer(self):
        """Create report footer"""
        return f"""
        <div class="footer">
            <p><strong>Mental Health Prediction Dashboard</strong></p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Developed by: Divyanshi Sahu, Deeksha Singh, Chhavi Agrahari, Mishika Kulshrestha</p>
            <p>GL Bajaj Institute of Technology & Management | Department of CSE (Data Science)</p>
            <p style="margin-top: 10px;"><strong>CONFIDENTIAL - For Personal Use Only</strong></p>
        </div>
        """
    
    def generate_html_report(self, prediction_result, input_data):
        """
        Generate complete HTML report
        
        Args:
            prediction_result: Dictionary with prediction results
            input_data: Dictionary with user input data
            
        Returns:
            HTML string
        """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mental Health Assessment Report</title>
            {self.report_style}
        </head>
        <body>
            <div class="container">
                {self._create_header()}
                {self._create_risk_summary(prediction_result)}
                {self._create_input_summary(input_data)}
                {self._create_feature_analysis(prediction_result['feature_contributions'])}
                {self._create_recommendations(prediction_result['risk_level'], input_data)}
                {self._create_resources(prediction_result['risk_level'])}
                {self._create_disclaimer()}
                {self._create_footer()}
            </div>
        </body>
        </html>
        """
        
        return html


def generate_html_report(prediction_result, input_data):
    """
    Quick function to generate HTML report
    
    Args:
        prediction_result: Prediction results dictionary
        input_data: User input data dictionary
        
    Returns:
        HTML string
    """
    generator = HTMLReportGenerator()
    return generator.generate_html_report(prediction_result, input_data)


if __name__ == "__main__":
    # Example usage
    print("HTML Report Generator Module")
    print("No external dependencies required!")
    print("Use generate_html_report() to create HTML reports")