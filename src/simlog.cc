#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <string>

#define  LOCAL_ENCRYPT(STR) do { \
    char *p = (char *) STR; \
		uint32 size = strlen(p); \
    for (uint32 ui1=0; ui1<size; ui1++) \
        *p++ ^= 42; \
} while (0)
#define  LOCAL_DECRYPT(STR) LOCAL_ENCRYPT(STR)
#define  LOCAL_FNAME "simlog.exml"

using namespace std;

class SimLog {
public:
	SimLog();
	~SimLog();
	time_t t_start, t_end;
	void get_send_data(stringstream &data);
};

SimLog::SimLog()
{
	time(&t_start);
}

#define MEMFROB_DEC2BUF(b, STR) do { \
	strcpy(b, STR); \
	LOCAL_DECRYPT(b); \
} while (0)

SimLog::~SimLog()
{
	int sock;
	struct sockaddr_in server_addr;
	struct hostent *host;
	stringstream send_data;

	/* Check env(SIMLOG_RUNLOG) */
	char buf[64];
	MEMFROB_DEC2BUF(buf, "\171\143\147\146\145\155\165\170\177\144\146\145\155");
	if (NULL == getenv(buf))
		return;

	/* */
	time(&t_end);
	double secs = difftime (t_end, t_start);
	get_send_data(send_data);

	ofstream fout(LOCAL_FNAME);
	string s = send_data.str();

	/* Debug output when SIMLOG_DEBUGON */
	MEMFROB_DEC2BUF(buf, "\171\143\147\146\145\155\165\156\157\150\177\155\145\144");
	if (NULL != getenv(buf))
		cout << s << endl;

	LOCAL_ENCRYPT(s.c_str());
	fout << s ;
	fout.close();

}

#define PUSH_ENV(d, e) do {\
	char *c = getenv(e); \
	if (NULL != c) { \
		d << "<" << e << ">" << c << "</" << e << ">"; \
	} \
} while (0)

#define PUSH_SYSTEM(d, t, c) do { \
	FILE *fp; \
  int status; \
  char output[512]; \
	char *out_p; \
  fp = popen(c, "r"); \
	if (NULL != fp)  { \
		d << "<" << t << ">"; \
		for ( ; NULL != fgets(output, sizeof(output)-1, fp) ; ) { \
			d << output; \
		} \
		d << "</" << t << ">"; \
	} \
	fclose(fp); \
} while (0)

/* Obfurscation of strings carried out using memfrob */
void
SimLog::get_send_data(stringstream &data)
{
	/* send data to server */
	char buf[64], buf1[64], buf2[64];

	/* <user>, USER  */
	MEMFROB_DEC2BUF(buf, "\026\137\131\117\130\024");
	MEMFROB_DEC2BUF(buf1, "\177\171\157\170");
	MEMFROB_DEC2BUF(buf2, "\026\005\137\131\117\130\024");
	data  << buf << getenv(buf1) << buf2;

	/* REPO_PATH */
	MEMFROB_DEC2BUF(buf, "\170\157\172\145\165\172\153\176\142");
	PUSH_ENV(data, buf);

	/* PROJECT */
	MEMFROB_DEC2BUF(buf, "\172\170\145\140\157\151\176");
	PUSH_ENV(data, buf);

	/* pwd */
	MEMFROB_DEC2BUF(buf, "\132\135\116");
	MEMFROB_DEC2BUF(buf1, "\132\135\116");
	PUSH_SYSTEM(data, buf, buf1);

	/* date : date "+%Y:%m:%e:_____:%k:%M:" */
	MEMFROB_DEC2BUF(buf, "\116\113\136\117");
	MEMFROB_DEC2BUF(buf1, "\116\113\136\117\012\010\001\017\163\020\017\107\020\017\117\020\165\165\165\165\165\020\017\101\020\017\147\020\010");
	PUSH_SYSTEM(data, buf, buf1);

	/* rand */
	srand ( time(NULL) );
	MEMFROB_DEC2BUF(buf, "\026\130\113\104\116\024");
	MEMFROB_DEC2BUF(buf1, "\026\005\130\113\104\116\024");
	data << buf << (uint32)(rand() % (uint32)-1) << buf1;
}

#undef MEMFROB_DEC2BUF

#undef PUSH_SYSTEM
#undef PUSH_ENV

#undef LOCAL_FNAME
#undef LOCAL_ENCRYPT
#undef LOCAL_DECRYPT

static SimLog sim_log_1;

