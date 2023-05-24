import matplotlib.pyplot as plt
import seaborn as sns

def TwinCAT_two_variable_plot(TwinCAT_velocities, TwinCAT_dfs, data_type_one='Velocity m/s', data_type_two='SetCurr',
                              scaling_factor=2, palette='muted', time_start=0, time_end=3500):
    sns.set_style("darkgrid")
    plt.figure(figsize=(16*scaling_factor,9*scaling_factor))
    colors = sns.color_palette(palette)

    for i, velocity in enumerate(TwinCAT_velocities):
        ax1 = plt.subplot(len(TwinCAT_dfs) + 1, 1, i+1)
        ax2 = ax1.twinx()

        
        sns.lineplot(data=TwinCAT_dfs[velocity].data, x="Time (ms)", y=data_type_one, ax=ax1, color=colors[0])
        
        sns.lineplot(data=TwinCAT_dfs[velocity].data, x="Time (ms)", y=data_type_two, ax=ax2, color=colors[1])
        
        ax1.set_xlim(time_start, time_end)
        
        ax1_max_y_value = abs(TwinCAT_dfs[velocity].data[data_type_one]).max()
        ax1.set_ylim(-ax1_max_y_value,ax1_max_y_value)
        
        ax2_max_y_value = abs(TwinCAT_dfs[velocity].data[data_type_two]).max()
        ax2.set_ylim(-ax2_max_y_value,ax2_max_y_value)
        
        ax1.set_ylabel(data_type_one)
        ax2.set_ylabel(data_type_two)
        
        labels = [TwinCAT_dfs[velocity].position_range + " " + data_type_two,
                  TwinCAT_dfs[velocity].position_range + " " + data_type_one]

        plt.legend(labels,loc='upper right')
        plt.tight_layout()

        plt.title('{data_type_one} and {data_type_two} at {velocity}mm/s'.format(data_type_one=data_type_one,data_type_two=data_type_two,velocity=velocity))
