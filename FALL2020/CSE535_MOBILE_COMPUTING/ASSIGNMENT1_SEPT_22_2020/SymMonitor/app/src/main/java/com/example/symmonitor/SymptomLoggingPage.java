package com.example.symmonitor;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.RatingBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

public class SymptomLoggingPage extends AppCompatActivity implements AdapterView.OnItemSelectedListener {
    String[] Symptoms = {"Nausea", "Headache", "Diarrhea", "Soar Throat", "Fever", "Muscle Ache", "Loss of Smell or Taste", "Cough", "Shortness of Breath", "Feeling Tired"};
    float[] symptomRatingArray;
    RatingBar ratingBar;
    int respRate, heartRate;
    SQLiteDatabase db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_symptom_logging_page);

        symptomRatingArray = new float[10];

        Intent intent = getIntent();
        heartRate = intent.getIntExtra("heartRate", 0);
        respRate = intent.getIntExtra("respRate", 0);

        TextView symptomLogginHeaderTextView = (TextView) findViewById(R.id.symptomLoggingPageHeaderTextView);
        symptomLogginHeaderTextView.setText("System Logging Page");

        ratingBar = (RatingBar) findViewById(R.id.ratingBar);

        Spinner spin = (Spinner) findViewById(R.id.symptomsListSpinner);
        spin.setOnItemSelectedListener(this);

        //Creating the ArrayAdapter instance having the bank name list
        ArrayAdapter aa = new ArrayAdapter(this,android.R.layout.simple_spinner_item,Symptoms);
        aa.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        //Setting the ArrayAdapter data on the Spinner
        spin.setAdapter(aa);


        Button uploadSignsSymptoms = (Button) findViewById(R.id.uploadSignsSymptoms);
        uploadSignsSymptoms.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO Auto-generated method stub
                try{
                    db = openOrCreateDatabase(Environment.getExternalStorageDirectory()+"/databaseFolder/Kumarasamy",MODE_PRIVATE,null);
                    System.out.println(db);
                    //db = SQLiteDatabase.openOrCreateDatabase(Environment.getExternalStorageDirectory()+"/databaseFolder/Kumarasamy.db", null);
                    db.beginTransaction();
                    try {
                        //"Nausea", "Headache", "Diarrhea", "Soar Throat", "Fever", "Muscle Ache", "Loss of Smell or Taste", "Cough", "Shortness of Breath", "Feeling Tired"};
                        //perform your database operations here ...
                        db.execSQL("CREATE TABLE IF NOT EXISTS Kumarasamy ("
                                + " recID integer PRIMARY KEY autoincrement, "
                                + " HeartRate numeric, "
                                + " RespiratoryRate numeric, "
                                + " Nausea numeric, "
                                + " Headache numeric, "
                                + " Diarrhea numeric, "
                                + " Soar_Throat numeric, "
                                + " Fever numeric, "
                                + " Muscle_Ache numeric, "
                                + " Loss_of_Smell_or_Taste numeric, "
                                + " Cough numeric, "
                                + " Shortness_of_Breath numeric, "
                                + " Feeling_Tired numeric ); " );

                        db.setTransactionSuccessful(); //commit your changes
                    }
                    catch (SQLiteException e) {
                        //report problem
                    }
                    finally {
                        db.endTransaction();
                    }
                }catch (SQLException e){

                    Toast.makeText(SymptomLoggingPage.this, e.getMessage(), Toast.LENGTH_LONG).show();
                }
                try {
                    //perform your database operations here ...
                    db.execSQL( "insert into Kumarasamy(HeartRate, " +
                            "RespiratoryRate,Nausea,Headache,Diarrhea,Soar_Throat," +
                            "Fever,Muscle_Ache,Loss_of_Smell_or_Taste,Cough," +
                            "Shortness_of_Breath,Feeling_Tired) values ('"+heartRate+"'," +
                            "'"+respRate+"','"+symptomRatingArray[0]+"','"+symptomRatingArray[1]+
                            "','"+symptomRatingArray[2]+"','"+symptomRatingArray[3]+"'," +
                            "'"+symptomRatingArray[4]+"','"+symptomRatingArray[5]+"'," +
                            "'"+symptomRatingArray[6]+"','"+symptomRatingArray[7]+"'," +
                            " '"+symptomRatingArray[8]+"','"+symptomRatingArray[9] +"' );" );
                    //db.setTransactionSuccessful(); //commit your changes
                    Toast.makeText(SymptomLoggingPage.this, "Successfully stored in Database!", Toast.LENGTH_LONG).show();

                }
                catch (SQLiteException e) {
                    //report problem
                }

            }
        });


    }
    //Performing action onItemSelected and onNothing selected

    public void onItemSelected(AdapterView<?> arg0, View arg1, final int position, long id) {
        ratingBar.setOnRatingBarChangeListener(new RatingBar.OnRatingBarChangeListener() {

            @Override
            public void onRatingChanged(RatingBar ratingBar, float rating, boolean fromUser) {
                Toast.makeText(getApplicationContext(), Symptoms[position]+" "+String.valueOf(ratingBar.getRating()), Toast.LENGTH_LONG).show();
                symptomRatingArray[position] = ratingBar.getRating();
            }
        });
        ratingBar.setRating((float) 0.0);
    }

    @Override
    public void onNothingSelected(AdapterView<?> arg0) {
        // TODO Auto-generated method stub

    }
}