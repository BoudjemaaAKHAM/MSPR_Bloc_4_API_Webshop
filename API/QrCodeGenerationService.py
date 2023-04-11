import qrcode


def generatecode(data, path, filename):
    # Creating a QRCode object of the size specified by the user
    qr = qrcode.QRCode(version=10,
                       box_size=10,
                       border=5)
    qr.add_data(data)  # Adding the data to be encoded to the QRCode object
    qr.make(fit=True)  # Making the entire QR Code space utilized
    img = qr.make_image()  # Generating the QR Code
    filedirec = path + filename  # Getting the directory where the file has to be save
    img.save(f'{filedirec}.png')  # Saving the QR Code
    # Showing the pop up message on saving the file