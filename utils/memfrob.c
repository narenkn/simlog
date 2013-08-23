
#include <stdio.h>
#include <string.h>

int
main(int argc, char *argv[])
{
	if (argc < 2)
		return 0;

	/* ENCRYPT */
	unsigned int ui1;
	unsigned int len = strlen(argv[1]);
//	printf("before:%s\n", argv[1]);
	memfrob(argv[1], len);
//	printf("after:%s\n", argv[1]);
	for (ui1=0; ui1<len; ui1++) {
		printf("\\%03o", argv[1][ui1]);
	}
	printf("\n");

#if 0
	/* DECRYPT */
	char str[128], *s1, *s2;
	unsigned int ui2;
	if (argc < 3)
		return 0;
	len = strlen(argv[2]);
	len >>= 2;
	for (ui1=0, s1=argv[2], s2=str; ui1<len; ui1++, s2++, s1+=3) {
		s1+=1;
		sscanf(s1, "%o", &ui2);
		s2[0] = ui2;
	}
	s2[0] = 0;
	printf("%s", str);
#endif

	return 0;
}
