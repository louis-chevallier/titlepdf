# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 13:16:06 2020

@author: chevallierl
"""
import sys, time, os
from logging import info, error, warning, critical, basicConfig, INFO, WARNING, ERROR
import matplotlib.pyplot as plt
import pdfreader
from pdfreader import SimplePDFViewer
from pdfreader import PDFDocument
from pdfrw import PdfReader
import pdftitle, glob
import fitz
from PIL import Image, ImageQt
import win32com.client
from tkinter import *
from tkinter import *
from tkinter.ttk import *
  

from PIL import Image,ImageTk
from pdf2image import convert_from_path
import numpy as np
from tqdm import tqdm
#print(dir(win32com))
import cv2
import _thread
from time import sleep

format = '%(pathname)s:%(lineno)s:[%(asctime)ss%(msecs)03d]:%(message)s'

logd =  os.path.dirname(sys.argv[0])
basicConfig(level=ERROR, #INFO, 
            filename=os.path.join(logd, 'myapplog.txt'), filemode='w',
            format=format,
            datefmt="%Hh%Mm%S")

"""
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
# set a format which is simpler for console use
formatter = logging.Formatter(format)
console.setFormatter(formatter)
#logging.getLogger("").addHandler(console)
"""

"""
info(logd)
error(logd)
warning(logd)
critical("")
"""
#sys.exit(0)

info("")
info(dir(pdftitle))
#print("logd=",logd)
from swinlnk.swinlnk import SWinLnk
swl = SWinLnk()
warning(sys.argv)
"""
time.sleep(12)

"""

limages = []


try :
    # creating tkinter window 
    root = Tk() 
    

    
    warning(os.getcwd())
    pdf_dir = "C:\\Users\\chevallierl\\OneDrive - Interdigital Communications Inc\\papers"
    
    
    if len(sys.argv) > 1 :
        pdf_dir = sys.argv[1]
    else :
        pdf_dir = os.path.dirname(sys.argv[0])
        pdf_dir = "C:\\Users\\chevallierl\\OneDrive - Interdigital Communications Inc\\papers"
    #pdf_dir = "C:\\Users\\chevallierl\\OneDrive - Interdigital Communications Inc\\papers"
    info(pdf_dir)    
    warning(pdf_dir)
    #sys.exit(0)
    files = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    files += glob.glob(os.path.join(pdf_dir, '*/*.pdf'))
    warning(files)
    
    imagesDir = os.path.join(pdf_dir, "images")
    os.makedirs(imagesDir, exist_ok=True)

    
    def process(pdf) :
        warning("=============================================================")
        warning(pdf)
        text = ""
        pno=0
        foo = ""
        try :
            bn = os.path.basename(pdf)
            doc = fitz.open(pdf)
            page = doc.loadPage(pno)
            m2 = fitz.Matrix(2,2)
            pix = page.getPixmap(matrix=m2)
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            foo = os.path.join(imagesDir, bn + "_page0.png")
            
            warning(foo)
            #sys.exit(0)
            img.save(foo)
        except Exception as e :
            info(e)
            import traceback
            traceback.print_exc()
            warning(pdf)
            
        ico = "ico.ico"
        #img.save(ico)
        
        def link(lnk) :
            shell = win32com.client.Dispatch("WScript.Shell")
            warning(pdf)
            warning(lnk)
            shortcut = shell.CreateShortcut(lnk)
            shortcut.TargetPath = pdf
            shortcut.IconLocation = ico   #"C:\path_to_.exe,1"
            shortcut.Save()
        try :
            dn,bn = os.path.split(pdf)
            info(bn)
            title = pdftitle.get_title_from_file(pdf)
            warning(("title ==========", title))
            title = title.replace(':', '_').strip('()')
            lnk = os.path.join(dn, title + '.lnk')
            #swl.create_lnk(pdf, lnk)
            #link(lnk)            
            
            info("done")
        except Exception as e :
            warning("pb with " + pdf + str(e))
            warning("using pdwrw")
            try :
                title = PdfReader(pdf).Info.Title
                # Remove surrounding brackets that some pdf titles have
                title=title.replace(':', '_').strip('()')
                #link(os.path.join(dn, title + '.lnk'))
            except Exception as e1 :
                title = ""
                warning("pb again with " + pdf + str(e1))
        text = title.encode()
        """        
        try :
            warning(title)        
            with open(pdf, "rb") as fd :
                viewer = SimplePDFViewer(fd)
                viewer.render()
                markdown = viewer.canvas.text_content
                #warning(markdown)
                strings = viewer.canvas.strings
                #warning(strings)
                plain_text = "|".join(viewer.canvas.strings)
                all_page_images = viewer.canvas.images
                all_page_inline_images = viewer.canvas.inline_images
                img = all_page_images['img0']
                img.Type, img.Subtype
        except :
            pass
        
        try :
            with open(pdf, "rb") as fd :
                #warning(plain_text)
                doc = PDFDocument(fd)
                page = next(doc.pages())
                warning(page)
                xo = page.Resources.XObject
                warning(xo)
                warning(xo.keys()[0])
                img0 = xo.keys()[0]
                xobj = page.Resources.XObject[img0]
                warning(xobj)
                warning((xobj.Type, xobj.Subtype))
                pil_image = xobj.to_Pillow()
                pil_image.save("extracted.png")
                plt.imgshow(pil_image.numpy()); plt.show(block=True)
        except :
            pass
        images = convert_from_path(pdf)
        warning(images[0])
        pi = images[0]
        plt.imshow(np.asarray(pi)); plt.show(block=True)
        """
        return (foo, pdf, text)


    def threadmain():
        t = Tk()
        b = Button(text='test', command=exit)
        b.grid(row=0)
        progress = Progressbar(root, orient = HORIZONTAL, 
                               length = len(files),
                               mode = 'determinate')
        t.mainloop()


    #_thread.start_new_thread(threadmain, ())

    """
    for ipdf, pdf in tqdm(enumerate(list(files)), total=len(files)) :
        info("")
        #progress['value'] = ipdf
        process(pdf)
    info("")
    """
    limages = [ process(pdf) for ipdf, pdf in  tqdm(enumerate(list(files)), total=len(files))]

    
    #time.sleep(12)
    

    html = """
    <!DOCTYPE html>
    <html>

       <head>
          <title> %d papers</title>
       </head>

       <body>
          %s
       </body>

    </html>
    """

    enc = lambda im,pdf,text : '<p hidden> %s </p> <a href="%s" > <img src="%s" alt = "%s" /> </a>' % (text, pdf, im, pdf)

    shtml = html % (len(files), '\n'.join([enc(im,f,text) for im,f,text in limages]))
    with open(os.path.join(pdf_dir, 'index.html'), 'w') as the_file:
        the_file.write(shtml)

except Exception as ee :
    import traceback
    traceback.print_exc()
    warning(ee)







warning("done")
