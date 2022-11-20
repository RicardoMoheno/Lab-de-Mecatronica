#include <Servo.h>
#include <Stepper.h>

const int stepsPerRevolution = 511;  // La cantidad de pasos que vamos a girar por movimiento (4to de vuelta)
String command; //Creamos una variable para guardar nuestros comandos

// Declaramos los pines de nuestros steppers
Stepper myStepperN(stepsPerRevolution, 30, 32, 31, 33);
Stepper myStepperE(stepsPerRevolution, 22, 24, 23, 25);
Stepper myStepperS(stepsPerRevolution, 38, 40, 39, 41);
Stepper myStepperW(stepsPerRevolution, 46, 48, 47, 49);

// Declaramos los servos
Servo servoN;
Servo servoE;
Servo servoS;
Servo servoW;

void setup() {
  // Especificamos las velocidad en RPM de los servos
  myStepperN.setSpeed(60);
  myStepperE.setSpeed(60);
  myStepperS.setSpeed(60);
  myStepperW.setSpeed(60);

  // Declaramos los pines a los que se conectan los servos
  servoW.attach(2);
  servoS.attach(3);
  servoE.attach(4);
  servoN.attach(5);

  // Iniciamos el puerto serial
  Serial.begin(9600);

  //Abrimos el robot
  abreRobot();
}
/*////////////////////////////////////////////////////////////////////////////
//                       Ciclo principal del programa                       //
// Esta función es la que se ejecuta constantemente, mientras el puerto     //
// esté disponible, se recibirán comandos y se llaman a las funciones       //
// correspondientes                                                         //
//                                                                          //
////////////////////////////////////////////////////////////////////////////*/

void loop() {
  while (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();
    if (command.equals("O")){
      abreRobot();
    } else if (command.equals("C")){
      cierraRobot();
    } else if (command.equals("F")){
      giraS_CW();
      delay(200);
    } else if (command.equals("F'")){
      giraS_CCW();
      delay(200);
    } else if (command.equals("F2")){
      giraS_2CW();
      delay(200);
    } else if (command.equals("R")){
      giraE_CW();
      delay(200);
    } else if (command.equals("R'")){
      giraE_CCW();
      delay(200);
    } else if (command.equals("R2")){
      giraE_2CW();
      delay(200);
    } else if (command.equals("L")){
      giraW_CW();
      delay(200);
    } else if (command.equals("L'")){
      giraW_CCW();
      delay(200);
    } else if (command.equals("L2")){
      giraW_2CW();
      delay(200);
    } else if (command.equals("B")){
      giraN_CW();
      delay(200);
    } else if (command.equals("B'")){
      giraN_CCW();
      delay(200);
    } else if (command.equals("B2")){
      giraN_2CW();
      delay(200);
    } else if (command.equals("U")){
      giraCubo();
      delay(200);
      giraS_CW();
      delay(200);
      regresaCubo();
      delay(200);
    } else if (command.equals("U'")){
      giraCubo();
      delay(200);
      giraS_CCW();
      delay(200);
      regresaCubo();
      delay(200);
    } else if (command.equals("U2")){
      giraCubo();
      delay(200);
      giraS_2CW();
      delay(200);
      regresaCubo();
    } else if (command.equals("D")){
      giraCubo();
      delay(200);
      giraN_CW();
      delay(200);
      regresaCubo();
      delay(200);
    } else if (command.equals("D'")){
      giraCubo();
      delay(200);
      giraN_CCW();
      delay(200);
      regresaCubo();
      delay(200);
    } else if (command.equals("D2")){
      giraCubo();
      delay(200);
      giraN_2CW();
      delay(200);
      regresaCubo();
    }
  }
}

/*////////////////////////////////////////////////////////////////////////////
//                        Movimientos del lado norte                        //
// Estas funciones se encargan de los movimientos del lado trasero del      //
// robot.                                                                   //
//                                                                          //
////////////////////////////////////////////////////////////////////////////*/

void giraN_CW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperN.step(1);
  }
  delay(50);
  servoN.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperN.step(-1);
  }
  delay(50);
  servoN.write(55);
}

void giraN_CCW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperN.step(-1);
  }
  servoN.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperN.step(1);
  }
  delay(50);
  servoN.write(55);
}

void giraN_2CW(){
  for (int i = 0; i <= 2*stepsPerRevolution; i++) {
    myStepperN.step(1);
  }
}

