import os
import subprocess

# Define the directory where the files are located
directory = os.getcwd()

# Loop through each file in the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.bval'):
            # Get the full path of the .bval file
            bval_path = os.path.join(root, file)
            
            # Derive the base filename (without extension)
            base_filename = file.replace('.bval', '')
            
            # Construct paths for .bvec and NIfTI
            bvec_path = os.path.join(root, base_filename + '.bvec')
            nii_path = os.path.join(root, base_filename)  # NIfTI without extension
            bet_output = os.path.join(root, base_filename)  # BET output
            out_output = os.path.join(root, 'o' + base_filename)  # Output for dtifit
            
            # Run the 'bet' command for brain extraction
            bet_command = ['bet', nii_path, bet_output, '-f', '0.3', '-g', '0', '-n', '-m']
            print(f'Running BET command: {" ".join(bet_command)}')
            subprocess.run(bet_command)
            
            bet_output = bet_output + '_mask'  # BET appends "mask"

            # Run the 'dtifit' command for tensor derivation

            dtifit_command = [
                'dtifit', '--save_tensor',
                '--data=' + nii_path,
                '--out=' + out_output,
                '--mask=' + bet_output,
                '--bvecs=' + bvec_path,
                '--bvals=' + bval_path
            ]
            print(f'Running dtifit command: {" ".join(dtifit_command)}')
            subprocess.run(dtifit_command)
