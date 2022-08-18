# main.py
def main():
    with open('esp32_PWM_ADCcontrol.py', 'r') as f:
        exec(f.read())
    
if __name__ == '__main__':
    main()
