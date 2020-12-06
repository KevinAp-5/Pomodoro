all: send_music send_file change_name add_exe_permission

change_name:
	sudo mv /usr/local/bin/pomodoro.py /usr/local/bin/pomodoro
add_exe_permission:
	sudo chmod +x /usr/local/bin/pomodoro
send_file:
	sudo cp pomodoro.py /usr/local/bin/
send_music:
	sudo cp sound.mp3 /usr/local/bin/

