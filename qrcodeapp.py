import tkinter as tk
from tkinter import messagebox
from tkinter.constants import RAISED, RIDGE
from tkinter import filedialog
import cv2
import qrcode
import os , sys

def makeQR(link , filename):
    data = link.get()
    if filename.get()[-4:] == ".png":
        QRCodefile = filename.get()
    else:
        QRCodefile = filename.get() + ".png"
    QRimage = qrcode.make(data)
    try:
        QRimage.save(QRCodefile)
    except:
        messagebox.showerror(title="Error!" , message="Please enter a valid file name.")
        return
    messagebox.showinfo(title="Saved" , message="QR Image saved to " + os.getcwd() + '\\' + QRCodefile)

def show_decoded(data):
    global output
    output.configure(state='normal')
    output.delete(0.0 , tk.END)
    output.insert('end' , data)
    output.configure(state='disabled')

def webcam():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    messagebox.showinfo(title="Keep in mind" , message="Click 'Q' to close the webcam.")
    while True:
        _,img = cap.read()
        data, vertices_array, _ = detector.detectAndDecode(img)
        if vertices_array is not None:
            if data:
                messagebox.showinfo(title="QR code detected!" , message="Data: " + data)
                show_decoded(data)
                break
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            return
    orignal_stdout = sys.stdout
    with open("QRcodes.txt" , 'a') as f:
        sys.stdout = f
        print(data + '\n')
        sys.stdout = orignal_stdout
    messagebox.showinfo(title="Saved" , message="QR data saved to " + os.getcwd() + '\\QRcodes.txt')
    cap.release()
    cv2.destroyAllWindows()

def decode(filepath):
    filename = filepath.get()
    try:
        image = cv2.imread(filename)
        detector = cv2.QRCodeDetector()
        data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    except:
        messagebox.showerror(title="Error!" , message="Please select a valid image file.")
        return
    if vertices_array is not None:
        messagebox.showinfo(title="QR code detected!" , message="Data: " + data)
    else:
        messagebox.showerror(title="Error" , message="Can't extract data from QR code!")
    show_decoded(data)

def browseFiles():
    global qrpath
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = [
                                              ('Images' , "*.png*"),
                                              ("Images" , "*.jpeg*"),
                                              ("Images" , "*.jpg*")
                                          ])
    qrpath.delete(0 , tk.END)
    qrpath.insert(0 , filename)

window = tk.Tk()
window.title('QR Encoder & Decoder')
window.resizable(width=False , height=False)

CGfont = ('Century Gothic' , 18 , 'bold')
labelfont = ('Lucidia Bright' , 10 , 'normal')

encodelabel = tk.Label(window , text="Encoding" , font= CGfont , pady=1)
encodelabel.pack()

enc_frame = tk.Frame(window ,bd=5, relief=RIDGE, pady=10, padx=10)
enc_frame.pack(expand=True , fill='x')

decodelabel = tk.Label(window , text="Decoding" , font= CGfont , pady=1)
decodelabel.pack()

dec_frame = tk.Frame(window ,bd=5, relief=RIDGE, pady=10, padx=10)
dec_frame.pack()

lb = tk.Label(enc_frame ,font= labelfont , text="Type your link please!")
lb.pack()

link = tk.Entry(enc_frame  ,width=50)
link.pack()

file_label = tk.Label(enc_frame,font= labelfont , text="Save file name as:")
file_label.pack()

filename = tk.Entry(enc_frame, width=50)
filename.insert(0 , ".png")
filename.pack()

generateQR_Button = tk.Button(enc_frame, bd=3 , relief= RAISED , text="Generate QRcode" ,command=lambda:makeQR(link , filename), padx=5 , pady=3)
generateQR_Button.pack(pady=7)

browse_label = tk.Label(dec_frame,font= labelfont , text="Path to QR image:")
browse_label.pack()

qrpath = tk.Entry(dec_frame, width=50)
qrpath.pack(pady=1)

browsefile = tk.Button(dec_frame, bd=3 , relief= RAISED , text="Browse file" , command=lambda:browseFiles() , padx=5, pady=3)
browsefile.pack(pady=2)

outlabel = tk.Label(dec_frame , font= labelfont , text="Data from QR to copy:")
outlabel.pack(pady=1)

output = tk.Text(dec_frame, width=38 , height=2 , state='disabled' ,bg='#FFFAF0')
output.pack(pady=1)

decodeButton = tk.Button(dec_frame, bd=3 , relief= RAISED , text="Decode QR" , command=lambda:decode(qrpath) , padx=5, pady=3)
decodeButton.pack(pady=3 ,side=tk.LEFT , anchor= 'e' , expand=True)

webcamB = tk.Button(dec_frame, bd=3 , relief= RAISED , text="Decode QR with a webcam", command=lambda:webcam(), padx=5, pady=3)
webcamB.pack(pady=3 ,side=tk.RIGHT , anchor= 'w' , expand=True)

sign = tk.Label(window , text="Designed by: Abdulrahman M. Itman" ,font=labelfont)
sign.pack(pady=3)

window.mainloop()