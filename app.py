import os
import sys
import time
import argparse
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file (if it exists)
load_dotenv()

# -----------------------------
# Configuration
# -----------------------------
SENDER_EMAIL = "USER_EMAIL"
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RESUME_FILE = "Resume.pdf"
EXCEL_FILE = "emails.xlsx"

# -----------------------------
# Argument parser
# -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Read email, company, role, and recruiter name from emails.xlsx and send a personalized email."
    )
    parser.add_argument("--excel-file", default=EXCEL_FILE, help="Excel file containing Email, Company, Role, and Recruiter_Name columns.")
    parser.add_argument("--resume-file", default=RESUME_FILE, help="Attachment file to send with the email.")
    parser.add_argument("--subject", default=None, help="Optional custom subject.")
    parser.add_argument("--dry-run", action="store_true", help="Preview rows from the Excel file without sending email.")
    return parser.parse_args()

# -----------------------------
# Build email body
# -----------------------------
def build_body(company, role, recruiter_name):
    return f"""
Dear {recruiter_name},

I hope you are doing well. I am interested in the {role} opportunity at {company}. 

I am very enthusiastic about the chance to contribute to {company} as a {role}. My resume is attached for your review, and I would be grateful for the opportunity to discuss my background and experience in relation to the position. 

I am especially interested in learning more about the work being done at {company} and how my skills can support the {role} team. Thank you for your time and consideration. 

I look forward to the possibility of speaking with you. 

Best regards,

[USER NAME]
Phone: +91 [XXXXXXXXXX]
Email: [USER_EMAIL]
"""

# -----------------------------
# Read rows from Excel
# -----------------------------
def get_rows(excel_file):
    if not os.path.exists(excel_file):
        print(f"Excel file not found: {excel_file}")
        sys.exit(1)

    df = pd.read_excel(excel_file)
    required_columns = ["Email", "Company", "Role", "Recruiter_Name"]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"Missing required columns in {excel_file}: {', '.join(missing)}")
        sys.exit(1)

    rows = []
    for _, row in df.iterrows():
        email = str(row["Email"]).strip() if pd.notna(row["Email"]) else ""
        company = str(row["Company"]).strip() if pd.notna(row["Company"]) else ""
        role = str(row["Role"]).strip() if pd.notna(row["Role"]) else ""
        recruiter_name = str(row["Recruiter_Name"]).strip() if pd.notna(row["Recruiter_Name"]) else ""

        if not email or not company or not role or not recruiter_name:
            print(f"Skipping incomplete row: Email={email!r}, Company={company!r}, Role={role!r}, Recruiter_Name={recruiter_name!r}")
            continue

        rows.append({
            "Email": email,
            "Company": company,
            "Role": role,
            "Recruiter_Name": recruiter_name,
        })

    return rows

# -----------------------------
# Main
# -----------------------------
def main():
    args = parse_args()

    if not APP_PASSWORD:
        print("Missing GMAIL_APP_PASSWORD in .env or environment variables.")
        sys.exit(1)

    rows = get_rows(args.excel_file)
    if not rows:
        print("No valid rows found in the Excel file.")
        sys.exit(1)

    if args.dry_run:
        print("Dry run enabled. Previewing rows from the Excel file:")
        for row in rows:
            print(f"Email={row['Email']} | Company={row['Company']} | Role={row['Role']} | Recruiter_Name={row['Recruiter_Name']}")
        print(f"Total rows prepared: {len(rows)}")
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)

        for row in rows:
            subject = args.subject or f"Application for {row['Role']} at {row['Company']}"
            body = build_body(row["Company"], row["Role"], row["Recruiter_Name"])
            recipient = row["Email"]

            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = SENDER_EMAIL
            msg["To"] = recipient
            msg.set_content(body)

            # Attach resume if available
            if os.path.exists(args.resume_file):
                with open(args.resume_file, "rb") as f:
                    file_data = f.read()

                msg.add_attachment(
                    file_data,
                    maintype="application",
                    subtype="pdf",
                    filename=os.path.basename(args.resume_file)
                )
            else:
                print(f"Warning: {args.resume_file} not found. Sending email without attachment.")

            server.send_message(msg)
            print(f"✓ Sent email to {recipient} for {row['Role']} at {row['Company']}.")

            # Delay to avoid Gmail rate limits
            time.sleep(2)

        server.quit()
        print("Done!")

    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
