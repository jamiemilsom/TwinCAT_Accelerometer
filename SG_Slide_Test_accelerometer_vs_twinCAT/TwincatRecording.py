import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import convolve

class TwincatRecording:
    def __init__(self,path):
        self.path = path
        self.filename = os.path.basename(path)[:-4]
        
        self.position_range, self.velocity = self.filename.split("_")
        self.position_one, self.position_two = self.position_range.split("-")
        
        self.rising_edge_position = float(self.position_one) + 2.5

        self.data = pd.read_csv(self.path,sep='\t',skip_blank_lines=True,skiprows=4)
        self.data.rename(columns={'Name': 'Time (ms)'},inplace=True)

        idx = ((self.data['ActPos'].shift(1) < self.rising_edge_position) & (self.data['ActPos'] >= self.rising_edge_position) & (self.data['ActPos'].shift(-1) >= self.rising_edge_position)).idxmax()
        self.data.drop(self.data.index[:idx],inplace=True)
        self.data.reset_index(drop=True, inplace=True)
        
        self.data['Time (ms)'] = self.data['Time (ms)'] - self.data['Time (ms)'].iloc[0]

        self.data['Velocity m/s'] = self.data['ActVelo'] / 1000
        self.data['Time (s)'] = self.data['Time (ms)'] / 1000
        

        
    def convolve_velocity(self,length_of_kernel):
                
        convolve_vector = np.ones(length_of_kernel) / length_of_kernel
        self.data['Convolved Velocity m/s'] = convolve(self.data['Velocity m/s'].values,convolve_vector,mode='same')

    
    def calculate_acceleration(self, length_of_kernel):
        
        self.convolve_velocity(length_of_kernel)
        velocity_interp_func = interp1d(self.data['Time (s)'], self.data['Velocity m/s'],kind='cubic')
        velocity_interp_values = velocity_interp_func(self.data['Time (s)'])
        dt = 0.25e-3  # Twincat is very consistent so magic number allowed (seconds)
        self.data['Acceleration m/s^2'] = np.gradient(velocity_interp_values, dt)
        
    def convolve_acceleration(self,length_of_kernel):
                
        convolve_vector = np.ones(length_of_kernel) / length_of_kernel
        self.data['Convolved Acceleration m/s^2'] = convolve(self.data['Acceleration m/s^2'].values,convolve_vector,mode='same')

    
    def __repr__(self):
        
        return "This TwinCAT recording is at {velocity}mm/s from {position_one}mm to {position_two}mm along the slide. For Debugging rising edge:{rising_edge_position}mm".format(
            velocity=self.velocity,
            position_one=self.position_one,
            position_two=self.position_two,
            rising_edge_position = self.rising_edge_position
            )
