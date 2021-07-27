#include <Servo.h>

#define AC_POWER

// [No.1, No.2, No.3, No.4]
const int cgrb[4] = {98, 98, 98, 98}; // 10, 4, 12, 8
const int crls[4] = {75, 75, 75, 75};
const int crls_big[4] = {60, 60, 60, 60};
const int crls_chon[4] = {90, 90, 90, 90};

const int crot_l[4] = {180, 180, 180, 180}; // 9, 2, 11, 7
const int crot_r[4] = {85, 85, 85, 85};

int grb[4];
int rls[4];
int chon[4];
int rls_big[4];
int rot_l[4];
int rot_r[4];

char buf[30];
int idx = 0;
long data[2];

Servo arm_grab[4];
Servo arm_rot[4];
Servo* calib_arm[8];

void calib_motor(int num, int deg) {
  calib_arm[num]->write(deg);
}

void move_motor(int num, int gl) {
  if(gl == 1)arm_rot[num].write(rot_r[num]);
  else arm_rot[num].write(rot_l[num]);
}

void release_arm(int num) {
  arm_grab[num].write(rls[num]);
}

void grab_arm(int num) {
  arm_grab[num].write(grb[num]);
}

void release_big_arm(int num) {
  arm_grab[num].write(rls_big[num]);
}

void chon_arm(int num) {
  arm_grab[num].write(grb[num]);
  delay(100);
  arm_grab[num].write(chon[num]);
  delay(100);
  arm_grab[num].write(grb[num]);
}

void setup() {
  Serial.begin(115200);

  for (int i = 0;i < 4;i++) {
    grb[i] = cgrb[i];
    rls[i] = crls[i];
    rls_big[i] = crls_big[i];
    chon[i] = crls_chon[i];
    rot_l[i] = crot_l[i];
    rot_r[i] = crot_r[i];
  }

  arm_rot[2].attach(11, 500, 2500);
  arm_grab[2].attach(12, 500, 2500);
  arm_rot[3].attach(7, 500, 2500);
  arm_grab[3].attach(8, 500, 2500);
  arm_rot[0].attach(9, 500, 2500);
  arm_grab[0].attach(10, 500, 2500);
  arm_rot[1].attach(2, 500, 2500);
  arm_grab[1].attach(4, 500, 2500);

  calib_arm[0] = &arm_rot[0];
  calib_arm[1] = &arm_grab[0];
  calib_arm[2] = &arm_rot[1];
  calib_arm[3] = &arm_grab[1];
  calib_arm[4] = &arm_rot[2];
  calib_arm[5] = &arm_grab[2];
  calib_arm[6] = &arm_rot[3];
  calib_arm[7] = &arm_grab[3];

#ifdef AC_POWER
  // Output HIGH from M1 
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  analogWrite(3, 255);
  digitalWrite(2, HIGH);
  digitalWrite(4, LOW);
#endif

  for (int i = 0; i < 4; i++) arm_rot[i].write(rot_l[i]);
  for (int i = 0; i < 4; i++) arm_grab[i].write(grb[i]);  
}

void loop() {
  while (1) {
    if (Serial.available()) {
      buf[idx] = Serial.read();
      if (buf[idx] == '\n') {
        buf[idx] = '\0';
        data[0] = atoi(strtok(buf, " "));
        data[1] = atoi(strtok(NULL, " "));
        if (data[1] == 1000) grab_arm(data[0]);
        else if (data[1] == 2000) release_arm(data[0]);
        else if (data[1] == 3000) release_big_arm(data[0]);
        else if (data[1] == 4000) chon_arm(data[0]);
        else if (data[1] >= 10000) {  // command id: 10000 -
          if (data[1] >= 12000) {   // Set offset
            int c = data[1] - 12100;
            int rot = (data[0] % 2 == 0);
            int n = data[0] / 2;
            if (rot) { // ROT
              rot_l[n] = crot_l[n] + c;
              rot_r[n] = crot_r[n] + c;
              arm_rot[n].write(rot_l[n]);
            } else {                // GRB
              grb[n] = cgrb[n] + c;
              rls[n] = crls[n] + c;
              rls_big[n] = crls_big[n] + c;
              chon[n] = crls_chon[n] + c;
              arm_grab[n].write(grb[n]);
            }
          } else {
            calib_motor(data[0], data[1]-10000);
          }
        }
        else move_motor(data[0], data[1]);
        idx = 0;
      }
      else {
        idx++;
      }
    }
  }
}
