import pandas as pd
import matplotlib.pyplot as plt

def analysis(df,choice):
    """
    This function performs an extended analysis based on user input.
    It collects information about the stage name, displacement step,
    axis under investigation, and direction of image capture.
    """
    print("\nExtended Analysis")
    # Collecting user inputs
    stg_name = input("\n Enter the stage name: ")

    disp_step = int(input("\n Enter the displacement step (mm): "))

    axes_options = [
        'X_theta', 'Y_theta', 'Z_theta',
        'obj_x', 'obj_y', 'obj_z',
        'R_cam_X_theta', 'R_cam_Y_theta', 'R_cam_Z_theta',
        'cam_x', 'cam_y', 'cam_z'
    ]

    print("\nSelect the axis under investigation:")
    for idx, axis in enumerate(axes_options, 1):
        print(f"{idx}. {axis}")

    axis_choice = int(input("Enter the number corresponding to the axis: "))
    if 1 <= axis_choice <= len(axes_options):
        selected_axis = axes_options[axis_choice - 1].lower()
        print(f"You selected: {selected_axis}")
    else:
        print("Invalid choice. Please select a valid axis number.")

    if choice == '1':
        strt_pt_origin = int(input("Enter the starting position (mm): "))
        ref_pos = [strt_pt_origin + i * disp_step for i in range(len(df))]
    elif choice == '2':
        strt_pt_end_pos = int(input("Enter the starting position (mm): "))
        ref_pos = [strt_pt_end_pos - i * disp_step for i in range(len(df))]
    else:
        print("Invalid choice. Please select 1 or 2.")

    # --- New code for creating a new DataFrame and calculating parameters ---
    if selected_axis in df.columns:
        new_df = pd.DataFrame()
        new_df['ref_pos'] = ref_pos
        new_df[selected_axis] = df[selected_axis].values

         # Calculate measured displacement as difference between consecutive values
        new_df['measured displacement'] = new_df[selected_axis].diff().fillna(0).abs()

        new_df['displacement_error'] = new_df['measured displacement'] - disp_step

        new_df['percentage_error'] = (new_df['displacement_error'] / disp_step) * 100

        # Calculate average percentage error (ignoring the first row)
        avg_percentage_error = new_df['percentage_error'].iloc[1:].abs().mean()
        print(f"\nAverage Percentage Error: {avg_percentage_error:.2f}%")

        # Ignore the first row for plotting
        plot_df = new_df.iloc[1:]

        # Plot 1: ref_pos vs measured displacement
        plt.figure(figsize=(8, 5))
        plt.plot(plot_df['ref_pos'], plot_df['measured displacement'], marker='o')
        plt.xlabel('Reference Position (mm)')
        plt.ylabel('Measured Displacement (mm)')
        plt.title('Reference Position vs Measured Displacement for ' + selected_axis +' of ' + stg_name)
        plt.axhline(y=disp_step, color='r', linestyle='--', label='Expected Displacement')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('ref_pos_vs_measured_displacement.png')
        plt.show()

        # Plot 2: ref_pos vs displacement error
        plt.figure(figsize=(8, 5))
        plt.plot(plot_df['ref_pos'], plot_df['displacement_error'], marker='o', color='red')
        plt.xlabel('Reference Position (mm)')
        plt.ylabel('Displacement Error (mm)')
        plt.title('Reference Position vs Displacement Error for ' + selected_axis +' of ' + stg_name)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('ref_pos_vs_displacement_error.png')
        plt.show()
    else:
        print(f"Column '{selected_axis}' not found in the DataFrame.")

    new_df.to_excel('new_camera_data.xlsx', index=False)


