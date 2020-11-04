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

class Tester_GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Image Conv PCD")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.create_widget()

    def create_widget(self):
        generate_button=tkinter.Button(self.root, text="generate Test Cases", width=20, command=self.imagedownload_page)
        generate_button.grid(row=0,column=0,columnspan=3,pady=20,padx=((400-20)/2))
        create_test_file=tkinter.Button(self.root, text="Create Test File", width=20, command=self.create_test_file_page)
        create_test_file.grid(row=1,column=0,columnspan=3,pady=20,padx=((400-20)/2))
        start_test=tkinter.Button(self.root, text="start testing", width=20, command=self.testing_page)
        start_test.grid(row=2, column=0, columnspan=3, pady=20, padx=((400 - 20) / 2))
        #self.select_button=tkinter.Button()
        self.root.mainloop()


    def imagedownload_page(self):
        #panel
        self.downloader_page = tkinter.Toplevel(self.root)
        self.downloader_page.grab_set()
        self.downloader_page.title("New Window")
        self.downloader_page.geometry("500x300")
        self.downloader_page.resizable(False, False)
        #widgetStarthere
        tkinter.Label(self.downloader_page,text="Select your save location(default/testpool)").grid(row=0,column=0)
        self.download_dir_bar = tkinter.Entry(self.downloader_page, width=55)
        self.download_dir_bar.grid(row=1, column=0, padx=4, pady=4)
        self.browse_button = tkinter.Button(self.downloader_page, text="browse", width=20,
                                              command=self.browse_downloader_dir)
        self.browse_button.grid(row=1, column=1)
        self.start_download_button=tkinter.Button(self.downloader_page, text="start", width=20,
                                              command=self.start_download)
        self.start_download_button.grid(row=2, column=0,pady=20,columnspan=2)

    def create_test_file_page(self):
        self.create_test_file_page = tkinter.Toplevel(self.root)
        self.create_test_file_page.grab_set()
        self.create_test_file_page.title("New Window")
        self.create_test_file_page.geometry("500x300")
        self.create_test_file_page.resizable(False, False)
        # widgetStarthere
        tkinter.Label(self.create_test_file_page, text="create test file Menu").grid(row=0, column=0)
        tkinter.Label(self.create_test_file_page, text="Images' Folder").grid(row=1, column=0,pady=4)
        self.test_image_folder_bar=tkinter.Entry(self.create_test_file_page, width=40)
        self.test_image_folder_bar.grid(row=1,column=1,pady=4)
        self.test_image_folder_button=tkinter.Button(self.create_test_file_page,text="browse",width=15,command=self.browse_testfile_dir)
        self.test_image_folder_button.grid(row=1,column=2,padx=2,pady=4)



        tkinter.Label(self.create_test_file_page, text="Text To store").grid(row=2, column=0)
        self.test_file_bar = tkinter.Entry(self.create_test_file_page, width=40)
        self.test_file_bar.grid(row=2, column=1, pady=4)
        self.test_file_button = tkinter.Button(self.create_test_file_page, text="browse", width=15,
                                                       command=self.browse_testfile)
        self.test_file_button.grid(row=2, column=2, padx=2, pady=4)

        storing_button=tkinter.Button(self.create_test_file_page, text="store to txt", width=15,command=self.start_storing_to_txt)
        storing_button.grid(row=3, column=0, pady=20 ,padx=((500-40)/4),columnspan=3)



    def testing_page(self):
        self.testing_page= tkinter.Toplevel(self.root)
        self.testing_page.grab_set()
        self.testing_page.title("New Window")
        self.testing_page.geometry("500x300")
        self.testing_page.resizable(False, False)
        # widgetStarthere
        tkinter.Label(self.testing_page, text="coming soon").grid(row=0, column=0)

    def start_download(self):
        print("downloadstarted")
        ImgDownloader.start_download(self.selected_download_folder)
        AutomatedRename.rename_tool(self.selected_download_folder)

    def start_storing_to_txt(self):
        print("storing started")
        imagetostore.store_to_files(self.selected_test_image_folder,self.selected_textfile)

    def browse_downloader_dir(self):
        self.selected_download_folder = filedialog.askdirectory()
        print(self.selected_download_folder)
        self.download_dir_bar.delete(0, "end")
        self.download_dir_bar.insert(0,self.selected_download_folder)

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



Tester_GUI()