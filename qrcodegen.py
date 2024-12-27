from flask import Flask, render_template, request
import qrcode
import os

qrcodegen = Flask(__name__)
# Ensure the directory for generated QR codes exists
os.makedirs("static/generated_qrcodes", exist_ok=True)

def generate_qr_codes(input_url, qrcode_size, qrcode_border, outputfile):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qrcode_size,
        border=qrcode_border,
    )
    qr.add_data(input_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Save the QR code image
    img.save(outputfile)

@qrcodegen.route("/")
def home():
    return render_template("qrcodegene/index.html")

@qrcodegen.route("/generate", methods=["POST"])
def generate():
    # Retrieve form data
    input_url = request.form.get("input")
    qrcode_size = int(request.form.get("size"))
    qrcode_border = int(request.form.get("border"))


    outputfile = os.path.join("static/generated_qrcodes", request.form.get("outputpath"))

    # Generate the QR code
    generate_qr_codes(input_url, qrcode_size, qrcode_border, outputfile)

    # Render the result page with the path to the generated QR code
    return render_template("qrcodegene/result.html", qrcode_path=outputfile)

if __name__ == "__main__":
    qrcodegen.run(debug=True)


