package com.ftb.activity;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import com.ftb.R;
import com.ftb.model.Patient;

public class ViewPatient extends Activity {
    String blank = "                   ";

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_patient);
        Bundle extras = getIntent().getExtras();
        setTitle(extras.getString("name"));
        String id = extras.getString("id");
        Patient patient = Patient.get(this, id);

        displayPatient(patient);

    }

    private void displayPatient(Patient patient) {
        LinearLayout layout = (LinearLayout) findViewById(R.id.viewSection);
        layout.addView(getTextView("Name" + blank.substring(4)+ patient.name));
        layout.addView(getTextView("Age" + blank.substring(3)+patient.patientdetails.age));
        layout.addView(getTextView("Town"+ blank.substring(4)+patient.address.town));
        layout.addView(getTextView("Family History" + blank.substring(14)+patient.familyhistory.affected_relation));
    }

    private TextView getTextView(String patientName) {
        TextView name = new TextView(this);
        name.setText(patientName);
        return name;
    }
}