import qrcode
qr = qrcode.QRCode(
    version = 4,
    box_size = 10,
    border = 5
)
data = "https://github.com/vickypedia-12"

qr.add_data(data)
qr.make(fit = True)
img = qr.make_image(fill="black", backColor = "white")
img.save("Github.png")