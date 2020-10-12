all: change_name add_exe_permission make_command

change_name:
	mv pomodoro.py pomodoro
add_exe_permission:
	chmod +x pomodoro
make_command:
	sudo cp pomodoro /usr/local/bin/

