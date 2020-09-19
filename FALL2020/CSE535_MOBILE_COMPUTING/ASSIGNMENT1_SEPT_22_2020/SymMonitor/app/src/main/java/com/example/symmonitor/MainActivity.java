package com.example.symmonitor;

import androidx.appcompat.app.AppCompatActivity;

import android.hardware.camera2.CameraManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.VideoView;

public class MainActivity extends AppCompatActivity {

    private static final int VIDEO_CAPTURE = 101;
    private Uri fileUri;
    private String mCameraId;
    private CameraManager mCameraManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button symptomsButton = (Button) findViewById(R.id.symptoms);
        Button uploadSignsButton = (Button) findViewById(R.id.uploadSigns);
        Button measureHeartRateButton = (Button) findViewById(R.id.measureHeartRate);
        Button measureRespRateButton = (Button) findViewById(R.id.measureRespRate);

        if(!hasCamera()){
            bt1.setEnabled(false);
        }

        measureHeartRateButton.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.M)
            @Override
            public void onClick(View view) {
                startRecording();
            }
        });

        Button bt2 = (Button) findViewById(R.id.button4Act1);

        bt2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                DownloadTask dw1 = new DownloadTask();
                Toast.makeText(getApplicationContext(),"Running Background Task", Toast.LENGTH_LONG).show();
                dw1.execute();

            }
        });

        Button bt3 = (Button)findViewById(R.id.button3);

        bt3.setEnabled(false);

        bt3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                VideoView vv2 = (VideoView)findViewById(R.id.videoView);
                vv2.setVideoURI(fileUri);
                vv2.start();
            }
        });

        Button bt5 = (Button)findViewById(R.id.button4);
        bt5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                UploadTask up1 = new UploadTask();
                Toast.makeText(getApplicationContext(),"Stating to Upload",Toast.LENGTH_LONG).show();
                up1.execute();
            }
        });
    }
}