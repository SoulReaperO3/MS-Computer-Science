package com.example.basicfirstapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.ImageFormat;
import android.hardware.Camera;
import android.os.Bundle;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {
    Camera camera;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView tv = (TextView)findViewById(R.id.textView);
        tv.setText("This is the first screen Test 1 Android studio in windows");

        Button buttonOne = (Button)findViewById(R.id.button);

        buttonOne.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                camera = Camera.open();
                Camera.Parameters cameraParam = camera.getParameters();
                cameraParam.setPreviewFormat(ImageFormat.NV21);
                camera.setDisplayOrientation(90);
                camera.setParameters(cameraParam);
                cameraParam = camera.getParameters();
                SurfaceView preview = (SurfaceView) findViewById(R.id.surfaceView);
                SurfaceHolder mHolder = preview.getHolder();
                //mHolder.addCallback(this);
                try {
                    camera.setPreviewDisplay(mHolder);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                cameraParam.setFlashMode(Camera.Parameters.FLASH_MODE_TORCH);
                camera.setParameters(cameraParam);
                camera.startPreview();
            }
        });

        camera.setPreviewCallback(new Camera.PreviewCallback() {
            @Override
            public void onPreviewFrame(byte[] data, Camera camera) {
                int frameHeight = camera.getParameters().getPreviewSize().height;
                int frameWidth = camera.getParameters().getPreviewSize().width;
                // number of pixels//transforms NV21 pixel data into RGB pixels
                int rgb[] = new int[frameWidth * frameHeight];
                // convertion
                //int[] myPixels = decodeYUV420SP(rgb, data, frameWidth, frameHeight);
            }
        });

    }


}