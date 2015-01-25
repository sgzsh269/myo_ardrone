
import myo
import math

PI = 3.14

class _Listener(myo.DeviceListener):

    def __init__(self, analytics, *args, **kwargs):
        super(_Listener, self).__init__(*args, **kwargs)
        self.analytics = analytics

    def on_connect(self, myo, timestamp):
        print("Myo connected")
        myo.vibrate("short")

    def on_sync(self, myo, timestamp, arm, x_direction):
        print("Myo worn on {0}, with x-axis {1}".format(arm, x_direction))
        self.analytics.on_sync()

    def on_unsync(self, myo, timestamp):
        print("Myo unsynced")
        self.analytics.on_unsync()

    def on_orientation_data(self, myo, timestamp, orientation):
        x = orientation[0]
        y = orientation[1]
        z = orientation[2]
        w = orientation[3]
        tait_bryan = quaternions_to_TaitBryan(x, y, z, w)
        yaw = tait_bryan[0]
        pitch = tait_bryan[1]
        roll = tait_bryan[2]
        self.analytics.on_yaw(yaw)
        self.analytics.on_pitch(pitch)
        self.analytics.on_roll(roll)

    def on_pose(self, myo, timestamp, pose):
        self.analytics.on_pose(pose)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        x = acceleration[0]
        y = acceleration[1]
        z = acceleration[2]
        r = math.sqrt(x**2 + y**2 + z**2)
        self.analytics.on_acceleration(r)


class Analytics():

    def on_sync(self):
        pass

    def on_unsync(self):
        pass

    def on_yaw(self, yaw):
        pass

    def on_roll(self, roll):
        pass

    def on_pitch(self, pitch):
        pass

    def on_pose(self, pose):
        pass

    def on_acceleration(self, acceleration):
        pass

    def start(self):
        myo.init()
        hub = myo.Hub()
        hub.set_locking_policy(myo.locking_policy.none)
        hub.run(1000, _Listener(self))


def quaternions_to_TaitBryan(x, y, z, w):

    yaw = -math.atan2(2*(x*y + z*w), x*x - y*y - z*z + w*w)
    pitch = -math.asin(-2*x*z + 2*y*w)
    roll = math.atan2(2*(y*z + x*w), -x*x - y*y + z*z + w*w)

    if abs(pitch) > 1/2.0 * PI:
        if pitch > 0:
            pitch = 1/2.0 * PI
        else:
            pitch = -1/2.0 * PI

    return (yaw, pitch, roll)


class TaitBryanAngle():

    def __init__(self, threshold):
        self.reference = 0.0
        self.threshold = threshold
        self.current_angle = 0.0

    def set_current_value(self, angle):
        self.current_angle = angle

    def set_reference(self):
        if self.current_angle != 0.0:
            self.reference = self.current_angle

    def get_delta(self):
        return self.current_angle - self.reference



