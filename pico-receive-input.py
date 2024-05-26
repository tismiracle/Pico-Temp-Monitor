import sys
import machine
from machine import Pin,SPI
import framebuf
import time
import math
import _thread
#aa


led = Pin(25, machine.Pin.OUT)
#led = machine.Pin(24, machine.Pin.OUT)

#def led_on():
#    led(1)

#def led_off():
#    led(0)


DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
class LED_light():
    def __init__(self):
        self.led = Pin(25, machine.Pin.OUT)

    def on(self):
        self.led(1)

    def off(self):
        self.led(0)

class OLED_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 64

        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,2000_000)
        self.spi = SPI(1,20000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()

        self.white =   0xffff
        self.black =   0x0000

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)

        self.write_cmd(0xAE) #turn off OLED display

        self.write_cmd(0x00)   #set lower column address
        self.write_cmd(0x10)   #set higher column address

        self.write_cmd(0xB0)   #set page address

        self.write_cmd(0xdc)    #et display start line
        self.write_cmd(0x00)
        self.write_cmd(0x81)    #contract control
        self.write_cmd(0x6f)    #128
        self.write_cmd(0x21)    # Set Memory addressing mode (0x20/0x21) #

        self.write_cmd(0xa0)    #set segment remap
        self.write_cmd(0xc0)    #Com scan direction
        self.write_cmd(0xa4)   #Disable Entire Display On (0xA4/0xA5)

        self.write_cmd(0xa6)    #normal / reverse
        self.write_cmd(0xa8)    #multiplex ratio
        self.write_cmd(0x3f)    #duty = 1/64

        self.write_cmd(0xd3)    #set display offset
        self.write_cmd(0x60)

        self.write_cmd(0xd5)    #set osc division
        self.write_cmd(0x41)

        self.write_cmd(0xd9)    #set pre-charge period
        self.write_cmd(0x22)

        self.write_cmd(0xdb)    #set vcomh
        self.write_cmd(0x35)

        self.write_cmd(0xad)    #set charge pump enable
        self.write_cmd(0x8a)    #Set DC-DC enable (a=0:disable; a=1:enable)
        self.write_cmd(0XAF)

    def show(self):
        self.write_cmd(0xb0)
        for page in range(0,64):
            self.column = 63 - page
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0,16):
                self.write_data(self.buffer[page*16+num])
                

class Display():
    def __init__(self):
        self.OLED = OLED_1inch3()

        
class ProgressBar():
    def __init__(self, pos_x, pos_y, display):
        self.display = display
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        
    def calculate_bar(self, amount):
        #OLED.text("[]", 110, height + 10, OLED.white)
        #14 ich
        #14 pustych miejsc
        # - to zużycie
        used = math.floor((amount/100) * 14)
        empty_char = " "
        used_char = "-"
        #OLED.text("[--------------]", 2, height + 10, OLED.white)
        self.display.OLED.text("[" + (used_char * used) + (empty_char * (14 - used)) + "]", self.pos_x, self.pos_y + 10, self.display.OLED.white)
        #self.display.OLED.show()
        
class TextLabel():
    def __init__(self, pos_x, pos_y, display):
        self.display = display
        self.pos_x = pos_x
        self.pos_y = pos_y


    #display.OLED.text("CPU Temp:" + splitted_v[0], 2, 10, display.OLED.white)
    def display_widget(self, text_label):
        self.display.OLED.text(text_label, self.pos_x, self.pos_y, self.display.OLED.white)
        #self.display.OLED.show()
    

if __name__ == '__main__':
    display = Display()

    cpu_temp = TextLabel(2, 0, display)
    cpu_load = TextLabel(2, 10, display)
    gpu_temp = TextLabel(2, 30, display)
    gpu_load = TextLabel(2, 40, display)
    
    cpu_progress_bar = ProgressBar(2, 10, display)
    gpu_progress_bar = ProgressBar(2, 40, display)
    
    
    

    waiting = """Waiting for
data..."""
    display.OLED.fill(display.OLED.black)
    display.OLED.text(waiting, 2, 10, display.OLED.white)
    display.OLED.show()
    
    try:
        while True:
         
        # read a command from the host
            display.OLED.fill(display.OLED.black)
            
            v = sys.stdin.readline()
            splitted_v = v.split()

            cpu_temp.display_widget("CPU Temp:" + splitted_v[0])
            cpu_load.display_widget("CPU Load:" + splitted_v[1])
            gpu_temp.display_widget("GPU Temp:" + splitted_v[2])
            gpu_load.display_widget("GPU Load:" + splitted_v[3])
            
            cpu_progress_bar.calculate_bar(int(splitted_v[1]))
            gpu_progress_bar.calculate_bar(int(splitted_v[3]))
            
            
            
            display.OLED.show()
            
    except Exception as error:
        display.OLED.fill(display.OLED.black)
        display.OLED.text("Error", 2, 10, display.OLED.white)
        display.OLED.show()













