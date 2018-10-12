import RPi.GPIO as GPIO
import time
class Steper:
    en = 12
    a1_pin = 17 #A
    a2_pin = 27 #B
    b1_pin = 23 #/A
    b2_pin = 24 #/B

    forward_seq = ['1100', '0110', '0011', '1001']
    reverse_seq = ['1001', '0011', '0110', '1100']
    ###                ###
    #   測試單元計數用變數  #
    ###                ###

    # test_count = [0,0,0,0]

    ###                     ###
    #   測試單元計數用變數結束    #
    ###                     ###

    def __init__(self):
        GPIO.setmode(GPIO.BCM) # BCM
        GPIO.setup(en, GPIO.OUT)
        GPIO.setup(a1_pin, GPIO.OUT)
        GPIO.setup(a2_pin, GPIO.OUT)
        GPIO.setup(b1_pin, GPIO.OUT)
        GPIO.setup(b2_pin, GPIO.OUT)
        GPIO.output(en, GPIO.HIGH)

    def release():
        GPIO.cleanup()

    def set_step(step):

        GPIO.output(a1_pin, step[0] == '1')
        GPIO.output(a2_pin, step[1] == '1')
        GPIO.output(b1_pin, step[2] == '1')
        GPIO.output(b2_pin, step[3] == '1')

        ###                                 ###
        #   以下為拿來測試總和的步數是否符合預期    #
        #   要測試記得變數也要去除註解!           #
        ###                                 ###

        # for i in range(4):
        #     if step == self.forward_seq[i]:
        #         self.test_count[i] += 1
        # 
    # def test_step_info(self):
    #     sum = 0
    #     for i in range(len(self.count)):
    #         sum += self.count[i]

    #     print("forward_seq " , self.forward_seq , end="\n")
    #     print(self.count, end="\n")
    #     print("總共走 ", sum , " 步")

        ###         ###
        #   測試碼結束  #
        ###         ###
    
    
    

    


    def NonlinearSpeed(self, steps):
        """geometric progression (200 steps = Make a turn)"""
        
        NonlinearStep = 4 #公比
        multiple = 1
        StartDelay = int(32 * multiple) # 4的倍數 An
        EndDelay = int(8 * multiple)    # 4的倍數 A1
        n = (StartDelay - EndDelay)/NonlinearStep + 1
        keepStep = (steps) / 4 - n * 2
        isNonlinear = keepStep > 0

        # print("n : " , n)
        # print("keepStep : ",keepStep)

        if isNonlinear:
            # Start to accelerate
            for delay in range(StartDelay,EndDelay-1,-(NonlinearStep)):
                self.forward_single(delay/(1000 * multiple))
                # print("Start : ", delay)
                pass
            # Stable speed
            self.forward(EndDelay/1000,int(keepStep))
            
            # Slow down
            for delay in range(EndDelay,StartDelay+1,NonlinearStep):
                self.forward_single(delay/(1000 * multiple))
                # print("End : ", delay)
                pass
        else:
            self.forward(EndDelay/1000,int(steps))
        
        if steps % NonlinearStep != 0:
            self.forward_single(StartDelay/1000,step_seq=steps % NonlinearStep)
            pass
    def forward(self, delay, steps, seq = forward_seq):
        self._ward(delay = delay,seq = seq, steps= steps)
    def backwards(self, delay, steps, seq = reverse_seq):
        self._ward(delay,seq,steps=steps)
    def forward_single(self, delay, seq = forward_seq, step_seq=4):
        self._ward(delay=delay,seq=seq,step_seq=step_seq)
    def backwards_single(self, delay, seq = reverse_seq, step_seq=4):
        self._ward(delay=delay,seq=seq,step_seq=step_seq)
    def _ward(self, delay, seq, steps=1, step_seq=4):
        # if step > 1:4
        #     print("delay ",delay)
        #     print("seq",seq)
        #     print("step",step)
        #     print("step_seq",step_seq)
        if steps > 1:
            i = 0
            while i < steps:
                i += 1
                for step in seq:
                    self.set_step(step)
                    # print(delay)
                    time.sleep(delay)
        else:
            if step_seq == 4:
                for step in seq:
                    self.set_step(step)
                    time.sleep(delay)
                    # print(delay)
            else:
                for i in range(step_seq):
                    self.set_step(seq[i])
                    time.sleep(delay)