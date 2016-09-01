import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

class ButtonSet:
    def __init__(self, px, mx, kx):
        self.buttonP = Button(px, '+')
        self.buttonM = Button(mx, '-')
        self.stVal = kx

        self.buttonP.on_clicked(self.button_handler_p)
        self.buttonM.on_clicked(self.button_handler_m)

    def button_handler_p(self, event):
        self.stVal += 0.1

    def button_handler_m(self, event):
        self.stVal -= 0.1


class PID_Cal:
    plt.ion()

    def __init__(self, startKp, startKi, startKd):
        self.bbox_props = dict(boxstyle="Square,pad=0.3", fc="white", ec="black", lw=1)
        x_w = 0.75 # Default element width

        self.output = 0
        self.testlim = 0
        self.timestep = 0

        # Set up figure and subplots
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0.125, 0.5, x_w, 0.375])
        self.points, = self.ax.plot([], [])
        #self.ax.set_ylim([0,12])
        self.ax.set_ylim([32,90])
        plt.title("Taris PID Calibration Tool")

        # PID plotting

        self.pred = self.fig.add_axes([0.125, 0.24, 0.75, 0.2])
        self.pid_points, = self.pred.plot([], [])
        self.pred.set_ylim(0,100)

        # Gain values for PID
        self.Ki = startKi
        self.Kd = startKd
        self.Kp = startKp

        # Additional parameters
        self.ref = self.fig.add_axes([0.125, 0.05, 0.1, 0.1])
        self.updateText()
        self.ref.axis('off')

        self.key = self.fig.add_axes([1, 1, 0.1, 0.1])
        keystring = "Set Kp until system oscillates.\nSet Kd to attenuate.\nRepeat until Kd no longer quiets system.\nSet Ki to attenuate."
        self.ref.text(3, 0.1, keystring,
        horizontalalignment='left',
        verticalalignment='bottom',
        bbox=self.bbox_props)
        self.key.axis('off')

        # Integral Buttons
        isl_px = self.fig.add_axes([0.25, 0.07, 0.045, 0.03])
        isl_mx = self.fig.add_axes([0.3, 0.07, 0.045, 0.03])
        self.isl_buttons = ButtonSet(isl_px, isl_mx, self.Ki)

        # Proportional Buttons
        psl_px = self.fig.add_axes([0.25, 0.11, 0.045, 0.03])
        psl_mx = self.fig.add_axes([0.3, 0.11, 0.045, 0.03])
        self.psl_buttons = ButtonSet(psl_px, psl_mx, self.Kp)

        # Derivative Buttons
        dsl_px = self.fig.add_axes([0.25, 0.15, 0.045, 0.03])
        dsl_mx = self.fig.add_axes([0.3, 0.15, 0.045, 0.03])
        self.dsl_buttons = ButtonSet(dsl_px, dsl_mx, self.Kd)

    def addPoint(self, timeVal, yVal):
        '''Add a point to the scrolling plot'''
        self.points.set_xdata(np.append(self.points.get_xdata(), timeVal))
        self.points.set_ydata(np.append(self.points.get_ydata(), yVal))
        self.ax.autoscale_view(scalex=True,scaley=True)
        self.ax.relim()
        self.updateText()
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def getKx(self):
        return round(self.isl_buttons.stVal, 2), round(self.psl_buttons.stVal, 2), round(self.dsl_buttons.stVal, 2)

    def updateText(self):
        newStr= "Kd: " + str(self.Kd) + "\nKp: " + str(self.Kp) + "\nKi: " + str(self.Ki)
        self.ref.text(0.25, 0.25 , newStr,
        horizontalalignment='left',
        verticalalignment='bottom',
        bbox=self.bbox_props)


    def plotSystemTime(self, cv, t):

        self.output = cv
        self.pid_points.set_xdata(np.append(self.pid_points.get_xdata(), t))
        self.pid_points.set_ydata(np.append(self.pid_points.get_ydata(), self.output))
        self.pred.autoscale_view(scalex=True,scaley=False)
        self.pred.relim()
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
    

    def runCal(self):
        plt.show()
        print("Running calibration tool...")
        time.sleep(1)
        self.timestep = 0
             
    def updateCal(self, current_value, pwm_value):
        print("Adding point: " + str(current_value))
        self.addPoint(self.timestep, current_value)
        self.Ki, self.Kp, self.Kd = self.getKx()
        self.plotSystemTime(pwm_value*100, self.timestep)
        self.timestep +=1
        return self.Kp, self.Ki, self.Kd
                
