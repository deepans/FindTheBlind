package com.ftb.activity;

import android.app.Activity;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import com.ftb.R;
import com.ftb.model.Patient;

public class ViewPatientActivity extends Activity {
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
        layout.addView(getTextView("Name  : " + patient.name));
        layout.addView(getTextView("Age  : " + patient.getAge()));
        layout.addView(getTextView("Town  : " + patient.getTown()));
        layout.addView(getTextView("Family History  : " + patient.familyhistory.affected_relation));

    }

    private TextView getTextView(String text) {
        TextView name = new TextView(this);
        name.setText(text);
        name.setTextColor(ColorStateList.valueOf(Color.BLACK));
        return name;
    }
}