from flask import Flask, render_template_string, request
import base64

# for QR
import qrcode

app = Flask(__name__)

# Example image path
image_path = 'qr_code.png'

def generat_qr(payload):
    # Generate QR code image
    img = qrcode.make(payload)

    # Save image to a file
    img.save('qr_code.png')

@app.route('/generate-qr/<data>')
def generate(data):
    generat_qr(data)
    # Open the image file and read its contents as bytes
    with open(image_path, 'rb') as f:
        img_bytes = f.read()

    # Convert the image bytes to a base64 encoded string
    encoded_img = base64.b64encode(img_bytes).decode('utf-8')

    # Create the HTML template and pass in the base64 encoded image string
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Image Rendering UI</title>
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twemoji/13.1.0/twemoji.min.css" integrity="sha512-JUbjgJNcAQ2XpUJQs5uJth6NVx+ejNB4pW0+V6JLsRl/1yKcNl+Z8c3Uyehsc14EwkW5QYU+tw1c8gW0ns96OQ==" crossorigin="anonymous" />

        <style>
        /* Set image to 20% rounded corners */
        .rounded-img {
            border-radius: 7%;
        }
        
        /* Center image in both width and height of screen */
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        </style>
    </head>
    <body>
        <div class="container-fluid center">
            <h1 class="display-4 px-3">Your QR Code is here. <span class="twemoji twemoji-32">&#x1F609;</span>
            </h1>
            <img class="rounded-img img-fluid" src="data:image/jpeg;base64,{{ image }}" alt="your-image-description">
        </div>
        
        <!-- Bootstrap JavaScript -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    </body>
    </html>

    """
    return render_template_string(html_template, image=encoded_img)

if __name__ == '__main__':
    app.run()
