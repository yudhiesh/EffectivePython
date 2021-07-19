import os
import sys
import time
import subprocess

# Use subprocess to Manage Child Processes

# result = subprocess.run(
#    ["echo", "Hello from the child!"], capture_output=True, encoding="utf-8"
# )
# result.check_returncode()  # No exception means clean exit
# print(result.stdout)

## Decoupling the child process from the parent frees up the parent process to
## run many child processes in parallel. Here I do this by starting all the child
## processes together with Popen upfront
# start = time.time()
# sleep_procs = []
# for _ in range(10):
#    proc = subprocess.Popen(["sleep", "1"])
#    sleep_procs.append(proc)

##
# for proc in sleep_procs:
#    proc.communicate()

# end = time.time()
# delta = end - start
## Takes about 1.05 seconds to perform all the 10 tasks concurrently
# print(f"Process took: {delta:.3} seconds")

## If these processes ran in a sequential manner then the total delay would be
## 10+ seconds rather than ~1 second

## You can also pipe data from a Python program into a subprocess and retrieve
## its output.


def run_encrypt(data):
    """
    Use the openssl command-line tool to encrypt some data.
    This function starts the child process with CLI arguments and I/O pipes
    """
    env = os.environ.copy()

    env["password"] = "zhsklsdfjw4e2888jsda/sfshnssd/m/KJ)2329#"
    proc = subprocess.Popen(
        ["openssl", "enc", "-des3", "-pass", "env:password"],
        env=env,
        stdin=subprocess.PIPE,  # Allow sending of data to process's stdin
        stdout=subprocess.PIPE,  # To retrieve the result instead of None
    )
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure that the child gets the input
    return proc


# procs = []
# for _ in range(3):
#    data = os.urandom(10)
#    proc = run_encrypt(data)
#    procs.append(proc)

# for proc in procs:
#    out, _ = proc.communicate()
#    print("Out: ", out)


def run_hash(input_stdin):
    """
    Start the openssl CLI tool as a subprocess to generate a Whirpool hash of
    the input stream

    Args:
        input_stdin -> Earlier subprocess that passes input to this process
    """
    return subprocess.Popen(
        ["openssl", "dgst", "-whirlpool", "-binary"],
        stdin=input_stdin,
        stdout=subprocess.PIPE,
    )


def sleep_pipe(input_stdin):
    return subprocess.Popen(["sleep", "1"], stdin=input_stdin, stdout=subprocess.PIPE)


# Now, one set of processes is used to encrypt some data and another set of
# processes is used to hash their encrypted output.

encrypt_procs = []
hash_procs = []
sleep_procs = []

start = time.time()
for _ in range(3):
    data = os.urandom(100)
    # Encrypt the data first
    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    sleep_proc = sleep_pipe(encrypt_proc.stdout)
    sleep_procs.append(sleep_proc)

    # Pass the encrypted data stream to run_hash()
    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    # Ensures that the child consumes the input stream and the communicate()
    # method doesn't inadvertently steal input from the child
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None

    sleep_proc.stdout.close()
    sleep_proc.stdout = None


for proc in encrypt_procs:
    try:
        proc.communicate(timeout=0.1)
        assert proc.returncode == 0
    except subprocess.TimeoutExpired:
        print("Exit status", proc.poll())
        proc.terminate()
        proc.wait()
        sys.exit(1)

for proc in sleep_procs:
    try:
        # timeout of 0.1 should cause the entire process to end if the sleep is
        # longer than 0.1
        proc.communicate(timeout=2)
        assert proc.returncode == 0
    except subprocess.TimeoutExpired:
        print("Exit status", proc.poll())
        proc.terminate()
        proc.wait()
        sys.exit(1)

for proc in hash_procs:
    try:
        out, _ = proc.communicate(timeout=0.1)
        print(out[-10:])
        assert proc.returncode == 0
    except subprocess.TimeoutExpired:
        print("Exit status", proc.poll())
        proc.terminate()
        proc.wait()
        sys.exit(1)

end = time.time()
delta = end - start
print(f"Took {delta:.3} seconds")
