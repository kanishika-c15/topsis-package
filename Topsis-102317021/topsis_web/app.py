from flask import Flask, render_template, request
import os
import smtplib
from email.message import EmailMessage
from topsis import run_topsis   # <-- IMPORTANT (correct import)

app = Flask(__name__)

# Folder to store uploaded & result files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    # -------- Read form data --------
    file = request.files["file"]
    weights = request.form["weights"]
    impacts = request.form["impacts"]
    email = request.form["email"]

    # -------- File paths --------
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "result.csv")

    # -------- Save uploaded file --------
    file.save(input_path)

    # -------- Run TOPSIS --------
    run_topsis(input_path, weights, impacts, output_path)

    # -------- Prepare Email --------
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = "your_email@gmail.com"   # <-- replace
    msg["To"] = email
    msg.set_content("Please find the attached TOPSIS result file.")

    # Attach result.csv
    with open(output_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="result.csv"
        )

    # -------- Send Email --------
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            "your_email@gmail.com",        # <-- replace
            "YOUR_APP_PASSWORD"            # <-- Gmail App Password
        )
        server.send_message(msg)

    return "Result sent to your email successfully!"

# -------- Run Flask App --------
if __name__ == "__main__":
    app.run(debug=True)
