# from talelle_setup import Path, TALELLE_DIR, config_log
# TALELLE_TOOL = Path(__file__).stem
# config_log(TALELLE_TOOL)

import sys
import os
import json
import datetime
import subprocess

# import logging
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QLineEdit, QComboBox, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap



# logger = logging.getLogger(__name__)
# logger.info(f'{TALELLE_TOOL} started')


# ffmpeg -ss 00:10:51 -to 00:13:20 -i input.mp4 -map 0:v:0 -map 0:a:0 -sn -c copy output.mp4



class CropperThread(QThread):
    command_line = "ffmpeg -ss {start_time} -to {end_time} -i {media_path_stem}.mp4 -map 0:v:0 -map 0:a:0 -sn -c copy {media_path_stem}_cropped.mp4 -y"

    creationStarted = Signal()
    progressUpdated = Signal(int, str, str)
    creationFinished = Signal()
    errorOccurred = Signal(str, tuple)

    def __init__(self, media_path_stem, start_time, end_time):
        super().__init__()
        self.current_command = self.command_line.format(media_path_stem=media_path_stem, start_time=start_time, end_time=end_time)
        print(self.current_command)

    def run(self):
        self.creationStarted.emit()
        try:
            # run subprocess with self.current_command
            process = subprocess.Popen(self.current_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # print stdout and stderr for debugging
            print("Process output:")
            print(stdout.decode())
            print(stderr.decode())

            if process.returncode != 0:
                self.errorOccurred.emit(stdout, stderr)
            self.creationFinished.emit()
        except Exception as e:
            print(f"Error occurred: {e}")
            self.errorOccurred.emit(e.args[0], e.args[1:])

    def communicate_callback(self, value, label=None, count=None):
        self.progressUpdated.emit(value, label, count)





class MediaCropper(QWidget):
    def __init__(self):
        super().__init__()
        # settings = self.load_settings()
        # self.current_language = self.get_language(settings)
        # self.translations = self.load_translations(self.current_language)
        # self.project_path, self.project_folder = self.get_project_path(settings)
        # self.images_folder = self.get_images_folder(settings)

        # declare QComponent groups
        # self.locale_subjects = dict()
        # self.direction_subjects = list()

        # declare QComponents
        # self.langComboBox = None
        self.mediaLineEdit = None
        self.startLineEdit = None
        self.endLineEdit = None

        self.setup_ui()
        # self.apply_settings()
        # self.change_language(self.current_language)

    # @staticmethod
    # def get_settings_file():
    #     return os.path.join(TALELLE_DIR, f'{TALELLE_TOOL}.json')

    # def save_settings(self):
    #     settings = {
    #         'language': self.current_language,
    #         'projectPath': self.project_path,
    #         'projectFolder': self.project_folder,
    #         'imagesFolder': self.images_folder
    #     }
    #     try:
    #         with open(self.get_settings_file(), 'w') as f:
    #             json.dump(settings, f)
    #     except Exception as e:
    #         QMessageBox.warning(self, self.translate_key('saving_settings_warning'), str(e))

    # def load_settings(self):
    #     settings = {
    #         'language': 'English',
    #     }
    #     try:
    #         with open(self.get_settings_file(), 'r') as f:
    #             settings.update(json.load(f))
    #     except FileNotFoundError:
    #         pass
    #     return settings

    # def apply_settings(self):
    #     self.langComboBox.setCurrentText(self.current_language)


    # @staticmethod
    # def get_language(settings):
    #     logger.warning('getting language!!!!!')
    #     return settings.get('language', 'English')

    # @staticmethod
    # def get_project_path(settings) -> tuple[str, str]:
    #     return \
    #         settings.get('projectPath', os.path.expanduser("~")), \
    #         settings.get('projectFolder', 'projects')

    # @staticmethod
    # def get_images_folder(settings) -> str:
    #     return settings.get('imagesFolder', 'images')

    # @staticmethod
    # def load_language_codes():
    #     path = 'locales/language_codes.json'
    #     with open(path, 'r', encoding='utf-8') as f:
    #         return json.load(f)

    # @classmethod
    # def load_language_names(cls):
    #     language_codes = cls.load_language_codes()
    #     return list(language_codes.keys())

    # @classmethod
    # def load_translations(cls, language_name):
    #     language_codes = cls.load_language_codes()
    #     language_code = language_codes.get(language_name, "en")
    #     path = f'locales/{language_code}.json'
    #     with open(path, 'r', encoding='utf-8') as f:
    #         return json.load(f)

    # def translate_key(self, text_key):
    #     return self.translations.get(text_key, text_key)

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Update Logo
        logoLabel = QLabel(self)
        logoPixmap = QPixmap('images/logo.png')
        scaledLogoPixmap = logoPixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)
        logoLabel.setPixmap(scaledLogoPixmap)
        logoLabel.setFixedSize(scaledLogoPixmap.size())
        layout.addWidget(logoLabel)

        # Language selection
        # languageLabel = QLabel()
        # langComboBox = QComboBox()
        # langComboBox.addItems(self.load_language_names())
        # langComboBox.currentTextChanged.connect(self.change_language)
        # langLayout = QHBoxLayout()
        # langLayout.addWidget(languageLabel)
        # langLayout.addWidget(langComboBox)
        # layout.addLayout(langLayout)


        # Media selection
        mediaLabel = QLabel()
        mediaLabel.setText('נתיב לסרטון')
        mediaLineEdit = QLineEdit()
        mediaButton = QPushButton()
        mediaButton.setText('בחר')

        mediaButton.clicked.connect(self.choose_media)
        mediaLayout = QHBoxLayout()
        mediaLayout.addWidget(mediaLabel)
        mediaLayout.addWidget(mediaLineEdit)
        mediaLayout.addWidget(mediaButton)
        mediaLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
        layout.addLayout(mediaLayout)

        # Duration selection
        startLabel = QLabel()
        startLabel.setText('תחילת הקטע')
        startLineEdit = QLineEdit()
        endLabel = QLabel()
        endLabel.setText('סיום הקטע')
        endLineEdit = QLineEdit()
        durationLayout = QHBoxLayout()
        durationLayout.addWidget(startLabel)
        durationLayout.addWidget(startLineEdit)
        durationLayout.addWidget(endLabel)
        durationLayout.addWidget(endLineEdit)
        durationLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
        layout.addLayout(durationLayout)


        # Process button
        processButton = QPushButton('גזור סרטון')
        processButton.clicked.connect(self.crop)
        layout.addWidget(processButton)


        # TODO: Apply locale
        # self.locale_subjects['language_label'] = languageLabel
        # self.locale_subjects['project_name_label'] = projNameLabel
        # self.locale_subjects['create_project'] = createProjButton
        # self.locale_subjects['new_project_label'] = newProjLabel
        #
        # self.direction_subjects.append(langLayout)
        # self.direction_subjects.append(createProjLayout)

        # self.langComboBox = langComboBox
        self.mediaLineEdit = mediaLineEdit
        self.startLineEdit = startLineEdit
        self.endLineEdit = endLineEdit

        # self.newProjLabel = newProjLabel


    def choose_media(self):
        # Implement the logic to choose media (image/video) here
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                     'בחר סרטון', # self.translate_key('choose_project'),
                                                     dir=os.path.expanduser("~"))
        if file_path:
            # proj_path = os.path.normpath(proj_path)
            self.mediaLineEdit.setText(file_path)


    # def change_language(self, language):
    #     self.current_language = language
    #     self.translations = self.load_translations(language)
    #
    #     # Update texts
    #     self.setWindowTitle(self.translate_key('title'))
    #
    #     for locale_key in self.locale_subjects:
    #         self.locale_subjects[locale_key].setText(self.translate_key(locale_key))
    #
    #     # Update layout
    #     is_rtl = (language == 'עברית')
    #     for direction_subject in self.direction_subjects:
    #         direction_subject.setDirection(QHBoxLayout.Direction.RightToLeft if is_rtl else QHBoxLayout.Direction.LeftToRight)
    #
    #     self.save_settings()


    def crop(self):
        # Implement the logic to crop the media here
        media_path = self.mediaLineEdit.text()
        start_time_str = self.startLineEdit.text()
        end_time_str = self.endLineEdit.text()

        # Validate inputs - media_path extension mp4.
        if not media_path.endswith('.mp4'):
            QMessageBox.warning(self, 'שגיאה', 'אנא בחר סרטון בפורמט MP4.')
            return

        # Validate inputs - media_path exists
        if not os.path.exists(media_path):
            QMessageBox.warning(self, 'שגיאה', f'הסרטון שבחרת {media_path} לא קיים.')
            return


        # Validate inputs - start_time and end_time format HH:MM:SS or MM:SS or SS
        time_tempate = '{hh}:{mm}:{ss}'

        start_time_components = start_time_str.split(':')
        end_time_components = end_time_str.split(':')

        start_time_padded = time_tempate.format(
            hh=start_time_components[-3] if len(start_time_components) == 3 else '00',
            mm=start_time_components[-2] if len(start_time_components) >= 2 else '00',
            ss=start_time_components[-1])
        end_time_padded = time_tempate.format(hh=end_time_components[-3] if len(end_time_components) == 3 else '00',
                                              mm=end_time_components[-2] if len(end_time_components) >= 2 else '00',
                                              ss=end_time_components[-1])
        try:
            start_time = datetime.datetime.strptime(start_time_padded, '%H:%M:%S')
            end_time = datetime.datetime.strptime(end_time_padded, '%H:%M:%S')

            # Validate inputs - start_time < end_time
            if start_time >= end_time:
                QMessageBox.warning(self, 'שגיאה', 'זמן ההתחלה חייב להיות קטן מזמן הסיום.')
                print(f'start_time: {start_time}, end_time: {end_time}')
                return
        except ValueError:
            QMessageBox.warning(self, 'שגיאה', 'אנא הזן את זמן ההתחלה והסיום בפורמט HH:MM:SS.')
            print(f'start_time: {start_time_padded}, end_time: {end_time_padded}')
            return


        media_path_stem = media_path.removesuffix('.mp4')

        # Here you would implement the actual cropping logic using a library like moviepy or ffmpeg
        # For now, we will just show a message box indicating success
        QMessageBox.information(self, 'הצלחה', f'אני הולך חותך את הסרטון מ-{start_time_padded} ל-{end_time_padded} ב-{media_path}.')


        try:
            self.crpThread = CropperThread(media_path_stem, start_time_str, end_time_str)
            # self.crpThread.creationStarted.connect(self.on_crop_started)
            # self.crpThread.progressUpdated.connect(self.update_progress_bar)
            self.crpThread.creationFinished.connect(self.on_crop_finished)
            self.crpThread.errorOccurred.connect(self.raise_an_error)
            self.crpThread.start()
        except Exception as e:
            QMessageBox.warning(self, 'שגיאה', 'אירעה שגיאה בעת חיתוך הסרטון: ')
            print(e)



    def on_crop_finished(self):
        # self.set_progress_status('finished')
        # self.processButton.setEnabled(True)
        QMessageBox.information(self, 'הצלחה', 'הסרטון נחתך בהצלחה.',
                                QMessageBox.StandardButton.Ok)


    def raise_an_error(self, err_key, arr_args):
        # self.reset_progress()
        # self.processButton.setEnabled(True)
        QMessageBox.warning(self, 'שגיאה', 'אירעה שגיאה בעת חיתוך הסרטון: ' + str(arr_args))


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    app = QApplication(sys.argv)
    window = MediaCropper()
    window.show()
    sys.exit(app.exec())
