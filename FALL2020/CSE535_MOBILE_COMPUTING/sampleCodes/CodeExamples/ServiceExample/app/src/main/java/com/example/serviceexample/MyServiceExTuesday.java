package com.example.serviceexample;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;
import android.widget.Toast;

public class MyServiceExTuesday extends Service {
    public MyServiceExTuesday() {

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startID){
        int i;

        for(i=0;i<10;i++){
            Toast.makeText(getApplicationContext(),"No: "+i,Toast.LENGTH_LONG).show();
        }
        return Service.START_NOT_STICKY;
    }


    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
