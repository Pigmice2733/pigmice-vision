:
cd ~/pigmice-vision

if ifconfig | grep 10.27.33.20:
then
  python robot_vision.py 2>&1. > /home/pi/robot_vision_output.txt
  # This will save all the error messages into the output file.
  # To view these errors cat into the file (cat robot_vision_output.txt)
else
  python robot_vision.py --config ~/.pigmice-config-dev.yaml
fi
