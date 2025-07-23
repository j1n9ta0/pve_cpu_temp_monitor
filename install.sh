#!/bin/bash

remove_app() {

    systemctl disable --now cpu-temp-monitor
    rm -rf /usr/lib/systemd/system/cpu-temp-monitor.service
    rm -rf /usr/local/bin/cpu-temp-monitor.py
    rm -rf /usr/local/etc/cpu-temp-monitor.conf
    systemctl daemon-reload

}

install_app() {

    cp -a cpu-temp-monitor.py /usr/local/bin
    cp -a cpu-temp-monitor.conf /usr/local/etc
    cp -a cpu-temp-monitor.service /usr/lib/systemd/system
    systemctl daemon-reload
    systemctl enable --now cpu-temp-monitor
    systemctl status cpu-temp-monitor

}

remove_app
install_app

