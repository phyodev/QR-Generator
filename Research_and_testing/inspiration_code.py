import qrcode

# Generate QR code image
img = qrcode.make('Hello, World!')

# Save image to a file
img.save('hello_world.png')