
import libardrone

from myo.lowlevel import pose_t
from time import sleep

import myo_analytics

PI = 3.14
THRESHOLD_ANGLE = 1/9.0 * PI

motor_speed = 0.1
drone = libardrone.ARDrone()


class MainController(myo_analytics.Analytics):
    """
    +x direction towards elbow
    """

    def __init__(self):
        self.is_aligned = False
        self.is_synced = False
        self.yaw = myo_analytics.TaitBryanAngle(THRESHOLD_ANGLE)
        self.roll = myo_analytics.TaitBryanAngle(THRESHOLD_ANGLE)
        self.pitch = myo_analytics.TaitBryanAngle(THRESHOLD_ANGLE)
        self.left_right_control = FlightController(
                                                   THRESHOLD_ANGLE,
                                                   drone.move_right,
                                                   drone.move_left
                                                  )
        self.up_down_control = FlightController(
                                                   THRESHOLD_ANGLE,
                                                   drone.move_down,
                                                   drone.move_up
                                                  )

        self.turn_left_right_control = FlightController(
                                                   THRESHOLD_ANGLE,
                                                   drone.turn_left,
                                                   drone.turn_right
                                                  )
        self.forward_backward_control = FlightController(
                                                         None,
                                                         drone.move_forward,
                                                         drone.move_backward
                                                        )

    def on_sync(self):
        self.is_synced = True

    def on_unsync(self):
        self.is_synced = False

        drone.hover()

    def on_yaw(self, yaw):
        self.yaw.set_current_value(yaw)
        if self.is_calibrated():
            self.left_right_control.fly_at_angle(self.yaw)

    def on_pitch(self, pitch):
        self.pitch.set_current_value(pitch)
        if self.is_calibrated():
            self.up_down_control.fly_at_angle(self.pitch)

    def on_roll(self, roll):
        self.roll.set_current_value(roll)
        if self.is_calibrated():
            self.turn_left_right_control.fly_at_angle(self.roll)

    def on_pose(self, pose):
        print(pose)
        if pose == pose_t.fist:
            self.yaw.set_reference()
            drone.takeoff()

            self.is_aligned = True
            print("System calibrated, drone ready to fly using myo!")

        elif pose == pose_t.fingers_spread:
            emergency_mask = self.get_drone_emergency()
            self.is_aligned = False
            if emergency_mask == 0:
                print("Drone is landing")
                drone.land()
            else:
                print("Drone in emergency mode being reset")
                while emergency_mask == 1:
                    drone.reset()
                    sleep(2)
                    emergency_mask = self.get_drone_emergency()
            drone.trim()
            print("System needs to be realigned. Use Fist pose to realign and set base position")

        elif pose == pose_t.wave_out or pose == pose_t.wave_in:
            self.forward_backward_control.fly_straight(pose)

    def get_drone_emergency(self):
        return drone.navdata["drone_state"]["emergency_mask"]

    def is_calibrated(self):
        return self.is_aligned and self.is_synced


class FlightController():

    def __init__(self, threshold, action, opposite_action):
        self.threshold = threshold
        self.action = action
        self.opposite_action = opposite_action
        self.hover_toggle = False

    def fly_at_angle(self, tait_bryan_angle):
        delta = tait_bryan_angle.get_delta()
        if abs(delta) > self.threshold:
            if delta > 0:
                self._send_command(self.action)
            else:
                self._send_command(self.opposite_action)
            tait_bryan_angle.set_reference()

    def fly_straight(self, pose):
        if pose == pose_t.wave_out:
            self._send_command(self.action)
        elif pose == pose_t.wave_in:
            self._send_command(self.opposite_action)

    def _send_command(self, command):
        if self.hover_toggle:
            print("hover")
            drone.hover()
            self.hover_toggle = False
        else:
            print(command.__name__)
            command()
            self.hover_toggle = True

def run():
    print("Sync your Myo and make a Fist pose to calibrate the system")
    print("Position of the Fist pose determines the critical base position")
    drone.set_speed(motor_speed)
    MainController().start()


if __name__ == "__main__":
    run()
