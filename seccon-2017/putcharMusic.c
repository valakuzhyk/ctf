//#include <math.h>

main(t,i,j){unsigned char p[]="###<f_YM\204g_YM\204g_Y_H #<f_YM\204g_YM\204g_Y_H #+-?[WKAMYJ/7 #+-?[WKgH #+-?[WKAMYJ/7hk\206\203tk\\YJAfkkk";for(i=0;t=1;i=(i+1)%(sizeof(p)-1)){double x=pow(1.05946309435931,p[i]/6+13);for(j=1+p[i]%6;t++%(8192/j);)putchar(t>>5|(int)(t*x));}}

/*main(t,i,j){
  unsigned char p[]="###<f_YM\204g_YM\204g_Y_H #<f_YM\204g_YM\204g_Y_H #+-?[WKAMYJ/7 #+-?[WKgH #+-?[WKAMYJ/7hk\206\203tk\\YJAfkkk";
  for(i=0;t=1;i=(i+1)%(sizeof(p)-1)){
    double x=pow(1.05946309435931,p[i]/6+13);
    for(j=1+p[i]%6;t++%(8192/j);) {
      putchar(t>>5|(int)(t*x));
    }
  }
}*/
