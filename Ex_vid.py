import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QComboBox
from PyQt5.QtCore import pyqtSlot
import pympi
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip

import numpy as np


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Extract Videos App'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 300
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.labl = QLabel(self)
        # self.labl.setText('abc')

        self.all_label = QLabel(self)

        self.video_label = QLabel(self)

        self.ann_label = QLabel(self)

        button = QPushButton('Select annotation file', self)        
        button.move(0,10)
        button.resize(180,32)
        button.clicked.connect(self.on_click)

        button_video = QPushButton('Select video file', self)        
        button_video.move(0,50)
        button_video.resize(180,32)
        button_video.clicked.connect(self.video_click)

        self.info_label1 = QLabel(self)
        self.info_label1.move(15,130)
        self.info_label1.setText("Select tier from which you want to extract the annotations")

        button_all = QPushButton('Extract all annotations from tier', self)        
        button_all.move(200,150)
        button_all.resize(230,32)
        button_all.clicked.connect(self.all_annotations)

        button_one = QPushButton('Extract one annotation', self)        
        button_one.move(200,198)
        button_one.resize(230,32)
        button_one.clicked.connect(self.extract_one)
        

        self.combo = QComboBox(self)
        # combo.addItem("Apple")
        self.combo.move(10, 150)
        self.combo.activated[str].connect(self.to_print)

        self.combo_annotations = QComboBox(self)
        # combo.addItem("Apple")
        self.combo_annotations.move(10, 200)
        self.combo_annotations.activated[str].connect(self.only_one_annotation)

        self.show()

    @pyqtSlot()
    def on_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Choose a file", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.combo.clear()
            self.labl.setText(str(fileName))
            self.labl.adjustSize()
            self.labl.move(190, 16)
            self.file_eaf = pympi.Eaf(file_path=fileName)
            self.tier_names = self.file_eaf.get_tier_names()
            for tier_name in self.tier_names:
                self.combo.addItem(str(tier_name))
    
    def video_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Choose a file", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.video_label.setText(str(fileName))
            self.video_label.adjustSize()
            self.video_label.move(190, 57)
    
    def to_print(self, text):
        self.all_label.setText(str(text))
        self.all_label.adjustSize()
        self.all_label.move(200, 150)
        self.all_label.hide()

        # add all the annotations to the other combo box
        my_file = pympi.Eaf(file_path=self.labl.text())
        my_annotations = my_file.get_annotation_data_for_tier(str(text))
        self.combo_annotations.clear()
        for annotatio in my_annotations:
            self.combo_annotations.addItem(str(annotatio[2]))


    def all_annotations(self):
        # print(self.all_label.text())
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption='Select directory to save extracted videos',
        )
        if path:
            print(path)
        selected_file = pympi.Eaf(file_path=self.labl.text())
        annotations = selected_file.get_annotation_data_for_tier(self.all_label.text())
        video_name = self.video_label.text()
        count = 0
        for annotation in annotations:
            # t1 = annotation[0]/1000
            # t2 = annotation[1]/1000
            # input_video_path = video_name
            # output_video_path = path+'/'+str(annotation[0])+".mp4"
            # print(output_video_path)

            # with VideoFileClip(input_video_path) as video:
            #     new = video.subclip(t_start= t1)
            #     new.write_videofile(filename=output_video_path, audio_codec='aac')

            start = annotation[0]
            end = annotation[1]
            print(start/1000,end/1000)
            
            ffmpeg_extract_subclip(video_name, start/1000, end/1000, targetname=path+'/'+str(annotation[2])+'_'+str(count)+".mp4")
            # Comment next line if you don't want to extract the frames for each video
            # video_to_frames("Data/"+str(gloss)+"/Videos/"+"%#05d.mp4" % (count+1), "Data/"+str(gloss)+"/"+"%#05d" % (count+1) )
            count = count+1
        print("FINISHED")  

    def only_one_annotation(self,text):
        self.ann_label.setText(str(text))
        self.ann_label.adjustSize()
        self.ann_label.move(200, 350)
        self.ann_label.hide()

    def extract_one(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption='Select directory to save extracted video',
        )
        if path:
            print(path)
        selected_file = pympi.Eaf(file_path=self.labl.text())
        annotations2 = selected_file.get_annotation_data_for_tier(self.all_label.text())
        video_name = self.video_label.text()
        for annotation in annotations2:
            # print(self.ann_label.text())
            if annotation[2] == self.ann_label.text():
                start = annotation[0]
                end = annotation[1]
                # print(start/1000,end/1000)
                
                ffmpeg_extract_subclip(video_name, start/1000, end/1000, targetname=path+'/'+str(self.ann_label.text())+".mp4")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())