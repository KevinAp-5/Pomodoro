all: change_name add_exe_permission make_command send_music

change_name:
	mv pomodoro.py pomodoro
add_exe_permission:
	chmod +x pomodoro
make_command:
	sudo cp pomodoro /usr/local/bin/

send_music:
	sudo cp sound.mp3 /usr/local/bin/

