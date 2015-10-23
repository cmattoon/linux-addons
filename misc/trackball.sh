#!/bin/bash
DEVICE="Logitech USB Trackball"
PRESENT=$(xinput | grep "${DEVICE}")
SET_PROP="xinput set-int-prop"

if [ ! -z "${PRESENT}" ]; then
    xinput set-button-map "${DEVICE}" 1 2 3 4 5 6 7 8 9
    $SET_PROP "${DEVICE}" "Evdev Wheel Emulation Button" 8 8
    $SET_PROP "${DEVICE}" "Evdev Wheel Emulation" 8 1
    $SET_PROP "${DEVICE}" "Evdev Wheel Emulation Axes" 8 6 7 4 5
    $SET_PROP "${DEVICE}" "Evdev Wheel Emulation X Axis" 8 6
    $SET_PROP "${DEVICE}" "Evdev Drag Lock Buttons" 8 9
fi