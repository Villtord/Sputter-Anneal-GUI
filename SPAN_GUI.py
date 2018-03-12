#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 19:23:47 2018

@author: villtord
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 20:02:12 2017

@author: villtord
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal,QTimer
from PyQt5.QtGui import QIcon
from SPAN_UI import Ui_Dialog
import sys
import pickle
import pprint
import math as mt
from datetime import datetime

time_factor = 6000

class ExampleApp(QWidget, Ui_Dialog):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('hot.png'))
        
        self.cycles_count=0
        self.elapsed_time=0
        global time_factor
        
        self.Load_Button.clicked.connect(self.load_file) # Load function
        self.Save_Button.clicked.connect(self.save_file) # Save function
        self.Start_Button.clicked.connect(self.start_toggle) # Start function
        self.Sputter_Button.clicked.connect(self.activate_sputter)  # Activate/deactivate sputter
        self.Anneal_Button.clicked.connect(self.activate_anneal)     # Activate/deactivate anneal
        
        self.my_sputter = sputter_procedure()      
        self.my_anneal = anneal_procedure()
        self.progress_update = total_countdown()
        
        self.my_sputter.end_trigger.connect(self.sputter_end)
        self.my_anneal.end_trigger.connect(self.anneal_end)
        self.progress_update.update_trigger.connect(self.update_progress_bar)
    
    def load_file(self):
        """ read values from saved file to a dictionary and then load it to GUI """
        load_file_name = QFileDialog.getOpenFileName(self, 'Open file', '','*.pkl')
        
        with open(load_file_name[0], 'rb') as f:
            loaded_settings = pickle.load(f)
        
        f.close()
