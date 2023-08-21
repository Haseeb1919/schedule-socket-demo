import socket
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname()) 
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    """Sends a message to the server."""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    return client.recv(2048).decode(FORMAT)

total_on_time = 0
device_on_time = 0
device_is_on = False

def turn_off_device():
    global total_on_time, device_on_time, device_is_on
    if device_is_on:
        response = send("turn off")
        if response == "Device state is now: off":
            device_off_time = time.time()
            total_on_time += device_off_time - device_on_time
            print("Device was turned ON for: {:.2f} seconds".format(device_off_time - device_on_time))
            device_is_on = False
    else:
        print("Device is already off.")



def turn_on_device():
    global total_on_time, device_on_time, device_is_on
    if not device_is_on:
        response = send("turn on")
        if response == "Device state is now: on":
            device_on_time = time.time()
            device_is_on = True
            print("Device is now ON")
    else:
        print("Device is already on.")




def quit_program():
    global total_on_time
    if device_is_on:
        turn_off_device()
    print("Total Device On-Time: {:.2f} seconds".format(total_on_time))
    send("quit")
    exit()



def get_user_input():
    user_input = input("Do you want to turn on, turn off, or set a schedule for the device? \n")
    return user_input



def schedule_device_action(action_func, time_to_wait):
    print(f"Scheduling device {action_func.__name__} in {time_to_wait:.2f} seconds.")
    time.sleep(time_to_wait)
    action_func()



def schedule():
    while True:
        action = input("Do you want to schedule the device to turn on? (yes/no) \n ").lower()
        if action not in ["yes", "no"]:
            print("Invalid input. Please enter 'yes' or 'no'.")
            return

        if action == "no":
            break

        time_unit = input("Do you want to set the schedule in hours or minutes? ").lower()
        if time_unit not in ["hours", "minutes"]:
            print("Invalid input. Please choose 'hours' or 'minutes'.")
            return

        time_conversion = 60 if time_unit == "minutes" else 3600  # Conversion factor

        start_time = int(input(f"Enter the starting point in {time_unit}: "))
        end_time = int(input(f"Enter the ending point in {time_unit}: "))

        start_time_seconds = start_time * time_conversion
        end_time_seconds = end_time * time_conversion

        if action == "yes":
            schedule_device_action(
                action_func=turn_on_device,
                time_to_wait=start_time_seconds,
            )
            schedule_device_action(
                action_func=turn_off_device,
                time_to_wait=end_time_seconds - start_time_seconds,
            )
            
            break

while True:
    user_input = get_user_input()

    if user_input == "turn on":
        if not device_is_on:
            response = send("turn on")
            if response == "Device state is now: on":
                device_on_time = time.time()
                device_is_on = True
                print("Device is now ON")
    elif user_input == "turn off":
        turn_off_device()
    elif user_input == "schedule":
        schedule()
    elif user_input == "quit":
        quit_program()
    else:
        print("Invalid input.")
