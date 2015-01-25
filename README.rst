myo_ardrone: Control AR Drone using Myo armband
===============================================

Dependencies
------------

- Myo SDK
- myo-python
- python-ardrone


Usage
-----

1. Calibrate the system
    a) Sync Myo with +X axis pointing towards elbow
    b) Align the system by making a Fist pose.
       This sets the base position used as a reference for yaw, pitch, roll rotations.
       An ideal base position would be Myo arm kept straight and parallel to the ground

2. Yaw arm left/right to move drone left/right.
   Yaw arm back to the set base position from left/right to make the drone hover at the last position

3. Pitch arm up/down to move drone up/down.
   Pitch arm back to the set base position from up/down to make the drone hover at the last position

4. Roll arm left/right to turn drone left/right.
   Roll arm back to the set base position from left/right to make the drone hover at the last position

5. Perform the Wave-out pose to move the drone forward.
   Perform the Wave-out again to make the drone hover at the last position.

6. Perform the Wave-in pose to move the drone backward. a
   perform the Wave-in again to make the drone hover at the last position.


License
-------

MIT License

http://www.opensource.org/licenses/mit-license.php