from fpdf import FPDF, XPos, YPos
import os

class ResumeReport(FPDF):

    def header(self):

        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(31, 78, 121)

        self.cell(
            0,
            10,
            'AI Resume Intelligence Report',
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align='C'
        )

        self.set_font('Helvetica', '', 10)

        self.set_text_color(100, 100, 100)

        self.cell(
            0,
            6,
            'Skill Extraction & Career Prediction',
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align='C'
        )

        self.ln(4)

        self.set_draw_color(31, 78, 121)

        self.line(10, self.get_y(), 200, self.get_y())

        self.ln(6)

    def footer(self):

        self.set_y(-15)

        self.set_font('Helvetica', 'I', 8)

        self.set_text_color(150, 150, 150)

        self.cell(
            0,
            10,
            f'Page {self.page_no()}',
            align='C'
        )

def generate_report(
    skills,
    predicted_roles,
    summary,
    reasoning,
    output_path='report_output.pdf'
):

    pdf = ResumeReport()

    pdf.add_page()

    # SUMMARY SECTION

    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(31, 78, 121)

    pdf.cell(
        0,
        10,
        'Resume Summary',
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT
    )

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(60, 60, 60)

    pdf.multi_cell(0, 7, summary)

    pdf.ln(5)

    # SKILLS SECTION

    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(31, 78, 121)

    pdf.cell(
        0,
        10,
        'Extracted Skills',
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT
    )

    pdf.ln(2)

    technical = skills.get('technical', [])
    soft = skills.get('soft', [])

    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(50, 50, 50)

    pdf.cell(
        0,
        8,
        'Technical Skills:',
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT
    )

    pdf.set_font('Helvetica', '', 10)

    for skill in technical:
        pdf.cell(
            0,
            6,
            f'- {skill.title()}',
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )

    pdf.ln(2)

    pdf.set_font('Helvetica', 'B', 11)

    pdf.cell(
        0,
        8,
        'Soft Skills:',
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT
    )

    pdf.set_font('Helvetica', '', 10)

    for skill in soft:
        pdf.cell(
            0,
            6,
            f'- {skill.title()}',
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )

    pdf.ln(6)

    # ROLE PREDICTION SECTION

    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(31, 78, 121)

    pdf.cell(
        0,
        10,
        'Career Predictions',
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT
    )

    pdf.ln(2)

    for i, role in enumerate(predicted_roles):

        label = role['role']

        confidence = role['confidence']

        pdf.set_font('Helvetica', 'B', 11)

        pdf.cell(
            0,
            8,
            f'{i+1}. {label} ({confidence}%)',
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )

        bar_x = 15
        bar_y = pdf.get_y()

        bar_width = 170

        fill_width = (confidence / 100) * bar_width

        pdf.set_fill_color(220, 220, 220)

        pdf.rect(bar_x, bar_y, bar_width, 5, 'F')

        pdf.set_fill_color(31, 78, 121)

        pdf.rect(bar_x, bar_y, fill_width, 5, 'F')

        pdf.ln(10)

    # REASONING SECTION

    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(31, 78, 121)

    pdf.cell(
        0,
        10,
        'Prediction Reasoning',
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT
    )

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(60, 60, 60)

    pdf.multi_cell(0, 7, reasoning)

    os.makedirs(
        os.path.dirname(output_path)
        if os.path.dirname(output_path)
        else '.',
        exist_ok=True
    )

    pdf.output(output_path)

    return output_path