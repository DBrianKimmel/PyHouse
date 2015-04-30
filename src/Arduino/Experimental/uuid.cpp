#include <avr/eeprom.h>
#define eeprom_read_to(dst_p, eeprom_field, dst_size) eeprom_read_block(dst_p, (void *)offsetof(__eeprom_data, eeprom_field), MIN(#define eeprom_read(dst, eeprom_field) eeprom_read_to(&dst, eeprom_field, sizeof(dst))
#define eeprom_write_from(src_p, eeprom_field, src_size) eeprom_write_block(src_p, (void *)offsetof(__eeprom_data, eeprom_field), #define eeprom_write(src, eeprom_field) { typeof(src) x = src; eeprom_write_from(&x, eeprom_field, sizeof(x)); }
#define MIN(x,y) ( x > y ? y : x )
const int buflen = 32;
/*
 * __eeprom_data is the magic name that maps all of the data we are
 * storing in our EEPROM
 */
struct __eeprom_data {
	int first;
	int second;
	boolean third;
	char fourth[buflen];
	char fifth[buflen];
};
void setup() {
	Serial.begin(57600);
	/*
	 * Writing simple variables to the EEPROM becomes simple
	 *
	 * First argument is the value to write, second argument is which field
	 * (in __eeprom_data) to write to.
	 */
	int q = 132;
	eeprom_write(q, first);
	eeprom_write(5958, second);
	eeprom_write(false, third);
	eeprom_write("Hello from EEPROM!", fourth);
	/*
	 * You can even write from a pointer address if need be
	 *
	 * First argument is the pointer to write from.
	 * Second argument is the field (in __eeprom_data)
	 * to write to.
	 * Third argument is the buffer length
	 */
	const char * buf = "Another hello looks like this";
	eeprom_write_from(buf, fifth, strlen(buf)+1);
	int a, b;
	boolean c;
	char d[buflen], e[buflen];
	char *e_p = e;
	/*
	 * Reading back is just as simple. First argument is the variable to read
	 * back to, the second argument is the field (in __eeprom_data) to read
	 * from.
	 */
	eeprom_read(a, first);
	eeprom_read(b, second);
	eeprom_read(c, third);
	eeprom_read(d, fourth);
	/*
	 * You can read back to a pointer address, if you need to.
	 */
eeprom_read_to(e_p, fifth, buflen);
Serial.println(a);
Serial.println(b);
Serial.println(c ? "TRUE" : "FALSE");
Serial.println(d);
Serial.println(e_p);
/*
 * The eeprom_write macros do bounds checking,
 * so you can't overrun a buffer.
 *
 * In __eeprom_data, 'third' is a one-byte boolean, but
 * eeprom_write knows this so only the first char 'T' is written
 * to EEPROM
 */
eeprom_write("This is a buffer overflow", third);
/*
 * If you have an array, like char[], you can write & read a single
 * array entry from a particular constant index
 *
 * Unfortunately, it only works for constant indexes not variables.
 * eeprom_write('X', fourth[x]) does not work with these macros.
 */
eeprom_write('X', fourth[3]);
eeprom_read(d, fourth);
char x;
eeprom_read(x, fourth[3]);
Serial.println(d);
Serial.println(x);
}
void loop() {}
