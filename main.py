import logging
from reportlab.lib import colors
from reportlab.lib.units import mm, inch, pica
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

log = logging.getLogger(__name__)

base_table_input_style = [
    ('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.black),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('LINEBEFORE', (0, 0), (0, 0), 1, colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 0),
    ('LEFTPADDING', (0, 0), (-1, -1), 2),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
]

base_input_row_height = 9 * mm
base_table_width = int((letter[0] - (11 * mm * 2)) - mm - 2)


def get_header():
    header = '<font size=10 fontName="Helvetica-Bold">' \
             'EQUIPMENT INSPECTION AND MAINTENANCE WORKSHEET</font>' \
             '<br/>' \
             '<font size=7 fontName="Helvetica">' \
             'For use of this form, see DA PAM 750-8; the proponent agency is DCS, G-4.' \
             '</font>'
    header_style = ParagraphStyle(name = 'Main Heading', alignment = TA_CENTER, leading = 10)
    header_paragraph = Paragraph(header, header_style)

    data = [[header_paragraph]]

    table_style = TableStyle([
        ('LINEABOVE', (0, 0), (0, 0), 1, colors.black),
        ('LINEBEFORE', (0, 0), (0, 0), 1, colors.black),
        ('LINEAFTER', (0, 0), (0, 0), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (0, 0), 1),
    ])

    table = Table(data)
    table.setStyle(table_style)
    return table


def get_header_data():
    text_style = ParagraphStyle(name = 'Data Input', alignment = TA_LEFT, leading = 8, fontSize = 8)
    column_width = int((letter[0] - (10 * mm * 2)) / 2) - mm - 2

    data_line_1 = [
        ['1. ORGANIZATION', '2. NOMENCLATURE AND MODEL']
    ]
    table_style_tuples_line_1 = [
        *base_table_input_style,
        ('LINEAFTER', (1, 0), (1, 0), 1, colors.black),
    ]
    table_style_line_1 = TableStyle(table_style_tuples_line_1)
    table_line_1 = Table(
        data_line_1,
        rowHeights = [base_input_row_height for i in range(1)],
        colWidths = [column_width for i in range(1)]
    )
    table_line_1.setStyle(table_style_line_1)

    data_raw_line_2 = [
        ['3. REGISTRATION/SERIAL/NSN', '4<i>a</i>. MILES', '<i>b</i>. HOURS', '<i>c</i>. ROUNDS FIRED',
         '<i>d</i>. HOT STARTS', '5. DATE', '6. TYPE INSPECTION']
    ]
    table_style_tuples_line_2 = [
        *base_table_input_style,
        ('LINEAFTER', (len(data_raw_line_2[0]) - 1, 0), (len(data_raw_line_2[0]) - 1, 0), 1, colors.black),
    ]
    table_style_line_2 = TableStyle(table_style_tuples_line_2)
    data_line_2 = [[Paragraph(item, text_style) for item in row] for row in data_raw_line_2]
    table_line_2 = Table(
        data_line_2,
        rowHeights = [base_input_row_height for i in range(1)],
        colWidths = [50 * mm + 5, *[19 * mm for i in range(4)], 30 * mm, 34 * mm]
    )
    table_line_2.setStyle(table_style_line_2)

    return [table_line_1, table_line_2]


def get_applicable_reference():
    header_text_style = ParagraphStyle(
        name = 'Data Input Applicable Reference',
        alignment = TA_CENTER,
        leading = 8,
        fontSize = 8
    )

    data_header = [['7.', Paragraph('APPLICABLE REFERENCE', header_text_style)]]
    table_style_tuples_header = [
        *base_table_input_style,
        ('LINEAFTER', (1, 0), (1, 0), 1, colors.black),
    ]
    table_header_style = TableStyle(table_style_tuples_header)
    table_header = Table(
        data_header,
        rowHeights = [11 for i in range(1)],
        colWidths = [0, base_table_width]
    )
    table_header.setStyle(table_header_style)

    data_line_1 = [
        ['TM NUMBER', 'TM DATE', 'TM NUMBER', 'TM DATE'],
    ]
    table_style_tuples_line_1 = [
        *base_table_input_style,
        ('LINEAFTER', (3, 0), (3, 0), 1, colors.black),
    ]
    table_style_line_1 = TableStyle(table_style_tuples_line_1)
    table_line_1 = Table(
        data_line_1,
        rowHeights = [base_input_row_height for i in range(1)],
        colWidths = [
            (base_table_width / 2) * 0.65,
            (base_table_width / 2) * 0.35,
            (base_table_width / 2) * 0.65,
            (base_table_width / 2) * 0.35
        ]
    )
    table_line_1.setStyle(table_style_line_1)

    line_2_text_style = ParagraphStyle(name = 'Line 2 Text', alignment = TA_LEFT, leading = 10, fontSize = 10)
    data_line_2 = [
        ['COLUMN a - Enter RM item number.<br/>'
         'COLUMN b - Enter the applicable condition status symbol.<br/>'
         'COLUMN c - Enter deficiencies and shortcomings.',
         'COLUMN d - Show corrective action for deficiency or shortcoming listed in Column c.<br/>'
         'COLUMN e - Individual ascertaining completed corrective action initial in this column.']
    ]
    table_style_tuples_line_2 = [
        *base_table_input_style,
        ('LINEAFTER', (1, 0), (1, 0), 1, colors.black),
        ('LEFTPADDING', (0, 0), (1, 0), 4 * mm),
        ('TOPPADDING', (0, 0), (1, 0), 1 * mm),
        ('RIGHTPADDING', (0, 0), (1, 0), 0),
    ]
    table_style_line_2 = TableStyle(table_style_tuples_line_2)
    table_line_2 = Table(
        [[Paragraph(item, line_2_text_style) for item in row] for row in data_line_2],
        # rowHeights = [base_input_row_height for i in range(1)],
        colWidths = [(base_table_width / 2), (base_table_width / 2)]
    )
    table_line_2.setStyle(table_style_line_2)

    return [table_header, table_line_1, table_line_2]


def get_status_symbols():
    header_text_style = ParagraphStyle(
        name = 'Data Header Status Symbols',
        alignment = TA_CENTER,
        leading = 10,
        fontSize = 10
    )
    data_header = [[Paragraph('STATUS SYMBOLS', header_text_style)]]
    table_style_tuples_header = [
        *base_table_input_style,
        ('LINEAFTER', (0, 0), (0, 0), 1, colors.black),
    ]
    table_header_style = TableStyle(table_style_tuples_header)
    table_header = Table(
        data_header,
        # rowHeights = [11 for i in range(1)],
        colWidths = [base_table_width]
    )
    table_header.setStyle(table_header_style)

    line_2_text_style = ParagraphStyle(name = 'Status Symbols Text', alignment = TA_LEFT, leading = 11, fontSize = 10)
    data_line_2 = [
        ['"X" - Indicates a deficiency in the equipment that places it in an inoperable status.'
         '<br/>'
         'CIRCLED "X" - Indicates a deficiency, however, the equipment may be operated under specific limitations as '
         'directed by higher authority or as prescribed locally, until corrective action can be accomplished.'
         '<br/>'
         'HORIZONTAL DASH "(-)" - Indicates that a required inspection, component replacement, maintenance operation '
         'check, or test flight is due but has not been accomplished, or an overdue MWO has not been accomplished.'
         '<br/>',

         'DIAGONAL "(/)" - Indicates a material defect other than a deficiency which must be corrected to increase '
         'efficiency or to make the item completely serviceable.'
         '<br/>'
         'LAST NAME INITIAL IN BLACK, BLUE-BLACK INK, OR PENCIL - Indicates that a completely satisfactory '
         'condition exists.'
         '<br/>'
         'FOR AIRCRAFT - Status symbols will be recorded in red.']
    ]
    table_style_tuples_line_2 = [
        *base_table_input_style[1:],
        ('LINEAFTER', (1, 0), (1, 0), 1, colors.black),
        ('LEFTPADDING', (0, 0), (0, 0), 2 * mm),
        ('LEFTPADDING', (1, 0), (1, 0), 4 * mm),
        ('TOPPADDING', (0, 0), (1, 0), 1 * mm),
        ('RIGHTPADDING', (0, 0), (1, 0), 0),
    ]
    table_style_line_2 = TableStyle(table_style_tuples_line_2)
    table_line_2 = Table(
        [[Paragraph(item, line_2_text_style) for item in row] for row in data_line_2],
        colWidths = [(base_table_width / 2), (base_table_width / 2)]
    )
    table_line_2.setStyle(table_style_line_2)

    end_text_style = ParagraphStyle(
        name = 'Data End Status Symbols',
        alignment = TA_CENTER,
        leading = 10,
        fontSize = 10
    )
    end_data = [
        [
            Paragraph(
                '<i>ALL INSPECTIONS AND EQUIPMENT CONDITIONS RECORDED ON THIS FORM HAVE BEEN DETERMINED '
                'IN ACCORDANCE WITH DIAGNOSTIC PROCEDURES AND STANDARDS IN THE TM CITED HEREON.</i>',
                end_text_style
            )
        ]
    ]
    end_table_style_tuples = [
        *base_table_input_style,
        ('LINEAFTER', (0, 0), (0, 0), 1, colors.black),
    ]
    end_table_style = TableStyle(end_table_style_tuples)
    end_table = Table(
        end_data,
        # rowHeights = [11 for i in range(1)],
        colWidths = [base_table_width]
    )
    end_table.setStyle(end_table_style)

    return [table_header, table_line_2, end_table]


def get_signature():
    signature_text_style = ParagraphStyle(name = 'Data Input', alignment = TA_LEFT, leading = 8, fontSize = 8)
    signature_data = [
        ['8<i>a</i>. SIGNATURE <font size=7><i>(Person(s) performing inspection)</i></font>',
         '8<i>b</i>. TIME',
         '9<i>a</i>. SIGNATURE <font size=7><i>(Maintenance Supervisor)</i></font>',
         '9<i>b</i>. TIME',
         '10. MANHOURS REQUIRED'],
    ]
    signature_table_style_tuples = [
        *base_table_input_style,
        ('LINEAFTER', (4, 0), (4, 0), 1, colors.black),
        ('RIGHTPADDING', (4, 0), (4, 0), 0),
    ]
    signature_table_style = TableStyle(signature_table_style_tuples)
    signature_table = Table(
        [[Paragraph(item, signature_text_style) for item in row] for row in signature_data],
        rowHeights = [base_input_row_height * 2 for i in range(1)],
        colWidths = [
            base_table_width * 0.33,
            base_table_width * 0.11,
            base_table_width * 0.33,
            base_table_width * 0.11,
            base_table_width * 0.12
        ]
    )
    signature_table.setStyle(signature_table_style)

    return signature_table


def create_2404():
    margin = 10 * mm

    doc = SimpleDocTemplate(
        "testing.pdf",
        pagesize = letter,
        leftMargin = margin,
        rightMargin = margin,
        topMargin = margin,
        bottomMargin = margin
    )
    story = [
        get_header(),
        *get_header_data(),
        *get_applicable_reference(),
        *get_status_symbols(),
        get_signature()
    ]

    # can = canvas.Canvas("something.pdf")
    # fonts = can.getAvailableFonts()

    doc.build(story)


if __name__ == '__main__':
    create_2404()
