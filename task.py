import os
import shutil
import time
import argparse
from datetime import datetime

def logmessage(message, log_file):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"{timestamp} - {message}"
    
    print(formatted_message)
    
    with open(log_file, 'a') as log:
        log.write(formatted_message + "\n")

def syncfolders(source, copy, logfile):
    if not os.path.exists(copy):
        os.makedirs(copy)
        logmessage(f"Backup directory created: {copy}", logfile)

    for root, dirs, files in os.walk(source):
        source_path = os.path.relpath(root, source)
        copy_path = os.path.join(copy, source_path)
        
        if not os.path.exists(copy_path):
            os.makedirs(copy_path)
            logmessage(f"Backup directory created: {copy_path}", logfile)

        for file in files:
            source_file = os.path.join(root, file)
            copy_file = os.path.join(copy_path, file)
            
            if not os.path.exists(copy_file):
                shutil.copy2(source_file, copy_file)
                logmessage(f"New file copied: {source_file} para {copy_file}", logfile)
            elif os.path.getmtime(source_file) > os.path.getmtime(copy_file):
                shutil.copy2(source_file, copy_file)
                logmessage(f"Updated file: {source_file} para {copy_file}", logfile)

    for root, dirs, files in os.walk(copy):
        copy_path = os.path.relpath(root, copy)
        source_path = os.path.join(source, copy_path)

        if not os.path.exists(source_path):
            shutil.rmtree(root)
            logmessage(f"Directory removed from backup: {root}", logfile)
            continue

        for file in files:
            backup_file = os.path.join(root, file)
            source_file = os.path.join(source_path, file)
            if not os.path.exists(source_file):
                os.remove(backup_file)
                logmessage(f"File removed from backup: {backup_file}", logfile)

def runbackup(source_folder, copy_folder, logfile, interval):
    while True:
        logmessage("Starting synchronization...", logfile)
        syncfolders(source_folder, copy_folder, logfile)
        logmessage("Synchronization complete. Waiting for the next cycle...", logfile)
        time.sleep(interval * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronization complete. Waiting for the next cycle...")
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--backup', type=str, required=True)
    parser.add_argument('--interval', type=int, default=30)
    parser.add_argument('--log', type=str, default="backup_log.txt")

    args = parser.parse_args()

    runbackup(args.source, args.backup, args.log, args.interval)