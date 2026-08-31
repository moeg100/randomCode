#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>

int main(int argc, char *argv[])
{
    printf("--- Master Process Starting (pid: %d) ---\n\n", (int) getpid());

    // Create a pipe for inter-process communication (IPC)
    // pipefd[0] is the read end, pipefd[1] is the write end
    int pipefd[2];
    if (pipe(pipefd) == -1) {
        perror("pipe failed");
        exit(1);
    }

    int rc = fork();
    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        exit(1);
    } 
    else if (rc == 0) {
        // --- CHILD PATH ---
        printf("[Child (pid: %d)]: Sending secret message to parent...\n", (int) getpid());
        
        // Close unused read end of the pipe
        close(pipefd[0]); 
        
        char msg[] = "Hello from the underground!";
        write(pipefd[1], msg, strlen(msg) + 1);
        close(pipefd[1]); // Done writing

        printf("[Child]: Replacing myself with the 'ls -l' command now...\n\n");
        
        // Define the arguments for the external command
        // ls -l lists files in the current directory in long format
        char *args[] = {"ls", "-l", NULL}; 
        
        // execvp replaces the current child process image with 'ls'
        // If successful, the code below this line will NEVER execute
        execvp(args[0], args); 
        
        // This only runs if execvp fails
        perror("execvp failed");
        exit(1);
    } 
    else {
        // --- PARENT PATH ---
        // Close unused write end of the pipe
        close(pipefd[1]); 

        char buffer[100];
        // Read the message sent by the child through the pipe
        read(pipefd[0], buffer, sizeof(buffer));
        close(pipefd[0]); // Done reading

        printf("[Parent (pid: %d)]: Received message from child: \"%s\"\n", (int) getpid(), buffer);
        printf("[Parent]: Waiting for child to finish executing its external command...\n\n");

        int status;
        int wc = wait(&status); // Wait for child and harvest its exit status

        printf("\n[Parent]: Child %d has terminated (wc: %d).\n", rc, wc);
        
        // Check how the child exited
        if (WIFEXITED(status)) {
            printf("[Parent]: Child exited normally with code %d.\n", WEXITSTATUS(status));
        }
    }

    return 0;
}
