package com.example.symmonitor;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.StrictMode;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import java.io.File;

public class MainActivity extends AppCompatActivity {

    private static final int VIDEO_CAPTURE = 101;
    private Uri fileUri;
    private String mCameraId;
    private CameraManager mCameraManager;
    private RespRateReceiver respRateReceiver;
    int respRate = 0, heartRate = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView heartRateTextView = (TextView) findViewById(R.id.heartRateTextView);
        TextView respRateTextView = (TextView) findViewById(R.id.respRateTextView);
        heartRateTextView.setText("");
        respRateTextView.setText("");

        Button symptomsButton = (Button) findViewById(R.id.symptoms);
        Button uploadSignsButton = (Button) findViewById(R.id.uploadSigns);
        Button measureHeartRateButton = (Button) findViewById(R.id.measureHeartRate);
        Button measureRespRateButton = (Button) findViewById(R.id.measureRespRate);

        if (!hasCamera()) {
            measureHeartRateButton.setEnabled(false);
        }

        measureHeartRateButton.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.M)
            @Override
            public void onClick(View view) {
                startRecording();
            }
        });

        measureRespRateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Register BroadcastReceiver
                //to receive event from our service
                respRateReceiver = new RespRateReceiver();
                IntentFilter intentFilter = new IntentFilter();
                intentFilter.addAction(AccelSensorHandler.CALC_RESP_RATE);
                registerReceiver(respRateReceiver, intentFilter);

                Intent startSenseService = new Intent(MainActivity.this, AccelSensorHandler.class);
                startService(startSenseService);
            }
        });

        symptomsButton.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.M)
            @Override
            public void onClick(View view) {
                Intent startSymptomLogging = new Intent(MainActivity.this, SymptomLoggingPage.class);
                startSymptomLogging.putExtra("heartRate", heartRate);
                startSymptomLogging.putExtra("respRate", respRate);
                startActivity(startSymptomLogging);
            }
        });


    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    public void startRecording() {
        File mediaFile = new
                File(Environment.getExternalStorageDirectory().getAbsolutePath()
                + "/myvideo.mp4");
        StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder();
        StrictMode.setVmPolicy(builder.build());

        boolean isFlashAvailable = getApplicationContext().getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA_FLASH);

        if (!isFlashAvailable) {
            Toast.makeText(getApplicationContext(), "error flash", Toast.LENGTH_LONG).show();
        }

        mCameraManager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);

        try {
            mCameraId = mCameraManager.getCameraIdList()[0];
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }

        try {
            mCameraManager.setTorchMode(mCameraId, true);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }

        fileUri = Uri.fromFile(mediaFile);
        Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        intent.putExtra(MediaStore.EXTRA_DURATION_LIMIT, 45);
        intent.putExtra(MediaStore.EXTRA_OUTPUT, fileUri);
        startActivityForResult(intent, VIDEO_CAPTURE);
    }

    private boolean hasCamera() {
        if (getPackageManager().hasSystemFeature(
                PackageManager.FEATURE_CAMERA_ANY)) {
            return true;
        } else {
            return false;
        }
    }

    protected void onActivityResult(int requestCode,
                                    int resultCode, Intent data) {

        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == VIDEO_CAPTURE) {
            if (resultCode == RESULT_OK) {
                Toast.makeText(this, "Video has been saved", Toast.LENGTH_LONG).show();
                VideoView vv = (VideoView) findViewById(R.id.videoView);
                vv.setVideoURI(fileUri);
                vv.start();
            } else if (resultCode == RESULT_CANCELED) {
                Toast.makeText(this, "Video recording cancelled.",
                        Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(this, "Failed to record video",
                        Toast.LENGTH_LONG).show();
            }
        }
    }

    private class RespRateReceiver extends BroadcastReceiver {

        @Override
        public void onReceive(Context arg0, Intent arg1) {
            // TODO Auto-generated method stub

            respRate = arg1.getIntExtra("RESP_RATE_RETURNED", 0);
            unregisterReceiver(respRateReceiver);
            TextView respRateTextView = (TextView) findViewById(R.id.respRateTextView);
            respRateTextView.setText(String.valueOf(respRate) + " breaths per minute");

        }
    }
}