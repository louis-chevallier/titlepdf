# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 13:16:06 2020

@author: chevallierl
"""
import sys, time, os
import logging
from logging import info, error, warning, critical, basicConfig, INFO, WARNING, ERROR
import matplotlib.pyplot as plt
import pdfreader
from pdfreader import SimplePDFViewer
from pdfreader import PDFDocument
from pdfrw import PdfReader
import pdftitle, glob
import fitz
import PyPDF2
from functools import reduce
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


cwd = os.getcwd()

logd =  os.path.dirname(sys.argv[0])
basicConfig(level=WARNING if cwd == "C:\\dev\\titlepdf" else ERROR, 
            filename=None if cwd == "C:\\dev\\titlepdf"  else os.path.join(logd, 'myapplog.txt'), 
            filemode='w',
            format=format,
            datefmt="%Hh%Mm%S")

info(cwd)

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
extractImages = False
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


    info(pdf_dir)    
    warning(pdf_dir)
    #sys.exit(0)
    files = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    files += glob.glob(os.path.join(pdf_dir, '*/*.pdf'))
    #warning(files)
    
    files = [ { "path" : e, "date" : os.stat(e)[9] } for e in files] 
    files = sorted(files , key = lambda x : x["date"], reverse=True)
 
    files = files[:3]
 
 
    #warning(files)
   
    imagesDir = os.path.join(pdf_dir, "images")
    os.makedirs(imagesDir, exist_ok=True)

    
    def process(dpdf) :
        warning("=============================================================")
        pdf = dpdf["path"]

        warning(pdf)
        title = ""
        pno=0
        foo = ""
        full = ""
        try :
            bn = os.path.basename(pdf)
            doc = fitz.open(pdf)
            page = doc.loadPage(pno)
            m2 = fitz.Matrix(2,2)
            pix = page.getPixmap(matrix=m2)
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            im0 = os.path.join(imagesDir, bn + "_page0.png")
            img.save(im0)
            warning("read page #0")           
            full = ''.join([ p.getText() for p in doc])
            warning("read full (%d chars)" % len(full))
            
            if extractImages :
                for i in range(len(doc)) :
                    for img in doc.getPageImageList(i) :
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        mode = "RGBA" if pix.alpha else "RGB"
                        pil = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                        #plt.imshow(np.asarray(pil)); plt.show(block=True)
                #warning(foo)
            #sys.exit(0)

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
            warning(bn)
            title = pdftitle.get_title_from_file(pdf)
            title = title.replace(':', '_').strip('()')
            lnk = os.path.join(dn, title + '.lnk')
            warning((f"{title=}"))
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
                warning(f"{title=}")
                #link(os.path.join(dn, title + '.lnk'))
            except Exception as e1 :
                title = ""
                warning("pb again with " + pdf + str(e1))
        title = title.encode()
        full = full.encode()
        #warning(f"{text=}")
        #warning(title)
        #warning(str(title.encode()))
        #text = title
        warning(f"{title=}")
        
        if False :            
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
            except  Exception as e1:
                warning("simpleviewer failed")
                warning(str(e1))
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
                    #pil_image.save("extracted.png")
                    #plt.imgshow(pil_image.numpy()); plt.show(block=True)
            except  Exception as e1:
                warning("pdfdocument failed")
                warning(str(e1))
                pass
            
            try :
                with open(pdf, "rb") as fd :
                    input1 = PyPDF2.PdfFileReader(fd)
                    page0 = input1.getPage(0)
                    xobject = page0['/Resources']["/XObject"].getObject()
            except Exception as e1:
                warning("pypdf2 failed")
                warning(str(e1))
                pass
                
            
        if False :    
            images = convert_from_path(pdf)
            warning(images[0])
            pi = images[0]
        #plt.imshow(np.asarray(pi)); plt.show(block=True)
        
        return (im0, pdf, title, full)


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
    
<style type="text/css">
p {
}
div {
  border: 1px solid black;
  }
.visibility {
  visibility: hidden;
  }
.display {
  display: none;
  }
  </style>
<div>1 : Ceci est un div normal</div>
<div class="visibility">2 : Ceci est un div avec visibility: hidden</div>
<div>3 : Ceci est un div normal</div>
<div class="display">4 : Ceci est un div avec display: none</div>
<div>5 : Ceci est un div normal</div>


           <div clsss="form-container">
              <form class="form">
                  <input id="search" type="text" class="input" placeholder="search..."/>
              </form>

            </div>
<head>
    <title> %d papers</title>
    <script> 
        LIST 
        
        const searchInput = document.querySelector('.input')
        searchInput.addEventListener("input", (e) => {
            let value = e.target.value
            if (value && value.trim().length > 0){
                value = value.trim().toLowerCase()
                console.log(value);
                re = new RegExp(value)
                const found = texts.find(el => el['full'].indexOf(value) >= 0);
                console.log(found);
                const foundre = texts.find(el => re.test(el['full']));
                console.log(foundre);
                console.log(window);
                console.log(foundre.href);
                h = foundre.href;
                window.location.href = '#' + h;
                var top = document.getElementById('#' + h).offsetTop; //Getting Y of target element
                window.scrollTo(0, top); 
            }
        })

      
        
        </script>  
       </head>

       <body>
       
       
        
          %s
       </body>

    </html>
    """

    href = lambda i: 'H' + str(i).zfill(5)

    def process(txt) :
        return reduce(lambda s, p : s.replace(p, '_'), "%-()?/[]'`\",:", txt) 

    def listf(x) : 
        i, (im0, pdf, title, full) = x 
        return '{ href : "' + href(i) + '" , title : "' + process(str(title)) + '", full : "' + process(str(full)) + '" }'
        
    html = html.replace("LIST", "const texts = [ " + ',\n'.join(map(listf, enumerate(limages))) + "]")


    enc = lambda i, im0, pdf, title, full : '  <p id="#%s" title = "%s" >  <a href="%s" > <img src="%s" alt = "%s" /> </a>  </p>' % ( href(i), title,  pdf, im0, pdf)

    shtml = html % (len(files), '\n'.join([enc(i, im0,pdf,title, full) for i, (im0, pdf, title, full) in enumerate(limages)]))
    with open(os.path.join(pdf_dir, 'index.html'), 'w') as the_file:
        the_file.write(shtml)

except Exception as ee :
    import traceback
    traceback.print_exc()
    warning(ee)







warning("done")
