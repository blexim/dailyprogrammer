#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <pthread.h>

#define max(a, b) (((a) > (b)) ? (a) : (b))

#define THREADS 16

int l;
int r;
int n;
int trials;

int walk(int l, int r, int steps) {
  int loc = 0;
  int lim = 0;

  for (int i = 0; i < steps; i++) {
    int x = rand();

    if (x <= l) {
      loc--;
    } else if (x <= r) {
      loc++;
    }

    lim = max(lim, loc);
  }

  return lim;
}

void *walks(void *p) {
  int id = (int) p;
  int sum = 0;

  for (int i = 0; i < trials; i++) {
    sum += walk(l, r, n);
  }

  return (void *) sum;
}

int main(int argc, char *argv[]) {
  int sum;
  double lf, rf, avg;
  pthread_t threads[THREADS];

  srand(time(NULL));

  lf = atof(argv[1]);
  rf = atof(argv[2]);
  n = atoi(argv[3]);
  trials = atoi(argv[4]);

  l = lf * RAND_MAX;
  r = l + (rf * RAND_MAX);

  for (int i = 0; i < THREADS; i++) {
    pthread_create(&threads[i], NULL, walks, (void *) i);
  }

  sum = 0;

  for (int i = 0; i < THREADS; i++) {
    void *v;

    pthread_join(threads[i], &v);

    sum += (int) v;
  }

  avg = sum / ((double) (trials*THREADS));

  printf("%f\n", avg);
}
