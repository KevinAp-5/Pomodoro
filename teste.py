import sys
from time import sleep

for x in range(10):
    sys.stdout.write(f'\rcomendo cu de {x} curioso')
    sys.stdout.flush()
    sleep(0.5)
print()

