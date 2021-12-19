'''
节拍器
creation date: 2021/12/12
'''

import tkinter
from tkinter import messagebox, ttk
import winsound
import threading
import time

#def resize(ev=None):
#    label.config(font='Helverica -%d bold' % scale.get())


# 用于中止翻放线程的变量
is_stop = True

def sleep_mills(mills: int):
    ''' 精确的计算器，以毫秒为单位 '''
    start = time.perf_counter_ns()
    ns = mills * (10 ** 6)
    while time.perf_counter_ns() - start < ns:
        pass

# 开始播放
def start_play():
    # 获取输入的值
    meteronome_num = metronome_str.get()
    if not meteronome_num: 
        messagebox.showwarning('警告', '请输入节拍数')
        return
    # 每分钟的拍数
    meteronome_num = int(meteronome_num)
    if meteronome_num < 1:
        meteronome_num = 1

    metronome_entry.config(state = tkinter.DISABLED)
    count_down_entry.config(state = tkinter.DISABLED)
    start_btn.config(state = tkinter.DISABLED)
    stop_btn.config(state = tkinter.NORMAL)

    # 获取倒计时
    count_down_num = count_down_minutes.get()
    if not count_down_num:
        messagebox.showwaring('警告', '请输入倒计时分钟数')
        return
    count_down_num = int(count_down_num)
    if count_down_num < 1:
        count_down_num = 1
    

    print('输入的节拍数值为', meteronome_num)

    # 用于线程中：播放节拍 
    def bk_play():
        # beep 一声的时长（ms)
        beep_duration = 50
        if meteronome_num <= 120:
            beep_duration = 80

        # 每发出一声之间的间隔 # python 的休眠不是很精确
        sleep_duration = ((60000 - meteronome_num * beep_duration) // meteronome_num) / 1000
        print(f'每发出一声之间的间隔(s):{sleep_duration:.3f} ')

        global is_stop
        is_stop = False
        while not is_stop: 
            winsound.Beep(2000, beep_duration)
            # print('.', is_stop, time.ctime())
            time.sleep(sleep_duration)
            # sleep_mills(sleep_duration)

    # 用于线程中, 倒计时
    def count_down_play(count_down_num):
        # 转为时：分：秒
        count_down_num *= 60 # 转为秒
        count_down_display.set(...)
        global is_stop
        while not is_stop and count_down_num > 0:
            text = ''
            hour = count_down_num // 3600
            miute = (count_down_num - hour * 3600) // 60
            second = count_down_num % 60
            if hour:
                text = f'{hour:02d}:'
            text += f'{miute:02d}:{second:02d}'
            count_down_display.set(text)

            time.sleep(1)
            count_down_num -= 1
        # 停止
        stop_play()
        count_down_display.set('')

    bk_thread = threading.Thread(target=bk_play)
    bk_thread.daemon = True
    bk_thread.start()

    count_down_thread = threading.Thread(target=count_down_play, args=(count_down_num, ))
    count_down_thread.daemon = True
    count_down_thread.start()


    
# 停止播放
def stop_play():
    global is_stop
    is_stop = True
    metronome_entry.config(state = tkinter.NORMAL)
    count_down_entry.config(state = tkinter.NORMAL)
    start_btn.config(state = tkinter.NORMAL)
    stop_btn.config(state = tkinter.DISABLED)

    
def valid_only_num_metronome(context):
    ''' 只能是 1 至 3位长的数字, 并只能小于等于300'''
    if not context:
        return True

    if context.isdigit() and int(context) <= 300: 
        return True
    return False

def valid_only_num_count_down(context):
    ''' 只能是 1 至 3位长的数字'''
    if not context:
        return True

    if context.isdigit() and int(context) <= 999: 
        return True
    return False


# 创建顶层窗口
top = tkinter.Tk()
top.style = ttk.Style()
top.style.theme_use('xpnative')

layout_row = 1

top.title('节拍器') 
top.geometry('250x150')
label = ttk.Label(top, text='节拍器', font='Helvetica -12 bold', justify='center')
label.grid(row=layout_row, column=1, columnspan=2)
### 让 packer 来管理和显示控件件
#label.pack(fill=tkinter.Y, expand=1)

# scale = tkinter.Scale(top, from_=10, to=40,
#         orient=tkinter.HORIZONTAL, command=resize)
# scale.set(12)
# scale.pack(fill=tkinter.X, expand=1)

# -- 每分钟节拍数 ---
layout_row += 1
ttk.Label(top, text='每分钟节拍数：').grid(row=layout_row, column=1, stick=tkinter.E)
# pack(fill=tkinter.Y, expand=1)
#   输入框中的内容
metronome_str = tkinter.StringVar(top, value='60')

metronome_entry = ttk.Entry(top, text='每分钟节拍数：', 
        textvariable=metronome_str,
        # 发生任何变化，则调用 validatecommand
        validate='key',
        # %P 代表输入框的实时内容
        validatecommand=(top.register(valid_only_num_metronome) , '%P') 
        )
metronome_entry.grid(row=layout_row, column=2, stick=tkinter.N+tkinter.E+tkinter.W)
# pack()

# -- 倒计时 ---
layout_row += 1
ttk.Label(top, text='倒计时(分钟):').grid(row=layout_row, column=1, stick=tkinter.E)
#      输入的倒计时分钟数
count_down_minutes = tkinter.StringVar(top, value='10')
count_down_entry = ttk.Entry(top, text='倒计时器分钟数:',
        textvariable=count_down_minutes,
        validate='key',
        # %P 代表输入框的实时内容
        validatecommand=(top.register(valid_only_num_count_down) , '%P') 
        )
count_down_entry.grid(row=layout_row, column=2, stick=tkinter.N+tkinter.E+tkinter.W)

# 显示时、分、秒
layout_row += 1
count_down_display = tkinter.StringVar(top)
ttk.Entry(top, 
        textvariable=count_down_display, 
        state=tkinter.DISABLED,
        justify='center').grid(row=layout_row, column=1, columnspan=2, stick=tkinter.N+tkinter.E+tkinter.W) 



# 开始播放按钮
layout_row += 1
start_btn = ttk.Button(top, text='开始播放',
        command=start_play)
# start_btn.pack(fill=tkinter.X, expand=1)
start_btn.grid(row=layout_row, column=1, stick=tkinter.N+tkinter.E+tkinter.W)

# 结束播放按钮
stop_btn = ttk.Button(top, text='停止播放',
        state=tkinter.DISABLED,
        command=stop_play)
# stop_btn.pack(fill=tkinter.X, expand=1)
stop_btn.grid(row=layout_row, column=2, stick=tkinter.N+tkinter.E+tkinter.W)

# 退出按钮
layout_row += 1
quit = ttk.Button(top, text='退出',
        command=top.quit, 
        #activeforeground='white',
        #activebackground='red')
        )
# quit.pack(fill=tkinter.X, expand=1)
# quit.pack()
quit.grid(row=layout_row, column=1, columnspan=2, stick=tkinter.N+tkinter.E+tkinter.W)


# 运行这个 GUI 应用
tkinter.mainloop()

