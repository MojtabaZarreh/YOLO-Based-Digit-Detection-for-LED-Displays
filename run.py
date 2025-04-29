import subprocess
import time

def run_main_script():
    while True:
        try:
            process = subprocess.Popen(["python", "main.py"])
            process.wait()  

            print("Main script stopped. Restarting...")
        except Exception as e:
            print(f"Error in watchdog: {e}")
            print("Restarting after 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    run_main_script()