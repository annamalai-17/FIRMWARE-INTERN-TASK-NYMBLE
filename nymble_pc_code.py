import serial
import time

port = 'COM10'  # port number
baud_rate = 2400

ser = serial.Serial(port, baud_rate, timeout=1)

try:
    file_path = r"C:\Users\lokke\Desktop\nymble_firmware_intern_annamalai\nymble_text.txt"

    # Variables for measuring data transmission speed
    bit_counter = 0
    time_interval = 5  # Setting the time interval for measuring in seconds
    start_time = time.time()

    while True:
        user_input = input("Enter a character to send to Arduino (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        try:
            # Reading the content of the text file
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Sending the file content to Arduino
            ser.write(file_content.encode())

            # Waiting for a moment to allow Arduino to process and send data back
            time.sleep(3)

            # Recording the start time for measuring data reception speed
            start_time = time.time()

            # Reading and printing the looped-back data from Arduino
            received_data = ser.readline().decode('utf-8').rstrip()
            print("Received data from Arduino:", received_data)

            # Updating counter
            bit_counter += len(received_data) * 8

            # Checking if the time interval has passed
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_interval:
                # Calculating and printing the bit rate
                bit_rate = bit_counter / elapsed_time
                print(f"Bit Rate: {bit_rate} bits/second")

                # Reseting counters for the next interval
                bit_counter = 0
                start_time = time.time()

        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")

except KeyboardInterrupt:
    # Closing the serial port when the program is interrupted
    ser.close()
    print("Serial port closed.")
