#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

// Initialized data (data segment)
int global_init = 42;
char global_str[] = "hello from data";

// Uninitialized data (BSS)
int global_bss;
static int static_bss;

void recurse(int depth) {
    int local = depth;
    if (depth < 5) {
        printf("  stack frame depth %d: %p (local=%d)\n", depth, (void *)&local, local);
        recurse(depth + 1);
    }
}

int main(int argc, char *argv[], char *envp[]) {
    printf("=== Process Memory Layout Explorer ===\n\n");

    printf("CODE / TEXT SEGMENT:\n");
    printf("  main()           : %p\n", (void *)main);
    printf("  recurse()        : %p\n", (void *)recurse);
    printf("  printf() (libc)  : %p\n", (void *)printf);

    printf("\nDATA SEGMENT (initialized):\n");
    printf("  global_init      : %p  = %d\n", (void *)&global_init, global_init);
    printf("  global_str       : %p  = \"%s\"\n", (void *)global_str, global_str);

    printf("\nBSS SEGMENT (zero-initialized):\n");
    printf("  global_bss       : %p  = %d\n", (void *)&global_bss, global_bss);
    printf("  static_bss       : %p  = %d\n", (void *)&static_bss, static_bss);

    printf("\nHEAP:\n");
    void *h1 = malloc(16);
    void *h2 = malloc(1024);
    void *h3 = malloc(1);
    printf("  malloc(16)       : %p\n", h1);
    printf("  malloc(1024)     : %p\n", h2);
    printf("  malloc(1)        : %p\n", h3);
    printf("  → heap grows upward\n");

    int local_var = 99;
    char local_arr[32];
    printf("\nSTACK:\n");
    printf("  local_var        : %p  = %d\n", (void *)&local_var, local_var);
    printf("  local_arr        : %p\n", (void *)local_arr);
    printf("  &argc            : %p\n", (void *)&argc);
    printf("  argv pointer     : %p\n", (void *)argv);
    printf("  envp pointer     : %p\n", (void *)envp);

    printf("\n  Stack growth (downward) via recursion:\n");
    recurse(0);

    printf("\nARGV / ENVIRONMENT (usually above the stack):\n");
    printf("  argv[0] string   : %p  (\"%s\")\n", (void *)argv[0], argv[0]);
    if (envp[0])
        printf("  envp[0]          : %p  (\"%.50s…\")\n", (void *)envp[0], envp[0]);

    printf("\nTypical order (low → high addresses):\n");
    printf("  Text < Data < BSS < Heap  ……  Stack < argv/env strings\n");
    printf("  (bases randomized by ASLR/PIE on every run)\n");

    free(h1); free(h2); free(h3);
    return 0;
}