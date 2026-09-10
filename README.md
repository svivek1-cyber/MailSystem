# Email Sender

Lightweight Python email sender supporting attachments (PDF, XLSX, DOCX, etc.), HTML links, and inline graphics.

Usage

- Edit `app.py` with your SMTP credentials, recipient address(es), and file paths.
- Run the example:

```bash
python app.py
```

**Features**

- Attach arbitrary files (PDF, Excel, etc.)
- Include links inside the HTML body
- Embed inline graphics (referenced by `cid` in HTML, e.g. `<img src="cid:logo">`)

**Files**

- [app.py](email_sender.py): core implementation
- [requirements.txt](requirements.txt): dependency hints

### Notes

- This project uses the Python standard library (`smtplib`, `email`) and requires Python 3.8+.
- Ensure attachments and inline image paths exist before running.

### **To get create your own YOUR_GMAIL_APP_PASSWORD**

1. go to [https://myaccount.google.com/apppasswords]()
2. create your own and copy 16 character password and paste.
