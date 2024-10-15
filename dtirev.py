import os
import subprocess

def reverse_first_row_bvec(bvec_path, bvec_rev_path):
    with open(bvec_path, 'r') as f:
        lines = f.readlines()
    
    # Split the first row and reverse the sign of each element
    first_row = lines[0].split()
    reversed_first_row = [-float(x) for x in first_row]
    
    # Keep the second and third rows unchanged
    second_row = lines[1].strip()
    third_row = lines[2].strip()
    
    # Write the reversed bvec file
    with open(bvec_rev_path, 'w') as f:
        f.write(' '.join(map(str, reversed_first_row)) + '\n')
        f.write(second_row + '\n')
        f.write(third_row + '\n')

# Use the current working directory
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
            out_reversed = os.path.join(root, 'r' + base_filename)  # Reversed output
            
            # Construct path for reversed bvec
            bvec_rev_path = os.path.join(root, base_filename + '_rev.bvec')
            
            # Create reversed bvec file
            reverse_first_row_bvec(bvec_path, bvec_rev_path)
            
            # Run the 'bet' command for brain extraction
            bet_command = ['bet', nii_path, bet_output, '-f', '0.3', '-g', '0', '-n', '-m']
            print(f'Running BET command: {" ".join(bet_command)}')
            subprocess.run(bet_command)
            bet_output = bet_output + '_mask'  # BET appends "mask"

            # Run the 'dtifit' command with the reversed bvec file
            dtifit_command = [
                'dtifit', '--save_tensor',
                '--data=' + nii_path,
                '--out=' + out_reversed,
                '--mask=' + bet_output,
                '--bvecs=' + bvec_rev_path,
                '--bvals=' + bval_path
            ]
            print(f'Running dtifit command with reversed bvec: {" ".join(dtifit_command)}')
            subprocess.run(dtifit_command)
