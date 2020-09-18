package edu.asu.impact.databasetutorial;

import android.os.Bundle;
import android.os.Environment;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.view.Menu;
import android.view.MenuItem;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.os.Build;


public class MainActivity extends AppCompatActivity {
    SQLiteDatabase db;
    EditText patientID;
    EditText Age;
    String patientIDText;
    String ageText;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
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
        patientID = (EditText) findViewById(R.id.editText1);
        Age = (EditText) findViewById(R.id.editText2);
        Button btn = (Button) findViewById(R.id.button1);
        btn.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO Auto-generated method stub
                try{
                    db = SQLiteDatabase.openOrCreateDatabase(Environment.getExternalStorageDirectory()+"/databaseFolder/myDB", null);
                    db.beginTransaction();
                    try {
                        //perform your database operations here ...
                        db.execSQL("create table tblPat ("
                                + " recID integer PRIMARY KEY autoincrement, "
                                + " name text, "
                                + " age text ); " );

                        db.setTransactionSuccessful(); //commit your changes
                    }
                    catch (SQLiteException e) {
                        //report problem
                    }
                    finally {
                        db.endTransaction();
                    }
                }catch (SQLException e){

                    Toast.makeText(MainActivity.this, e.getMessage(), Toast.LENGTH_LONG).show();
                }
            }
        });

        patientID.setOnEditorActionListener(new TextView.OnEditorActionListener() {

            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                // TODO Auto-generated method stub
                patientIDText = v.getText().toString();
                return false;
            }
        });

        Age.setOnEditorActionListener(new TextView.OnEditorActionListener() {

            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                // TODO Auto-generated method stub
                ageText = v.getText().toString();
                return false;
            }
        });

        Button btn1 = (Button) findViewById(R.id.button2);
        btn1.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO Auto-generated method stub
                if(patientIDText != null){
                    if(ageText != null){
                        //db.beginTransaction();
                        try {
                            //perform your database operations here ...
                            db.execSQL( "insert into tblPat(name, age) values ('"+patientIDText+"', '"+ageText+"' );" );
                            //db.setTransactionSuccessful(); //commit your changes
                        }
                        catch (SQLiteException e) {
                            //report problem
                        }
                        finally {
                            //db.endTransaction();
                        }
                    }else{
                        Toast.makeText(MainActivity.this, "Please enter a Age", Toast.LENGTH_LONG).show();
                    }
                }else{
                    Toast.makeText(MainActivity.this, "Please enter a patient ID", Toast.LENGTH_LONG).show();
                }
            }
        });
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
