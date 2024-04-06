from flask import Flask, render_template_string, request
import base64
from PIL import Image

# for QR
import qrcode

app = Flask(__name__)

image_path = 'static/images/qr_code.png'

def resize_image(path, size):
    base_width= size
    img = Image.open(path)
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img.save(path)

def generat_qr(payload):
    # Generate QR code image
    img = qrcode.make(payload)

    # Save image to a file
    img.save(image_path)
    resize_image(image_path, 400)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        generat_qr(request.form['data'])
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
                body{
                    height: 100vh;
                }
                .container {
                    height: 100%;
                }
                .qr-code-gif{
                    width: 250px;
                    height: 250px;
                }
                </style>
            </head>
            <body>
                <div class="container container d-flex flex-column flex-md-row align-items-center justify-content-center">
                    <img class="img-fluid" src="data:image/jpeg;base64,{{ image }}" alt="your-image-description">
                    <h1 class="display-4 px-3">Here!! Your QR Code<span class="twemoji twemoji-32">&#x1F609;</span> <br> <a href="/" class="btn btn-outline-info rounded-pill">Generate again</a>
                    </h1>
                    <br>
                </div>
                
                <!-- Bootstrap JavaScript -->
                <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
            </body>
            </html>

        """
        return render_template_string(html_template, image=encoded_img)
    
    html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QR Generator</title>
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twemoji/13.1.0/twemoji.min.css" integrity="sha512-JUbjgJNcAQ2XpUJQs5uJth6NVx+ejNB4pW0+V6JLsRl/1yKcNl+Z8c3Uyehsc14EwkW5QYU+tw1c8gW0ns96OQ==" crossorigin="anonymous" />


        <style>

        body{
            height: 100vh;
        }
        .container {
            height: 100%;
        }
        .qr-code-gif{
            width: 250px;
            height: 250px;
        }

        </style>
        </head>
        <body>

            <div class="container d-flex flex-column flex-md-row align-items-center justify-content-center">
                <img class="qr-code-gif mx-md-5" src="./static/images/qr-code.gif" alt="animated qr code gif">
                <div class="">
                    <h1 class="">QR Generator</h1><br>
                    <form method="post" action="/">
                        <div class="mb-5">
                            <input class="form-control py-4 rounded-pill" name="data" type="text" placeholder="paste your entry here">
                        </div>
                        <input class="btn btn-outline-info rounded-pill" class="float: right;" type="submit" value="Generate">
                    </form>
                </div>
            </div>

            <!-- Bootstrap JavaScript -->
            <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

            </body>
        </html>

        """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run()
