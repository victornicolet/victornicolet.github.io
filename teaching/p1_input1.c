int input1_simple_loop()
{
  int n = 10;
  int i, sum = 0;
  for ( i = 1; i <= 10; i++ ) {
    sum += i;
  }

  return sum;
}

/*
   Read variables: sum, i
   Write: sum, i
   Reaching defs: n = 10, i = 0, sum = 0
   Live variables: sum.
   Index: i
   No dependency
 */
