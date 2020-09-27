package com.example.opencvtutorial

import android.graphics.Bitmap
import android.media.MediaMetadataRetriever
import android.media.MediaMetadataRetriever.OPTION_CLOSEST_SYNC
import android.media.MediaPlayer
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import org.opencv.android.OpenCVLoader
import java.io.File


class MainActivity : AppCompatActivity() {


    @RequiresApi(Build.VERSION_CODES.Q)
    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        if (!OpenCVLoader.initDebug())
        {
            Toast.makeText(applicationContext,"OpenCV fail",Toast.LENGTH_LONG).show();
        }


        var A = getExternalFilesDir(null);
        var t = Toast.makeText(applicationContext,A.toString(),Toast.LENGTH_LONG);
        t.show();
        var bt1 = findViewById(R.id.button) as Button;

        bt1.setOnClickListener(View.OnClickListener {

            val videoFile = File(getExternalFilesDir(null).toString()+"/FingertipVideo.mp4");

            val videoFileUri: Uri = Uri.parse(videoFile.toString())

            val retriever = MediaMetadataRetriever()

            retriever.setDataSource(videoFile.absolutePath)
            val rev: ArrayList<Bitmap?> = ArrayList<Bitmap?>()

//Create a new Media Player

//Create a new Media Player
            val mp: MediaPlayer = MediaPlayer.create(baseContext, videoFileUri)


                    val i = 0;
                    val bitmap: Bitmap? = retriever.getFrameAtTime(
                        i.toLong(),
                        OPTION_CLOSEST_SYNC
                    )

            // Write your algo

            if (bitmap != null) {
                Toast.makeText(applicationContext,bitmap.getColor(89,97).toString(),Toast.LENGTH_LONG).show()
            };


            //Toast.makeText(applicationContext,getExternalFilesDir(null).toString()+"/imageCap.jpg",Toast.LENGTH_LONG).show();
        })

    }
}