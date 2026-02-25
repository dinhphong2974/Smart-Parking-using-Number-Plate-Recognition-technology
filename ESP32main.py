import time
import sys
import select
from machine import Pin, PWM, I2C
from lcd import I2cLcd

# Cảm biến siêu âm
trig_in = Pin(5, Pin.OUT)
echo_in = Pin(18, Pin.IN)
trig_out = Pin(4, Pin.OUT)
echo_out = Pin(19, Pin.IN)

# Servo barrier
servo_in = PWM(Pin(26), freq=50)
servo_out = PWM(Pin(13), freq=50)

# Ngưỡng khoảng cách mở barrier (cm)
openDistance = 12

# Trạng thái barrier
barrierOpen_in = False
barrierOpen_out = False
sensorOutActive = True

# Khởi tạo I2C
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)  # Điều chỉnh SDA/SCL theo board

# Khởi tạo LCD
lcd = I2cLcd(i2c, i2c_addr=0x27, num_lines=2, num_columns=16)

# Bật đèn nền
lcd.backlight_on()

# Xóa màn hình
lcd.clear()

# Góc → duty cycle
def set_servo_angle(servo, angle):
    duty = int((angle / 180.0 * 2 + 0.5) / 20 * 1023)
    servo.duty(duty)

# Mở và đóng barrier
def open_barrier_in():
    global barrierOpen_in, sensorOutActive
    set_servo_angle(servo_in, 90)
    barrierOpen_in = True
    sensorOutActive = True
    trig_out.on()
    time.sleep(1)

def close_barrier_in():
    global barrierOpen_in
    set_servo_angle(servo_in, 10)
    time.sleep(1)
    barrierOpen_in = False

def open_barrier_out():
    global barrierOpen_out
    set_servo_angle(servo_out, 90)
    barrierOpen_out = True
    time.sleep(1)

def close_barrier_out():
    global barrierOpen_out
    set_servo_angle(servo_out, 0)
    time.sleep(1)
    barrierOpen_out = False

# Đo khoảng cách
def get_distance(trig, echo):
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    start = time.ticks_us()
    timeout = 30000
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), start) > timeout:
            return 999
    start = time.ticks_us()
    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), start) > timeout:
            return 999
    end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    distance = (duration * 0.0343) / 2
    return distance

def main():
    global sensorOutActive, barrierOpen_in

    set_servo_angle(servo_in, 10)
    set_servo_angle(servo_out, 0)
    trig_out.on()
    
    while True:
        distance_in = get_distance(trig_in, echo_in)
        distance_out = get_distance(trig_out, echo_out) if sensorOutActive else 50

        try:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                command = sys.stdin.readline().strip()
                if command == '1':
                    open_barrier_out()
                    if get_distance(trig_out, echo_out) > openDistance:
                        time.sleep(0.2)
                        close_barrier_out()
                    sensorOutActive = True
                    trig_out.on()
                elif command == '0':
                    sensorOutActive = True
                else:
                    lcd.clear()
                    time.sleep_ms(50)
                    lcd.putstr(str(command)[:16])
                    time.sleep_ms(50)
        except Exception as e:
            print("Serial Read Error:", e)

        # Xe ra
        if distance_out < openDistance:  
            sensorOutActive = False
            trig_out.off()
            print("checkout_started")
            time.sleep(0.5)
            
        # Xe vào
        if distance_in < openDistance and not barrierOpen_in:
            open_barrier_in()
            time.sleep(0.5)
            print("Welcome In")
        elif distance_in > openDistance and barrierOpen_in:
            time.sleep(0.2)
            close_barrier_in()

        time.sleep(0.1)

# Khởi chạy
main()


