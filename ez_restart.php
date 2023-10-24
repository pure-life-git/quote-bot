<?php 
    `pid=$(head -n 1 pid.txt)`;
    `kill -INT $pid`;
    `git pull`;
    `python3 bot.py`;
?>