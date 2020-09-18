package edu.asu.impact.threadexample;

import android.os.Bundle;
import android.os.Message;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.ProgressBar;
import android.os.Handler;
import android.widget.Toast;
import android.os.AsyncTask;
import android.view.View.OnClickListener;
import android.widget.TextView;
import java.util.Random;


public class MainActivity extends AppCompatActivity {
    ProgressBar pgBar;
    Handler threadHandle = new Handler(){
        @Override
        public void handleMessage(Message msg){
            pgBar.incrementProgressBy(1);
            Toast.makeText(MainActivity.this, "Thread execution state: " + pgBar.getProgress(), Toast.LENGTH_SHORT).show();
            if(pgBar.getProgress() == pgBar.getMax()){
                pgBar.setVisibility(View.INVISIBLE);
                Toast.makeText(MainActivity.this, "Thread execution Complete", Toast.LENGTH_LONG).show();
            }

        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        pgBar = (ProgressBar) findViewById(R.id.progress1);
        pgBar.setMax(10);
        pgBar.setProgress(0);

        Button btn = (Button) findViewById(R.id.button1);
        btn.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO Auto-generated method stub
                new slowTask().execute();
            }
        });

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }

    @Override
    public void onStart(){
        super.onStart();

        Thread threadRun = new Thread(new Runnable() {

            @Override
            public void run() {
                // TODO Auto-generated method stub
                try{
                    for(int i = 0;i<10;i++){
                        Random rnd = new Random();
                        Message msg = threadHandle.obtainMessage(1,Integer.toString(rnd.nextInt(101)));
                        threadHandle.sendMessage(msg);
                    }
                    myHandler2.post(foreGroundTask);
                }catch(Throwable t){

                }
            }
        });

        threadRun.start();
    }

    Handler myHandler2 = new Handler();
    private Runnable foreGroundTask = new Runnable() {

        @Override
        public void run() {
            // TODO Auto-generated method stub
            ProgressBar pgBar2 = (ProgressBar) findViewById(R.id.progressBar1);
            pgBar2.setProgress(0);
            pgBar2.setMax(100);
            while(pgBar2.getProgress() != pgBar2.getMax()){
                try {
                    Thread.sleep(10);
                    Toast.makeText(MainActivity.this, "Hi from thread 2", Toast.LENGTH_SHORT).show();
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                pgBar2.incrementProgressBy(5);

            }
            Toast.makeText(MainActivity.this, "Thread 2 has ended", Toast.LENGTH_SHORT).show();
        }
    };

    TextView tv;
    private class slowTask extends AsyncTask<String, Long, Void>{
        @Override
        protected void onPreExecute(){
            tv = (TextView) findViewById(R.id.textView1);

            tv.setText("Tasks before the slow job is posted");
        }

        @Override
        protected Void doInBackground(String... params) {
            // TODO Auto-generated method stub
            try {
                for(Long i = 0L; i<10L;i++){
                    Thread.sleep(100);
                    publishProgress((Long) i);
                }
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }


            return null;
        }
        @Override
        protected void onProgressUpdate(Long... value){
            tv.setText("Working on "+value[0]);
        }
        @Override
        protected void onPostExecute(final Void unused){
            tv.setText("Done with the Computation");
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