#       pprint.pprint(loaded_settings)
        self.Sputter_Button.setChecked(loaded_settings['Sputter_Button'])
        self.Sputter_Energy.setText(loaded_settings['Sputter_Energy'])
        self.Sputter_Pressure.setText(loaded_settings['Sputter_Pressure'])
        self.Sputter_Time.setText(loaded_settings['Sputter_Time'])
        self.Sputter_Pause.setText(loaded_settings['Sputter_Pause'])
        
        self.Anneal_Button.setChecked(loaded_settings['Anneal_Button'])
        self.Anneal_Current.setText(loaded_settings['Anneal_Current'])
        self.Anneal_Ramp.setText(loaded_settings['Anneal_Ramp'])
        self.Anneal_Time.setText(loaded_settings['Anneal_Time'])
        self.Anneal_Pause.setText(loaded_settings['Anneal_Pause'])
        
        self.Hot_Sputter_Current.setText(loaded_settings['Hot_Sputter_Current'])
        self.Hot_Sputter_Delay.setText(loaded_settings['Hot_Sputter_Delay'])
        self.Hot_Sputter_radioButton.setChecked(loaded_settings['Hot_Sputter_radioButton']) 
        
        self.spinBox.setValue(loaded_settings['spinBox'])
        
    def save_file(self):
        """ write values from table to a dictionary and then save it to a .pkl file """
        save_string={}
        
        save_string["Sputter_Button"]=self.Sputter_Button.isChecked()
        save_string["Sputter_Energy"]=self.Sputter_Energy.text()
        save_string["Sputter_Pressure"]=self.Sputter_Pressure.text()
        save_string["Sputter_Time"]=self.Sputter_Time.text()
        save_string["Sputter_Pause"]=self.Sputter_Pause.text()
        
        save_string["Anneal_Button"]=self.Anneal_Button.isChecked()
        save_string["Anneal_Current"]=self.Anneal_Current.text()
        save_string["Anneal_Ramp"]=self.Anneal_Ramp.text()
        save_string["Anneal_Time"]=self.Anneal_Time.text()
        save_string["Anneal_Pause"]=self.Anneal_Pause.text()
        
        save_string["Hot_Sputter_Current"]=self.Hot_Sputter_Current.text()
        save_string["Hot_Sputter_Delay"]=self.Hot_Sputter_Delay.text()
        save_string["Hot_Sputter_radioButton"]=self.Hot_Sputter_radioButton.isChecked()
        
        save_string["spinBox"]=self.spinBox.value()
        
        save_file_string = QFileDialog.getSaveFileName(self, 'Save file as', '')
        
        if save_file_string[0].endswith('.pkl'):
            with open(save_file_string[0], 'wb') as f:
                pickle.dump(save_string, f)
        else:
            with open(save_file_string[0] + '.pkl', 'wb') as f:
                pickle.dump(save_string, f)
        f.close()
        
    def group_status(self,Flag):
            print ("disabling/enabling buttons")
        
            self.Sputter_Button.setEnabled(bool(Flag))
            self.Sputter_Energy.setEnabled(bool(Flag))
            self.Sputter_Pressure.setEnabled(bool(Flag))
            self.Sputter_Time.setEnabled(bool(Flag))
            self.Sputter_Pause.setEnabled(bool(Flag))
            
            self.Anneal_Button.setEnabled(bool(Flag))
            self.Anneal_Current.setEnabled(bool(Flag))
            self.Anneal_Ramp.setEnabled(bool(Flag))
            self.Anneal_Time.setEnabled(bool(Flag))
            self.Anneal_Pause.setEnabled(bool(Flag))
            
            self.Hot_Sputter_Current.setEnabled(bool(Flag))
            self.Hot_Sputter_Delay.setEnabled(bool(Flag))
            self.Hot_Sputter_radioButton.setEnabled(bool(Flag))
            self.Start_Button.setChecked(bool(Flag))
            
    def activate_sputter(self):
        
        Flag = False
        if self.Sputter_Button.isChecked():
            Flag = True
            
        self.Sputter_Energy.setEnabled(bool(Flag))
        self.Sputter_Pressure.setEnabled(bool(Flag))
        self.Sputter_Time.setEnabled(bool(Flag))
        self.Sputter_Pause.setEnabled(bool(Flag))
        self.Hot_Sputter_Current.setEnabled(bool(Flag))
        self.Hot_Sputter_Delay.setEnabled(bool(Flag))
        self.Hot_Sputter_radioButton.setEnabled(bool(Flag))    
        
    def activate_anneal(self):
        
        Flag = False
        if self.Anneal_Button.isChecked():
            Flag = True
        self.Anneal_Current.setEnabled(bool(Flag))
        self.Anneal_Ramp.setEnabled(bool(Flag))
        self.Anneal_Time.setEnabled(bool(Flag))
        self.Anneal_Pause.setEnabled(bool(Flag))
        
    def start_toggle(self):
        """ Main action when start button pressed """
        self.cycles_count=0
        self.elapsed_time=0
        
        if self.Start_Button.text()=="Start!":
            
            self.progressBar.setValue(0)

            self.Start_Button.setText('Stop!')
            
            self.group_status('')
            
            """ here we define total time and set up update of the progress bar """
            
            self.total_time = 0
            str(datetime.now())
            
            if self.Sputter_Button.isChecked():             
                self.total_time = self.total_time+float(self.Sputter_Time.text())+float(self.Sputter_Pause.text())
                                 
            if self.Anneal_Button.isChecked():
                self.total_time = (self.total_time+float(self.Anneal_Time.text())+
                                                   float(self.Anneal_Ramp.text())+
                                                   float(self.Anneal_Pause.text()))
            self.total_time = self.total_time*int(self.spinBox.value())
            self.progress_update.start(self.total_time)
            print ("total time: ", self.total_time)
            
            """ main cycle itself """
                            
            if self.Sputter_Button.isChecked(): 
                
                self.my_sputter.start(int(self.Sputter_Energy.text()),
                                      float(self.Sputter_Pressure.text()),
                                      int(self.Sputter_Time.text()))
                
                if self.Hot_Sputter_radioButton.isChecked():
                    
                    self.timer_1 = QTimer(self)
                    self.timer_1.setSingleShot(True)
                    self.timer_1.timeout.connect(lambda: self.my_anneal.start_hot_sputter(float(self.Hot_Sputter_Current.text())))
                    
                    self.timer_1.start(int(self.Hot_Sputter_Delay.text())*time_factor)
            
            elif self.Anneal_Button.isChecked():
                
                self.my_anneal.start(float(self.Anneal_Current.text()),
                                     int(self.Anneal_Ramp.text()),
                                     int(self.Anneal_Time.text()))
            
            else:  
                pass
                       
        else:
            
            """ Stop all possible timers that are still running and processes """
            
            self.my_sputter.stop()
            self.my_anneal.stop()
            
            for i in ["self.timer_1", "self.timer_2", "self.timer_3", "self.timer_4",
                      "self.timer_5", "self.timer_6", "self.timer_7"]:
                try:
                    self.stop_timer(eval(i))
                except:
                    pass
            
            self.progress_update.stop()
            self.progressBar.setValue(0)
            self.group_status('whatever')
            self.Start_Button.setText('Start!')
            print(str(datetime.now()))
            
    
    def stop_timer(self, timer_name):
        try:
            if timer_name:
                print (timer_name, " detected")
                timer_name.stop()
                timer_name.deleteLater()
                print (timer_name, " stopped")
        except:
            pass
    
    def sputter_end(self):
        
        if self.Hot_Sputter_radioButton.isChecked():
            
            self.my_anneal.end_hot_sp_anneal()
        
        if self.Anneal_Button.isChecked():
            
            self.timer_2 = QTimer(self)
            self.timer_2.setSingleShot(True)
            self.timer_2.timeout.connect(lambda: self.my_anneal.start(float(self.Anneal_Current.text()),
                                                               int(self.Anneal_Ramp.text()),
                                                               int(self.Anneal_Time.text())))
            self.timer_2.start(int(self.Sputter_Pause.text())*time_factor)
        
        else:
            
            self.cycles_count+=1
            
            if self.cycles_count<int(self.spinBox.value()):
                
                self.timer_3 = QTimer(self)
                self.timer_3.setSingleShot(True)
                self.timer_3.timeout.connect(lambda: self.my_sputter.start(int(self.Sputter_Energy.text()),
                                                                    float(self.Sputter_Pressure.text()),
                                                                    int(self.Sputter_Time.text())))
                self.timer_3.start(int(self.Sputter_Pause.text())*time_factor)
                
                if self.Hot_Sputter_radioButton.isChecked():

                    self.timer_4 = QTimer(self)
                    self.timer_4.setSingleShot(True)
                    self.timer_4.timeout.connect(lambda: self.my_anneal.start_hot_sputter(float(self.Hot_Sputter_Current.text())))
                    self.timer_4.start((int(self.Hot_Sputter_Delay.text())+int(self.Sputter_Pause.text()))*time_factor)                    
            
            else:
                self.group_status('whatever')
                self.Start_Button.setChecked(False)
                self.Start_Button.setText('Start!')
                self.progress_update.stop()
                self.progressBar.setValue(100)
                pass
            
    def anneal_end(self):
            
        self.cycles_count+=1
        
        if self.cycles_count<int(self.spinBox.value()):
                        
            if self.Sputter_Button.isChecked():
                
                self.timer_5 = QTimer(self)
                self.timer_5.setSingleShot(True)
                self.timer_5.timeout.connect(lambda: self.my_sputter.start(int(self.Sputter_Energy.text()),
                                                                    float(self.Sputter_Pressure.text()),
                                                                    int(self.Sputter_Time.text())))
                self.timer_5.start(int(self.Anneal_Pause.text())*time_factor)
                
                if self.Hot_Sputter_radioButton.isChecked():

                    self.timer_6 = QTimer(self)
                    self.timer_6.setSingleShot(True)
                    self.timer_6.timeout.connect(lambda: self.my_anneal.start_hot_sputter(float(self.Hot_Sputter_Current.text())))
                    self.timer_6.start((int(self.Hot_Sputter_Delay.text())+int(self.Anneal_Pause.text()))*time_factor)
            
            else:
                self.timer_7 = QTimer(self)
                self.timer_7.setSingleShot(True)
                self.timer_7.timeout.connect(lambda: self.my_anneal.start(float(self.Anneal_Current.text()),
                                                                   int(self.Anneal_Ramp.text()),
                                                                   int(self.Anneal_Time.text())))
                self.timer_7.start(int(self.Anneal_Pause.text())*time_factor)

        else:
            self.group_status('whatever')
            self.Start_Button.setChecked(False)
            self.Start_Button.setText('Start!')
            self.progress_update.stop()
            self.progressBar.setValue(100)
            pass
        
    def update_progress_bar(self):
        
        self.elapsed_time+=1
        if self.total_time>0:            
            self.progressBar.setValue(mt.floor(self.elapsed_time*100/(self.total_time*60)))
        else:   
            self.progressBar.setValue(100)
            
    def __del__ (self):
        quit()

