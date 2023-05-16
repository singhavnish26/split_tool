import yaml
import sys
import signal
import os
import time
from datetime import datetime
import logging
from pathlib import Path


def monitor_directory(input_dir, file_extensions):
    logging.basicConfig(filename='new_files.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Define the path to the directory you want to monitor
    dir_path = input_dir#"/SMB_HES_PRD/Event-profile"

    # Get the list of files in the directory
    dir_files = os.listdir(dir_path)

    # Store the list of files as a set
    dir_files_set = set(dir_files)

    # Monitor the directory for new files
    while True:
        # Get the updated list of files in the directory
        updated_dir_files = os.listdir(dir_path)

        # Store the updated list of files as a set
        updated_dir_files_set = set(updated_dir_files)

        # Find the difference between the updated set of files and the original set of files
        new_files_set = updated_dir_files_set - dir_files_set

        # Check if there are new files in the directory
        if new_files_set:
            logging.info("New file(s) found!")
            for file in new_files_set:
                logging.info(file)
                return file #Here take care of one file at a time only

        # Update the original set of files to be the updated set of files
        dir_files_set = updated_dir_files_set



def SIGTERMhandler(sig, frame):
    print("Exiting...")
    sys.stdout.flush()
    sys.exit()


signal.signal(signal.SIGTERM, SIGTERMhandler)


# calculate file size in KB, MB, GB
def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


# with open('/home/admin-zonososs-IPv6/techno-py/splitmd.yaml') as yamlfile:
with open('testsplitmd.yaml') as yamlfile:
    config = yaml.safe_load(yamlfile)
indir = config.get("indir")
if indir is None:
    print(f"Missing indir input in config yaml file")
    sys.exit()
outdir = config.get("outdir")
if outdir is None:
    print(f"Missing outdir input in config yaml file")
    sys.exit()
lineLimit = config.get("lineLimit")
if lineLimit is None:
    print(f"Missing lineLimit input in config yaml file")
    sys.exit()
extensionList = config.get("extension")
if extensionList is None:
    print(f"Missing extension input in config yaml file")
    sys.exit()

while True:
    try:
        print(f"Waiting for new file in directory {indir} (press Cntrl-c to exit)")
        sys.stdout.flush()

        input_dir = indir
        file_extensions = extensionList

        file_name=None
        file_name = monitor_directory(input_dir, file_extensions)
        if file_name!=None:
            print(f"Recieved new file in directory {indir} (press Cntrl-c to exit)")
            print(f"Recieved new file name is {file_name})")
            sys.stdout.flush()
            lastDot = file_name.rfind(".")
            fExt = file_name[lastDot + 1:]
            fName = file_name[:lastDot]

            # additional
            Path_p = ''
            Path_p = indir + '/' + file_name

            print("\n Initial Path name is : "+ Path_p)
            print("\n Initial file name is : " + file_name)
            #Handling .tmp issue
            if '.txt.tmp' in file_name:
                print("\n Entered for 1st")
                while True:
                    time.sleep(10)
                    path_check = Path(Path_p)
                    Exist1 = path_check.is_file()


                    if Exist1 == False:
                        print("\n Entered for 2nd")
                        Path_p =  Path_p.replace('.tmp','')
                        print("\n Second Path name is : " + Path_p)
                        path_check = Path(Path_p)
                        Exist2 = path_check.is_file()

                        if Exist2 == True :
                            print("\n Entered for 3rd")
                            if '.txt.tmp' in file_name:
                                print("\n Entered for 4th")
                                file_name=file_name.replace('.tmp','')
                                lastDot = file_name.rfind(".")
                                fExt = file_name[lastDot + 1:]
                                fName = file_name[:lastDot]
                                print(f"Recieved file name changed to {file_name})")
                                break

            print("\n Final Path name is : " + Path_p)
            f_size = os.path.getsize(Path_p)
            print('Initial file size is', f_size)
            l_size = f_size
            success_Flag = False

            StartTime = time.time()

            while (time.time() < (StartTime + (30 * 60))):

                try:
                    path_check = Path(Path_p)
                    Exist1 = path_check.is_file()
                    if Exist1== False:
                        if '.txt.tmp' in Path_p:
                            Path_p=Path_p.replace('.tmp','')
                            file_name = file_name.replace('.tmp','')
                            lastDot = file_name.rfind(".")
                            fExt = file_name[lastDot + 1:]
                            fName = file_name[:lastDot]

                    f_size = os.path.getsize(Path_p)
                    time.sleep(10)
                    l_size = os.path.getsize(Path_p)
                except :
                    print("\n Seems like file extension error of .txt.tmp")

                    path_check = Path(Path_p)
                    Exist1 = path_check.is_file()
                    if Exist1 == False:
                        Path_p = Path_p.replace('.tmp','')
                        file_name = file_name.replace('.tmp','')
                        lastDot = file_name.rfind(".")
                        fExt = file_name[lastDot + 1:]
                        fName = file_name[:lastDot]

                        f_size = os.path.getsize(Path_p)
                        time.sleep(10)
                        l_size = os.path.getsize(Path_p)

                if f_size == l_size:
                    success_Flag=True
                    break

            if success_Flag == True:
                print('Complete file size is', f_size)
            else:
                print(f"Unable to fully capture the file in 15 minutes.Check for failed - {file_name}")
                x = '/root/techno_splitmd/fileIncomplete/'
                sDT = datetime.now()
                dts_string = sDT.strftime("%H_%M_%S %d_%m_%Y")

                FileName = dts_string + '.txt'
                print('Incomplete file size is', f_size)
                with open(x + FileName, 'a') as f:
                    f.write("New file opened: \n\n")
            ##NEW LOGIC ABOVE END
            if (lastDot > 0) and (fExt in file_extensions):
                infile = open(indir + "/" + file_name, "r")
                outfile = infile  # NOP to initialize outfile to avoid interpreter complain!
                lines = infile.readlines()

                i = 0
                suffix = 0  # NOP to initialize suffix to avoid ocasional error!
                for line in lines:
                    i += 1
                    if i % lineLimit == 1:
                        suffix = int(i / lineLimit) + 1
                        if suffix > 1:
                            outfile.close()
                        outfile = open(outdir + "/" + fName + "_" + str(suffix) + "." + fExt, "w")
                    outfile.writelines(line)
                outfile.close()
                print(f"{suffix} split files created in directory {outdir} (press Cntrl-c to exit)")
                sys.stdout.flush()
            else:
                print(f"file name format not recognized, only extensions allowed are: {extensionList}")
                sys.stdout.flush()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.stdout.flush()
        sys.exit()
