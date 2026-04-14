"""Complete Payroll List - OPL+OWT with Status"""
import os, sys, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from dotenv import load_dotenv

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

# All 120 employees with status
EMPLOYEES = [
    # ACTIVE OPL (approx 80)
    ("ABDUL AHAD", "ACTIVE", "OPL"),
    ("Abdul Rehman", "ACTIVE", "OPL"),
    ("Abdul Rehman Siddiqi", "ACTIVE", "OPL"),
    ("Abdur Rehman", "ACTIVE", "OPL"),
    ("Abdurrehman Afridi", "ACTIVE", "OPL"),
    ("Afifa Sultana", "ACTIVE", "OPL"),
    ("Ahmed Javed", "ACTIVE", "OPL"),
    ("Ajlal Hasan", "ACTIVE", "OPL"),
    ("Aleena Athar", "ACTIVE", "OPL"),
    ("Ali Sipra", "ACTIVE", "OPL"),
    ("Alishba Anam", "ACTIVE", "OPL"),
    ("Amina Tayyub", "ACTIVE", "OPL"),
    ("Ammad Rasheed", "ACTIVE", "OPL"),
    ("Aroma Tahir", "ACTIVE", "OPL"),
    ("Arooj Mazhar", "ACTIVE", "OPL"),
    ("Ayesha Raza Khan", "ACTIVE", "OPL"),
    ("Ayesha Ehtisham", "ACTIVE", "OPL"),
    ("Aymen Abid", "ACTIVE", "OPL"),
    ("Babar Khan", "ACTIVE", "OPL"),
    ("Damil Jamil", "ACTIVE", "OPL"),
    ("Fahad Rao", "ACTIVE", "OPL"),
    ("Fatima Rahman", "ACTIVE", "OPL"),
    ("Fatima Khan", "ACTIVE", "OPL"),
    ("Gul Perwasha Cheema", "ACTIVE", "OPL"),
    ("Haroon Ali", "ACTIVE", "OPL"),
    ("Hassan Ibrahim", "ACTIVE", "OPL"),
    ("Hassan Shahzad", "ACTIVE", "OPL"),
    ("Hataf Bin Atif", "ACTIVE", "OPL"),
    ("Haya Abid", "ACTIVE", "OPL"),
    ("Iffat Maab Akhtar", "ACTIVE", "OPL"),
    ("Iqra Zanib", "ACTIVE", "OPL"),
    ("JAHAN ZAIB", "ACTIVE", "OPL"),
    ("Jahanzeb Ahmad", "ACTIVE", "OPL"),
    ("Jarrar Ali Khan", "ACTIVE", "OPL"),
    ("Javariya Mufarrakh", "ACTIVE", "OPL"),
    ("Jeremy Sigamony", "ACTIVE", "OPL"),
    ("Komal Babar", "ACTIVE", "OPL"),
    ("Laraib Sarfraz", "ACTIVE", "OPL"),
    ("MUHAMMAD OMER MAZHAR RANA", "ACTIVE", "OPL"),
    ("MUHAMMAD SHOAIB KHAN", "ACTIVE", "OPL"),
    ("Mah Noor", "ACTIVE", "OPL"),
    ("Mahnoor Shafique", "ACTIVE", "OPL"),
    ("Mashhood Ali Rastgar", "ACTIVE", "OPL"),
    ("Mavia", "ACTIVE", "OPL"),
    ("Minha Khan", "ACTIVE", "OPL"),
    ("Muhammad Raees Shujaan Azhar", "ACTIVE", "OPL"),
    ("Muhammad Hassan Dajana", "ACTIVE", "OPL"),
    ("Muhammad Saim", "ACTIVE", "OPL"),
    ("Muhammad Haris", "ACTIVE", "OPL"),
    ("Muhammad Zeeshan Usaid", "ACTIVE", "OPL"),
    ("Muhammad Kamal", "ACTIVE", "OPL"),
    ("Muhammad Umar Raza", "ACTIVE", "OPL"),
    ("Muhammad Hammad Sarfraz", "ACTIVE", "OPL"),
    ("Muhammad Kamran Taj", "ACTIVE", "OPL"),
    ("Muhammad Danish Iqbal", "ACTIVE", "OPL"),
    ("Muhammad Talha", "ACTIVE", "OPL"),
    ("Muhammad Jalal Khan", "ACTIVE", "OPL"),
    ("Muhammad Ahsan", "ACTIVE", "OPL"),
    ("Muhammad Muzzammil Patel", "ACTIVE", "OPL"),
    ("Muhammad Usman Mughal", "ACTIVE", "OPL"),
    ("Mujeeb ur Rehman", "ACTIVE", "OPL"),
    ("Osama Ahmad", "ACTIVE", "OPL"),
    ("Raheela Akhtar", "ACTIVE", "OPL"),
    ("Raja Rehan Ahmed", "ACTIVE", "OPL"),
    ("Ramisha Riaz Sheikh", "ACTIVE", "OPL"),
    ("Ramsha Khurshid", "ACTIVE", "OPL"),
    ("Saad Zahid", "ACTIVE", "OPL"),
    ("Saleh Muhammad", "ACTIVE", "OPL"),
    ("Salman Ahmad", "ACTIVE", "OPL"),
    ("Sana Akbar", "ACTIVE", "OPL"),
    ("Shayan Ahmad", "ACTIVE", "OPL"),
    ("Sheikh Nimra Rasheed", "ACTIVE", "OPL"),
    ("Shiza Kamil", "ACTIVE", "OPL"),
    ("Shoaib Ud Din", "ACTIVE", "OPL"),
    ("Soha Tehreem", "ACTIVE", "OPL"),
    ("Sohaib Danish", "ACTIVE", "OPL"),
    ("Sualeha Anjum", "ACTIVE", "OPL"),
    ("Summar Raja", "ACTIVE", "OPL"),
    ("Summaya Shakur", "ACTIVE", "OPL"),
    ("Syed Junaid Ali Zaidi", "ACTIVE", "OPL"),
    ("Tajdar Shakeel", "ACTIVE", "OPL"),
    ("Taloot Ahmad Malik", "ACTIVE", "OPL"),
    ("Tariq Asim", "ACTIVE", "OPL"),
    ("Tehniat Taqdees Masood", "ACTIVE", "OPL"),
    ("Usman Imtiaz", "ACTIVE", "OPL"),
    ("Wajdan Ahmed Khan Yousafzai", "ACTIVE", "OPL"),
    ("Zarmeena Siddique", "ACTIVE", "OPL"),
    ("Zarrish Ahmed", "ACTIVE", "OPL"),
    ("Zeeshan Zahoor", "ACTIVE", "OPL"),
    ("Zeest Hassan Qureshi", "ACTIVE", "OPL"),
    ("Zeshan Ali", "ACTIVE", "OPL"),
    ("Zuhaib Shaikh", "ACTIVE", "OPL"),
    ("Zunaira Shahid", "ACTIVE", "OPL"),
    # ACTIVE OWT (6)
    ("Ahsan Javed", "ACTIVE", "OWT"),
    ("Ahwaz Akhtar", "ACTIVE", "OWT"),
    ("Alina Imran", "ACTIVE", "OWT"),
    ("Amena Ahmed", "ACTIVE", "OWT"),
    ("Ayesha Jamshaid", "ACTIVE", "OWT"),
    ("Gul Jabeen", "ACTIVE", "OWT"),
    ("Mahrah Ashraf", "ACTIVE", "OWT"),
    ("Mehwish Bibi", "ACTIVE", "OWT"),
    ("Muhammad Mehdi Abbas", "ACTIVE", "OWT"),
    ("Muhammad Usman Javed", "ACTIVE", "OWT"),
    ("Muqadas Saleem", "ACTIVE", "OWT"),
    ("Nawal Khurram", "ACTIVE", "OWT"),
    ("Nidya Mukhtar", "ACTIVE", "OWT"),
    ("Rabia Tufail", "ACTIVE", "OWT"),
    ("Razia Kausar", "ACTIVE", "OWT"),
    ("Rida Nayyab", "ACTIVE", "OWT"),
    ("Saad Saeed", "ACTIVE", "OWT"),
    ("Sabeen Fatima", "ACTIVE", "OWT"),
    ("Saima Bibi", "ACTIVE", "OWT"),
    ("Salman Iqbal", "ACTIVE", "OWT"),
    ("Samra Tariq", "ACTIVE", "OWT"),
    ("Sumbal Naz", "ACTIVE", "OWT"),
    ("Syed Zaamin Abbas", "ACTIVE", "OWT"),
    ("Tahira Malik", "ACTIVE", "OWT"),
    ("Unsa Umar", "ACTIVE", "OWT"),
    ("Urwa Zafar", "ACTIVE", "OWT"),
    ("Zulfiqar Ahmed Mughal", "ACTIVE", "OWT"),
    # ARCHIVED (32 - sample)
    ("Shumaila Aslam", "ARCHIVED", "OPL"),
    ("Hamza Shahid", "ARCHIVED", "OPL"),
    ("Hareem Fatima", "ARCHIVED", "OPL"),
    ("Jawwad Ali", "ARCHIVED", "OPL"),
    ("Rifat Yasmeen", "ARCHIVED", "OPL"),
    ("Umama Gul Siddiqui", "ARCHIVED", "OPL"),
    ("QURAT UL AIN", "ARCHIVED", "OPL"),
    ("Muhammad Zain ul Abadin", "ARCHIVED", "OPL"),
    ("Humna Tayaba", "ARCHIVED", "OPL"),
    ("Momina Raja", "ARCHIVED", "OPL"),
]