class sputter_procedure(QThread):
    """ This class defines the sputter process itself """
    
    end_trigger = pyqtSignal()   
    global time_factor
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()        
        print ("sputter initializeed")
      
    def start(self, Sputter_Energy, Sputter_Pressure, Sputter_Time):

        print ("*sputter started")
        print(str(datetime.now()))
        
        self.Sputter_Energy = Sputter_Energy
        self.Sputter_Pressure = Sputter_Pressure
        self.Sputter_Time = Sputter_Time
        
        """ Here should be communication with sputter gun """
        
        self.timer_8 = QTimer(self)
        self.timer_8.timeout.connect(self.emit_end_sputter)
        self.timer_8.setSingleShot(True)
        self.timer_8.start(self.Sputter_Time*time_factor)

    def emit_end_sputter(self):
        
        print ("*sputter finished")
        print(str(datetime.now()))
        """Here the sputter gun and valve must be ramped down"""
        
        self.end_trigger.emit()
    
    def stop(self):
        
        print ("sputter interrupted")
        try:
            self.timer_8.stop()
            self.timet_8.deleteLater()           
        except:
            pass
        """Here the sputter gun and valve must be ramped down"""
        quit()
        
class anneal_procedure(QThread):
    """ This class defines the anneal process itself """
    global time_factor
    end_trigger = pyqtSignal()
    hot_sp_start_trigger = pyqtSignal()
    
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()
        print ("anneal initializeed")
      
    def start(self, current, ramp, time):
        print ("***anneal started")
        print(str(datetime.now()))
        """ Here should be communication with power supply """
        
        self.anneal_current = current
        self.anneal_time = time*time_factor
        self.anneal_ramp = ramp*time_factor
    
        self.timer_9 = QTimer(self)
        self.timer_9.timeout.connect(self.end_signal_anneal)
        self.timer_9.setSingleShot(True)
        self.timer_9.start(self.anneal_ramp+self.anneal_time)
   
    def end_signal_anneal(self):
        
        print ("***anneal finished")
        print(str(datetime.now()))
        self.end_trigger.emit()
        
    def start_hot_sputter(self, hs_current):
        print("*****hot sputter started")
        print(str(datetime.now()))
        
        self.hs_current = hs_current

        
    def end_hot_sp_anneal(self):
        
        print ("*****hot_sputter_finished")
        print(str(datetime.now()))
        """Deactivate here"""
    
    def stop(self):
        print ("anneal interrupted")
        try:
            self.timer_9.stop()
            self.timet_9.deleteLater()           
        except:
            pass
        """Deactivate here"""
        quit()
          
class total_countdown(QThread):
    """ This class defines the progressbar update process """
    update_trigger = pyqtSignal()
    end_trigger = pyqtSignal()
    
    def __init__(self, *args, **kwargs):      

        super(self.__class__, self).__init__()        
        print ("### total_countdown initializeed")
      
    def start(self,Total_time):
        
        print ("### countdown started")
        
        self.Total_time = Total_time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.emit_update_sputter)
        self.timer.start(1000)

    def emit_update_sputter(self):
  
        self.update_trigger.emit()
    
    def stop(self):
        self.timer.stop()
        self.timer.deleteLater()

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function