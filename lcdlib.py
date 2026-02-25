from machine import I2C
from time import sleep_ms

DEFAULT_I2C_ADDR = 0x27

# Các bit mask
MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4

class I2cLcd:
    def __init__(self, i2c, i2c_addr=DEFAULT_I2C_ADDR, num_lines=2, num_columns=16):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 1 << SHIFT_BACKLIGHT

        sleep_ms(20)  # Chờ LCD khởi động

        # Reset LCD 3 lần
        self.hal_write_init_nibble(0x30)
        sleep_ms(5)
        self.hal_write_init_nibble(0x30)
        sleep_ms(1)
        self.hal_write_init_nibble(0x30)
        sleep_ms(1)

        # Chế độ 4 bit
        self.hal_write_init_nibble(0x02)
        sleep_ms(1)


        # Cấu hình chức năng: 2 dòng, 5x8 font
        self.hal_write_command(0x28)
        self.display_on()
        self.clear()
        self.hal_write_command(0x06)  # Chế độ tăng địa chỉ, không dịch màn hình

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble & 0x0F) << SHIFT_DATA)
        self.hal_write_byte(byte)

    def hal_write_byte(self, byte):
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E | self.backlight]))
        self.i2c.writeto(self.i2c_addr, bytearray([(byte & ~MASK_E) | self.backlight]))

    def hal_write_nibble(self, nibble, mode=0):
        byte = ((nibble & 0x0F) << SHIFT_DATA) | mode
        self.hal_write_byte(byte)

    def hal_write_command(self, cmd):
        self.hal_write_nibble(cmd >> 4, 0)
        self.hal_write_nibble(cmd & 0x0F, 0)
        if cmd in [0x01, 0x02]:  # clear, home cần lâu hơn
            sleep_ms(2)
        else:
            sleep_ms(1)          # các lệnh khác vẫn nên delay nhẹ 1ms


    def hal_write_data(self, data):
        self.hal_write_nibble(data >> 4, MASK_RS)
        self.hal_write_nibble(data & 0x0F, MASK_RS)
        sleep_ms(1)  # thêm delay sau mỗi ký tự


    def putstr(self, string):
        for char in string:
            self.hal_write_data(ord(char))

    def clear(self):
        self.hal_write_command(0x01)
        sleep_ms(2)

    def home(self):
        self.hal_write_command(0x02)
        sleep_ms(2)

    def set_cursor(self, row, col):
        addr = col + (0x40 if row else 0x00)
        self.hal_write_command(0x80 | addr)

    def display_on(self):
        self.hal_write_command(0x0C)

    def display_off(self):
        self.hal_write_command(0x08)

    def cursor_on(self):
        self.hal_write_command(0x0E)

    def cursor_off(self):
        self.hal_write_command(0x0C)

    def blink_on(self):
        self.hal_write_command(0x0F)

    def blink_off(self):
        self.hal_write_command(0x0C)

    def backlight_on(self):
        self.backlight = 1 << SHIFT_BACKLIGHT
        self.i2c.writeto(self.i2c_addr, bytearray([self.backlight]))

    def backlight_off(self):
        self.backlight = 0
        self.i2c.writeto(self.i2c_addr, bytearray([self.backlight]))

    def create_char(self, location, charmap):
        location &= 0x7  # chỉ cho phép 0-7
        self.hal_write_command(0x40 | (location << 3))
        for i in range(8):
            self.hal_write_data(charmap[i])

    def scroll_display_left(self):
        self.hal_write_command(0x18)

    def scroll_display_right(self):
        self.hal_write_command(0x1C)
