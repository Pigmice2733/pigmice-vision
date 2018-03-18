:
cd ~/pigmice-vision

if ifconfig | grep 10.27.33.20:
then
  python robot_vision.py
else
  python robot_vision.py --config ~/.pigmice-config-dev.yaml
fi