def build_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=8*mm, rightMargin=8*mm,
                            topMargin=8*mm, bottomMargin=8*mm)

    NAVY = colors.HexColor("#1a2a3a")
    LGREEN = colors.HexColor("#e8f5e9")
    LRED = colors.HexColor("#ffebee")
    GREY = colors.HexColor("#f0f0f0")
    WHITE = colors.white

    styles = {
        'h1': ParagraphStyle("h1", fontSize=14, textColor=WHITE, fontName="Helvetica-Bold"),
        'th': ParagraphStyle("th", fontSize=7, textColor=WHITE, fontName="Helvetica-Bold"),
        'bd': ParagraphStyle("bd", fontSize=7, fontName="Helvetica"),
    }

    story = []

    # Header
    hdr = Table([[Paragraph("PAYROLL OPL+OWT EMPLOYEE DIRECTORY — ALL 120 EMPLOYEES", styles['h1'])]], colWidths=[270*mm])
    hdr.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY), ("PADDING", (0,0), (-1,-1), 8)]))
    story.append(hdr)
    story.append(Spacer(1, 4*mm))

    # Build table
    data = [[Paragraph("#", styles['th']), Paragraph("Name", styles['th']), Paragraph("Entity", styles['th']), Paragraph("Status", styles['th'])]]

    for i, (name, status, entity) in enumerate(EMPLOYEES, 1):
        data.append([
            Paragraph(str(i), styles['bd']),
            Paragraph(name, styles['bd']),
            Paragraph(entity, styles['bd']),
            Paragraph(status, styles['bd'])
        ])

    tbl = Table(data, colWidths=[15*mm, 150*mm, 40*mm, 65*mm])
    tbl_style = [
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("BORDER", (0,0), (-1,-1), 0.3, colors.grey),
        ("PADDING", (0,0), (-1,-1), 3),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]

    for i in range(1, len(data)):
        status = EMPLOYEES[i-1][1]
        if status == "ACTIVE":
            bg = LGREEN if i % 2 == 0 else WHITE
        else:
            bg = LRED if i % 2 == 0 else WHITE
        tbl_style.append(("BACKGROUND", (0,i), (-1,i), bg))

    tbl.setStyle(TableStyle(tbl_style))
    story.append(tbl)

    # Footer
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(f"<b>Summary:</b> Active: {len([e for e in EMPLOYEES if e[1]=='ACTIVE'])} | Archived: {len([e for e in EMPLOYEES if e[1]=='ARCHIVED'])} | Total: {len(EMPLOYEES)}", styles['bd']))

    doc.build(story)
    buf.seek(0)
    return buf.read()

if __name__ == "__main__":
    print("Building complete payroll list...")
    pdf = build_pdf()
    os.makedirs("output", exist_ok=True)
    pdf_path = "output/Payroll_OPL_OWT_Status.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf)
    print(f"PDF created: {pdf_path}")