/*////////////////////////////////////////////////////////////////////////////
//                        Movimientos del lado este                         //
// Estas funciones se encargan de los movimientos del lado derecho del      //
// robot.                                                                   //
//                                                                          //
////////////////////////////////////////////////////////////////////////////*/

void giraE_CW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(1);
  }
  servoE.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(-1);
  }
  delay(50);
  servoE.write(55);
}

void giraE_CCW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(-1);
  }
  servoE.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(1);
  }
  delay(50);
  servoE.write(55);
}

void giraE_2CW(){
  for (int i = 0; i <= 2*stepsPerRevolution; i++) {
    myStepperE.step(1);
  }
}
  
/*////////////////////////////////////////////////////////////////////////////
//                        Movimientos del lado sur                          //
// Estas funciones se encargan de los movimientos del lado de enfrente del  //
// robot.                                                                   //
//                                                                          //
////////////////////////////////////////////////////////////////////////////*/

void giraS_CW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperS.step(1);
  }
  servoS.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperS.step(-1);
  }
  delay(50);
  servoS.write(55);
}

void giraS_CCW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperS.step(-1);
  }
  servoS.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperS.step(1);
  }
  delay(50);
  servoS.write(55);
}

void giraS_2CW(){
  for (int i = 0; i <= 2*stepsPerRevolution; i++) {
    myStepperS.step(1);
  }
}

/*////////////////////////////////////////////////////////////////////////////
//                        Movimientos del lado oeste                        //
// Estas funciones se encargan de los movimientos del lado izquierdo del    //
// robot.                                                                   //
//                                                                          //
////////////////////////////////////////////////////////////////////////////*/

void giraW_CW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperW.step(1);
  }
  servoW.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperW.step(-1);
  }
  delay(50);
  servoW.write(55);
}

void giraW_CCW() {
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperW.step(-1);
  }
  servoW.write(0);
  delay(50);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperW.step(1);
  }
  delay(50);
  servoW.write(55);
}

void giraW_2CW(){
  for (int i = 0; i <= 2*stepsPerRevolution; i++) {
    myStepperW.step(1);
  }
}


/*////////////////////////////////////////////////////////////////////////////
//                        Abrir y cerrar el robot                           //
// Estas funciones se encargan de abrir y cerrar los servos en orden para   //
// meter o sacar el cubo del robot.                                         //
//                                                                          //
////////////////////////////////////////////////////////////////////////////*/

void abreRobot() {
  servoN.write(0);
  delay(15);
  servoE.write(0);
  delay(15);
  servoS.write(0);
  delay(15);
  servoW.write(0);
  delay(15);
}

void cierraRobot() {
  servoN.write(50);
  delay(15);
  servoE.write(50);
  delay(15);
  servoS.write(50);
  delay(15);
  servoW.write(50);
  delay(15);
}

/*////////////////////////////////////////////////////////////////////////////
//                           Girar el cubo entero                           //
// Estas funciones se encargan de hacer que el cubo gire completo de modo   //
// que las caras de arriba y abajo se puedan girar.                         //
//                                                                          //
////////////////////////////////////////////////////////////////////////////*/

void giraCubo() {
  servoN.write(0);
  delay(15);
  servoS.write(0);
  delay(15);
  servoE.write(70);
  delay(15);
  servoW.write(70);
  delay(200);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(-1);
    myStepperW.step(1);
  }
  delay(200);
  servoN.write(50);
  delay(15);
  servoS.write(50);
  delay(15);
  servoE.write(0);
  delay(15);
  servoW.write(0);
  delay(200);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(1);
    myStepperW.step(-1);
  }
  delay(200);
  servoE.write(50);
  delay(15);
  servoW.write(50);
  delay(15);
}

void regresaCubo() {
  servoN.write(0);
  delay(15);
  servoS.write(0);
  delay(15);
  servoE.write(70);
  delay(15);
  servoW.write(70);
  delay(200);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(1);
    myStepperW.step(-1);
  }
  delay(200);
  servoN.write(50);
  delay(15);
  servoS.write(50);
  delay(15);
  servoE.write(0);
  delay(15);
  servoW.write(0);
  delay(200);
  for (int i = 0; i <= stepsPerRevolution; i++) {
    myStepperE.step(-1);
    myStepperW.step(1);
  }
  delay(200);
  servoE.write(50);
  delay(15);
  servoW.write(50);
  delay(15);
}
