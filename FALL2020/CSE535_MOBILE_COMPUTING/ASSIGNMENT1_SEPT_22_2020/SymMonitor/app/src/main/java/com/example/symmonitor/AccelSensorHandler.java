package com.example.symmonitor;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Environment;
import android.os.IBinder;
import android.widget.Toast;

import java.io.File;
import java.io.FileWriter;
import java.io.IOError;
import java.io.IOException;

public class AccelSensorHandler extends Service implements SensorEventListener {

    private SensorManager accelManage;
    private Sensor senseAccel;
    float accelValuesX[] = new float[450];
    float accelValuesY[] = new float[450];
    float accelValuesZ[] = new float[450];
    int index = 0;

    public AccelSensorHandler() {
    }

    @Override
    public void onCreate(){
        Toast.makeText(this, "Service Started", Toast.LENGTH_LONG).show();
        accelManage = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        senseAccel = accelManage.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        accelManage.registerListener(this, senseAccel, SensorManager.SENSOR_DELAY_NORMAL);

    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        // TODO Auto-generated method stub
        Sensor mySensor = sensorEvent.sensor;

        if (mySensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            index++;
            accelValuesX[index] = sensorEvent.values[0];
            accelValuesY[index] = sensorEvent.values[1];
            accelValuesZ[index] = sensorEvent.values[2];
            if(index >= 449){
                index = 0;
                accelManage.unregisterListener(this);
                callMeasureRespRate();
                //accelManage.registerListener(this, senseAccel, SensorManager.SENSOR_DELAY_NORMAL);
            }
        }
    }

    private void callMeasureRespRate() {
        Toast.makeText(AccelSensorHandler.this, "Started Writing File", Toast.LENGTH_LONG).show();

        File output = new File(Environment.getExternalStorageDirectory().getPath()+"/CSVBreathe.csv");
        FileWriter dataOutput = null;
        try {
            dataOutput = new FileWriter(output);
        } catch (IOException e) {
            e.printStackTrace();
        }

        for(int i=0;  i<450; i++) {
            try {
                dataOutput.append(accelValuesX[i]+"\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        for(int i=0;  i<450; i++) {
            try {
                dataOutput.append(accelValuesY[i]+"\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        for(int i=0;  i<450; i++) {
            try {
                dataOutput.append(accelValuesZ[i]+"\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        try {
            dataOutput.flush();
            dataOutput.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        Toast.makeText(AccelSensorHandler.this, "Done Writing", Toast.LENGTH_LONG).show();


    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
}
