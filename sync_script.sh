#!/bin/bash
cd ~/workspace/projects/domobot
git pull && git add -A && git commit -a -m "desktop commit: `date +'%Y-%m-%d %H-%M-%S'`" && git push

