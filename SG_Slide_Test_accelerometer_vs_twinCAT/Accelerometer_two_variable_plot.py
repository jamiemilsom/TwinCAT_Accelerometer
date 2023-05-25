import matplotlib.pyplot as plt
import seaborn as sns

def Accelerometer_two_variable_plot(Accelerometer_velocities, Accelerometer_dfs,TC=False, data_type_one='Acceleration m/s^2', data_type_two='Magnetic field Z(ʯt)',
                              scaling_factor=2, palette='muted', time_start=0, time_end=3500):
    sns.set_style("darkgrid")
    plt.figure(figsize=(16*scaling_factor,9*scaling_factor))
    colors = sns.color_palette(palette)
    
    if TC == False:
        for i, velocity in enumerate(Accelerometer_velocities):
            ax1 = plt.subplot(len(Accelerometer_dfs) + 1, 1, i+1)
            ax2 = ax1.twinx()

            
            sns.scatterplot(data=Accelerometer_dfs[velocity].data, x="Elapsed Time (ms)", y=data_type_one, ax=ax1, color=colors[0])
            
            sns.scatterplot(data=Accelerometer_dfs[velocity].data, x="Elapsed Time (ms)", y=data_type_two, ax=ax2, color=colors[1])
            
            ax1.set_xlim(time_start, time_end)
            
            ax1_max_y_value = abs(Accelerometer_dfs[velocity].data[data_type_one]).max()
            ax1.set_ylim(-ax1_max_y_value,ax1_max_y_value)
            
            ax2_max_y_value = abs(Accelerometer_dfs[velocity].data[data_type_two]).max()
            ax2.set_ylim(-ax2_max_y_value,ax2_max_y_value)
            
            ax1.set_ylabel(data_type_one)
            ax2.set_ylabel(data_type_two)

            labels = [Accelerometer_dfs[velocity].position_range + " " + data_type_two,
                        Accelerometer_dfs[velocity].position_range + " " + data_type_one]

            plt.legend(labels,loc='upper right')
            plt.tight_layout()

            plt.title('{data_type_one} and {data_type_two} at {velocity}mm/s'.format(data_type_one=data_type_one,data_type_two=data_type_two,velocity=velocity))
    
    elif TC == True:
        for i, velocity in enumerate(Accelerometer_velocities):
            ax1 = plt.subplot(len(Accelerometer_dfs) + 1, 1, i+1)
            ax2 = ax1.twinx()

            
            sns.lineplot(data=Accelerometer_dfs[velocity].TC_data, x="Time (ms)", y=data_type_one, ax=ax1, color=colors[0])
            
            sns.lineplot(data=Accelerometer_dfs[velocity].TC_data, x="Time (ms)", y=data_type_two, ax=ax2, color=colors[1])
            
            ax1.set_xlim(time_start, time_end)
            
            ax1_max_y_value = abs(Accelerometer_dfs[velocity].TC_data[data_type_one]).max()
            ax1.set_ylim(-ax1_max_y_value,ax1_max_y_value)
            
            ax2_max_y_value = abs(Accelerometer_dfs[velocity].TC_data[data_type_two]).max()
            ax2.set_ylim(-ax2_max_y_value,ax2_max_y_value)
        
            ax1.set_ylabel(data_type_one)
            ax2.set_ylabel(data_type_two)

            labels = [Accelerometer_dfs[velocity].position_range + " " + data_type_two,
                        Accelerometer_dfs[velocity].position_range + " " + data_type_one]

            plt.legend(labels,loc='upper right')
            plt.tight_layout()

            plt.title('{data_type_one} and {data_type_two} at {velocity}mm/s'.format(data_type_one=data_type_one,data_type_two=data_type_two,velocity=velocity))
