BEGIN {
  FS = "."
}
{
  if (NF == 3) {
    if ($3 ~ /-/) {
      split($3,a,"-")
      # if a tag with revision is on current head it'll be 2 elements long:
      # 1.1.1-2
      # if a tag with revision is on an earlier commit it'll be 4 elements long:
      # 1.1.1-2-1-accee835
      if (length(a) == 2 || length(a) == 4) {
        sum = a[2] + 1;
        printf "%s.%s.%s-%s", $1, $2, a[1], sum
      # if a tag without revision is on an earlier commit it'll be 3 elements long:
      # 1.1.1-1-accee835
      } else if (length(a) == 3) {
        printf "%s.%s.%s-%s", $1, $2, a[1], 1
      }
    } else {
      printf "%s.%s.%s-1", $1, $2, $3
    }
  }
}
