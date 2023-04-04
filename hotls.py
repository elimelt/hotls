#!/usr/bin/env python3
import sys
import os
import subprocess
import datetime

def main():
    if len(sys.argv) < 2 or (sys.argv[1] != "history" and sys.argv[1] != "hotls"):
        print("Invalid argument. Usage: " + sys.argv[0] + " {history|hotls [day-range]}")
        sys.exit(1)

    if sys.argv[1] == "history":
        # collect git history for each file
        history = {}
        for root, dirs, files in os.walk('.'):
            for file in files:
                path = os.path.join(root, file)
                history[path] = subprocess.run(['git', 'log', '-p', path],
                                                capture_output=True, text=True).stdout

        # sort files by length of their git history
        sorted_files = sorted(history, key=lambda file: len(history[file]), reverse=True)

        # print sorted files and git history
        for file in sorted_files:
            print(history[file])

    elif sys.argv[1] == "hotls":
        # set date range (default last 30 days)
        since_when = 30
        if (len(sys.argv) != 2): 
            if (type(int(sys.argv[2])) != int): print('day range must be an integer number')
            else: since_when = int(sys.argv[2]) 
       
        date_curr = datetime.date.today()
        d = datetime.timedelta(days=since_when)
        date_since = date_curr - d
        print(date_since)

        # collect git log output for each file
        file_counts = {}
        for root, dirs, files in os.walk('.'):
            for file in files:
                path = os.path.join(root, file)
                count = subprocess.run(['git', 'log', '--pretty=format:', '--name-only','--after='+str(date_since.isoformat()), path],
                                       capture_output=True, text=True).stdout.count(file)
                file_counts[path] = count

        # sort files by count in the git history
        sorted_files = sorted(file_counts, key=lambda file: file_counts[file], reverse=True)

        # find the max count
        max_count = max(file_counts.values())

        # print files with color gradient based on count
        for file in sorted_files:
            count = file_counts[file]
            # calculate color based on the count
            if(max_count > 0): g = 255 * count // max_count
            else : g = 0
            r = 255 - g
            # create ANSI escape code for color
            color = f"\033[38;2;{r};{g};0m"
            # print colored file name 
            print(f"{color}{file}\033[0m")

if __name__ == "__main__":
    main()

