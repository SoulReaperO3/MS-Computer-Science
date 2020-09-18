package com.example.boundedserviceex;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.widget.Toast;

public class MyService extends Service {
    public MyService() {
    }
    public class LocalBinder extends Binder {
        MyService getService() {
            // Return this instance of LocalService so clients can call public methods
            return MyService.this;
        }
    }
    private final IBinder binder = new LocalBinder();

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        int i;
        for(i=0;i<10;i++){
            Toast.makeText(getApplicationContext(),"No: "+i,Toast.LENGTH_LONG).show();
        }
        return binder;
        //throw new UnsupportedOperationException("Not yet implemented");
    }
}
