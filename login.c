#include <stdio.h>
#include <string.h>

#define debug_report(progname, fmt, ...) printf("%s: " fmt "\n", progname, ##__VA_ARGS__)

char g_flag[100];

int main(int argc, char **argv) {
  /* Input password */
  char password[100];
  printf("Password: ");
  scanf("%[^\n]", password);

  /* Check password */
  if (strcmp(password, g_flag)) {
    debug_report(argv[0], "Auth NG");
    debug_report(argv[0], "Invalid password: %s", password);

  } else {
    debug_report(argv[0], "Auth OK");
    debug_report(argv[0], "FLAG: %s", g_flag);
  }
  
  return 0;
}

__attribute__((constructor))
void setup() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  /* Read the flag into `g_flag` */
  FILE *fp = fopen("/flag.txt", "r");
  if (!fp) {
    strcpy(g_flag, "FLAG{dummy}");
  } else {
    fread(g_flag, 1, sizeof(g_flag), fp);
    fclose(fp);
    /* Remove newline */
    g_flag[strcspn(g_flag, "\n")] = '\0';
  }
}
