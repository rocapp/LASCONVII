#include <stdio.h>

int main()
{
  int nr_steps = 1000;
  double dt = 0.001;
  double t[nr_steps];
  int i;
  for (i=0;i<nr_steps;i++){
    t[i] = (double) i*dt;
  }
  double v[nr_steps];
  v[0] = 0.0;
  for(i=1;i<nr_steps;i++){
    v[i] = 0.0;
  }
  double tau = 0.1;
  double I = 2.0;
  double thresh = 1.0;
  double reset = -1.0;
  for (i=0;i<nr_steps;i++){
    double dv_dt = -(v[i]-I)/tau;
    double vv = v[i] + dv_dt*dt;
    if (vv > thresh){
      v[i+1] = reset;
    }
    else {
      v[i+1] = vv;
    }
  }
  for(i=0;i<nr_steps;i++){
    printf("t = %f, v = %f\n", t[i], v[i]);
  }
  return 0;
}
