import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import convolve
from scipy.integrate import cumtrapz

class AccelerometerRecording:
     def __init__(self,path):
          self.path = path
          
          self.filename = os.path.basename(path)[:-8]
          self.position_range, self.velocity = self.filename.split("_")
          self.position_one, self.position_two = self.position_range.split("-")

          with open(path,'r') as file:
               first_line = file.readline().rstrip()

          if not first_line.endswith(','):
               first_line += ','
          
          with open(path, 'r+') as file:
               content = file.readlines()
               content[0] = first_line + '\n'
               file.seek(0)
               file.writelines(content)

          self.data = pd.read_csv(path)
          self.data.rename(columns={self.data.columns[0]: 'Time h/m/s/ms', self.data.columns[1]: 'Device Name'}, inplace=True)
          
          self.data['Time h/m/s/ms'] = pd.to_datetime(self.data['Time h/m/s/ms'].str.strip(), format='%H:%M:%S.%f')
          self.data['Elapsed Time (s)'] = (self.data['Time h/m/s/ms'] - self.data.loc[0, 'Time h/m/s/ms']).dt.total_seconds()

          self.data['Elapsed Time (ms)'] = self.data['Elapsed Time (s)'] * 1000
          self.data['Acceleration m/s^2'] = self.data['Acceleration X(g)'] * 9.81
          self.data = self.data.drop_duplicates(subset=['Elapsed Time (ms)'],keep='first')
          


            
     def interpolate_acceleration(self):
          
          min_time = self.data['Elapsed Time (ms)'].min()
          max_time = self.data['Elapsed Time (ms)'].max()
          num_points = int((max_time - min_time) / 0.25) + 1
          self.TC_data = pd.DataFrame()
          self.TC_data['Time (ms)'] = np.linspace(min_time, max_time, num_points)
                
          acceleration_interp_func = interp1d(self.data['Elapsed Time (ms)'], self.data['Acceleration m/s^2'],kind='cubic')
          self.TC_data['Acceleration m/s^2'] = acceleration_interp_func(self.TC_data['Time (ms)'])
          
     def calculate_velocity(self):
          self.TC_data['Velocity m/s'] = cumtrapz(self.TC_data['Acceleration m/s^2'],x=self.TC_data['Time (ms)'],initial=0) / 1000
          
     def convolve_velocity(self, length_of_kernel):
          convolve_vector = np.ones(length_of_kernel) / length_of_kernel
          self.TC_data['Convolved Velocity m/s^2'] = convolve(self.TC_data['Velocity m/s'].values,convolve_vector,mode='same')
    



     def __repr__(self):
               return "This Accelerometer recording is at {velocity}mm/s from {position_one}mm to {position_two}mm along the slide.".format(
               velocity=self.velocity,
               position_one=self.position_one,
               position_two=self.position_two
               )


