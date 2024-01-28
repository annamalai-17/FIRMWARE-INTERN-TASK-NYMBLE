import serial
import time

# Specify the port name (you need to change this based on your system)
# port = '/dev/ttyUSB0'  # For Linux
port = 'COM10'  # For Windows

# Specify the baud rate used in your Arduino code
baud_rate = 2400

# Create a serial connection
ser = serial.Serial(port, baud_rate, timeout=1)

try:
    file_path = r"C:\Users\lokke\Desktop\nymble_firmware_intern_annamalai\nymble_text.txt"
    while True:
        # Get user input for the file path
        user_input = input("Enter a character to send to Arduino (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        try:
            # Read the content of the text file
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Send the file content to Arduino
            ser.write(file_content.encode())

            # Record the start time for measuring data transmission speed
            start_time = time.time()

            # Wait for a moment to allow Arduino to process and send data back
            time.sleep(3)

            # Read and print the looped-back data from Arduino
            received_data = ser.readline().decode('utf-8').rstrip()
            print("Received data from Arduino:", received_data)

            # Calculate and print the real-time data transmission speed
            elapsed_time = time.time() - start_time
            total_bits_transmitted = len(file_content) * 8
            data_rate = total_bits_transmitted / elapsed_time
            print(f"Data Transmission Speed: {data_rate} bits/second")

        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")

except KeyboardInterrupt:
    # Close the serial port when the program is interrupted
    ser.close()
    print("Serial port closed.")
