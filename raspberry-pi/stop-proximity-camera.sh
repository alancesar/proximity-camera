PROXIMITY_CAMERA=$(pgrep -f proximity-camera.py)
if [ -z "$PROXIMITY_CAMERA" ]; then
  echo "Camera is not running..."
else
  kill -9 "$PROXIMITY_CAMERA"
fi
