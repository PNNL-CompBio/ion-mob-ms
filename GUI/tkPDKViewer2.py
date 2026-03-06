"""
tkPDKViewer2.py - PDF Document Viewer Widget for Tkinter

Author: Jeremy Jacobson
Email: jeremy.jacobson@pnnl.gov

Description:
    Implements a PDF document viewer widget integrated into Tkinter applications.
    Converts PDF pages to raster images and displays them in scrollable text widget
    with optional progress tracking during document loading. Supports both immediate
    and deferred loading modes for flexible performance optimization.
    
    Key Features:
    - PDF-to-image conversion using PyMuPDF (fitz) library
    - Threaded document loading for non-blocking UI
    - Optional progress bar with percentage display
    - Configurable widget dimensions
    - Dual scrollbars (horizontal and vertical) for navigation
    - Support for large multi-page PDF documents
"""

try:
    from tkinter import *
    import fitz
    from tkinter.ttk import Progressbar
    from threading import Thread
    import math
    import urllib.request

except Exception as e:
    print(f"This error occurred while importing necessary modules or library {e}")


class ShowPdf:
    """
    PDF viewer widget for Tkinter applications.
    Converts PDF documents to raster images for display in scrollable text widget.
    """
    img_object_li = []

    def __init__(self):
        """
        Initialize PDF viewer widget with empty state.
        
        Parameters:
            None
        
        Returns:
            None
        """
        self.display_msg = None
        self.frame = None
        self.text = None

    def pdf_view(self, master, width=1200, height=600, pdf_location="", bar=True, load="after"):
        """
        Create and return PDF viewer widget for parent container.
        
        Configures scrollbars, optional progress indicator, and initializes PDF
        loading process. The actual PDF conversion can be deferred (threaded)
        or immediate based on load parameter.
        
        Parameters:
            master: Parent Tkinter widget container
            width (int): Widget width in pixels (default 1200)
            height (int): Widget height in pixels (default 600)
            pdf_location (str): File path to PDF document to display
            bar (bool): Show progress bar during loading (default True)
            load (str): Loading mode - 'after' for threaded deferred loading,
                       other values for immediate blocking load
        
        Returns:
            Frame: Tkinter Frame widget containing configured PDF viewer
        """
        self.frame = Frame(master, width=width, height=height, bg="white")

        scroll_y = Scrollbar(self.frame, orient="vertical")
        scroll_x = Scrollbar(self.frame, orient="horizontal")

        scroll_x.pack(fill="x", side="bottom")
        scroll_y.pack(fill="y", side="right")

        percentage_view = 0
        percentage_load = StringVar()

        if bar and load == "after":
            self.display_msg = Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)

            loading = Progressbar(self.frame, orient=HORIZONTAL, length=100, mode='determinate')
            loading.pack(side=TOP, fill=X)

        self.text = Text(self.frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, width=width,
                         height=height)
        self.text.pack(side="left")

        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)

        def add_img():
            """
            Convert PDF pages to raster images and insert into display widget.
            Updates progress indicator as pages are processed.
            """
            percentage_bar = 0
            open_pdf = fitz.open(pdf_location)

            for page in open_pdf:
                pix = page.get_pixmap()
                pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
                img = pix1.tobytes('ppm')
                timg = PhotoImage(data=img)
                self.img_object_li.append(timg)
                if bar and load == "after":
                    percentage_bar = percentage_bar + 1
                    percentage_view = (float(percentage_bar) / float(len(open_pdf)) * float(100))
                    loading['value'] = percentage_view
                    percentage_load.set(f"Please wait!, your pdf is loading {int(math.floor(percentage_view))}%")
            if bar and load == "after":
                loading.pack_forget()
                self.display_msg.pack_forget()

            for i in self.img_object_li:
                self.text.image_create(END, image=i)
                self.text.insert(END, "\n\n")
            self.text.configure(state="disabled")

        def start_pack():
            """
            Initiate PDF conversion in separate thread for non-blocking UI.
            """
            t1 = Thread(target=add_img)
            t1.start()

        if load == "after":
            master.after(250, start_pack)
        else:
            start_pack()

        return self.frame


def main():
    """
    Test and demonstrate PDF viewer functionality with sample document.
    
    Downloads sample PDF from ETS GRE research validity data website and
    displays it in testing window.
    
    Parameters:
        None
    
    Returns:
        None
    """
    root = Tk()
    root.geometry("700x780")

    # Download sample PDF for testing purposes
    urllib.request.urlretrieve("https://www.ets.org/Media/Tests/GRE/pdf/gre_research_validity_data.pdf",
                               "pdf-sample.pdf")
    d = ShowPdf().pdf_view(root, pdf_location=r"pdf-sample.pdf", width=100, height=200)
    d.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
