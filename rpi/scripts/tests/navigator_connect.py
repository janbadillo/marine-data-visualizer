import bluerobotics_navigator as navigator



# Test script to be ran on Raspberry Pi, to test the navigator. 

def main() -> None:
    print("Navigator initialization...")
    navigator.init()
    print("Navigator initialized")
    navigator.set_led(navigator.UserLed.Led1, True)





if __name__ == "__main__":
    main()