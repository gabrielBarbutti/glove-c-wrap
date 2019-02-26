#include <stdio.h>
#include "../GloVe/src/shuffle.c"

int shuffle_wrap(int argc, char **argv){
  int func_ret;
  FILE *old_stdin = stdin;
  FILE *old_stdout = stdout;

  stdin = fopen(argv[1], "r");
  freopen(argv[2], "w", stdout);

  func_ret = shuffle_main(argc, argv);

  fclose(stdin);
  fclose(stdout);
  stdin = old_stdin;
  stdout = old_stdout;
  return func_ret;
}
