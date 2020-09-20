package com.example.symmonitor;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.RatingBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

public class SymptomLoggingPage extends AppCompatActivity implements AdapterView.OnItemSelectedListener {
    String[] Symptoms = {"Nausea", "Headache", "Diarrhea", "Soar Throat", "Fever", "Muscle Ache", "Loss of Smell or Taste", "Cough", "Shortness of Breath", "Feeling Tired"};
    float[] symptomRatingArray = new float[10];
    RatingBar ratingBar;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_symptom_logging_page);

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