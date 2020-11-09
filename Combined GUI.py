import tkinter
import urllib.request
import json
import random
import shutil
import os
from tkinter import ttk,filedialog
import ImgDownloader
import AutomatedRename
import imagetostore
import threading
import time
import ART_Algo


class Tester_GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Image Conv PCD")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.create_widget()
        #self.not_in_progress = False

    def create_widget(self):
        generate_button=tkinter.Button(self.root, text="Generate Test Cases", width=20, command=self.imagedownload_page)
        generate_button.grid(row=0,column=0,columnspan=3,pady=20,padx=((400-40)/2))
        create_test_file=tkinter.Button(self.root, text="Create Test File", width=20, command=self.create_test_file_page)
        create_test_file.grid(row=1,column=0,columnspan=3,pady=20,padx=((400-40)/2))
        start_test=tkinter.Button(self.root, text="Start Testing", width=20, command=self.testing_page)
        start_test.grid(row=2, column=0, columnspan=3, pady=20, padx=((400 - 40) / 2))
        #self.select_button=tkinter.Button()
        self.root.mainloop()


    def imagedownload_page(self):
        #panel
        self.downloader_page = tkinter.Toplevel(self.root)
        self.downloader_page.grab_set()
        self.downloader_page.title("Download Image")
        self.downloader_page.geometry("575x300")
        self.downloader_page.resizable(False, False)
        #widgetStarthere
        tkinter.Label(self.downloader_page,text="Image Generator").grid(row=0,column=0,columnspan=4,pady=4)
        tkinter.Label(self.downloader_page,text="Amount:").grid(row=1,column=0)
        self.No_of_generated_image=tkinter.Entry(self.downloader_page,width=6)
        self.No_of_generated_image.insert(0, '200')
        self.No_of_generated_image.grid(row=1,column=1)
        tkinter.Label(self.downloader_page, text="Folder:").grid(row=2, column=0)
        self.download_dir_bar = tkinter.Entry(self.downloader_page, width=55)
        self.download_dir_bar.grid(row=2, column=1, padx=4, pady=4,columnspan=2)
        self.browse_button = tkinter.Button(self.downloader_page, text="Browse", width=20,
                                              command=self.browse_downloader_dir)
        self.browse_button.grid(row=2, column=3)
        self.start_download_button=tkinter.Button(self.downloader_page, text="Start", width=20,
                                              command=self.start_download)

        self.start_download_button.grid(row=3, column=0,pady=20,columnspan=4)
        self.progress_var_download_image = tkinter.DoubleVar()
        self.maximum_store = 0
        self.progressbar_download_image = ttk.Progressbar(self.downloader_page, length=500, variable=self.progress_var_download_image,
                                                          maximum=int(self.No_of_generated_image.get()))
        self.progressbar_download_image.grid(row=4, column=0,pady=20,columnspan=4)

    def create_test_file_page(self):
        self.create_test_file_page = tkinter.Toplevel(self.root)
        self.create_test_file_page.grab_set()
        self.create_test_file_page.title("Store Text To File")
        self.create_test_file_page.geometry("500x300")
        self.create_test_file_page.resizable(False, False)
        # widgetStarthere
        tkinter.Label(self.create_test_file_page, text="Create Test File Menu").grid(row=0, column=0)
        tkinter.Label(self.create_test_file_page, text="Images' Folder").grid(row=1, column=0,pady=4)
        self.test_image_folder_bar=tkinter.Entry(self.create_test_file_page, width=40)
        self.test_image_folder_bar.grid(row=1,column=1,pady=4)
        self.test_image_folder_button=tkinter.Button(self.create_test_file_page,text="Browse",width=15,command=self.browse_testfile_dir)
        self.test_image_folder_button.grid(row=1,column=2,padx=2,pady=4)

        tkinter.Label(self.create_test_file_page, text="Text To Store").grid(row=2, column=0)
        self.test_file_bar = tkinter.Entry(self.create_test_file_page, width=40)
        self.test_file_bar.grid(row=2, column=1, pady=4)
        self.test_file_button = tkinter.Button(self.create_test_file_page, text="Browse", width=15,
                                                       command=self.browse_testfile)
        self.test_file_button.grid(row=2, column=2, padx=2, pady=4)

        self.storing_button=tkinter.Button(self.create_test_file_page, text="Store To .txt", width=15,command=self.start_storing_to_txt)
        self.storing_button.grid(row=3, column=0, pady=20 ,padx=((500-40)/4),columnspan=3)

        self.progress_var_store_text = tkinter.DoubleVar()
        self.progressbar_store_text  = ttk.Progressbar(self.create_test_file_page, length=500, variable=self.progress_var_store_text)
        self.progressbar_store_text.grid(row=4, column=0, pady=20, columnspan=4)


    def testing_page(self):
        self.testing_page = tkinter.Toplevel(self.root)
        self.testing_page.grab_set()
        self.testing_page.title("Testing Image Conversion Output")
        self.testing_page.geometry("600x400")
        self.testing_page.resizable(False, False)
        # widgetStarthere
        tkinter.Label(self.testing_page, text="Testpool file:").grid(row=0, column=0, pady=2)
        self.testpoolFile_input_bar = tkinter.Entry(self.testing_page, width=40)
        self.testpoolFile_input_bar.grid(row=0, column=1, padx=2)

        self.testpoolfile_browse_button = tkinter.Button(self.testing_page,text="Browse",width=15,command=self.browse_testpool_txt)
        self.testpoolfile_browse_button.grid(row=0,column=2,padx=2,pady=4)


        tkinter.Label(self.testing_page, text="Testpool Folder:").grid(row=1, column=0, pady=2)
        self.testpoolFolder_input_bar = tkinter.Entry(self.testing_page, width=40)
        self.testpoolFolder_input_bar.grid(row=1, column=1, padx=2)
        self.testpoolFolder_browse_button = tkinter.Button(self.testing_page,text="Browse",width=15,command=self.browse_testpool_dir)
        self.testpoolFolder_browse_button.grid(row=1,column=2,padx=2,pady=4)

        tkinter.Label(self.testing_page, text="No of Trial:").grid(row=2,column=0,pady=2)
        self.No_of_test_trial=tkinter.Entry(self.testing_page,width=10)
        self.No_of_test_trial.insert(0, '50')
        self.No_of_test_trial.grid(row=2,column=1,pady=2)
        self.test_page_report=ttk.Treeview(self.testing_page, selectmode ='browse')
        self.test_page_report.grid(row=3,column=0,columnspan=3,pady=4,padx=(15,0))
        verscrlbar = ttk.Scrollbar(self.testing_page,
                                   orient="vertical",
                                   command=self.test_page_report.yview)
        verscrlbar.grid(row=3,column=5)
        self.test_page_report.configure(xscrollcommand=verscrlbar.set)

        self.test_page_report["columns"] = ("1", "2")

        # Defining heading
        self.test_page_report['show'] = 'headings'

        self.test_page_report.column("1", width=180, anchor='c')
        self.test_page_report.column("2", width=370, anchor='se')

        self.test_page_report.heading("1", text="File")
        self.test_page_report.heading("2", text="Error Message")
        self.start_testing_button=tkinter.Button(self.testing_page,text="Start Testing",width=15,command=self.testing_function)
        self.start_testing_button.grid(row=4,column=0,padx=2,pady=4,columnspan=4)

        self.stringvar = tkinter.StringVar()
        self.stringvar.set('0/0')
        self.progress_var_testing = tkinter.DoubleVar()
        self.progressbar_testing = ttk.Progressbar(self.testing_page, length=400, variable=self.progress_var_testing)
        self.progressbar_testing.grid(row=5,column=0,padx=2,pady=4,columnspan=4)
        self.progressbar_text = tkinter.Label(self.testing_page, textvariable=self.stringvar, anchor='e', justify='right').grid(row=5,column=2, sticky = "E")


    def start_download(self):
        # create thread function for download
        self.progressbar_download_image["maximum"]=int(self.No_of_generated_image.get())
        def thread():
            self.browse_button["state"]="disabled"
            self.start_download_button["state"]="disabled"
            if (os.path.exists(self.selected_download_folder)):
                shutil.rmtree(self.selected_download_folder)
            if not os.path.exists(self.selected_download_folder):
                os.mkdir(self.selected_download_folder)
            quota_flag = True
            x=0#counter for image generation
            while(quota_flag):
                current_files = os.listdir(self.selected_download_folder)
                number_of_files = len(current_files)
                if(number_of_files <= int(self.No_of_generated_image.get())):
                    ImgDownloader.start_download(self.selected_download_folder,x)
                    self.progress_var_download_image.set(number_of_files)
                    time.sleep(0.02)
                    self.root.update_idletasks()
                else:
                    quota_flag = False
            AutomatedRename.rename_tool(self.selected_download_folder)
            print("Download completed")
            self.browse_button["state"]="active"
            self.start_download_button["state"]="active"
        # run thread 
        threading.Thread(target=thread).start()
    # storing to text
    def start_storing_to_txt(self):
        print("Storing Started")

        # create thread function for storing
        def thread():
            self.storing_button["state"] = "disabled"
            self.test_image_folder_button["state"] = "disabled"
            self.test_file_button["state"] = "disabled"
            imagetostore.store_to_files(self.selected_test_image_folder,self.selected_textfile, self.progress_var_store_text, self.progressbar_store_text,  self.root)
            self.storing_button["state"] = "active"
            self.test_image_folder_button["state"] = "active"
            self.test_file_button["state"] = "active"
        # run thread
        threading.Thread(target=thread).start()


    def testing_function(self):
        print("start testing")
        def thread():
            for i in self.test_page_report.get_children():
                self.test_page_report.delete(i)
            self.testpoolfile_browse_button["state"] = "disabled"
            self.testpoolFolder_browse_button["state"] = "disabled"
            self.start_testing_button["state"] = "disabled"
            ART_Algo.ART_algo(int(self.No_of_test_trial.get()),self.selected_testpool_txt,self.selected_testpool_folder,self.root,self.test_page_report, self.progress_var_testing, self.progressbar_testing, self.stringvar)
            self.testpoolfile_browse_button["state"] = "active"
            self.testpoolFolder_browse_button["state"] = "active"
            self.start_testing_button["state"] = "active"
        threading.Thread(target=thread).start()



    # image generator browse function
    def browse_downloader_dir(self):
        self.selected_download_folder = filedialog.askdirectory()
        print(self.selected_download_folder)
        self.download_dir_bar.delete(0, "end")
        self.download_dir_bar.insert(0,self.selected_download_folder)

    # create testpool.txt page browse function
    def browse_testfile_dir(self):
        self.selected_test_image_folder = filedialog.askdirectory()
        print(self.selected_test_image_folder)
        self.test_image_folder_bar.delete(0, "end")
        self.test_image_folder_bar.insert(0, self.selected_test_image_folder)
    def browse_testfile(self):
        self.selected_textfile = filedialog.askopenfilename(filetypes=[('text files', 'txt')])
        print(self.selected_textfile)
        self.test_file_bar.delete(0, "end")
        self.test_file_bar.insert(0, self.selected_textfile)

    # testing_page browsefile
    def browse_testpool_txt(self):
        self.selected_testpool_txt = filedialog.askopenfilename(filetypes=[('text files', 'txt')])
        print(self.selected_testpool_txt)
        self.testpoolFile_input_bar.delete(0, "end")
        self.testpoolFile_input_bar.insert(0, self.selected_testpool_txt)

    def browse_testpool_dir(self):
        self.selected_testpool_folder = filedialog.askdirectory()
        print(self.selected_testpool_folder)
        self.testpoolFolder_input_bar.delete(0, "end")
        self.testpoolFolder_input_bar.insert(0, self.selected_testpool_folder)




Tester_GUI()